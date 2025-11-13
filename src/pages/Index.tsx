/**
 * CGC CORE Dashboard - Main Page
 * OlympusMont Systems LLC
 */

import { useEffect, useState } from 'react';
import { SystemMetrics } from '@/components/cgc/SystemMetrics';
import { ModuleCard } from '@/components/cgc/ModuleCard';
import { AuditTrail } from '@/components/cgc/AuditTrail';
import { SecurityStatus } from '@/components/cgc/SecurityStatus';
import { LegalTechPanel } from '@/components/cgc/LegalTechPanel';import { cgcModules } from '@/data/cgcModules';
import { apiService } from '@/services/api';
import { Shield, Activity } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

const Index = () => {
  const [apiHealth, setApiHealth] = useState<any>(null);
  const [apiConnected, setApiConnected] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    // Check API health on mount
    const checkApiHealth = async () => {
      try {
        const health = await apiService.getHealth();
        setApiHealth(health);
        setApiConnected(true);
        
        toast({
          title: '✅ API Connected',
          description: `${health.service} v${health.version}`,
        });
      } catch (error) {
        console.error('API connection failed:', error);
        setApiConnected(false);
        
        toast({
          title: '⚠️ API Offline',
          description: 'Running in demo mode with mock data',
          variant: 'destructive',
        });
      }
    };

    checkApiHealth();

    // Poll health every 30 seconds
    const interval = setInterval(checkApiHealth, 30000);
    return () => clearInterval(interval);
  }, [toast]);

  return (
    <div className="min-h-screen bg-gradient-surface">
      {/* Header */}
      <header className="border-b border-border/50 bg-card/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-lg bg-gradient-cognitive flex items-center justify-center shadow-glow">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gradient-cognitive">
                  CGC CORE™
                </h1>
                <p className="text-sm text-muted-foreground">
                  Cognitive Governance Cycle v2.1.4
                </p>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              {/* API Status Indicator */}
              <div className="flex items-center gap-2 px-4 py-2 rounded-lg bg-card border border-border/50">
                <div className={`w-2 h-2 rounded-full ${apiConnected ? 'bg-success animate-pulse-glow' : 'bg-error'}`} />
                <span className="text-sm font-medium">
                  {apiConnected ? 'API Connected' : 'Demo Mode'}
                </span>
              </div>
              
              <div className="text-right">
                <div className="text-sm font-semibold text-foreground">
                  OlympusMont Systems™
                </div>
                <div className="text-xs text-muted-foreground">
                  olympusmont.com
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8 space-y-8">
        {/* System Metrics */}
        <section>
          <SystemMetrics />
        </section>

        {/* Core Modules Grid */}
        <section>
          <div className="flex items-center gap-3 mb-6">
            <Activity className="w-6 h-6 text-primary" />
            <h2 className="text-2xl font-bold text-foreground">
              Core Modules
            </h2>
            <div className="flex-1 h-px bg-gradient-to-r from-primary/50 to-transparent" />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {cgcModules.map((module) => (
              <ModuleCard key={module.id} module={module} />
            ))}
          </div>
        </section>

        {/* DiscipleAI Legal & Audit Trail */}
        <section className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <LegalTechPanel />
          <AuditTrail />
        </section>

        {/* Security Status */}
        <section>
          <SecurityStatus />
        </section>

        {/* API Info (if connected) */}
        {apiHealth && (
          <section className="p-6 rounded-lg bg-primary/5 border border-primary/20">
            <h3 className="text-lg font-semibold text-foreground mb-4">
              🔗 Live API Connection
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <div className="text-muted-foreground">Service</div>
                <div className="font-semibold">{apiHealth.service}</div>
              </div>
              <div>
                <div className="text-muted-foreground">Version</div>
                <div className="font-semibold">{apiHealth.version}</div>
              </div>
              <div>
                <div className="text-muted-foreground">CGC Core</div>
                <div className="font-semibold">
                  {apiHealth.cgc_loaded ? '✅ Loaded' : '❌ Offline'}
                </div>
              </div>
              <div>
                <div className="text-muted-foreground">Contract Analyzer</div>
                <div className="font-semibold">
                  {apiHealth.modules?.contract_analyzer ? '✅ Active' : '⚠️ Inactive'}
                </div>
              </div>
            </div>
          </section>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-border/50 bg-card/30 backdrop-blur-sm mt-16">
        <div className="container mx-auto px-6 py-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="text-sm text-muted-foreground text-center md:text-left">
              © 2025 OlympusMont Systems LLC. All rights reserved.
              <br />
              <span className="text-xs">
                CGC CORE™, PAN™, ECM™, PFM™, SDA™, TCO™ are trademarks of OlympusMont Systems.
              </span>
            </div>
            
            <div className="flex gap-4 text-sm">
              <a href="https://olympusmont.com" className="text-primary hover:underline">
                olympusmont.com
              </a>
              <span className="text-muted-foreground">|</span>
              <a href="https://api.olympusmont.com/api/health" className="text-primary hover:underline">
                API Docs
              </a>
              <span className="text-muted-foreground">|</span>
              <a href="https://github.com/soleroms/cgc-core" className="text-primary hover:underline">
                GitHub
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
