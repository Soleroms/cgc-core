import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Scale, FileText, CheckCircle, AlertTriangle } from "lucide-react";
import { legalModules } from "@/data/cgcModules";

export const LegalTechPanel = () => {
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return <CheckCircle className="w-4 h-4 text-success" />;
      case 'processing':
        return <AlertTriangle className="w-4 h-4 text-warning animate-pulse-glow" />;
      default:
        return <CheckCircle className="w-4 h-4 text-muted-foreground" />;
    }
  };

  return (
    <Card className="bg-gradient-module border-border/50 shadow-module">
      <div className="p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center">
            <Scale className="w-6 h-6 text-primary" />
          </div>
          <div>
            <h3 className="text-xl font-bold text-foreground">DisciplineAI Assistant</h3>
            <p className="text-sm text-muted-foreground">LegalTech Subsidiary Integration</p>
          </div>
        </div>

        <div className="space-y-3">
          {legalModules.map((module, index) => (
            <div
              key={module.id}
              className="p-4 bg-background/50 rounded-lg border border-border/50 hover:border-primary/30 transition-all duration-300 animate-slide-up"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    {getStatusIcon(module.status)}
                    <h4 className="text-sm font-semibold text-foreground">
                      {module.name}
                    </h4>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    {module.description}
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 mt-3 pt-3 border-t border-border/30">
                <div className="flex items-center gap-2">
                  <FileText className="w-4 h-4 text-primary" />
                  <div>
                    <div className="text-xs text-muted-foreground">Documents</div>
                    <div className="text-sm font-semibold text-foreground">
                      {module.documentsScanned.toLocaleString()}
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-success" />
                  <div>
                    <div className="text-xs text-muted-foreground">Compliance</div>
                    <div className="text-sm font-semibold text-success">
                      {module.complianceRate}%
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-6 p-4 bg-primary/5 rounded-lg border border-primary/20">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm font-semibold text-foreground mb-1">
                Integration Status
              </div>
              <div className="text-xs text-muted-foreground">
                Synchronized with CGC_CORE™ governance loop
              </div>
            </div>
            <Badge className="bg-success text-success-foreground">
              <CheckCircle className="w-3 h-3 mr-1" />
              Active
            </Badge>
          </div>
        </div>
      </div>
    </Card>
  );
};
