/**
 * 404 Not Found Page
 * OlympusMont Systems LLC
 */

import { Link } from 'react-router-dom';
import { Home, ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';

const NotFound = () => {
  return (
    <div className="min-h-screen bg-gradient-surface flex items-center justify-center p-6">
      <div className="max-w-md text-center space-y-6">
        <div className="text-9xl font-bold text-gradient-cognitive">
          404
        </div>
        
        <h1 className="text-3xl font-bold text-foreground">
          Page Not Found
        </h1>
        
        <p className="text-muted-foreground">
          The page you're looking for doesn't exist or has been moved.
        </p>
        
        <div className="flex gap-4 justify-center">
          <Button asChild>
            <Link to="/">
              <Home className="w-4 h-4 mr-2" />
              Go Home
            </Link>
          </Button>
          
          <Button variant="outline" onClick={() => window.history.back()}>
            <ArrowLeft className="w-4 h-4 mr-2" />
            Go Back
          </Button>
        </div>
        
        <div className="pt-8 text-sm text-muted-foreground">
          <a href="https://olympusmont.com" className="text-primary hover:underline">
            olympusmont.com
          </a>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
