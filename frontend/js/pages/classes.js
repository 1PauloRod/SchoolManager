import { getStudents } from "../api/student.js";
import { getTeachers } from "../api/teacher.js";
import {
    getClasses,
    getClassStudents,
    deleteClassStudents,
    postClassStudents,
    getClassTeachers,
    postClassTeachers,
    deleteClassTeachers
} from "../api/class.js";
import {
    container,
    button,
    pageHeader,
    sectionTitle,
    emptyState,
    listItem,
    joinMeta,
    openSelectModal
} from "../utils.js";
import { renderClassSchedule } from "./schedule.js";

// ------------------------------------------------------------
// Lista de turmas
// ------------------------------------------------------------

export async function fetchClasses() {
    try {
        const classes = await getClasses();
        renderClasses(classes);
    } catch (err) {
        console.error("Erro ao buscar turma: ", err);
    }
}

function renderClasses(classes) {
    container.innerHTML = "";

    container.appendChild(pageHeader("Turmas"));

    if (classes.length === 0) {
        container.appendChild(emptyState("Nenhuma turma cadastrada."));
        return;
    }

    classes.forEach((classs) => {
        const btnOpen = button("Abrir", () => openClass(classs), "primary");

        container.appendChild(
            listItem(
                {
                    title: classs.name,
                    meta: `Capacidade: ${classs.capacity}`
                },
                btnOpen
            )
        );
    });
}

// ------------------------------------------------------------
// Detalhe da turma (alunos + professores)
// ------------------------------------------------------------

async function openClass(classs) {
    try {
        const [students, teachers] = await Promise.all([
            getClassStudents(classs.id),
            getClassTeachers(classs.id)
        ]);

        renderClassDetail(classs, students, teachers);
    } catch (err) {
        console.error(err);
        alert("Não foi possível mostrar os estudantes");
    }
}

function renderClassDetail(classs, students, teachers) {
    container.innerHTML = "";

    container.appendChild(
        pageHeader(
            classs.name,
            button("Voltar", fetchClasses, "ghost"),
            button("Adicionar aluno", () => openAddStudentModal(classs, students)),
            button("Adicionar professor", () => openAddTeacherModal(classs, teachers)),
            button(
                "Grade de horários",
                () => renderClassSchedule(classs.id, () => openClass(classs)),
                "primary"
            )
        )
    );

    renderClassTeachers(classs, teachers);
    renderClassStudents(classs, students);
}

function renderClassTeachers(classs, teachers) {
    container.appendChild(sectionTitle("Professores", teachers.length));

    if (teachers.length === 0) {
        container.appendChild(emptyState("Nenhum professor nesta turma."));
        return;
    }

    teachers.forEach((teacher) => {
        const btnRemove = button("Remover", async () => {
            try {
                await deleteClassTeachers(classs.id, teacher.id);
                alert("Professor removido da turma.");
                openClass(classs);
            } catch (err) {
                console.error(err);
                alert("Não foi possível remover professor da turma.");
            }
        }, "danger");

        container.appendChild(
            listItem(
                {
                    title: teacher.name,
                    meta: joinMeta(
                        `#${teacher.id}`,
                        teacher.email,
                        teacher.specialty,
                        teacher.status
                    )
                },
                btnRemove
            )
        );
    });
}

function renderClassStudents(classs, students) {
    container.appendChild(sectionTitle("Alunos", students.length));

    if (students.length === 0) {
        container.appendChild(emptyState("Nenhum aluno nesta turma."));
        return;
    }

    students.forEach((student) => {
        const btnRemove = button("Remover", async () => {
            try {
                await deleteClassStudents(classs.id, student.id);
                alert("Aluno excluído da turma.");
                openClass(classs);
            } catch (err) {
                console.error(err);
                alert("Não foi possível excluir aluno da turma.");
            }
        }, "danger");

        container.appendChild(
            listItem(
                {
                    title: student.name,
                    meta: joinMeta(student.email, student.status)
                },
                btnRemove
            )
        );
    });
}

// ------------------------------------------------------------
// Modais de adicionar aluno / professor
// ------------------------------------------------------------

async function openAddStudentModal(classs, studentsInClass) {
    try {
        const allStudents = await getStudents();

        // Só alunos que ainda não estão na turma
        const options = allStudents
            .filter(student => !studentsInClass.some(s => s.id == student.id))
            .map(student => ({
                value: student.id,
                label: `${student.name} - ${student.email}`
            }));

        openSelectModal({
            title: "Adicionar aluno à turma",
            placeholder: "Selecione um aluno",
            options,
            emptyText: "Nenhum aluno disponível",
            requiredMessage: "Selecione um aluno.",
            errorMessage: "Não foi possível adicionar aluno à turma.",
            onSave: async (student_id) => {
                await postClassStudents(classs.id, student_id);
                alert("Aluno adicionado à turma.");
                openClass(classs);
            }
        });
    } catch (err) {
        console.error(err);
        alert("Não foi possível carregar os alunos.");
    }
}

async function openAddTeacherModal(classs, teachersInClass) {
    try {
        const allTeachers = await getTeachers();

        // Só professores que ainda não estão na turma
        const options = allTeachers
            .filter(teacher => !teachersInClass.some(t => t.id == teacher.id))
            .map(teacher => ({
                value: teacher.id,
                label: `${teacher.name} - ${teacher.email}`
            }));

        openSelectModal({
            title: "Adicionar professor à turma",
            placeholder: "Selecione um professor",
            options,
            emptyText: "Nenhum professor disponível",
            requiredMessage: "Selecione um professor.",
            errorMessage: "Não foi possível adicionar professor à turma.",
            onSave: async (teacher_id) => {
                await postClassTeachers(classs.id, teacher_id);
                alert("Professor adicionado à turma.");
                openClass(classs);
            }
        });
    } catch (err) {
        console.error(err);
        alert("Não foi possível carregar os professores.");
    }
}
