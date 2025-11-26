'use client'

import { useState } from 'react'

export default function AudioConverter() {
  const [files, setFiles] = useState<File[]>([])
  const [format, setFormat] = useState('mp3')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [messageType, setMessageType] = useState<'success' | 'error' | ''>('')
  const [progress, setProgress] = useState(0)

  const formats = ['mp3', 'wav', 'ogg', 'flac', 'aac', 'm4a', 'wma', 'aiff']

  const handleFileSelect = (selectedFiles: FileList | null) => {
    if (!selectedFiles) return
    setFiles(Array.from(selectedFiles))
    setMessage('')
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    const droppedFiles = e.dataTransfer.files
    if (droppedFiles) handleFileSelect(droppedFiles)
  }

  const removeFile = (index: number) => {
    setFiles(files.filter((_, i) => i !== index))
  }

  const handleConvert = async () => {
    if (files.length === 0) return

    setLoading(true)
    setMessage('')
    setProgress(0)
    
    // Simulate progress
    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 90) return prev
        return prev + 10
      })
    }, 200)

    const formData = new FormData()
    
    if (files.length === 1) {
      formData.append('audio_file', files[0])
      formData.append('output_format', format)

      try {
        const response = await fetch('/api/convert', {
          method: 'POST',
          body: formData
        })

        if (response.ok) {
          const blob = await response.blob()
          const url = URL.createObjectURL(blob)
          const a = document.createElement('a')
          a.href = url
          a.download = `${files[0].name.split('.')[0]}.${format}`
          a.click()
          URL.revokeObjectURL(url)
          
          clearInterval(progressInterval)
          setProgress(100)
          setMessage('Conversion successful!')
          setMessageType('success')
        } else {
          clearInterval(progressInterval)
          setProgress(0)
          const error = await response.json()
          setMessage(error.error || 'Conversion failed')
          setMessageType('error')
        }
      } catch (error) {
        clearInterval(progressInterval)
        setProgress(0)
        setMessage('Network error')
        setMessageType('error')
      }
    } else {
      files.forEach(file => formData.append('audio_files', file))
      formData.append('output_format', format)

      try {
        const response = await fetch('/api/convert-batch', {
          method: 'POST',
          body: formData
        })

        if (response.ok) {
          const blob = await response.blob()
          const url = URL.createObjectURL(blob)
          const a = document.createElement('a')
          a.href = url
          a.download = 'converted_files.zip'
          a.click()
          URL.revokeObjectURL(url)
          
          clearInterval(progressInterval)
          setProgress(100)
          setMessage(`Successfully converted ${files.length} files!`)
          setMessageType('success')
        } else {
          clearInterval(progressInterval)
          setProgress(0)
          const error = await response.json()
          setMessage(error.error || 'Conversion failed')
          setMessageType('error')
        }
      } catch (error) {
        clearInterval(progressInterval)
        setProgress(0)
        setMessage('Network error')
        setMessageType('error')
      }
    }

    setLoading(false)
    setTimeout(() => setProgress(0), 1000)
  }

  return (
    <>
      <div className="container">
        <div className="header">
          <h1>🎵 awaaj badlo</h1>
          <p>Convert your audio files to any format</p>
        </div>

        <div className="converter-box">
        <div
          className="upload-area"
          onDrop={handleDrop}
          onDragOver={(e) => e.preventDefault()}
          onClick={() => document.getElementById('fileInput')?.click()}
        >
          <input
            id="fileInput"
            type="file"
            accept="audio/*"
            multiple
            onChange={(e) => handleFileSelect(e.target.files)}
            style={{ display: 'none' }}
          />
          {files.length === 0 ? (
            <div>
              <p>Click to upload or drag and drop</p>
              <span>Supported: MP3, WAV, OGG, FLAC, AAC, M4A, WMA, AIFF</span>
              <span style={{ display: 'block', marginTop: '8px', fontSize: '0.9em' }}>
                Select multiple files for batch conversion
              </span>
            </div>
          ) : (
            <div className="files-count">
              <div className="count-icon">📁</div>
              <p>{files.length} file{files.length !== 1 ? 's' : ''} selected</p>
              <button className="clear-btn" onClick={(e) => { e.stopPropagation(); setFiles([]) }}>
                Clear All
              </button>
            </div>
          )}
        </div>

        <div className="format-selector">
          <label>Convert to:</label>
          <select value={format} onChange={(e) => setFormat(e.target.value)}>
            {formats.map(f => (
              <option key={f} value={f}>{f.toUpperCase()}</option>
            ))}
          </select>
        </div>

        <button
          className="convert-btn"
          onClick={handleConvert}
          disabled={files.length === 0 || loading}
        >
          {loading ? 'Converting...' : `Convert ${files.length} File${files.length !== 1 ? 's' : ''}`}
        </button>

        {loading && (
          <div className="progress-wrapper">
            <div className="progress-container">
              <div className="progress-bar" style={{ width: `${progress}%` }}></div>
            </div>
            <div className="progress-text">{progress}%</div>
          </div>
        )}

        {message && (
          <div className={`message ${messageType}`}>
            {message}
          </div>
        )}
        </div>
      </div>

      <div className="footer">
        Made by Sameer
      </div>
    </>
  )
}