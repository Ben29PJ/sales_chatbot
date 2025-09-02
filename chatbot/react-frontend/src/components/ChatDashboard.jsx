import React, { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Send, 
  Upload, 
  Globe, 
  Mic, 
  MicOff, 
  Volume2, 
  Trash2, 
  User, 
  LogOut,
  Sparkles,
  FileText,
  MessageSquare,
  Settings,
  Activity
} from 'lucide-react'
import toast from 'react-hot-toast'
import { useAuth } from '../contexts/AuthContext'
import { chatAPI, uploadAPI, speechAPI } from '../services/api'
import FileUpload from './FileUpload'
import ChatMessage from './ChatMessage'
import StatusPanel from './StatusPanel'

const ChatDashboard = () => {
  const { user, logout } = useAuth()
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId] = useState(() => `session-${Date.now()}`)
  const [isRecording, setIsRecording] = useState(false)
  const [mediaRecorder, setMediaRecorder] = useState(null)
  const [audioChunks, setAudioChunks] = useState([])
  const [status, setStatus] = useState(null)
  const [activeTab, setActiveTab] = useState('chat')
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [currentUtterance, setCurrentUtterance] = useState(null)
  
  const messagesEndRef = useRef(null)
  const fileInputRef = useRef(null)

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Load status on component mount
  useEffect(() => {
    loadStatus()
  }, [])

  const loadStatus = async () => {
    try {
      const response = await chatAPI.getStatus()
      setStatus(response.data)
    } catch (error) {
      console.error('Failed to load status:', error)
    }
  }

  const sendMessage = async (messageText = inputMessage) => {
    if (!messageText.trim()) return

    const userMessage = { 
      role: 'user', 
      content: messageText, 
      timestamp: new Date().toISOString() 
    }
    
    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)

    try {
      const response = await chatAPI.sendMessage(messageText, sessionId)
      
      if (response.data.success) {
        const assistantMessage = {
          role: 'assistant',
          content: response.data.response,
          timestamp: response.data.timestamp,
          sources: response.data.loaded_sources
        }
        
        setMessages(prev => [...prev, assistantMessage])
        await loadStatus() // Refresh status
      } else {
        toast.error('Failed to get response from assistant')
      }
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Failed to send message'
      toast.error(errorMessage)
      
      // Add error message to chat
      const errorChatMessage = {
        role: 'assistant',
        content: `Sorry, I encountered an error: ${errorMessage}`,
        timestamp: new Date().toISOString(),
        isError: true
      }
      setMessages(prev => [...prev, errorChatMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const handleFileUpload = async (file) => {
    if (!file) return

    const uploadToast = toast.loading('Uploading and processing file...')
    
    try {
      const response = await uploadAPI.uploadPDF(file)
      
      if (response.data.success) {
        toast.success('PDF uploaded successfully!', { id: uploadToast })
        await loadStatus()
        
        // Add system message about upload
        const systemMessage = {
          role: 'system',
          content: `📄 PDF uploaded: ${response.data.filename} (${response.data.word_count} words)`,
          timestamp: new Date().toISOString()
        }
        setMessages(prev => [...prev, systemMessage])
      }
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Failed to upload PDF'
      toast.error(errorMessage, { id: uploadToast })
    }
  }

  const handleWebsiteLoad = async (url) => {
    if (!url.trim()) return

    const loadToast = toast.loading('Loading website content...')
    
    try {
      const response = await uploadAPI.loadWebsite(url)
      
      if (response.data.success) {
        toast.success('Website content loaded successfully!', { id: loadToast })
        await loadStatus()
        
        // Add system message about website load
        const systemMessage = {
          role: 'system',
          content: `🌐 Website loaded: ${response.data.url} (${response.data.word_count} words)`,
          timestamp: new Date().toISOString()
        }
        setMessages(prev => [...prev, systemMessage])
      }
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Failed to load website'
      toast.error(errorMessage, { id: loadToast })
    }
  }

  const clearSources = async (sourceType = 'all') => {
    try {
      const response = await chatAPI.clearSource(sourceType)
      
      if (response.data.success) {
        toast.success(response.data.message)
        await loadStatus()
        setMessages([])
      }
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Failed to clear sources'
      toast.error(errorMessage)
    }
  }

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          sampleRate: 44100
        }
      })
      
      // Reset audio chunks before starting new recording
      const currentAudioChunks = []
      setAudioChunks([])
      
      const recorder = new MediaRecorder(stream, {
        mimeType: MediaRecorder.isTypeSupported('audio/webm;codecs=opus') 
          ? 'audio/webm;codecs=opus' 
          : 'audio/webm'
      })
      
      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          currentAudioChunks.push(event.data)
          setAudioChunks(prev => [...prev, event.data])
        }
      }
      
      recorder.onstop = async () => {
        stream.getTracks().forEach(track => track.stop())
        
        // Process audio chunks immediately using local array
        if (currentAudioChunks.length > 0) {
          try {
            const audioBlob = new Blob(currentAudioChunks, { 
              type: recorder.mimeType || 'audio/webm' 
            })
            
            console.log('Audio blob created:', {
              size: audioBlob.size,
              type: audioBlob.type
            })
            
            if (audioBlob.size > 0) {
              await handleSpeechToText(audioBlob)
            } else {
              toast.error('No audio data recorded. Please try again.')
            }
          } catch (error) {
            console.error('Error processing audio:', error)
            toast.error('Failed to process audio recording')
          }
        } else {
          toast.error('No audio data captured. Please try recording again.')
        }
        
        setAudioChunks([])
      }
      
      recorder.start(100) // Record in 100ms chunks
      setMediaRecorder(recorder)
      setIsRecording(true)
      toast.success('🎤 Recording started - speak clearly!')
    } catch (error) {
      console.error('Recording error:', error)
      toast.error(`Failed to start recording: ${error.message}`)
    }
  }

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop()
      mediaRecorder.stream.getTracks().forEach(track => track.stop())
      setIsRecording(false)
      toast.success('Recording stopped, processing...')
    }
  }

  const handleSpeechToText = async (audioBlob) => {
    try {
      const response = await speechAPI.speechToText(audioBlob)
      
      if (response.data.success && response.data.text) {
        setInputMessage(response.data.text)
        toast.success('Speech converted to text!')
      }
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Speech recognition failed'
      toast.error(errorMessage)
    }
  }

  const handleTextToSpeech = (text, messageId) => {
    if ('speechSynthesis' in window) {
      // Stop any currently playing speech
      if (isSpeaking) {
        stopTextToSpeech()
      }

      const utterance = new SpeechSynthesisUtterance(text)
      utterance.rate = 0.9
      utterance.pitch = 1
      utterance.volume = 0.8
      
      utterance.onstart = () => {
        setIsSpeaking(true)
        setCurrentUtterance(utterance)
      }
      
      utterance.onend = () => {
        setIsSpeaking(false)
        setCurrentUtterance(null)
      }
      
      utterance.onerror = () => {
        setIsSpeaking(false)
        setCurrentUtterance(null)
        toast.error('Speech playback failed')
      }
      
      window.speechSynthesis.speak(utterance)
      toast.success('Playing audio...')
    } else {
      toast.error('Text-to-speech not supported in this browser')
    }
  }

  const stopTextToSpeech = () => {
    if ('speechSynthesis' in window && isSpeaking) {
      window.speechSynthesis.cancel()
      setIsSpeaking(false)
      setCurrentUtterance(null)
      toast.success('Audio stopped')
    }
  }

  return (
    <div className="min-h-screen flex">
      {/* Sidebar */}
      <motion.div
        initial={{ x: -300 }}
        animate={{ x: 0 }}
        className="w-80 glass-effect border-r border-white/10 flex flex-col"
      >
        {/* Header */}
        <div className="p-6 border-b border-white/10">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 premium-gradient rounded-xl flex items-center justify-center">
              <Sparkles className="h-5 w-5 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-secondary-50">Wolf AI</h1>
              <p className="text-xs text-secondary-400">Premium Assistant</p>
            </div>
          </div>
        </div>

        {/* User Info */}
        <div className="p-4 border-b border-white/10">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-primary-500 rounded-full flex items-center justify-center">
              <User className="h-4 w-4 text-white" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-secondary-200 truncate">
                {user?.name}
              </p>
              <p className="text-xs text-secondary-500 truncate">
                {user?.email}
              </p>
            </div>
            <button
              onClick={logout}
              className="p-2 text-secondary-400 hover:text-danger-400 transition-colors"
              title="Logout"
            >
              <LogOut className="h-4 w-4" />
            </button>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="flex border-b border-white/10">
          {[
            { id: 'chat', icon: MessageSquare, label: 'Chat' },
            { id: 'upload', icon: Upload, label: 'Upload' },
            { id: 'status', icon: Activity, label: 'Status' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex-1 flex items-center justify-center px-4 py-3 text-sm font-medium transition-colors ${
                activeTab === tab.id
                  ? 'text-primary-400 border-b-2 border-primary-400'
                  : 'text-secondary-400 hover:text-secondary-200'
              }`}
            >
              <tab.icon className="h-4 w-4 mr-2" />
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <div className="flex-1 overflow-y-auto">
          {activeTab === 'upload' && (
            <div className="p-4 space-y-4">
              <FileUpload onFileUpload={handleFileUpload} />
              
              <div className="space-y-3">
                <h3 className="text-sm font-medium text-secondary-200">Load Website</h3>
                <input
                  type="url"
                  placeholder="https://example.com"
                  className="premium-input text-sm"
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      handleWebsiteLoad(e.target.value)
                      e.target.value = ''
                    }
                  }}
                />
                <p className="text-xs text-secondary-500">
                  Press Enter to load website content
                </p>
              </div>

              <div className="space-y-3">
                <h3 className="text-sm font-medium text-secondary-200">Clear Sources</h3>
                <div className="space-y-2">
                  <button
                    onClick={() => clearSources('pdf')}
                    className="w-full text-left px-3 py-2 text-sm text-secondary-300 hover:text-secondary-100 hover:bg-white/5 rounded-lg transition-colors"
                  >
                    Clear PDF
                  </button>
                  <button
                    onClick={() => clearSources('website')}
                    className="w-full text-left px-3 py-2 text-sm text-secondary-300 hover:text-secondary-100 hover:bg-white/5 rounded-lg transition-colors"
                  >
                    Clear Website
                  </button>
                  <button
                    onClick={() => clearSources('all')}
                    className="w-full text-left px-3 py-2 text-sm text-danger-400 hover:text-danger-300 hover:bg-danger-500/10 rounded-lg transition-colors"
                  >
                    Clear All & Reset
                  </button>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'status' && (
            <div className="p-4">
              <StatusPanel status={status} onRefresh={loadStatus} />
            </div>
          )}

          {activeTab === 'chat' && (
            <div className="p-4">
              <div className="space-y-3">
                <h3 className="text-sm font-medium text-secondary-200">Chat History</h3>
                <p className="text-xs text-secondary-500">
                  Your conversation with Wolf AI
                </p>
                {messages.length > 0 && (
                  <button
                    onClick={() => setMessages([])}
                    className="text-xs text-danger-400 hover:text-danger-300 transition-colors"
                  >
                    Clear Chat History
                  </button>
                )}
              </div>
            </div>
          )}
        </div>
      </motion.div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Chat Header */}
        <motion.div
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="glass-effect border-b border-white/10 p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-secondary-50">
                Wolf AI Assistant
              </h2>
              <p className="text-sm text-secondary-400">
                Your premium sales assistant ready to help
              </p>
            </div>
            <div className="flex items-center space-x-2">
              <div className="h-2 w-2 bg-success-500 rounded-full animate-pulse"></div>
              <span className="text-xs text-secondary-400">Online</span>
            </div>
          </div>
        </motion.div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          <AnimatePresence>
            {messages.length === 0 ? (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex flex-col items-center justify-center h-full text-center"
              >
                <div className="w-24 h-24 premium-gradient rounded-3xl flex items-center justify-center mb-6 shadow-premium-lg">
                  <Sparkles className="h-12 w-12 text-white" />
                </div>
                <h3 className="text-2xl font-bold text-secondary-50 mb-2">
                  Welcome to Wolf AI Premium
                </h3>
                <p className="text-secondary-400 max-w-md mb-6">
                  Upload a product catalog (PDF) or load website content to get started. 
                  I'm here to help with sales inquiries and product information.
                </p>
                <div className="flex flex-wrap gap-2 justify-center">
                  <span className="px-3 py-1 bg-primary-500/20 text-primary-300 text-xs rounded-full">
                    PDF Upload
                  </span>
                  <span className="px-3 py-1 bg-accent-500/20 text-accent-300 text-xs rounded-full">
                    Website Scraping
                  </span>
                  <span className="px-3 py-1 bg-success-500/20 text-success-300 text-xs rounded-full">
                    Voice Input
                  </span>
                </div>
              </motion.div>
            ) : (
              messages.map((message, index) => (
                <ChatMessage
                  key={index}
                  message={message}
                  messageId={index}
                  onTextToSpeech={handleTextToSpeech}
                  onStopSpeech={stopTextToSpeech}
                  isSpeaking={isSpeaking}
                />
              ))
            )}
          </AnimatePresence>
          
          {isLoading && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex items-center space-x-3 chat-message chat-assistant"
            >
              <div className="w-6 h-6 border-2 border-primary-500/30 border-t-primary-500 rounded-full animate-spin"></div>
              <span className="text-secondary-300">Wolf AI is thinking...</span>
            </motion.div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="border-t border-white/10 p-6"
        >
          <div className="flex items-end space-x-4">
            {/* Voice Recording Button */}
            <button
              onClick={isRecording ? stopRecording : startRecording}
              className={`p-3 rounded-xl transition-all duration-200 ${
                isRecording 
                  ? 'bg-danger-500 hover:bg-danger-600 text-white shadow-lg recording-pulse' 
                  : 'glass-effect text-secondary-400 hover:text-secondary-200 hover:bg-white/10'
              }`}
              title={isRecording ? 'Stop Recording' : 'Start Voice Recording'}
            >
              {isRecording ? (
                <MicOff className="h-5 w-5 animate-pulse" />
              ) : (
                <Mic className="h-5 w-5" />
              )}
            </button>

            {/* Message Input */}
            <div className="flex-1">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask me about products, pricing, features..."
                className="premium-input resize-none min-h-[3rem] max-h-32"
                rows={1}
                disabled={isLoading}
              />
            </div>

            {/* Send Button */}
            <button
              onClick={() => sendMessage()}
              disabled={!inputMessage.trim() || isLoading}
              className="premium-button p-3 disabled:opacity-50 disabled:cursor-not-allowed"
              title="Send Message"
            >
              <Send className="h-5 w-5" />
            </button>
          </div>

          {/* Quick Actions */}
          <div className="flex items-center justify-between mt-4">
            <div className="flex items-center space-x-2">
              <span className="text-xs text-secondary-500">Quick actions:</span>
              <button
                onClick={() => setActiveTab('upload')}
                className="text-xs text-primary-400 hover:text-primary-300 transition-colors"
              >
                Upload PDF
              </button>
              <span className="text-secondary-600">•</span>
              <button
                onClick={() => setActiveTab('upload')}
                className="text-xs text-accent-400 hover:text-accent-300 transition-colors"
              >
                Load Website
              </button>
            </div>
            
            <div className="text-xs text-secondary-500">
              Press Enter to send
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default ChatDashboard
