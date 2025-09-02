import React from 'react'
import { motion } from 'framer-motion'
import { Volume2, VolumeX, User, Sparkles, Info, AlertCircle } from 'lucide-react'

const ChatMessage = ({ message, messageId, onTextToSpeech, onStopSpeech, isSpeaking }) => {
  const isUser = message.role === 'user'
  const isSystem = message.role === 'system'
  const isError = message.isError

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}
    >
      <div className={`max-w-2xl ${isUser ? 'ml-16' : 'mr-16'}`}>
        {/* Message Container */}
        <div
          className={`px-6 py-4 rounded-2xl shadow-lg ${
            isUser 
              ? 'chat-user' 
              : isSystem 
                ? 'glass-effect border-accent-500/30' 
                : isError 
                  ? 'glass-effect border-danger-500/30'
                  : 'chat-assistant'
          }`}
        >
          {/* Message Header */}
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center space-x-2">
              {isUser ? (
                <User className="h-4 w-4 text-primary-400" />
              ) : isSystem ? (
                <Info className="h-4 w-4 text-accent-400" />
              ) : isError ? (
                <AlertCircle className="h-4 w-4 text-danger-400" />
              ) : (
                <Sparkles className="h-4 w-4 text-primary-400" />
              )}
              <span className="text-xs font-medium text-secondary-300">
                {isUser ? 'You' : isSystem ? 'System' : 'Wolf AI'}
              </span>
              {message.sources && message.sources.length > 0 && (
                <div className="flex space-x-1">
                  {message.sources.map((source, index) => (
                    <span
                      key={index}
                      className="px-2 py-0.5 bg-primary-500/20 text-primary-300 text-xs rounded-full"
                    >
                      {source}
                    </span>
                  ))}
                </div>
              )}
            </div>
            
            <div className="flex items-center space-x-2">
              {message.timestamp && (
                <span className="text-xs text-secondary-500">
                  {formatTimestamp(message.timestamp)}
                </span>
              )}
              {!isUser && !isSystem && onTextToSpeech && (
                <div className="flex items-center space-x-1">
                  <button
                    onClick={() => onTextToSpeech(message.content, messageId)}
                    disabled={isSpeaking}
                    className="p-1 text-secondary-400 hover:text-secondary-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    title="Read aloud"
                  >
                    <Volume2 className="h-3 w-3" />
                  </button>
                  {isSpeaking && (
                    <button
                      onClick={onStopSpeech}
                      className="p-1 text-danger-400 hover:text-danger-300 transition-colors"
                      title="Stop reading"
                    >
                      <VolumeX className="h-3 w-3" />
                    </button>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Message Content */}
          <div 
            className={`text-sm leading-relaxed ${
              isUser 
                ? 'text-secondary-100' 
                : isSystem 
                  ? 'text-accent-200' 
                  : isError 
                    ? 'text-danger-200'
                    : 'text-secondary-200'
            }`}
          >
            {message.content.split('\n').map((line, index) => (
              <p key={index} className={index > 0 ? 'mt-2' : ''}>
                {line}
              </p>
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  )
}

export default ChatMessage
