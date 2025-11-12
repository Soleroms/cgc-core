import { ModuleCard } from "@/components/cgc/ModuleCard";
import { SystemMetrics } from "@/components/cgc/SystemMetrics";
import { AuditTrail } from "@/components/cgc/AuditTrail";
import { LegalTechPanel } from "@/components/cgc/LegalTechPanel";
import { SecurityStatus } from "@/components/cgc/SecurityStatus";
import { cgcModules } from "@/data/cgcModules";
import { Brain, Shield } from "lucide-react";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border/50 bg-card/50 backdrop-blur-sm sticky top-0 z-50 shadow-elevated">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-lg bg-gradient-cognitive flex items-center justify-center shadow-primary">
                <Brain className="w-7 h-7 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gradient-cognitive">
                  CGC_CORE™
                </h1>
                <p className="text-sm text-muted-foreground">
                  Cognitive Governance Cycle v2.1.4
                </p>
              </div>
            </div>
            
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2 px-4 py-2 bg-encrypted/10 rounded-lg border border-encrypted/30">
                <Shield className="w-4 h-4 text-encrypted animate-pulse-glow" />
                <span className="text-sm font-semibold text-encrypted">
                  Secured
                </span>
              </div>
              <div className="text-right">
                <div className="text-sm font-semibold text-foreground">
                  OlympusMont Systems™
                </div>
                <div className="text-xs text-muted-foreground">
                  Powered by A.L. Soler
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        {/* System Metrics */}
        <section className="mb-8 animate-fade-in">
          <SystemMetrics />
        </section>

        {/* CGC Core Modules */}
        <section className="mb-8">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-foreground mb-2">
              Core Modules
            </h2>
            <p className="text-muted-foreground">
              Six interdependent modules governing cognitive decision-making
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {cgcModules.map((module, index) => (
              <div
                key={module.id}
                className="animate-slide-up"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <ModuleCard module={module} />
              </div>
            ))}
          </div>
        </section>

        {/* Subsidiary Integration & Audit Trail */}
        <section className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="animate-slide-up" style={{ animationDelay: '0.2s' }}>
            <LegalTechPanel />
          </div>
          <div className="animate-slide-up" style={{ animationDelay: '0.3s' }}>
            <AuditTrail />
          </div>
        </section>

        {/* Security Status */}
        <section className="animate-slide-up" style={{ animationDelay: '0.4s' }}>
          <SecurityStatus />
        </section>

        {/* Footer Info */}
        <section className="mt-12 p-6 bg-card/50 rounded-lg border border-border/50 text-center">
          <p className="text-sm text-muted-foreground mb-2">
            CGC_CORE™ - Transforming human and machine cognition into measurable, explainable, and legally compliant processes.
          </p>
          <p className="text-xs text-muted-foreground">
            Enterprise-grade cognitive governance | Full audit traceability | Legal compliance integration
          </p>
        </section>
      </main>
    </div>
  );
};

export default Index;
