// Ponto de entrada da página admin: liga os botões do menu às seções.

import { closeModals, container, searchInput } from "../utils.js";
import { fetchStudents } from "./students.js";
import { fetchTeachers } from "./teachers.js";
import { fetchClasses } from "./classes.js";
import { fetchSubjects } from "./subjects.js";

const sections = [
    { buttonId: "btnStudents", load: fetchStudents, searchPlaceholder: "Buscar aluno..." },
    { buttonId: "btnTeachers", load: fetchTeachers, searchPlaceholder: "Buscar professor..." },
    { buttonId: "btnClasses",  load: fetchClasses,  searchPlaceholder: "Buscar turma..." },
    { buttonId: "btnSubjects", load: fetchSubjects, searchPlaceholder: "Buscar disciplina..." }
];

function setActiveButton(activeButton) {
    sections.forEach(({ buttonId }) => {
        document.getElementById(buttonId).classList.toggle("active", buttonId === activeButton.id);
    });
}

// Filtra os itens exibidos (.list-item) pelo texto digitado na busca.
function filterItems() {
    const term = searchInput.value.trim().toLowerCase();

    container.querySelectorAll(".list-item").forEach((item) => {
        const matches = item.textContent.toLowerCase().includes(term);
        item.hidden = !matches;
    });
}

function renderHome() {
    sections.forEach(({ buttonId, load, searchPlaceholder }) => {
        const btn = document.getElementById(buttonId);

        btn.addEventListener("click", async () => {
            closeModals();
            setActiveButton(btn);

            searchInput.value = "";
            searchInput.placeholder = searchPlaceholder;

            await load();
        });
    });

    searchInput.addEventListener("input", filterItems);
}

renderHome();
