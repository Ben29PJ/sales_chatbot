import React, { createContext, useContext, useState, useEffect } from 'react'
import { api } from '../services/api'

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check for existing token on app start
    const token = localStorage.getItem('token')
    if (token) {
      // Set token in API client
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`
      
      // Try to get user info or validate token
      const userData = localStorage.getItem('user')
      if (userData) {
        try {
          setUser(JSON.parse(userData))
        } catch (e) {
          localStorage.removeItem('token')
          localStorage.removeItem('user')
        }
      }
    }
    setLoading(false)
  }, [])

  const login = async (email, password) => {
    try {
      const response = await api.post('/api/login', { email, password })
      const { user: userData, token } = response.data
      
      // Store token and user data
      localStorage.setItem('token', token)
      localStorage.setItem('user', JSON.stringify(userData))
      
      // Set token in API client
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`
      
      setUser(userData)
      return { success: true, data: response.data }
    } catch (error) {
      const message = error.response?.data?.detail || 'Login failed'
      return { success: false, error: message }
    }
  }

  const signup = async (name, email, password) => {
    try {
      const response = await api.post('/api/signup', { name, email, password })
      const { user: userData, token } = response.data
      
      // Store token and user data
      localStorage.setItem('token', token)
      localStorage.setItem('user', JSON.stringify(userData))
      
      // Set token in API client
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`
      
      setUser(userData)
      return { success: true, data: response.data }
    } catch (error) {
      const message = error.response?.data?.detail || 'Signup failed'
      return { success: false, error: message }
    }
  }

  const logout = async () => {
    try {
      await api.post('/api/logout')
    } catch (error) {
      // Even if API call fails, we still want to log out locally
      console.error('Logout API call failed:', error)
    }
    
    // Clear local storage and state
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    delete api.defaults.headers.common['Authorization']
    setUser(null)
  }

  const value = {
    user,
    login,
    signup,
    logout,
    loading
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}
