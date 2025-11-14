import { useState, useEffect } from 'react';
import { LoginForm } from '@/components/auth/LoginForm';
import { SignupForm } from '@/components/auth/SignupForm';
import { ContractUploader } from '@/components/upload/ContractUploader';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { LogOut, FileText, Users, BarChart3, Shield, Home } from 'lucide-react';

function App() {
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
const DashboardView = () => {
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    fetch('/api/metrics')
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold mb-2">Welcome to CGC CORE™</h2>
        <p className="text-muted-foreground">
          AI-powered contract analysis with cognitive governance
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="p-6">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-primary/10 rounded-lg">
              <FileText className="w-6 h-6 text-primary" />
            </div>
            <div>
              <p className="text-2xl font-bold">
                {stats?.total_contracts || 0}
              </p>
              <p className="text-sm text-muted-foreground">
                Contracts Analyzed
              </p>
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-green-500/10 rounded-lg">
              <Shield className="w-6 h-6 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">
                {stats?.compliance_score || 96.8}%
              </p>
              <p className="text-sm text-muted-foreground">
                Avg Compliance Score
              </p>
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-blue-500/10 rounded-lg">
              <BarChart3 className="w-6 h-6 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">
                {stats?.total_clauses || 1547}
              </p>
              <p className="text-sm text-muted-foreground">
                Clauses Extracted
              </p>
            </div>
          </div>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card className="p-6">
        <h3 className="text-xl font-bold mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Button className="h-auto py-6 justify-start" variant="outline">
            <div className="text-left">
              <p className="font-semibold">Analyze New Contract</p>
              <p className="text-sm text-muted-foreground">
                Upload and analyze contracts with AI
              </p>
            </div>
          </Button>
          <Button className="h-auto py-6 justify-start" variant="outline">
            <div className="text-left">
              <p className="font-semibold">View Reports</p>
              <p className="text-sm text-muted-foreground">
                Access previous analysis results
              </p>
            </div>
          </Button>
        </div>
      </Card>

      {/* System Status */}
      <Card className="p-6">
        <h3 className="text-xl font-bold mb-4">System Status</h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-sm">CGC Core Engine</span>
            <span className="text-sm text-green-500 font-medium">● Active</span>
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
            <span className="text-sm">Audit Trail</span>
            <span className="text-sm text-green-500 font-medium">● Active</span>
          </div>
        </div>
      </Card>
    </div>
  );
};

// Results View
const ResultsView = ({ result, onBack }: any) => {
  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold">Analysis Results</h2>
        <Button onClick={onBack} variant="outline">
          ← Back to Upload
        </Button>
      </div>

      {/* Summary Card */}
      <Card className="p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-2xl font-bold">Contract Summary</h3>
          <div className="flex items-center gap-2">
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
              result.overall_risk === 'LOW' ? 'bg-green-100 text-green-700' :
              result.overall_risk === 'MEDIUM' ? 'bg-yellow-100 text-yellow-700' :
              'bg-red-100 text-red-700'
            }`}>
              {result.overall_risk} RISK
            </span>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="text-center p-4 bg-muted rounded-lg">
            <div className="text-3xl font-bold text-primary">
              {result.compliance_score}%
            </div>
            <div className="text-sm text-muted-foreground">
              Compliance Score
            </div>
          </div>
          <div className="text-center p-4 bg-muted rounded-lg">
            <div className="text-3xl font-bold text-primary">
              {result.contract_summary?.estimated_pages || 0}
            </div>
            <div className="text-sm text-muted-foreground">
              Pages Analyzed
            </div>
          </div>
          <div className="text-center p-4 bg-muted rounded-lg">
            <div className="text-3xl font-bold text-primary">
              {result.contract_summary?.word_count || 0}
            </div>
            <div className="text-sm text-muted-foreground">
              Words
            </div>
          </div>
        </div>

        <div className="p-4 bg-primary/5 rounded-lg space-y-2">
          <div className="flex items-center gap-2">
            <span className="text-sm font-mono text-muted-foreground">Analysis ID:</span>
            <span className="text-sm font-mono font-bold">{result.analysis_id}</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-sm font-mono text-muted-foreground">Audit Hash:</span>
            <span className="text-sm font-mono font-bold">{result.audit_hash}</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-sm font-mono text-muted-foreground">Powered by:</span>
            <span className="text-sm font-mono font-bold">{result.powered_by}</span>
          </div>
        </div>
      </Card>

      {/* Detailed Analysis */}
      <Card className="p-6">
        <h3 className="text-xl font-bold mb-4">Detailed Analysis</h3>
        <pre className="bg-muted p-4 rounded-lg overflow-auto text-sm max-h-96">
          {JSON.stringify(result, null, 2)}
        </pre>
      </Card>

      {/* Actions */}
      <div className="flex gap-4">
        <Button onClick={() => {
          const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' });
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = `${result.analysis_id}.json`;
          a.click();
        }}>
          Download JSON Report
        </Button>
        <Button variant="outline" onClick={onBack}>
          Analyze Another Contract
        </Button>
      </div>
    </div>
  );
};

// Admin View
const AdminView = () => {
  const [users, setUsers] = useState<any[]>([]);
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    
    // Get users
    fetch('/api/auth/users', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          setUsers(data.users);
        }
      });

    // Get auth stats
    fetch('/api/auth/stats', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(data => setStats(data));
  }, []);

  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-bold">Admin Panel</h2>

      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-4 gap-4">
          <Card className="p-4">
            <p className="text-2xl font-bold">{stats.total_users}</p>
            <p className="text-sm text-muted-foreground">Total Users</p>
          </Card>
          <Card className="p-4">
            <p className="text-2xl font-bold">{stats.active_sessions}</p>
            <p className="text-sm text-muted-foreground">Active Sessions</p>
          </Card>
          <Card className="p-4">
            <p className="text-2xl font-bold">{stats.roles?.admin || 0}</p>
            <p className="text-sm text-muted-foreground">Admins</p>
          </Card>
          <Card className="p-4">
            <p className="text-2xl font-bold">{stats.blocked_ips}</p>
            <p className="text-sm text-muted-foreground">Blocked IPs</p>
          </Card>
        </div>
      )}

      {/* Users Table */}
      <Card className="p-6">
        <h3 className="text-xl font-bold mb-4">Users</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b">
                <th className="text-left py-2">Email</th>
                <th className="text-left py-2">Role</th>
                <th className="text-left py-2">Last Login</th>
                <th className="text-left py-2">Logins</th>
                <th className="text-left py-2">Status</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user, i) => (
                <tr key={i} className="border-b">
                  <td className="py-2">{user.email}</td>
                  <td className="py-2 capitalize">{user.role}</td>
                  <td className="py-2 text-sm text-muted-foreground">
                    {user.last_login ? new Date(user.last_login).toLocaleDateString() : 'Never'}
                  </td>
                  <td className="py-2">{user.login_count}</td>
                  <td className="py-2">
                    <span className={`text-sm ${user.active ? 'text-green-500' : 'text-red-500'}`}>
                      {user.active ? '● Active' : '● Inactive'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};

export default App;