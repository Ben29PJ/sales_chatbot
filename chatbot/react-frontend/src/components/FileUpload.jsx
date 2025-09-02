import React, { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { motion } from 'framer-motion'
import { Upload, FileText, X } from 'lucide-react'

const FileUpload = ({ onFileUpload }) => {
  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0]
    if (file) {
      onFileUpload(file)
    }
  }, [onFileUpload])

  const { getRootProps, getInputProps, isDragActive, acceptedFiles } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    multiple: false,
    maxSize: 10 * 1024 * 1024 // 10MB
  })

  return (
    <div className="space-y-4">
      <div>
        <h3 className="text-sm font-medium text-secondary-200 mb-3">
          Upload Product Catalog
        </h3>
        
        <motion.div
          {...getRootProps()}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className={`
            border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-all duration-200
            ${isDragActive 
              ? 'border-primary-400 bg-primary-500/10' 
              : 'border-secondary-600 hover:border-primary-500 hover:bg-primary-500/5'
            }
          `}
        >
          <input {...getInputProps()} />
          
          <div className="flex flex-col items-center space-y-3">
            <div className={`
              p-3 rounded-full transition-colors
              ${isDragActive 
                ? 'bg-primary-500/20 text-primary-400' 
                : 'bg-secondary-700/50 text-secondary-400'
              }
            `}>
              <Upload className="h-6 w-6" />
            </div>
            
            <div>
              <p className="text-sm font-medium text-secondary-200">
                {isDragActive ? 'Drop PDF here' : 'Upload PDF catalog'}
              </p>
              <p className="text-xs text-secondary-500 mt-1">
                Drag & drop or click to select (Max 10MB)
              </p>
            </div>
          </div>
        </motion.div>

        {/* File Preview */}
        {acceptedFiles.length > 0 && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            className="mt-3"
          >
            {acceptedFiles.map((file, index) => (
              <div
                key={index}
                className="flex items-center space-x-3 p-3 glass-effect rounded-lg"
              >
                <FileText className="h-5 w-5 text-primary-400" />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-secondary-200 truncate">
                    {file.name}
                  </p>
                  <p className="text-xs text-secondary-500">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
                <span className="text-xs text-success-400">
                  Ready to upload
                </span>
              </div>
            ))}
          </motion.div>
        )}
      </div>

      <div className="text-xs text-secondary-500 space-y-1">
        <p>• Supported format: PDF files only</p>
        <p>• Maximum file size: 10MB</p>
        <p>• Content will be used for sales assistance</p>
      </div>
    </div>
  )
}

export default FileUpload
