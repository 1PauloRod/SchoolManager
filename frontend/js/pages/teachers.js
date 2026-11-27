import {
    getTeachers,
    postTeachers,
    deleteTeacher,
    updateTeacher
} from "../api/teacher.js";
import {
    container,
    button,
    textInput,
    cpfInput,
    pageHeader,
    emptyState,
    listItem,
    joinMeta,
    renderForm
} from "../utils.js";

export async function fetchTeachers() {
    try {
        const teachers = await getTeachers();
        renderTeachers(teachers);
    } catch (err) {
        console.error("Erro ao buscar professor: ", err);
    }
}

function renderTeachers(teachers) {
    container.innerHTML = "";

    container.appendChild(
        pageHeader(
            "Professores",
            button("Cadastrar professor", renderAddTeacher, "primary")
        )
    );

    if (teachers.length === 0) {
        container.appendChild(emptyState("Nenhum professor cadastrado."));
        return;
    }

    teachers.forEach((teacher) => {
        const btnUpdate = button("Editar", () => renderEditTeacher(teacher));

        const btnDelete = button("Deletar", async () => {
            if (!confirm(`Remover o professor ${teacher.name}?`)) return;

            try {
                await deleteTeacher(teacher.id, teacher);
                fetchTeachers();
                alert("Professor removido com sucesso.");
            } catch (err) {
                console.error(err);
                alert("Não foi possível excluir professor.");
            }
        }, "danger");

        container.appendChild(
            listItem(
                {
                    title: teacher.name,
                    meta: joinMeta(
                        teacher.email,
                        teacher.specialty,
                        teacher.class_name
                    )
                },
                btnUpdate,
                btnDelete
            )
        );
    });
}

function renderAddTeacher() {
    const inputName      = textInput("Nome");
    const inputEmail     = textInput("Email");
    const inputCpf       = cpfInput();
    const inputSpecialty = textInput("Especialidade");

    renderForm({
        title: "Cadastrar professor",
        fields: [
            { label: "Nome",          input: inputName },
            { label: "Email",         input: inputEmail },
            { label: "CPF",           input: inputCpf },
            { label: "Especialidade", input: inputSpecialty }
        ],
        onCancel: fetchTeachers,
        onSave: async () => {
            try {
                await postTeachers({
                    name: inputName.value,
                    email: inputEmail.value,
                    cpf: inputCpf.value,
                    specialty: inputSpecialty.value
                });

                await fetchTeachers();
                alert("Professor cadastrado com sucesso!");
            } catch (err) {
                console.error("Erro ao cadastrar professor:", err);
                alert(err.message);
            }
        }
    });
}

function renderEditTeacher(teacher) {
    const inputName      = textInput("Nome", teacher.name);
    const inputEmail     = textInput("Email", teacher.email);
    const inputCpf       = cpfInput(teacher.cpf);
    const inputSpecialty = textInput("Especialidade", teacher.specialty);

    renderForm({
        title: "Editar professor",
        fields: [
            { label: "Nome",          input: inputName },
            { label: "Email",         input: inputEmail },
            { label: "CPF",           input: inputCpf },
            { label: "Especialidade", input: inputSpecialty }
        ],
        onCancel: fetchTeachers,
        onSave: async () => {
            try {
                await updateTeacher(teacher.id, {
                    name: inputName.value,
                    email: inputEmail.value,
                    cpf: inputCpf.value,
                    specialty: inputSpecialty.value
                });

                await fetchTeachers();
                alert("Professor atualizado com sucesso!");
            } catch (err) {
                console.error("Erro ao atualizar professor:", err);
                alert(err.message);
            }
        }
    });
}
