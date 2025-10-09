'use client'
import { useState } from 'react'
import { Card } from "@/components/ui/card"
import { Upload } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import axios from 'axios'

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) return

    setUploading(true)
    const formData = new FormData()
    formData.append('pdf_file', file)

    try {
      const response = await axios.post('http://localhost:8000/process-menu-pdf/', formData)
      console.log('Upload successful:', response.data)
      alert('Menu uploaded successfully!')
    } catch (error) {
      console.error('Upload failed:', error)
      alert('Upload failed. Please try again.')
    } finally {
      setUploading(false)
      setFile(null)
    }
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-6">Upload Menu</h1>
      <Card className="p-6">
        <form onSubmit={handleSubmit}>
          <div className="flex flex-col items-center justify-center">
            <Upload className="w-12 h-12 mb-4 text-primary" />
            <h2 className="text-2xl font-semibold mb-2">Upload PDF Menu</h2>
            <p className="text-muted-foreground mb-4">Drag and drop your menu PDF or click to browse</p>
            
            <div className="w-full max-w-md space-y-4">
              <div className="border-2 border-dashed rounded-lg p-8 text-center">
                <Input 
                  type="file" 
                  accept=".pdf"
                  className="hidden" 
                  id="menu-upload"
                  onChange={(e) => setFile(e.target.files?.[0] || null)}
                />
                <label 
                  htmlFor="menu-upload" 
                  className="cursor-pointer"
                >
                  {file ? file.name : <span className="text-primary">Choose a file</span>}
                </label>
              </div>
              <Button 
                className="w-full" 
                type="submit" 
                disabled={!file || uploading}
              >
                {uploading ? 'Uploading...' : 'Upload Menu'}
              </Button>
            </div>
          </div>
        </form>
      </Card>
    </div>
  )
}