import { useState } from 'react';
import { login as loginRequest} from '../../api/auth';
import { useAuth } from '../../context/AuthContext';

function LoginForm() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");
    const { login } = useAuth();

    async function handleSubmit(e){
        e.preventDefault();

        const response = await loginRequest(username, password);
        const data = await response.json()

        if (response.status == 200){
            login(data.access_token);
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