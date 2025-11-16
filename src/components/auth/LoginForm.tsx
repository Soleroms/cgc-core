import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Lock, Mail, AlertCircle, Loader2 } from 'lucide-react';

interface LoginFormProps {
  onSuccess: (token: string, user: any) => void;
  onSwitchToSignup: () => void;
}

export const LoginForm = ({ onSuccess, onSwitchToSignup }: LoginFormProps) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      console.log('Logging in...', { email });
      
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          email: email.toLowerCase().trim(), 
          password 
        })
      });

      const data = await response.json();
      console.log('Login response:', data);

      if (data.success) {
        localStorage.setItem('auth_token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        onSuccess(data.token, data.user);
      } else {
        setError(data.error || 'Login failed. Please check your credentials.');
      }
    } catch (err) {
      console.error('Login error:', err);
      setError('Connection error. Please check your internet and try again.');
    } finally {
      setLoading(false);
    }
  };

  const fillDemoCredentials = () => {
    setEmail('admin@olympusmont.com');
    setPassword('ChangeMe123!');
  };

  return (
    <Card className="w-full max-w-md p-8">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gradient-cognitive mb-2">
          CGC CORE™
        </h1>
        <p className="text-muted-foreground">
          Sign in to your account
        </p>
      </div>

      <form onSubmit={handleLogin} className="space-y-4">
        {error && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <div className="space-y-2">
          <label className="text-sm font-medium">Email</label>
          <div className="relative">
            <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
            <Input
              type="email"
              placeholder="you@company.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="pl-10"
              required
              autoComplete="email"
            />
          </div>
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium">Password</label>
          <div className="relative">
            <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
            <Input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="pl-10"
              required
              autoComplete="current-password"
            />
          </div>
        </div>

        <Button 
          type="submit" 
          className="w-full"
          disabled={loading || !email || !password}
        >
          {loading ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              Signing in...
            </>
          ) : (
            'Sign In'
          )}
        </Button>

        <div className="flex items-center justify-between text-sm">
          <button
            type="button"
            onClick={fillDemoCredentials}
            className="text-muted-foreground hover:text-primary transition-colors"
          >
            Use demo credentials
          </button>
          
          <button
            type="button"
            onClick={onSwitchToSignup}
            className="text-primary hover:underline font-medium"
          >
            Create account →
          </button>
        </div>
      </form>

      <div className="mt-6 p-4 bg-muted rounded-lg">
        <p className="text-xs text-muted-foreground text-center">
          <strong>Demo Account:</strong><br />
          admin@olympusmont.com / ChangeMe123!
        </p>
      </div>
    </Card>
  );
};