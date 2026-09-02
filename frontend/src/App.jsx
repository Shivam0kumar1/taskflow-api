import './App.css'
import { AuthProvider, useAuth } from './context/AuthContext'
import SignupForm from './components/auth/SignupForm'
import LoginForm from './components/auth/LoginForm'
import { useState } from 'react'

function AppContent() {
    const {isLoggedIn, logout} = useAuth()

    return(
        <div>
            <h1>Taskflow</h1>

            {isLoggedIn ? (
                <div>
                    <p>Welcome back! You are logged in.</p>
                    <button onClick={logout}>Logout</button>
                </div>
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