import { BASE_URL } from "../api/config.js";
import { getAuthHeaders } from "../api/config.js";


export async function getLevelschool(){

    const response = await fetch(`${BASE_URL}/classes/school-level/;`, 
        {
            method: "GET", 
            headers: getAuthHeaders()
        }
    )

     if (!response.ok) throw Error("Não foi possível buscar nível escolar.");

    return response.json();
}

export async function getClasses(){

    const response = await fetch(`${BASE_URL}/classes/`, 
        {
            method: "GET", 
            headers: getAuthHeaders()
        }
    )

     if (!response.ok) throw Error("Não foi possível buscar nível escolar.");

    return response.json();
}

export async function getClassStudents(class_id){
    
    const response = await fetch(`${BASE_URL}/classes/${class_id}/students/`, 
        {
            method: "GET", 
            headers: getAuthHeaders()
        })

    if (!response.ok) throw Error("Não foi possível buscar aluno na turma.");

    return response.json();
}

export async function deleteClassStudents(class_id, student_id){
    
    const response = await fetch(`${BASE_URL}/classes/${class_id}/students/`, 
        {
            method: "DELETE", 
            headers: getAuthHeaders(), 
            body: JSON.stringify({
                student_id: student_id
            })
        })

    if (!response.ok) throw Error("Não foi possível remover aluno da turma.");

    return response.json();
}

export async function postClassStudents(class_id, student_id){
    
    const response = await fetch(`${BASE_URL}/classes/${class_id}/students/`, 
        {
            method: "POST", 
            headers: getAuthHeaders(), 
            body: JSON.stringify({
                student_id: student_id
            })
        })

    if (!response.ok) throw Error("Não foi possível adicionar o aluno a turma.");

    return response.json();
}

export async function getClassTeachers(class_id){
    
    const response = await fetch(`${BASE_URL}/classes/${class_id}/teachers/`, 
        {
            method: "GET", 
            headers: getAuthHeaders()
        })

    if (!response.ok) throw Error("Não foi possível buscar professor na turma.");

    return response.json();
}

export async function postClassTeachers(class_id, teacher_id){
    
    const response = await fetch(`${BASE_URL}/classes/${class_id}/teachers/`, 
        {
            method: "POST", 
            headers: getAuthHeaders(), 
            body: JSON.stringify({
                teacher_id: teacher_id
            })
        })

    if (!response.ok) throw Error("Não foi possível adicionar professor a turma.");

    return response.json();
}

export async function deleteClassTeachers(class_id, teacher_id){
    
    const response = await fetch(`${BASE_URL}/classes/${class_id}/teachers/`, 
        {
            method: "DELETE", 
            headers: getAuthHeaders(), 
            body: JSON.stringify({
                teacher_id: teacher_id
            })
        })

    if (!response.ok) throw Error("Não foi possível remover professor da turma.");

    return response.json();
}

export async function getClassSubjects(class_id){
    
    const response = await fetch(`${BASE_URL}/classes/${class_id}/subjects/`, 
        {
            method: "GET", 
            headers: getAuthHeaders()
        })

    if (!response.ok) throw Error("Não foi possível buscar as disciplinas da turma.");

    return response.json();
}


export async function getClassSchedules(class_id){
    
    const response = await fetch(`${BASE_URL}/classes/${class_id}/schedule/`, 
        {
            method: "GET", 
            headers: getAuthHeaders()
        })

    if (!response.ok) throw Error("Não foi possível buscar a grade horária da turma.");

    return response.json();
}

export async function postClassSchedules(class_id, schedule){
    
    const response = await fetch(`${BASE_URL}/classes/${class_id}/schedule/`, 
        {
            method: "POST", 
            headers: getAuthHeaders(), 
            body: JSON.stringify(schedule) 
        })

    if (!response.ok) throw Error("Não foi possível salvar a grade horária da turma.");

    return response.json();
}