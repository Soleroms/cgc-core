import { useState, useEffect } from 'react';
import { LoginForm } from '@/components/auth/LoginForm';
import { SignupForm } from '@/components/auth/SignupForm';
import { ContractUploader } from '@/components/upload/ContractUploader';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { LogOut, FileText, Users, BarChart3, Shield, Home, Loader2, Activity } from 'lucide-react';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showSignup, setShowSignup] = useState(false);
  const [user, setUser] = useState<any>(null);
  const [currentView, setCurrentView] = useState('dashboard');
  const [analysisResult, setAnalysisResult] = useState<any>(null);

  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    const storedUser = localStorage.getItem('user');
    
    if (token && storedUser) {
      setIsAuthenticated(true);
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const handleLoginSuccess = (token: string, userData: any) => {
    setIsAuthenticated(true);
    localStorage.setItem('auth_token', token);
    localStorage.setItem('user', JSON.stringify(userData));
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
    setIsAuthenticated(false);
    setUser(null);
    setCurrentView('dashboard');
    setAnalysisResult(null);
  };

  const handleAnalysisComplete = (result: any) => {
    setAnalysisResult(result);
    setCurrentView('results');
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center p-6">
        <div className="absolute inset-0 bg-grid-pattern opacity-10"></div>
        
        {showSignup ? (
          <SignupForm 
            onSuccess={handleLoginSuccess}
            onSwitchToLogin={() => setShowSignup(false)}
          />
        ) : (
          <LoginForm 
            onSuccess={handleLoginSuccess}
            onSwitchToSignup={() => setShowSignup(true)}
          />
        )}
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-surface">
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-8">
              <div>
                <h1 className="text-2xl font-bold text-gradient-cognitive">
                  CGC CORE™
                </h1>
                <p className="text-xs text-muted-foreground">
                  OlympusMont Systems LLC
                </p>
              </div>
              
              <nav className="flex gap-2">
                <Button
                  variant={currentView === 'dashboard' ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => setCurrentView('dashboard')}
                >
                  <Home className="w-4 h-4 mr-2" />
                  Dashboard
                </Button>
                <Button
                  variant={currentView === 'analyze' ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => setCurrentView('analyze')}
                >
                  <FileText className="w-4 h-4 mr-2" />
                  Analyze
                </Button>
                {user?.role === 'admin' && (
                  <Button
                    variant={currentView === 'admin' ? 'default' : 'ghost'}
                    size="sm"
                    onClick={() => setCurrentView('admin')}
                  >
                    <Users className="w-4 h-4 mr-2" />
                    Admin
                  </Button>
                )}
              </nav>
            </div>

            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm font-medium">{user?.email}</p>
                <p className="text-xs text-muted-foreground capitalize">
                  {user?.role}
                </p>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={handleLogout}
              >
                <LogOut className="w-4 h-4 mr-2" />
                Logout
              </Button>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-6 py-8">
        {currentView === 'dashboard' && <DashboardView />}
        {currentView === 'analyze' && (
          <div className="max-w-4xl mx-auto">
            <ContractUploader onAnalysisComplete={handleAnalysisComplete} />
          </div>
        )}
        {currentView === 'results' && analysisResult && (
          <ResultsView result={analysisResult} onBack={() => setCurrentView('analyze')} />
        )}
        {currentView === 'admin' && user?.role === 'admin' && <AdminView />}
      </main>
    </div>
  );
}

const ResultsView = ({ result, onBack }: { result: any, onBack: () => void }) => (
  <Card className="p-6">
    <h2 className="text-3xl font-bold mb-4">Analysis Results</h2>
    <pre className="p-4 bg-muted rounded-lg text-sm overflow-auto max-h-96">
      {JSON.stringify(result, null, 2)}
    </pre>
    <Button onClick={onBack} className="mt-4">Back to Analysis</Button>
  </Card>
);

const AdminView = () => (
  <Card className="p-6">
    <h2 className="text-3xl font-bold mb-4">Admin Dashboard</h2>
    <p className="text-muted-foreground">User management and system configuration controls.</p>
  </Card>
);

const DashboardView = () => {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Flag to prevent state updates after component is unmounted
    let isMounted = true; 
    
    const token = localStorage.getItem('auth_token');

    const fetchMetrics = async () => {
      setLoading(true);
      try {
        console.log('🔍 Fetching metrics from API...');
       
        // FIX: The original code had a syntax error and duplicate fetch calls here.
        // We now correctly call fetch with the URL string and necessary options.
        const response = await fetch('/api/metrics', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`, // Pass token for authenticated requests
            'Content-Type': 'application/json',
          },
          cache: 'no-cache'
        });
        
        console.log('📡 Response status:', response.status);
        
        if (!response.ok) {
          // If the server returns a 4xx or 5xx, throw an error
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('✅ Metrics received:', data);
        
        // Only update state if the component is still mounted
        if (isMounted) {
          setStats(data);
        }

      } catch (err) {
        console.error('❌ Failed to fetch metrics:', err);
        // Set an empty state on failure (without demo/placeholder values)
        if (isMounted) {
            setStats(null);
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    // Run immediately and then set up the interval
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 3000);
    
    // Cleanup function runs when the component unmounts
    return () => {
        isMounted = false; 
        clearInterval(interval);
    };
  }, []); // Empty dependency array means this runs only on mount/unmount

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }
  
  // Display an error/no-data message if stats is null after loading
  if (!stats) {
    return (
        <Card className="p-6 text-center h-64 flex flex-col justify-center items-center">
            <Activity className="w-8 h-8 text-red-500 mb-4" />
            <h3 className="text-xl font-bold mb-2 text-red-500">System Metrics Unavailable</h3>
            <p className="text-muted-foreground">Could not connect to the CGC CORE™ API to fetch real-time data.</p>
        </Card>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold mb-2">Welcome to CGC CORE™</h2>
            <p className="text-muted-foreground">
              AI-powered contract analysis with cognitive governance
            </p>
          </div>
          {/* Status check based on data from the API */}
          {stats?.cgc_core_active ? (
            <div className="flex items-center gap-2 px-4 py-2 bg-green-500/10 rounded-lg border border-green-500/20">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
              <span className="text-sm font-medium text-green-500">CGC CORE LIVE</span>
            </div>
          ) : (
            <div className="flex items-center gap-2 px-4 py-2 bg-yellow-500/10 rounded-lg border border-yellow-500/20">
              <div className="w-2 h-2 bg-yellow-500 rounded-full" />
              <span className="text-sm font-medium text-yellow-500">STANDBY MODE</span>
            </div>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="p-6">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-primary/10 rounded-lg">
              <BarChart3 className="w-6 h-6 text-primary" />
            </div>
            <div>
              <p className="text-2xl font-bold">
                {stats?.total_decisions?.toLocaleString() || '0'}
              </p>
              <p className="text-sm text-muted-foreground">Total Decisions</p>
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-green-500/10 rounded-lg">
              <FileText className="w-6 h-6 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">
                {stats?.total_contracts?.toLocaleString() || '0'}
              </p>
              <p className="text-sm text-muted-foreground">Contracts Analyzed</p>
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-blue-500/10 rounded-lg">
              <Shield className="w-6 h-6 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">
                {stats?.avg_compliance_score?.toFixed(1) || '0.0'}%
              </p>
              <p className="text-sm text-muted-foreground">Avg Compliance Score</p>
            </div>
          </div>
        </Card>
      </div>

      {stats?.cgc_core_active && stats?.modules && (
        <Card className="p-6">
          <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
            <Activity className="w-5 h-5" />
            CGC CORE™ Modules
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {Object.entries(stats.modules).map(([key, module]: [string, any]) => (
              <div key={key} className="p-4 bg-muted rounded-lg border border-border hover:border-primary/50 transition-colors">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-semibold text-sm">{key}</span>
                  <span className={`text-xs px-2 py-1 rounded ${
                    module.status === 'active' 
                      ? 'bg-green-500/20 text-green-500' 
                      : 'bg-red-500/20 text-red-500'
                  }`}>
                    {module.status}
                  </span>
                </div>
                <div className="space-y-1 text-xs text-muted-foreground">
                  <div className="flex justify-between">
                    <span>Health:</span>
                    <span className="font-medium text-foreground">{module.health}%</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}

      <Card className="p-6">
        <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
          <Activity className="w-5 h-5" />
          System Status
        </h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-sm">CGC Core Engine</span>
            <span className={`text-sm font-medium ${
              stats?.cgc_core_active ? 'text-green-500' : 'text-yellow-500'
            }`}>
              ● {stats?.cgc_core_active ? 'Active' : 'Standby'}
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm">System Health</span>
            <span className="text-sm text-green-500 font-medium">
              {stats?.system_health || 0}%
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm">Audit Entries</span>
            <span className="text-sm font-medium">
              {stats?.audit_entries?.toLocaleString() || '0'}
            </span>
          </div>
        </div>
      </Card>
    </div>
  );
};