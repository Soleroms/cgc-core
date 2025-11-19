import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Upload, FileText, Loader2, CheckCircle2, AlertCircle } from 'lucide-react';

interface ContractUploaderProps {
  onAnalysisComplete: (result: any) => void;
}

export const ContractUploader = ({ onAnalysisComplete }: ContractUploaderProps) => {
  const [file, setFile] = useState<File | null>(null);
  // Using a single state for loading/analyzing simplifies UI logic
  const [loading, setLoading] = useState(false); 
  const [error, setError] = useState('');
  const [dragActive, setDragActive] = useState(false);

  // --- Helper Functions ---

  const clearFile = () => {
    setFile(null);
    setError('');
  };

  const validateAndSetFile = (selectedFile: File) => {
    // Validate file type
    const validTypes = [
      'application/pdf', 
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document', // DOCX
      'application/msword', // DOC
      'text/plain' // TXT
    ];
        
    if (!validTypes.includes(selectedFile.type) && !selectedFile.name.endsWith('.docx') && !selectedFile.name.endsWith('.doc')) {
      setError('Please upload PDF, DOCX, DOC, or TXT files only.');
      return;
    }

    // Validate file size (max 10MB)
    if (selectedFile.size > 10 * 1024 * 1024) {
      setError('File size must be less than 10MB.');
      return;
    }

    setFile(selectedFile);
    setError('');
  };

  // --- Drag/Drop Handlers ---

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  // --- Analysis/Upload Logic (Updated to use FormData) ---

  const analyzeContract = async () => {
    if (!file) return;

    setLoading(true);
    setError('');

    const formData = new FormData();
    // The server is expecting the file under the field name 'contract'
    formData.append('contract', file); 

    try {
      console.log('Uploading and analyzing contract...', { filename: file.name, size: file.size });
      
      const response = await fetch('/api/analyze-contract', {
        method: 'POST',
        // IMPORTANT: Do NOT set 'Content-Type': 'application/json'. 
        // The browser automatically sets 'multipart/form-data' with the correct boundary.
        body: formData, 
      });

      if (!response.ok) {
        // Attempt to read the error message from the server response
        let errorBody = await response.text();
        try {
            const errorJson = JSON.parse(errorBody);
            errorBody = errorJson.message || errorBody;
        } catch {}

        throw new Error(`Analysis failed (${response.status}): ${errorBody}`);
      }

      const result = await response.json();
      console.log('Analysis complete:', result);
      onAnalysisComplete(result);
      clearFile(); // Clear file upon successful analysis
    } catch (err: any) {
      console.error('Analysis error:', err);
      setError(err.message || 'Failed to analyze contract. Please check server status.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="p-8">
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-bold mb-2">Contract Analysis</h2>
          <p className="text-muted-foreground">
            Upload a contract for AI-powered analysis with CGC CORE™
          </p>
        </div>
        
        {error && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription className='ml-2'>{error}</AlertDescription>
          </Alert>
        )}

        {/* Upload Area */}
        <div
          className={`relative border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
            dragActive
              ? 'border-primary bg-primary/5'
              : 'border-border hover:border-primary/50'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            type="file"
            id="file-upload"
            className="hidden"
            accept=".pdf,.docx,.doc,.txt"
            onChange={handleFileInput}
            disabled={loading}
          />
          {!file ? (
            <label htmlFor="file-upload" className="cursor-pointer">
              <Upload className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
              <p className="text-lg font-medium mb-2">
                Drop your contract here or click to browse
              </p>
              <p className="text-sm text-muted-foreground">
                Supports **PDF**, **DOCX**, **DOC**, **TXT** (max 10MB)
              </p>
            </label>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center justify-center gap-3">
                <FileText className="w-8 h-8 text-primary" />
                <div className="text-left">
                  <p className="font-medium">{file.name}</p>
                  <p className="text-sm text-muted-foreground">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
                {!loading && (
                  <CheckCircle2 className="w-6 h-6 text-green-500 ml-4" />
                )}
              </div>
              {!loading && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={clearFile}
                >
                  Remove
                </Button>
              )}
            </div>
          )}
        </div>

        {/* Analyze Button */}
        {file && (
          <Button
            onClick={analyzeContract}
            className="w-full"
            size="lg"
            disabled={loading}
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Analyzing with CGC CORE™...
              </>
            ) : (
              <>
                <FileText className="w-4 h-4 mr-2" />
                Analyze Contract
              </>
            )}
          </Button>
        )}
        
        {/* Analysis Status Modules */}
        {loading && (
          <div className="space-y-3">
            <div className="flex items-center gap-3 p-4 bg-muted rounded-lg">
              <Loader2 className="w-5 h-5 animate-spin text-primary" />
              <div className="flex-1">
                <p className="font-medium">Running CGC CORE™ Analysis</p>
                <p className="text-sm text-muted-foreground">
                  Processing through 6 cognitive modules...
                </p>
              </div>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs">
              <div className="p-2 bg-primary/10 rounded font-medium text-center">
                <Loader2 className="w-3 h-3 animate-spin inline mr-1" />
                PAN™ Analyzing
              </div>
              <div className="p-2 bg-primary/10 rounded font-medium text-center">
                <Loader2 className="w-3 h-3 animate-spin inline mr-1" />
                ECM™ Calibrating
              </div>
              <div className="p-2 bg-primary/10 rounded font-medium text-center">
                <Loader2 className="w-3 h-3 animate-spin inline mr-1" />
                PFM™ Predicting
              </div>
              <div className="p-2 bg-primary/10 rounded font-medium text-center">
                <Loader2 className="w-3 h-3 animate-spin inline mr-1" />
                SDA™ Advising
              </div>
              <div className="p-2 bg-primary/10 rounded font-medium text-center">
                <Loader2 className="w-3 h-3 animate-spin inline mr-1" />
                TCO™ Auditing
              </div>
              <div className="p-2 bg-primary/10 rounded font-medium text-center">
                <Loader2 className="w-3 h-3 animate-spin inline mr-1" />
                CGC_LOOP™
              </div>
            </div>
          </div>
        )}

        {/* Info */}
        <div className="bg-muted p-4 rounded-lg">
          <p className="text-sm text-muted-foreground">
            <strong>How it works:</strong> Your contract is securely uploaded and analyzed through our 6-module            Cognitive Governance Core™. Analysis typically takes 10-30 seconds.
          </p>
        </div>
      </div>
    </Card>
  );
};