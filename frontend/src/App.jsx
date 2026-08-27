import './App.css'
import SignupForm from './components/auth/SignupForm'
import LoginForm from './components/auth/LoginForm'

function App(){
    return(
        <div>
            <h1>Taskflow</h1>
            <p>Welcome to Taskflow</p>

            <SignupForm/>
            <LoginForm/>
         </div>
        )
    }

export default App