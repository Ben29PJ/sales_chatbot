import React from 'react'
import { motion } from 'framer-motion'
import { 
  RefreshCw, 
  Activity, 
  FileText, 
  Globe, 
  MessageSquare, 
  CheckCircle, 
  XCircle,
  Clock
} from 'lucide-react'

const StatusPanel = ({ status, onRefresh }) => {
  if (!status) {
    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-medium text-secondary-200">System Status</h3>
          <button
            onClick={onRefresh}
            className="p-2 text-secondary-400 hover:text-secondary-200 transition-colors"
            title="Refresh Status"
          >
            <RefreshCw className="h-4 w-4" />
          </button>
        </div>
        <div className="text-center py-8">
          <div className="w-8 h-8 border-2 border-primary-500/30 border-t-primary-500 rounded-full animate-spin mx-auto mb-3"></div>
          <p className="text-sm text-secondary-400">Loading status...</p>
        </div>
      </div>
    )
  }

  const statusItems = [
    {
      icon: Activity,
      label: 'Server Status',
      value: status.status,
      color: status.status === 'running' ? 'success' : 'danger'
    },
    {
      icon: Clock,
      label: 'Uptime',
      value: status.uptime,
      color: 'primary'
    },
    {
      icon: MessageSquare,
      label: 'Active Sessions',
      value: status.conversations,
      color: 'accent'
    },
    {
      icon: FileText,
      label: 'PDF Loaded',
      value: status.sources?.pdf ? 'Yes' : 'No',
      color: status.sources?.pdf ? 'success' : 'secondary'
    },
    {
      icon: Globe,
      label: 'Website Loaded',
      value: status.sources?.website ? 'Yes' : 'No',
      color: status.sources?.website ? 'success' : 'secondary'
    }
  ]

  const getColorClasses = (color) => {
    const colors = {
      success: 'text-success-400 bg-success-500/20',
      danger: 'text-danger-400 bg-danger-500/20',
      primary: 'text-primary-400 bg-primary-500/20',
      accent: 'text-accent-400 bg-accent-500/20',
      secondary: 'text-secondary-400 bg-secondary-500/20'
    }
    return colors[color] || colors.secondary
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-4"
    >
      {/* Header */}
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-medium text-secondary-200">System Status</h3>
        <button
          onClick={onRefresh}
          className="p-2 text-secondary-400 hover:text-secondary-200 transition-colors hover:rotate-180 transform duration-300"
          title="Refresh Status"
        >
          <RefreshCw className="h-4 w-4" />
        </button>
      </div>

      {/* Status Items */}
      <div className="space-y-3">
        {statusItems.map((item, index) => (
          <motion.div
            key={item.label}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className="flex items-center justify-between p-3 glass-effect rounded-lg"
          >
            <div className="flex items-center space-x-3">
              <div className={`p-2 rounded-lg ${getColorClasses(item.color)}`}>
                <item.icon className="h-4 w-4" />
              </div>
              <span className="text-sm text-secondary-300">{item.label}</span>
            </div>
            <span className={`text-sm font-medium ${
              item.color === 'success' ? 'text-success-400' :
              item.color === 'danger' ? 'text-danger-400' :
              item.color === 'primary' ? 'text-primary-400' :
              item.color === 'accent' ? 'text-accent-400' :
              'text-secondary-400'
            }`}>
              {item.value}
            </span>
          </motion.div>
        ))}
      </div>

      {/* Sources Summary */}
      <div className="mt-6">
        <h4 className="text-xs font-medium text-secondary-300 mb-2 uppercase tracking-wider">
          Knowledge Sources
        </h4>
        <div className="space-y-2">
          <div className="flex items-center justify-between text-xs">
            <span className="text-secondary-400">Total Sources Loaded:</span>
            <span className="text-primary-400 font-medium">
              {status.total_sources_loaded}/2
            </span>
          </div>
          
          {status.total_sources_loaded === 0 && (
            <div className="flex items-center space-x-2 p-2 bg-warning-500/10 rounded-lg border border-warning-500/20">
              <XCircle className="h-4 w-4 text-warning-400" />
              <span className="text-xs text-warning-300">
                No knowledge sources loaded. Upload a PDF or load a website to start.
              </span>
            </div>
          )}
          
          {status.total_sources_loaded > 0 && (
            <div className="flex items-center space-x-2 p-2 bg-success-500/10 rounded-lg border border-success-500/20">
              <CheckCircle className="h-4 w-4 text-success-400" />
              <span className="text-xs text-success-300">
                Ready to assist with product inquiries
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Last Updated */}
      <div className="text-xs text-secondary-500 text-center pt-2 border-t border-white/5">
        Last updated: {new Date().toLocaleTimeString()}
      </div>
    </motion.div>
  )
}

export default StatusPanel
