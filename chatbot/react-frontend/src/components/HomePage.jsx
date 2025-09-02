import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Link } from 'react-router-dom'
import { 
  Sparkles, 
  Brain,
  MessageSquare,
  Zap,
  Shield,
  Users,
  ChevronRight,
  Play,
  ArrowRight,
  Star,
  Globe,
  FileText,
  Mic
} from 'lucide-react'

const HomePage = () => {
  const [activeFeature, setActiveFeature] = useState(0)
  const [isVideoPlaying, setIsVideoPlaying] = useState(false)

  const features = [
    {
      icon: <Brain className="h-8 w-8" />,
      title: "Intelligent AI Assistant",
      description: "Advanced AI powered by Groq's cutting-edge language models for superior conversation quality",
      color: "from-blue-500 to-purple-600"
    },
    {
      icon: <FileText className="h-8 w-8" />,
      title: "Document Intelligence",
      description: "Upload PDF catalogs and documents to create a comprehensive knowledge base for your business",
      color: "from-green-500 to-teal-600"
    },
    {
      icon: <Globe className="h-8 w-8" />,
      title: "Website Integration",
      description: "Scrape and analyze website content to keep your AI assistant updated with latest information",
      color: "from-orange-500 to-red-600"
    },
    {
      icon: <Mic className="h-8 w-8" />,
      title: "Voice Interaction",
      description: "Natural speech-to-text and text-to-speech capabilities for seamless voice conversations",
      color: "from-purple-500 to-pink-600"
    }
  ]

  const testimonials = [
    {
      name: "Sarah Johnson",
      role: "Sales Manager",
      company: "TechCorp Inc.",
      content: "Wolf AI has transformed our customer support. Response time decreased by 80% while maintaining high quality.",
      rating: 5
    },
    {
      name: "Michael Chen", 
      role: "CEO",
      company: "Innovation Labs",
      content: "The AI understands our products perfectly. It's like having an expert salesperson available 24/7.",
      rating: 5
    },
    {
      name: "Emily Rodriguez",
      role: "Customer Success",
      company: "GrowthCo",
      content: "Our customers love the voice interaction feature. It feels natural and professional.",
      rating: 5
    }
  ]

  const stats = [
    { number: "99.9%", label: "Uptime", icon: <Shield className="h-6 w-6" /> },
    { number: "10K+", label: "Conversations", icon: <MessageSquare className="h-6 w-6" /> },
    { number: "500+", label: "Happy Clients", icon: <Users className="h-6 w-6" /> },
    { number: "<1s", label: "Response Time", icon: <Zap className="h-6 w-6" /> }
  ]

  // Auto-rotate features
  useEffect(() => {
    const interval = setInterval(() => {
      setActiveFeature((prev) => (prev + 1) % features.length)
    }, 4000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Navigation */}
      <nav className="relative z-50 glass-effect border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <motion.div 
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center space-x-3"
            >
              <div className="w-10 h-10 premium-gradient rounded-xl flex items-center justify-center shadow-lg">
                <span className="text-2xl">🐺</span>
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">Wolf AI</h1>
                <p className="text-xs text-gray-300">Premium Assistant</p>
              </div>
            </motion.div>

            {/* Navigation Links */}
            <motion.div 
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="hidden md:flex items-center space-x-8"
            >
              <a href="#features" className="text-gray-300 hover:text-white transition-colors">
                Features
              </a>
              <a href="#about" className="text-gray-300 hover:text-white transition-colors">
                About
              </a>
              <a href="#testimonials" className="text-gray-300 hover:text-white transition-colors">
                Testimonials
              </a>
              <Link 
                to="/login"
                className="premium-button px-6 py-2 text-sm font-medium"
              >
                Login
              </Link>
              <Link 
                to="/signup"
                className="glass-effect px-6 py-2 text-sm font-medium text-white hover:bg-white/10 rounded-lg transition-all"
              >
                Sign Up
              </Link>
            </motion.div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 lg:py-32">
        {/* Background Animation */}
        <div className="absolute inset-0">
          <div className="absolute inset-0 bg-gradient-to-r from-blue-600/20 to-purple-600/20 animate-pulse"></div>
          {Array.from({ length: 50 }).map((_, i) => (
            <motion.div
              key={i}
              className="absolute w-1 h-1 bg-white rounded-full opacity-30"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
              }}
              animate={{
                y: [0, -20, 0],
                opacity: [0.3, 0.8, 0.3],
              }}
              transition={{
                duration: 3 + Math.random() * 2,
                repeat: Infinity,
                delay: Math.random() * 2,
              }}
            />
          ))}
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            {/* Main Hero Content */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              <div className="mb-8">
                <span className="inline-flex items-center px-4 py-2 rounded-full bg-white/10 text-white text-sm font-medium backdrop-blur-sm border border-white/20">
                  <Sparkles className="h-4 w-4 mr-2" />
                  Powered by Advanced AI Technology
                </span>
              </div>
              
              <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-white mb-6">
                Meet{' '}
                <span className="bg-gradient-to-r from-orange-400 via-yellow-500 to-orange-600 bg-clip-text text-transparent">
                  Wolf AI
                </span>
                <br />
                Your Premium Sales Assistant
              </h1>
              
              <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto leading-relaxed">
                Transform your customer interactions with intelligent AI that understands your products, 
                answers questions instantly, and helps close more deals.
              </p>

              {/* CTA Buttons */}
              <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
                <Link 
                  to="/signup"
                  className="premium-button px-8 py-4 text-lg font-semibold flex items-center space-x-2 group"
                >
                  <span>Get Started Free</span>
                  <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
                </Link>
                
                <button 
                  onClick={() => setIsVideoPlaying(true)}
                  className="glass-effect px-8 py-4 text-lg font-semibold text-white hover:bg-white/10 rounded-xl transition-all flex items-center space-x-2 group"
                >
                  <Play className="h-5 w-5 group-hover:scale-110 transition-transform" />
                  <span>Watch Demo</span>
                </button>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto">
                {stats.map((stat, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: index * 0.1 }}
                    className="text-center"
                  >
                    <div className="glass-effect p-4 rounded-xl border border-white/10">
                      <div className="flex justify-center mb-2 text-orange-400">
                        {stat.icon}
                      </div>
                      <div className="text-2xl md:text-3xl font-bold text-white mb-1">
                        {stat.number}
                      </div>
                      <div className="text-gray-400 text-sm">
                        {stat.label}
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 lg:py-32 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">
              Why Choose Wolf AI?
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Built with cutting-edge technology to deliver exceptional customer experiences
            </p>
          </motion.div>

          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Features List */}
            <div className="space-y-6">
              {features.map((feature, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                  className={`glass-effect p-6 rounded-2xl cursor-pointer transition-all duration-300 ${
                    activeFeature === index ? 'ring-2 ring-orange-400/50 bg-white/10' : 'hover:bg-white/5'
                  }`}
                  onClick={() => setActiveFeature(index)}
                >
                  <div className="flex items-start space-x-4">
                    <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${feature.color} flex items-center justify-center text-white shadow-lg`}>
                      {feature.icon}
                    </div>
                    <div className="flex-1">
                      <h3 className="text-xl font-bold text-white mb-2">
                        {feature.title}
                      </h3>
                      <p className="text-gray-300 leading-relaxed">
                        {feature.description}
                      </p>
                    </div>
                    <ChevronRight className="h-5 w-5 text-gray-400" />
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Feature Preview */}
            <motion.div
              key={activeFeature}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5 }}
              className="glass-effect p-8 rounded-2xl border border-white/10"
            >
              <div className={`w-16 h-16 rounded-2xl bg-gradient-to-r ${features[activeFeature].color} flex items-center justify-center text-white shadow-lg mb-6`}>
                {features[activeFeature].icon}
              </div>
              <h3 className="text-2xl font-bold text-white mb-4">
                {features[activeFeature].title}
              </h3>
              <p className="text-gray-300 text-lg leading-relaxed mb-6">
                {features[activeFeature].description}
              </p>
              <div className="bg-gradient-to-r from-slate-800 to-slate-700 p-4 rounded-xl">
                <div className="flex items-center space-x-2 text-green-400 text-sm">
                  <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                  <span>Feature Active</span>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-20 lg:py-32 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            {/* About Content */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
            >
              <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">
                About Wolf AI
              </h2>
              <div className="space-y-6 text-gray-300 text-lg leading-relaxed">
                <p>
                  Wolf AI is a revolutionary sales assistant that combines the power of 
                  artificial intelligence with deep product knowledge to deliver exceptional 
                  customer experiences.
                </p>
                <p>
                  Our platform is designed for businesses who want to provide instant, 
                  accurate, and personalized support to their customers while maintaining 
                  the human touch that builds trust and drives sales.
                </p>
                <p>
                  Built with enterprise-grade security and powered by the latest AI models, 
                  Wolf AI adapts to your business needs and grows with your company.
                </p>
              </div>
              
              <div className="mt-8 grid grid-cols-2 gap-6">
                <div className="glass-effect p-4 rounded-xl text-center">
                  <div className="text-2xl font-bold text-orange-400 mb-1">Enterprise</div>
                  <div className="text-sm text-gray-400">Grade Security</div>
                </div>
                <div className="glass-effect p-4 rounded-xl text-center">
                  <div className="text-2xl font-bold text-blue-400 mb-1">24/7</div>
                  <div className="text-sm text-gray-400">Always Available</div>
                </div>
              </div>
            </motion.div>

            {/* Wolf AI Visual */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="relative"
            >
              <div className="glass-effect p-8 rounded-3xl">
                <div className="text-center">
                  <motion.div
                    animate={{ 
                      rotateY: [0, 360],
                    }}
                    transition={{ 
                      duration: 8,
                      repeat: Infinity,
                      ease: "linear"
                    }}
                    className="w-32 h-32 premium-gradient rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-premium-lg"
                  >
                    <span className="text-6xl">🐺</span>
                  </motion.div>
                  <h3 className="text-2xl font-bold text-white mb-3">Wolf AI Core</h3>
                  <p className="text-gray-300 mb-6">
                    Intelligent. Reliable. Ready to serve your customers.
                  </p>
                  
                  {/* AI Status Indicators */}
                  <div className="space-y-3">
                    {[
                      { label: "Natural Language Processing", status: "Active" },
                      { label: "Voice Recognition", status: "Online" },
                      { label: "Knowledge Base", status: "Ready" }
                    ].map((item, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-white/5 rounded-lg">
                        <span className="text-sm text-gray-300">{item.label}</span>
                        <span className="text-xs text-green-400 flex items-center space-x-1">
                          <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                          <span>{item.status}</span>
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section id="testimonials" className="py-20 lg:py-32">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">
              Loved by Businesses Worldwide
            </h2>
            <p className="text-xl text-gray-300">
              See what our customers are saying about Wolf AI
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="glass-effect p-6 rounded-2xl border border-white/10"
              >
                <div className="flex items-center space-x-1 mb-4">
                  {Array.from({ length: testimonial.rating }).map((_, i) => (
                    <Star key={i} className="h-4 w-4 text-yellow-400 fill-current" />
                  ))}
                </div>
                <p className="text-gray-300 mb-6 italic">
                  "{testimonial.content}"
                </p>
                <div>
                  <div className="font-semibold text-white">{testimonial.name}</div>
                  <div className="text-sm text-gray-400">
                    {testimonial.role} at {testimonial.company}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 lg:py-32">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="glass-effect p-12 rounded-3xl border border-white/10"
          >
            <div className="w-20 h-20 premium-gradient rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-premium-lg">
              <span className="text-4xl">🐺</span>
            </div>
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
              Ready to Transform Your Business?
            </h2>
            <p className="text-xl text-gray-300 mb-8">
              Join thousands of businesses using Wolf AI to provide exceptional customer experiences.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link 
                to="/signup"
                className="premium-button px-8 py-4 text-lg font-semibold"
              >
                Start Your Free Trial
              </Link>
              <Link 
                to="/login"
                className="glass-effect px-8 py-4 text-lg font-semibold text-white hover:bg-white/10 rounded-xl transition-all"
              >
                Sign In
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="flex items-center space-x-3 mb-4 md:mb-0">
              <div className="w-8 h-8 premium-gradient rounded-lg flex items-center justify-center">
                <span className="text-lg">🐺</span>
              </div>
              <div>
                <div className="text-white font-bold">Wolf AI</div>
                <div className="text-xs text-gray-400">Premium Sales Assistant</div>
              </div>
            </div>
            <div className="text-gray-400 text-sm">
              © 2024 Wolf AI. All rights reserved.
            </div>
          </div>
        </div>
      </footer>

      {/* Video Modal */}
      <AnimatePresence>
        {isVideoPlaying && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
            onClick={() => setIsVideoPlaying(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="glass-effect p-8 rounded-2xl max-w-2xl w-full"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="text-center">
                <div className="w-16 h-16 premium-gradient rounded-2xl flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">🐺</span>
                </div>
                <h3 className="text-2xl font-bold text-white mb-4">
                  Wolf AI Demo
                </h3>
                <p className="text-gray-300 mb-6">
                  Experience the power of AI-driven customer support in action.
                </p>
                <div className="bg-gradient-to-r from-slate-800 to-slate-700 p-8 rounded-xl mb-6">
                  <div className="text-gray-400">
                    Demo video coming soon! In the meantime, try Wolf AI by signing up for free.
                  </div>
                </div>
                <button
                  onClick={() => setIsVideoPlaying(false)}
                  className="premium-button px-6 py-3"
                >
                  Close
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default HomePage
