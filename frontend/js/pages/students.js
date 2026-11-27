import {
    getStudents,
    postStudents,
    updateStudent,
    deleteStudent
} from "../api/student.js";
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

export async function fetchStudents() {
    try {
        const students = await getStudents();
        renderStudents(students);
    } catch (err) {
        console.error("Erro ao buscar estudantes: ", err);
    }
}

function renderStudents(students) {
    container.innerHTML = "";

    container.appendChild(
        pageHeader(
            "Alunos",
            button("Matricular aluno", renderAddStudent, "primary")
        )
    );

    if (students.length === 0) {
        container.appendChild(emptyState("Nenhum aluno cadastrado."));
        return;
    }

    students.forEach((student) => {
        const btnUpdate = button("Editar", () => renderEditStudent(student));

        const btnDelete = button("Deletar", async () => {
            if (!confirm(`Excluir o aluno ${student.name}?`)) return;

            try {
                await deleteStudent(student.id, student);
                alert("Aluno excluído com sucesso.");
                fetchStudents();
            } catch (err) {
                console.error(err);
                alert("Não foi possível excluir aluno.");
            }
        }, "danger");

        container.appendChild(
            listItem(
                {
                    title: student.name,
                    meta: joinMeta(
                        `#${student.id}`,
                        student.email,
                        student.class_name,
                        student.status
                    )
                },
                btnUpdate,
                btnDelete
            )
        );
    });
}

function renderAddStudent() {
    const inputName   = textInput("Nome");
    const inputMother = textInput("Nome da mãe");
    const inputFather = textInput("Nome do pai");
    const inputEmail  = textInput("Email");
    const inputCpf    = cpfInput();

    renderForm({
        title: "Matricular aluno",
        fields: [
            { label: "Nome",         input: inputName },
            { label: "Nome da mãe",  input: inputMother },
            { label: "Nome do pai",  input: inputFather },
            { label: "Email",        input: inputEmail },
            { label: "CPF",          input: inputCpf }
        ],
        onCancel: fetchStudents,
        onSave: async () => {
            try {
                await postStudents({
                    name: inputName.value,
                    email: inputEmail.value,
                    cpf: inputCpf.value,
                    mother_name: inputMother.value,
                    father_name: inputFather.value,
                    year: 0,
                    active: false
                });

                alert("Aluno cadastrado com sucesso!");
                await fetchStudents();
            } catch (err) {
                console.error("Erro ao cadastrar aluno:", err);
                alert(err.message);
            }
        }
    });
}

function renderEditStudent(student) {
    const inputName   = textInput("Nome", student.name);
    const inputMother = textInput("Nome da mãe", student.mother_name);
    const inputFather = textInput("Nome do pai", student.father_name);
    const inputEmail  = textInput("Email", student.email);
    const inputCpf    = cpfInput(student.cpf);

    renderForm({
        title: "Editar aluno",
        fields: [
            { label: "Nome",         input: inputName },
            { label: "Nome da mãe",  input: inputMother },
            { label: "Nome do pai",  input: inputFather },
            { label: "Email",        input: inputEmail },
            { label: "CPF",          input: inputCpf }
        ],
        onCancel: fetchStudents,
        onSave: async () => {
            try {
                await updateStudent(student.id, {
                    name: inputName.value,
                    email: inputEmail.value,
                    cpf: inputCpf.value,
                    mother_name: inputMother.value,
                    father_name: inputFather.value
                });

                await fetchStudents();
                alert("Aluno editado com sucesso!");
            } catch (err) {
                console.error("Erro ao atualizar aluno:", err);
                alert(err.message);
            }
        }
    });
}
