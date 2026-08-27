import { useState } from 'react';
import { signup } from '../../api/auth'

function SignupForm() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");

    async function handleSubmit(e){
        e.preventDefault();

        const response = await signup(username, password);
        const data = await response.json();

        if (response.status === 200) {
            setMessage("Account created successfully! You can now log in now.");
        }else{
            setMessage(data.details || "Signup Failed.");
        }
    }
    return (
        <form onSubmit={handleSubmit}>
            <h3>Create Account</h3>

            <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />

            <input
                type="password"
                placeholder="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />

            <button type="submit">Create Account</button>

            {message && <p>{message}</p>}
        </form>
    );
}

export default SignupForm;