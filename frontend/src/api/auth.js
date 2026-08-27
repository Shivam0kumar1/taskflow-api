import API_URL from "./client"

export async function signup(username, password){
    const response = await fetch(`${API_URL}/signup`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password}),
    });
    return response;
}

export async function login(username, password){
    const response = await fetch(`${API_URL}/login`, {
        method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({username, password}),
    });
    return response;
}