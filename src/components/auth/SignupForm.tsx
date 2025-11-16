import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Lock, Mail, AlertCircle, Loader2, CheckCircle2, User } from 'lucide-react';

interface SignupFormProps {
  onSuccess: (token: string, user: any) => void;
  onSwitchToLogin: () => void;
}

export const SignupForm = ({ onSuccess, onSwitchToLogin }: SignupFormProps) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Real-time password validation
  const passwordRequirements = {
    minLength: password.length >= 8,
    hasUppercase: /[A-Z]/.test(password),
    hasNumber: /[0-9]/.test(password),
    matches: password === confirmPassword && password.length > 0
  };

  const isPasswordValid = Object.values(passwordRequirements).every(req => req);

  // Real-time email validation
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  const isEmailValid = emailRegex.test(email);

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Frontend validation
    if (!isEmailValid) {
      setError('Please enter a valid email address');
      return;
    }

    if (!isPasswordValid) {
      setError('Please meet all password requirements');
      return;
    }

    setLoading(true);

    try {
      console.log('Creating account...', { email, name });
      
      // Create account
      const response = await fetch('/api/auth/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          email: email.toLowerCase().trim(), 
          password,
          name: name.trim()
        })
      });

      const data = await response.json();
      console.log('Signup response:', data);

      if (data.success) {
        // Auto-login after successful signup
        console.log('Auto-logging in...');
        const loginResponse = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 
            email: email.toLowerCase().trim(), 
            password 
          })
        });

        const loginData = await loginResponse.json();
        console.log('Auto-login response:', loginData);

        if (loginData.success) {
          localStorage.setItem('auth_token', loginData.token);
          localStorage.setItem('user', JSON.stringify(loginData.user));
          onSuccess(loginData.token, loginData.user);
        } else {
          setError('Account created! Please login manually.');
          setTimeout(() => onSwitchToLogin(), 2000);
        }
      } else {
        setError(data.error || 'Signup failed. Please try again.');
      }
    } catch (err) {
      console.error('Signup error:', err);
      setError('Connection error. Please check your internet and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md p-8">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gradient-cognitive mb-2">
          Create Account
        </h1>
        <p className="text-muted-foreground">
          Join CGC CORE™
        </p>
      </div>

      <form onSubmit={handleSignup} className="space-y-4">
        {error && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <div className="space-y-2">
          <label className="text-sm font-medium">Name (Optional)</label>
          <div className="relative">
            <User className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
            <Input
              type="text"
              placeholder="Your name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="pl-10"
            />
          </div>
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium">Email *</label>
          <div className="relative">
            <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
            <Input
              type="email"
              placeholder="you@company.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="pl-10"
              required
            />
            {email && (
              <div className="absolute right-3 top-3">
                {isEmailValid ? (
                  <CheckCircle2 className="h-4 w-4 text-green-500" />
                ) : (
                  <AlertCircle className="h-4 w-4 text-red-500" />
                )}
              </div>
            )}
          </div>
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium">Password *</label>
          <div className="relative">
            <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
            <Input
              type="password"
              placeholder="Create strong password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="pl-10"
              required
            />
          </div>
          
          {password && (
            <div className="space-y-1 mt-2 text-xs">
              <div className={`flex items-center gap-2 ${passwordRequirements.minLength ? 'text-green-600' : 'text-muted-foreground'}`}>
                {passwordRequirements.minLength ? (
                  <CheckCircle2 className="h-3 w-3" />
                ) : (
                  <AlertCircle className="h-3 w-3" />
                )}
                <span>At least 8 characters</span>
              </div>
              <div className={`flex items-center gap-2 ${passwordRequirements.hasUppercase ? 'text-green-600' : 'text-muted-foreground'}`}>
                {passwordRequirements.hasUppercase ? (
                  <CheckCircle2 className="h-3 w-3" />
                ) : (
                  <AlertCircle className="h-3 w-3" />
                )}
                <span>One uppercase letter</span>
              </div>
              <div className={`flex items-center gap-2 ${passwordRequirements.hasNumber ? 'text-green-600' : 'text-muted-foreground'}`}>
                {passwordRequirements.hasNumber ? (
                  <CheckCircle2 className="h-3 w-3" />
                ) : (
                  <AlertCircle className="h-3 w-3" />
                )}
                <span>One number</span>
              </div>
            </div>
          )}
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium">Confirm Password *</label>
          <div className="relative">
            <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
            <Input
              type="password"
              placeholder="Confirm your password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="pl-10"
              required
            />
            {confirmPassword && (
              <div className="absolute right-3 top-3">
                {passwordRequirements.matches ? (
                  <CheckCircle2 className="h-4 w-4 text-green-500" />
                ) : (
                  <AlertCircle className="h-4 w-4 text-red-500" />
                )}
              </div>
            )}
          </div>
          {confirmPassword && !passwordRequirements.matches && (
            <p className="text-xs text-red-500">Passwords do not match</p>
          )}
        </div>

        <Button 
          type="submit" 
          className="w-full"
          disabled={loading || !isEmailValid || !isPasswordValid}
        >
          {loading ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              Creating account...
            </>
          ) : (
            'Create Account'
          )}
        </Button>

        <div className="text-center text-sm">
          <button
            type="button"
            onClick={onSwitchToLogin}
            className="text-primary hover:underline"
          >
            Already have an account? Sign in
          </button>
        </div>
      </form>
    </Card>
  );
};