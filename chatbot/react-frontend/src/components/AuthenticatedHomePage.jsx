import React from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  MessageSquare, 
  Sparkles, 
  Users, 
  ArrowRight, 
  LogOut,
  FileText,
  Globe,
  Mic,
  BarChart3,
  Settings
} from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'

const AuthenticatedHomePage = () => {
  const { user, logout } = useAuth()

  const features = [
    {
      icon: <MessageSquare className="h-8 w-8" />,
      title: "Chat Assistant",
      description: "Access your AI-powered sales assistant for customer interactions",
      color: "from-blue-500 to-purple-600",
      link: "/dashboard",
      action: "Get Started"
    },
    {
      icon: <FileText className="h-8 w-8" />,
      title: "Document Management",
      description: "Upload and manage your product catalogs and documentation",
      color: "from-green-500 to-teal-600",
      link: "/dashboard",
      action: "Manage Files"
    },
    {
      icon: <BarChart3 className="h-8 w-8" />,
      title: "Analytics",
      description: "View insights and analytics from your customer interactions",
      color: "from-orange-500 to-red-600",
      link: "/dashboard",
      action: "View Analytics"
    }
  ]

  const quickActions = [
    { 
      title: "Start New Conversation", 
      icon: <MessageSquare className="h-5 w-5" />, 
      link: "/dashboard",
      color: "bg-primary-500 hover:bg-primary-600"
    },
    { 
      title: "Upload Documents", 
      icon: <FileText className="h-5 w-5" />, 
      link: "/dashboard",
      color: "bg-green-500 hover:bg-green-600"
    },
    { 
      title: "Voice Assistant", 
      icon: <Mic className="h-5 w-5" />, 
      link: "/dashboard",
      color: "bg-purple-500 hover:bg-purple-600"
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <motion.header
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="glass-effect border-b border-white/10"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 premium-gradient rounded-xl flex items-center justify-center shadow-lg">
                <span className="text-2xl">🐺</span>
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">Wolf AI</h1>
                <p className="text-xs text-gray-300">Premium Assistant</p>
              </div>
            </div>

            {/* User Info & Actions */}
            <div className="flex items-center space-x-4">
              <div className="glass-effect px-4 py-2 rounded-xl">
                <div className="flex items-center space-x-2">
                  <Users className="h-4 w-4 text-gray-300" />
                  <span className="text-sm text-white">Welcome, {user?.name}</span>
                </div>
              </div>
              <button
                onClick={logout}
                className="glass-effect px-4 py-2 rounded-xl hover:bg-white/10 text-gray-300 hover:text-white transition-all flex items-center space-x-2"
              >
                <LogOut className="h-4 w-4" />
                <span className="text-sm">Logout</span>
              </button>
            </div>
          </div>
        </div>
      </motion.header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Welcome Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <div className="w-24 h-24 premium-gradient rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-premium-lg">
            <span className="text-4xl">🐺</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Welcome to Wolf AI Dashboard
          </h1>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Your premium AI sales assistant is ready to help you provide exceptional customer experiences.
          </p>
        </motion.div>

        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-12"
        >
          <h2 className="text-2xl font-bold text-white mb-6 text-center">Quick Actions</h2>
          <div className="flex flex-wrap gap-4 justify-center">
            {quickActions.map((action, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 + index * 0.1 }}
              >
                <Link
                  to={action.link}
                  className={`${action.color} text-white px-6 py-3 rounded-xl font-semibold transition-all transform hover:scale-105 shadow-lg hover:shadow-xl flex items-center space-x-2`}
                >
                  {action.icon}
                  <span>{action.title}</span>
                </Link>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Feature Cards */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="grid md:grid-cols-3 gap-8 mb-12"
        >
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 + index * 0.1 }}
              className="glass-effect p-6 rounded-2xl border border-white/10 hover:border-white/20 transition-all duration-300 group"
            >
              <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${feature.color} flex items-center justify-center text-white shadow-lg mb-4 group-hover:scale-110 transition-transform`}>
                {feature.icon}
              </div>
              <h3 className="text-xl font-bold text-white mb-3">
                {feature.title}
              </h3>
              <p className="text-gray-300 mb-6 leading-relaxed">
                {feature.description}
              </p>
              <Link
                to={feature.link}
                className="inline-flex items-center text-primary-400 hover:text-primary-300 font-medium transition-colors group"
              >
                <span>{feature.action}</span>
                <ArrowRight className="h-4 w-4 ml-2 group-hover:translate-x-1 transition-transform" />
              </Link>
            </motion.div>
          ))}
        </motion.div>

        {/* Main CTA - Chat Assistant */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="text-center"
        >
          <div className="glass-effect p-8 rounded-3xl border border-white/10 max-w-2xl mx-auto">
            <div className="w-16 h-16 premium-gradient rounded-2xl flex items-center justify-center mx-auto mb-6">
              <MessageSquare className="h-8 w-8 text-white" />
            </div>
            <h2 className="text-3xl font-bold text-white mb-4">
              Ready to Start Selling?
            </h2>
            <p className="text-gray-300 mb-8">
              Access your AI-powered sales assistant and start providing exceptional customer support.
            </p>
            <Link
              to="/dashboard"
              className="premium-button px-8 py-4 text-lg font-semibold inline-flex items-center space-x-2 group"
            >
              <MessageSquare className="h-5 w-5" />
              <span>Launch Chat Assistant</span>
              <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default AuthenticatedHomePage
