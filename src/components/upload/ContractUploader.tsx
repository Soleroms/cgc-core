import { useState, useCallback } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Upload, FileText, X, Loader2, CheckCircle, AlertTriangle } from 'lucide-react';
import { Progress } from '@/components/ui/progress';

interface ContractUploaderProps {
  onAnalysisComplete: (result: any) => void;
}

export const ContractUploader = ({ onAnalysisComplete }: ContractUploaderProps) => {
  const [file, setFile] = useState<File | null>(null);
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState('');

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);

    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      validateAndSetFile(droppedFile);
    }
  }, []);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      validateAndSetFile(selectedFile);
    }
  };

  const validateAndSetFile = (file: File) => {
    setError('');

    // Validate file type
    const validTypes = [
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'text/plain'
    ];

    if (!validTypes.includes(file.type) && !file.name.match(/\.(pdf|docx|txt)$/i)) {
      setError('Invalid file type. Please upload PDF, DOCX, or TXT');
      return;
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      setError('File too large. Maximum size is 10MB');
      return;
    }

    setFile(file);
  };

  const handleUploadAndAnalyze = async () => {
    if (!file) return;

    setUploading(true);
    setProgress(0);
    setError('');

    try {
      // Read file as text
      const text = await file.text();
      
      // Simulate upload progress
      setProgress(30);

      // Get auth token
      const token = localStorage.getItem('auth_token');

      // Call analysis API
      const response = await fetch('/api/analyze-contract', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          contract_text: text,
          metadata: {
            filename: file.name,
            size: file.size,
            type: file.type,
            upload_date: new Date().toISOString()
          }
        })
      });

      setProgress(70);

      const result = await response.json();

      setProgress(100);

      if (response.ok) {
        setTimeout(() => {
          onAnalysisComplete(result);
          setUploading(false);
        }, 500);
      } else {
        throw new Error(result.error || 'Analysis failed');
      }

    } catch (err: any) {
      setError(err.message || 'Upload failed. Please try again.');
      setUploading(false);
      setProgress(0);
    }
  };

  const clearFile = () => {
    setFile(null);
    setError('');
    setProgress(0);
  };

  return (
    <Card className="p-6">
      <h2 className="text-2xl font-bold mb-4">Upload Contract for Analysis</h2>

      {/* Drop zone */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center transition-all
          ${dragging ? 'border-primary bg-primary/5 scale-105' : 'border-gray-300'}
          ${file ? 'bg-muted' : ''}
        `}
      >
        {!file ? (
          <>
            <input
              type="file"
              accept=".pdf,.docx,.txt"
              onChange={handleFileSelect}
              className="hidden"
              id="file-upload"
            />
            <label htmlFor="file-upload" className="cursor-pointer">
              <Upload className={`w-16 h-16 mx-auto mb-4 ${dragging ? 'text-primary' : 'text-gray-400'}`} />
              <p className="text-lg font-medium mb-2">
                {dragging ? 'Drop file here' : 'Drag & drop your contract'}
              </p>
              <p className="text-sm text-muted-foreground mb-4">
                or click to browse
              </p>
              <Button type="button" variant="outline">
                Select File
              </Button>
            </label>
            <p className="text-xs text-muted-foreground mt-4">
              Supported: PDF, DOCX, TXT (Max 10MB)
            </p>
          </>
        ) : (
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-background rounded-lg">
              <div className="flex items-center gap-3">
                <FileText className="w-8 h-8 text-primary" />
                <div className="text-left">
                  <p className="font-medium">{file.name}</p>
                  <p className="text-sm text-muted-foreground">
                    {(file.size / 1024).toFixed(1)} KB
                  </p>
                </div>
              </div>
              {!uploading && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={clearFile}
                >
                  <X className="w-4 h-4" />
                </Button>
              )}
            </div>

            {uploading && (
              <div className="space-y-2">
                <Progress value={progress} className="h-2" />
                <p className="text-sm text-center text-muted-foreground">
                  {progress < 30 && 'Uploading...'}
                  {progress >= 30 && progress < 70 && 'Analyzing with AI...'}
                  {progress >= 70 && progress < 100 && 'Finalizing...'}
                  {progress === 100 && 'Complete!'}
                </p>
              </div>
            )}

            {error && (
              <div className="flex items-center gap-2 p-3 bg-destructive/10 text-destructive rounded-lg">
                <AlertTriangle className="w-4 h-4" />
                <p className="text-sm">{error}</p>
              </div>
            )}

            {!uploading && !error && (
              <Button
                onClick={handleUploadAndAnalyze}
                className="w-full"
                size="lg"
              >
                <FileText className="w-4 h-4 mr-2" />
                Analyze Contract with AI
              </Button>
            )}
          </div>
        )}
      </div>
    </Card>
  );
};