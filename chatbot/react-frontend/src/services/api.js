import axios from 'axios'

// Create axios instance with base configuration
export const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API functions for different endpoints
export const authAPI = {
  login: (email, password) => api.post('/api/login', { email, password }),
  signup: (name, email, password) => api.post('/api/signup', { name, email, password }),
  logout: () => api.post('/api/logout'),
}

export const chatAPI = {
  sendMessage: (message, sessionId = 'default') => 
    api.post('/api/chat', { message, session_id: sessionId }),
  getStatus: () => api.get('/api/status'),
  clearSource: (sourceType = 'all') => 
    api.post('/api/clear_source', { source_type: sourceType }),
}

export const uploadAPI = {
  uploadPDF: (file) => {
    const formData = new FormData()
    formData.append('pdf', file)
    return api.post('/api/load_pdf', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  loadWebsite: (url) => api.post('/api/load_website', { url }),
}

export const speechAPI = {
  speechToText: (audioFile) => {
    const formData = new FormData()
    formData.append('audio', audioFile)
    return api.post('/api/speech-to-text', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  textToSpeech: (text) => api.post('/api/text-to-speech', { text }),
}

export default api
