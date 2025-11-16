import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Lock, Mail, AlertCircle, Loader2 } from 'lucide-react';

interface LoginFormProps {
  // onSucces ya no necesita el token ni el usuario, solo notifica que el proceso terminó
  onSuccess: () => void; 
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
      
      // Llamada a la API de Python para la autenticación
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
        // En un entorno de producción, la API de Python debería intercambiar credenciales por un
        // token de Firebase Custom Auth para usarlo aquí.
        // Dado que la integración completa está fuera de alcance, solo marcamos éxito.
        // El estado de Auth de Firebase es el punto de verdad en App.tsx.
        onSuccess(); 
      } else {
        setError(data.message || 'Error de inicio de sesión. Credenciales incorrectas.');
      }
    } catch (err) {
      console.error('Login failed:', err);
      setError('No se pudo conectar con el servidor. Inténtalo de nuevo.');
    } finally {
      setLoading(false);
    }
  };

  // Función para rellenar credenciales de demostración
  const fillDemoCredentials = () => {
    setEmail('admin@olympusmont.com');
    setPassword('ChangeMe123!');
    setError('');
  };

  return (
    <>
      {error && (
        <Alert variant="destructive" className="mb-4">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}
      
      <form onSubmit={handleLogin} className="space-y-6">
        <div className="space-y-4">
          {/* Campo de Correo Electrónico */}
          <div className="relative">
            <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
            <Input
              id="email"
              type="email"
              placeholder="Correo Electrónico"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="pl-10"
              required
              autoComplete="email"
              autoFocus
            />
          </div>

          {/* Campo de Contraseña */}
          <div className="relative">
            <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
            <Input
              id="password"
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
              Iniciando sesión...
            </>
          ) : (
            'Iniciar Sesión'
          )}
        </Button>

        <div className="flex items-center justify-between text-sm">
          <button
            type="button"
            onClick={fillDemoCredentials}
            className="text-muted-foreground hover:text-primary transition-colors"
          >
            Usar credenciales de demostración
          </button>
          
          <button
            type="button"
            onClick={onSwitchToSignup}
            className="text-primary hover:underline font-medium"
          >
            Crear cuenta →
          </button>
        </div>
      </form>

      <div className="mt-6 p-4 bg-muted rounded-lg">
        <p className="text-xs text-muted-foreground text-center">
          <strong>Cuenta Demo:</strong><br />
          Email: admin@olympusmont.com | Contraseña: ChangeMe123!
        </p>
      </div>
    </>
  );
};