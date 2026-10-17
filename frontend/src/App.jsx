import './App.css'
import { AuthProvider, useAuth } from './context/AuthContext'
import SignupForm from './components/auth/SignupForm'
import LoginForm from './components/auth/LoginForm'
import DashboardPage from './pages/DashboardPage'
import JobsTable from './components/jobs/JobsTable'

function AppContent() {
    const {isLoggedIn, logout} = useAuth()

    return(
        <div>
            <h1>Taskflow</h1>

            {isLoggedIn ? (
                <DashboardPage />
            ):(
            <div>
                <p>Welcome to Taskflow</p>
                <SignupForm/>
                <LoginForm/>
            </div>                
            )}
        </div>
    )
} 

function App(){
    return(
        <AuthProvider>
            <AppContent/>
        </AuthProvider>
        )
    }

export default App