import { BASE_URL } from "../api/config.js";
import { getAuthHeaders } from "../api/config.js";

export async function getStudents(){

    const response = await fetch(`${BASE_URL}/students/`, 
    {
        method: "GET", 
        headers: getAuthHeaders()
    })

    if (!response.ok){
        throw Error("Erro buscar estudante");
    }

    return response.json();
}

export async function postStudents(student){

    const response = await fetch(`${BASE_URL}/students/`, 
    {
        method: "POST", 
        headers: getAuthHeaders(), 
        body: JSON.stringify(student)
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

export async function updateStudent(student_id, student){

    const response = await fetch(`${BASE_URL}/students/${student_id}/`, 
        {
            method: 'PATCH', 
            headers: getAuthHeaders(), 
            body: JSON.stringify(student)
        }
    )

    const data = await response.json();

    if (!response.ok) {
        console.error("Erro da API:", data);
        throw new Error(
            `Erro ao atualizar estudante (${response.status}): ${JSON.stringify(data)}`
        );
    }

    return data;
}

export async function deleteStudent(student_id, student){
    
    const response = await fetch(`${BASE_URL}/students/${student_id}/`, 
        {
            method: "DELETE", 
            headers: getAuthHeaders(), 
            body: JSON.stringify(student)
        }
    ); 

    const data = await response.json();

    if (!response.ok) {
        console.error("Erro da API:", data);
        throw new Error(
            `Erro ao excluir alunos (${response.status}): ${JSON.stringify(data)}`
        );
    }

    return data;
}