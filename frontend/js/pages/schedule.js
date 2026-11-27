import {
    getClassSubjects,
    getClassTeachers,
    getClassSchedules,
    postClassSchedules
} from "../api/class.js";
import {
    container,
    el,
    button,
    selectControl,
    field,
    pageHeader,
    emptyState,
    closeModals,
    createModal
} from "../utils.js";

const DAYS = {
    1: "Segunda-feira",
    2: "Terça-feira",
    3: "Quarta-feira",
    4: "Quinta-feira",
    5: "Sexta-feira",
    6: "Sábado"
};

const MORNING_SLOTS = [
    { start_time: "07:50:00", end_time: "08:40:00" },
    { start_time: "08:40:00", end_time: "09:30:00" },
    { start_time: "09:30:00", end_time: "10:20:00" },
    { start_time: "10:20:00", end_time: "11:10:00" },
    { start_time: "11:10:00", end_time: "12:00:00" }
];

// ------------------------------------------------------------
// Grade de horários da turma
// onBack: função chamada pelo botão "Voltar" (volta para a turma)
// ------------------------------------------------------------

export async function renderClassSchedule(class_id, onBack) {
    closeModals();
    container.innerHTML = "";

    try {
        const schedules = await getClassSchedules(class_id);

        container.appendChild(
            pageHeader(
                "Grade de horários",
                onBack && button("Voltar", onBack, "ghost"),
                button(
                    "Adicionar aula",
                    () => openAddSchedule(class_id, onBack),
                    "primary"
                )
            )
        );

        if (schedules.length === 0) {
            container.appendChild(emptyState("Nenhuma aula cadastrada nesta turma."));
            return;
        }

        // Ordenar por dia e horário de início
        schedules.sort((a, b) => {
            if (a.weekday !== b.weekday) return a.weekday - b.weekday;
            return a.start_time.localeCompare(b.start_time);
        });

        const grid = el("div", "schedule-grid");

        Object.entries(DAYS).forEach(([weekday, dayName]) => {
            const daySchedules = schedules.filter(
                schedule => Number(schedule.weekday) === Number(weekday)
            );

            // Não mostrar dias sem aulas
            if (daySchedules.length === 0) return;

            const dayCard = el("div", "schedule-day");
            dayCard.appendChild(el("h3", "schedule-day-title", dayName));

            daySchedules.forEach(schedule => {
                const lesson = el("div", "lesson");

                const time = el(
                    "span",
                    "lesson-time",
                    `${schedule.start_time.slice(0, 5)} - ${schedule.end_time.slice(0, 5)}`
                );

                const info = el("div", "lesson-info");
                info.append(
                    el("p", "lesson-subject", schedule.subject_name),
                    el("p", "lesson-teacher", `Professor ${schedule.teacher_name}`)
                );

                lesson.append(time, info);
                dayCard.appendChild(lesson);
            });

            grid.appendChild(dayCard);
        });

        container.appendChild(grid);

    } catch (err) {
        console.error("Erro ao buscar grade:", err);
        alert("Não foi possível carregar a grade de horários.");
    }
}

// ------------------------------------------------------------
// Modal "Adicionar aula"
// ------------------------------------------------------------

export async function openAddSchedule(class_id, onBack) {
    closeModals();

    let subjects, teachers, schedules;

    try {
        [subjects, teachers, schedules] = await Promise.all([
            getClassSubjects(class_id),
            getClassTeachers(class_id),
            getClassSchedules(class_id)
        ]);
    } catch (err) {
        console.error("Erro ao carregar dados da aula:", err);
        alert("Não foi possível carregar as disciplinas, professores ou horários.");
        return;
    }

    // Disciplina
    const subjectSelect = selectControl(
        "Selecione uma disciplina",
        subjects.map(subject => ({
            value: subject.id,
            label: subject.subject_name
        }))
    );

    // Professor
    const teacherSelect = selectControl(
        teachers.length ? "Selecione um professor" : "Nenhum professor cadastrado na turma",
        teachers.map(teacher => ({
            value: teacher.id,
            label: teacher.name
        }))
    );
    teacherSelect.disabled = teachers.length === 0;

    // Dia da semana
    const weekdaySelect = selectControl(
        "Selecione o dia",
        Object.entries(DAYS).map(([value, label]) => ({ value, label }))
    );

    // Horário (depende do dia)
    const timeSelect = selectControl("Selecione primeiro o dia");
    timeSelect.disabled = true;

    function updateAvailableSlots() {
        timeSelect.innerHTML = "";
        timeSelect.disabled = true;

        if (!weekdaySelect.value) {
            timeSelect.add(new Option("Selecione primeiro o dia", ""));
            return;
        }

        const availableSlots = MORNING_SLOTS.filter(slot => {
            const occupied = schedules.some(schedule =>
                Number(schedule.weekday) === Number(weekdaySelect.value) &&
                schedule.start_time === slot.start_time &&
                schedule.end_time === slot.end_time
            );

            return !occupied;
        });

        if (availableSlots.length === 0) {
            timeSelect.add(new Option("Nenhum horário disponível", ""));
            return;
        }

        timeSelect.add(new Option("Selecione um horário", ""));

        availableSlots.forEach(slot => {
            timeSelect.add(new Option(
                `${slot.start_time.slice(0, 5)} - ${slot.end_time.slice(0, 5)}`,
                JSON.stringify(slot)
            ));
        });

        timeSelect.disabled = false;
    }

    weekdaySelect.addEventListener("change", updateAvailableSlots);

    // Botões
    const btnCancel = button("Cancelar", () => modal.remove(), "ghost");

    const btnSave = button("Salvar aula", async () => {
        const selectedSubject = subjects.find(s => s.id == subjectSelect.value);

        if (!selectedSubject) {
            alert("Selecione uma disciplina.");
            return;
        }

        if (!teacherSelect.value) {
            alert("Selecione um professor.");
            return;
        }

        if (!weekdaySelect.value) {
            alert("Selecione o dia da semana.");
            return;
        }

        if (!timeSelect.value) {
            alert("Selecione um horário disponível.");
            return;
        }

        const selectedSlot = JSON.parse(timeSelect.value);

        const scheduleData = {
            class_subject: selectedSubject.id,
            teacher_id: Number(teacherSelect.value),
            weekday: Number(weekdaySelect.value),
            start_time: selectedSlot.start_time,
            end_time: selectedSlot.end_time
        };

        try {
            btnSave.disabled = true;

            await postClassSchedules(class_id, scheduleData);

            alert("Aula adicionada com sucesso!");

            modal.remove();
            renderClassSchedule(class_id, onBack);

        } catch (err) {
            console.error("Erro ao salvar horário:", err);
            alert("Não foi possível adicionar a aula.");
            btnSave.disabled = false;
        }
    }, "primary");

    const modal = createModal({
        title: "Adicionar aula",
        description: "Preencha as informações para adicionar uma aula.",
        content: [
            field("Disciplina", subjectSelect),
            field("Professor", teacherSelect),
            field("Dia da semana", weekdaySelect),
            field("Horário da aula", timeSelect)
        ],
        actions: [btnCancel, btnSave]
    });
}
