import API_URL from "./client";

export async function getJobs(token, page=1, limit=5, status=null) {
    const params = new URLSearchParams({page, limit});
    if (status) {params.append("status",status)}

    const response = await fetch(`${API_URL}/jobs?${params}`,{
        headers:{ Authorization: `Bearer ${token}` }
    });
    return response
}

export async function createJob(token, title, description){
    const response = await fetch(`${API_URL}/jobs`,{
        method: "POST",
        headers:{
            "Content-Type":"application/json",
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({title,description}),
    });
    return response;
}

export async function updateJob(token, jobId, status) {
    const params = new URLSearchParams({status})
    const response = await fetch(`${API_URL}/jobs/${jobId}?${params}`,{
        method: "PUT",
        headers:{Authorization: `Bearer ${token}` },
    });
    return response    
}

export async function deleteJob(token, jobId) {
    const response = await fetch(`${API_URL}/jobs/${jobId}`,{
        method:"DELETE",
         headers:{Authorization: `Bearer ${token}` },       
    });
    return response
}