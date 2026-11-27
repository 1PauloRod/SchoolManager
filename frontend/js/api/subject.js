import { BASE_URL } from "../api/config.js";
import { getAuthHeaders } from "../api/config.js";

export async function getSubjects(){
    
    const response = await fetch(`${BASE_URL}/subjects/`, 
        {
            method: "GET", 
            headers: getAuthHeaders()
        }
    )

    if (!response.ok) throw Error("Não foi possível buscar a matéria");

    return response.json();
}

export async function postSubjects(subject){
    
    const response = await fetch(`${BASE_URL}/subjects/`, 
        {
            method: "POST", 
            headers: getAuthHeaders(),
            body: JSON.stringify(subject)
        }
    )

    const data = await response.json();

    if (!response.ok) {
        console.error("Erro da API:", data);
        throw new Error(
            `Erro ao cadastrar matéria (${response.status}): ${JSON.stringify(data)}`
        );
    }

    return data;
}

export async function deleteSubjects(subject_id, subject){
    
    const response = await fetch(`${BASE_URL}/subjects/${subject_id}/`, 
        {
            method: "DELETE", 
            headers: getAuthHeaders(),
            body: JSON.stringify(subject)
        }
    )

    const data = await response.json();

    if (!response.ok) {
        console.error("Erro da API:", data);
        throw new Error(
            `Erro ao deletar matéria (${response.status}): ${JSON.stringify(data)}`
        );
    }

    return data;
}