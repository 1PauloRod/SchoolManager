import {
    getSubjects,
    postSubjects,
    deleteSubjects
} from "../api/subject.js";
import {
    container,
    button,
    textInput,
    pageHeader,
    emptyState,
    listItem,
    joinMeta,
    renderForm
} from "../utils.js";

export async function fetchSubjects() {
    try {
        const subjects = await getSubjects();
        renderSubjects(subjects);
    } catch (err) {
        console.error("Erro ao buscar disciplina: ", err);
    }
}

function renderSubjects(subjects) {
    container.innerHTML = "";

    container.appendChild(
        pageHeader(
            "Disciplinas",
            button("Cadastrar disciplina", renderAddSubject, "primary")
        )
    );

    if (subjects.length === 0) {
        container.appendChild(emptyState("Nenhuma disciplina cadastrada."));
        return;
    }

    subjects.forEach((subject) => {
        // Obs.: não existe updateSubject na API, então só há o botão de deletar.
        // (O botão "Editar" original chamava renderEditTeacher(teacher) com uma
        // variável inexistente e quebrava ao clicar.)
        const btnDelete = button("Deletar", async () => {
            if (!confirm(`Remover a disciplina ${subject.name}?`)) return;

            try {
                await deleteSubjects(subject.id, subject);
                alert("Disciplina removida com sucesso.");
                fetchSubjects();
            } catch (err) {
                console.error(err);
                alert("Não foi possível excluir disciplina.");
            }
        }, "danger");

        container.appendChild(
            listItem(
                {
                    title: subject.name,
                    meta: joinMeta(
                        subject.code,
                        subject.workload_hour ? `${subject.workload_hour}h` : ""
                    )
                },
                btnDelete
            )
        );
    });
}

function renderAddSubject() {
    const inputName = textInput("Nome");
    const inputCode = textInput("Código");

    renderForm({
        title: "Cadastrar disciplina",
        fields: [
            { label: "Nome",   input: inputName },
            { label: "Código", input: inputCode }
        ],
        onCancel: fetchSubjects,
        onSave: async () => {
            try {
                await postSubjects({
                    name: inputName.value,
                    code: inputCode.value
                });

                alert("Disciplina cadastrada com sucesso!");
                fetchSubjects();
            } catch (err) {
                console.error("Erro ao cadastrar disciplina:", err);
                alert(err.message);
            }
        }
    });
}
