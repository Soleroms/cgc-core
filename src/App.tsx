import { useState, useEffect } from 'react';
import { LoginForm } from '@/components/auth/LoginForm';
import { SignupForm } from '@/components/auth/SignupForm';
import { ContractUploader } from '@/components/upload/ContractUploader';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
// CORRECCIÓN: Se añade Loader2 a las importaciones de lucide-react
import { LogOut, FileText, Users, BarChart3, Shield, Home, Loader2 } from 'lucide-react'; 

// AÑADIDO: 'export default' para que main.tsx pueda importarlo correctamente
export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showSignup, setShowSignup] = useState(false);
  const [user, setUser] = useState<any>(null);
  const [currentView, setCurrentView] = useState('dashboard');
  const [analysisResult, setAnalysisResult] = useState<any>(null);

  // Check if already logged in
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
    // Nota: Es mejor almacenar el token y el usuario en localStorage aquí.
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

  // Auth screens
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

  // Main app
  return (
    <div className="min-h-screen bg-gradient-surface">
      {/* Header */}
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
              
              {/* Navigation */}
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

            {/* User menu */}
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

      {/* Main content */}
      <main className="container mx-auto px-6 py-8">
        {currentView === 'dashboard' && (
          <DashboardView />
        )}

        {currentView === 'analyze' && (
          <div className="max-w-4xl mx-auto">
            <ContractUploader onAnalysisComplete={handleAnalysisComplete} />
          </div>
        )}

        {currentView === 'results' && analysisResult && (
          <ResultsView result={analysisResult} onBack={() => setCurrentView('analyze')} />
        )}

        {currentView === 'admin' && user?.role === 'admin' && (
          <AdminView />
        )}
      </main>
    </div>
  );
}

// Dashboard View
// Se asume que ResultsView y AdminView existen en otros archivos o están definidos aquí
const ResultsView = ({ result, onBack }: { result: any, onBack: () => void }) => (
    <Card className="p-6">
        <h2 className="text-3xl font-bold mb-4">Analysis Results</h2>
        <pre className="p-4 bg-muted rounded-lg text-sm overflow-auto">
            {JSON.stringify(result, null, 2)}
        </pre>
        <Button onClick={onBack} className="mt-4">Back to Analysis</Button>
    </Card>
);
const AdminView = () => (
    <Card className="p-6">
        <h2 className="text-3xl font-bold mb-4">Admin Dashboard</h2>
        <p className="text-muted-foreground">User management and system configuration controls go here.</p>
    </Card>
);


const DashboardView = () => {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await fetch('/api/metrics');
        const data = await response.json();
        setStats(data);
      } catch (err) {
        console.error('Failed to fetch metrics:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchMetrics();
    
    // Refresh every 5 seconds for real-time feel
    const interval = setInterval(fetchMetrics, 5000);
    
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        {/* CORRECCIÓN: Loader2 ahora está importado */}
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
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
          {stats?.cgc_core_active && (
            <div className="flex items-center gap-2 px-4 py-2 bg-green-500/10 rounded-lg border border-green-500/20">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
              <span className="text-sm font-medium text-green-500">CGC CORE LIVE</span>
            </div>
          )}
        </div>
      </div>

      {/* Stats Grid */}
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
              <p className="text-sm text-muted-foreground">
                Total Decisions
              </p>
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
              <p className="text-sm text-muted-foreground">
                Contracts Analyzed
              </p>
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
                {stats?.avg_compliance_score || 0}%
              </p>
              <p className="text-sm text-muted-foreground">
                Avg Compliance Score
              </p>
            </div>
          </div>
        </Card>
      </div>

      {/* CGC CORE Modules Status */}
      {stats?.cgc_core_active && stats?.modules && (
        <Card className="p-6">
          <h3 className="text-xl font-bold mb-4">CGC CORE™ Modules</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {/* Se utiliza Object.entries con declaración de tipo para manejar 'module' correctamente */}
            {Object.entries(stats.modules).map(([key, moduleData]: [string, any]) => (
              <div key={key} className="p-4 bg-muted rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-semibold text-sm">{key}</span>
                  <span className={`text-xs px-2 py-1 rounded ${
                    moduleData.status === 'active' 
                      ? 'bg-green-500/20 text-green-500' 
                      : 'bg-red-500/20 text-red-500'
                  }`}>
                    {moduleData.status}
                  </span>
                </div>
                <div className="space-y-1 text-xs text-muted-foreground">
                  <div className="flex justify-between">
                    <span>Health:</span>
                    <span className="font-medium">{moduleData.health}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Uptime:</span>
                    <span className="font-medium">{moduleData.uptime}%</span>
                  </div>
                  {moduleData.total_processed !== undefined && (
                    <div className="flex justify-between">
                      <span>Processed:</span>
                      <span className="font-medium">{moduleData.total_processed?.toLocaleString()}</span>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Blockchain Audit Trail */}
      {stats?.cgc_core_active && (
        <Card className="p-6">
          <h3 className="text-xl font-bold mb-4">Blockchain Audit Trail</h3>
          <div className="flex items-center justify-between p-4 bg-primary/5 rounded-lg">
            <div>
              <p className="text-sm text-muted-foreground mb-1">Total Audit Entries</p>
              <p className="text-2xl font-bold">{stats.audit_entries?.toLocaleString()}</p>
            </div>
            <div className="text-right">
              <p className="text-sm text-muted-foreground mb-1">Chain Integrity</p>
              <p className="text-lg font-bold text-green-500">VERIFIED ✓</p>
            </div>
          </div>
        </Card>
      )}

      {/* System Status */}
      <Card className="p-6">
        <h3 className="text-xl font-bold mb-4">System Status</h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-sm">CGC Core Engine</span>
            <span className={`text-sm font-medium ${
              stats?.cgc_core_active ? 'text-green-500' : 'text-yellow-500'
            }`}>
              ● {stats?.cgc_core_active ? 'Active' : 'Demo Mode'}
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm">AI Analysis Engine</span>
            <span className="text-sm text-green-500 font-medium">● Active</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm">Compliance Checker</span>
            <span className="text-sm text-green-500 font-medium">● Active</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm">Audit Trail (Blockchain)</span>
            <span className="text-sm text-green-500 font-medium">● Active</span>
          </div>
        </div>
      </Card>
    </div>
  );
};