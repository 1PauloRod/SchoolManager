import { BASE_URL } from "../api/config.js";
import { getAuthHeaders } from "../api/config.js";


export async function getTeachers(){

    const response = await fetch(`${BASE_URL}/teachers/`, 
        {
            method: "GET", 
            headers: getAuthHeaders()
        }
    );

    if (!response.ok) throw Error("Erro ao buscar professor.");

    return response.json();
}

export async function postTeachers(teacher){

    const response = await fetch(`${BASE_URL}/teachers/`, 
    {
        method: "POST", 
        headers: getAuthHeaders(), 
        body: JSON.stringify(teacher)
    })

    const data = await response.json();

    if (!response.ok) {
        console.error("Erro da API:", data);
        throw new Error(
            `Erro ao cadastrar estudante (${response.status}): ${JSON.stringify(data)}`
        );
    }

    return data;
}

export async function deleteTeacher(teacher_id, teacher){

    const response = await fetch(`${BASE_URL}/teachers/${teacher_id}/`, 
    {
        method: "DELETE", 
        headers: getAuthHeaders(), 
        body: JSON.stringify(teacher)
    })

    const data = await response.json();

    if (!response.ok) {
        console.error("Erro da API:", data);
        throw new Error(
            `Erro ao deletar professor (${response.status}): ${JSON.stringify(data)}`
        );
    }

    return data;
}

export async function updateTeacher(teacher_id, teacher){

    const response = await fetch(`${BASE_URL}/teachers/${teacher_id}/`, 
        {
            method: "PATCH", 
            headers: getAuthHeaders(), 
            body: JSON.stringify(teacher)
        }
    )

    const data = await response.json();

    if (!response.ok) {
        console.error("Erro da API:", data);
        throw new Error(
            `Erro ao editar professor (${response.status}): ${JSON.stringify(data)}`
        );
    }

    return data;
}