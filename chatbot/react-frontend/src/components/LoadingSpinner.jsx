import React from 'react'

const LoadingSpinner = ({ size = 'md', text = 'Loading...' }) => {
  const sizeClasses = {
    sm: 'h-6 w-6',
    md: 'h-8 w-8',
    lg: 'h-12 w-12',
    xl: 'h-16 w-16'
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <div className="relative">
        {/* Outer ring */}
        <div className={`${sizeClasses[size]} rounded-full border-4 border-primary-200/30`}></div>
        {/* Inner spinning ring */}
        <div className={`${sizeClasses[size]} rounded-full border-4 border-transparent border-t-primary-500 border-r-accent-500 animate-spin absolute top-0 left-0`}></div>
        {/* Center pulse */}
        <div className={`${sizeClasses[size]} rounded-full bg-gradient-to-r from-primary-500 to-accent-500 opacity-20 pulse-ring absolute top-0 left-0`}></div>
      </div>
      {text && (
        <p className="mt-4 text-secondary-300 font-medium animate-pulse">
          {text}
        </p>
      )}
    </div>
  )
}

export default LoadingSpinner
