import { useState } from 'react';
import { login } from '../../api/auth'

function LoginForm() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");

    async function handleSubmit(e){
        e.preventDefault();

        const response = await login(username, password);
        const data = await response.json()

        if (response.status == 200){
            const token = data.access_token
            console.log("Login Successful. Token:", token)
            setMessage("Login Successful.")
        }else{
            setMessage(data.detail || "Login failed.")
        }
    }
    return(
        <form onSubmit={handleSubmit}>
            <h3>Login</h3>

            <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e)=>setUsername(e.target.value)}
            />

            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />

            <button type='submit'>Login</button>

            {message && <p>{message}</p>}
        </form>
    );
}

export default LoginForm