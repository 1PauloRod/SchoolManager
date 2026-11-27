// Helpers compartilhados pelas páginas do painel admin.

export const container   = document.getElementById("cards");
export const searchInput = document.getElementById("search");

// ------------------------------------------------------------
// DOM básico
// ------------------------------------------------------------

export function el(tag, className = "", text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined && text !== null) node.textContent = text;
    return node;
}

export function button(text, onClick, variant = "") {
    const btn = el("button", ["btn", variant].filter(Boolean).join(" "), text);
    btn.type = "button";
    if (onClick) btn.addEventListener("click", onClick);
    return btn;
}

export function textInput(placeholder, value = "") {
    const input = el("input", "input");
    input.placeholder = placeholder;
    input.value = value ?? "";
    return input;
}

export function selectControl(placeholder, options = []) {
    const select = el("select", "input");
    select.add(new Option(placeholder, ""));
    options.forEach(({ value, label }) => select.add(new Option(label, value)));
    return select;
}

export function field(labelText, control) {
    const wrapper = el("label", "field");
    wrapper.append(el("span", "field-label", labelText), control);
    return wrapper;
}

// ------------------------------------------------------------
// CPF
// ------------------------------------------------------------

export function formatCpf(value = "") {
    let cpf = String(value).replace(/\D/g, "").slice(0, 11);

    cpf = cpf.replace(/(\d{3})(\d)/, "$1.$2");
    cpf = cpf.replace(/(\d{3})(\d)/, "$1.$2");
    cpf = cpf.replace(/(\d{3})(\d{1,2})$/, "$1-$2");

    return cpf;
}

export function cpfInput(value = "") {
    const input = textInput("CPF", formatCpf(value));
    input.maxLength = 14;
    input.inputMode = "numeric";
    input.addEventListener("input", () => {
        input.value = formatCpf(input.value);
    });
    return input;
}

// ------------------------------------------------------------
// Blocos de tela
// ------------------------------------------------------------

export function joinMeta(...parts) {
    return parts.filter(Boolean).join(" · ");
}

export function pageHeader(title, ...actions) {
    const header = el("div", "page-header");
    const actionsBox = el("div", "page-actions");

    actions.filter(Boolean).forEach(a => actionsBox.appendChild(a));

    header.append(el("h2", "page-title", title), actionsBox);
    return header;
}

export function sectionTitle(text, count) {
    const h = el("h3", "section-title", text);
    if (count !== undefined) h.appendChild(el("span", "count", count));
    return h;
}

export function emptyState(text) {
    return el("p", "empty-state", text);
}

export function listItem({ title, meta }, ...actions) {
    const item = el("div", "list-item");
    const info = el("div", "item-info");

    info.appendChild(el("p", "item-title", title));
    if (meta) info.appendChild(el("p", "item-meta", meta));

    const actionsBox = el("div", "item-actions");
    actions.filter(Boolean).forEach(a => actionsBox.appendChild(a));

    item.append(info, actionsBox);
    return item;
}

// Formulário de cadastro/edição renderizado dentro do container.
export function renderForm({ title, fields, onSave, onCancel }) {
    container.innerHTML = "";

    const form = el("form", "form-card");
    form.appendChild(el("h2", "form-title", title));

    fields.forEach(({ label, input }) => form.appendChild(field(label, input)));

    const save = el("button", "btn primary", "Salvar");
    save.type = "submit";

    const actions = el("div", "form-actions");
    actions.append(button("Cancelar", onCancel, "ghost"), save);
    form.appendChild(actions);

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        await onSave();
    });

    container.appendChild(form);
    form.querySelector("input")?.focus();
}

// ------------------------------------------------------------
// Modais
// ------------------------------------------------------------

export function closeModals() {
    document.querySelectorAll(".modal").forEach(modal => modal.remove());
}

export function createModal({ title, description, content = [], actions = [] }) {
    closeModals();

    const modal = el("div", "modal");
    const box   = el("div", "modal-box");

    box.appendChild(el("h3", "modal-title", title));
    if (description) box.appendChild(el("p", "modal-description", description));

    content.forEach(node => box.appendChild(node));

    const footer = el("div", "modal-actions");
    actions.forEach(a => footer.appendChild(a));
    box.appendChild(footer);

    modal.appendChild(box);
    modal.addEventListener("click", (event) => {
        if (event.target === modal) modal.remove();
    });

    document.body.appendChild(modal);
    return modal;
}

// Modal simples com um <select> (usado para adicionar aluno/professor à turma).
export function openSelectModal({
    title,
    placeholder,
    options,
    emptyText,
    requiredMessage,
    errorMessage,
    onSave
}) {
    const select = selectControl(placeholder, options);

    if (options.length === 0) {
        const empty = new Option(emptyText, "");
        empty.disabled = true;
        select.add(empty);
    }

    const btnCancel = button("Cancelar", () => modal.remove(), "ghost");

    const btnSave = button("Salvar", async () => {
        if (!select.value) {
            alert(requiredMessage);
            return;
        }

        try {
            await onSave(select.value);
            modal.remove();
        } catch (err) {
            console.error(err);
            alert(errorMessage);
        }
    }, "primary");

    const modal = createModal({
        title,
        content: [select],
        actions: [btnCancel, btnSave]
    });

    return modal;
}
