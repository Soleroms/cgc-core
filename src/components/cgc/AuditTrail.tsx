import { Card } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { Shield, Lock, CheckCircle } from "lucide-react";

export const AuditTrail = () => {
  const auditEntries = [
    {
      id: "1",
      timestamp: new Date(),
      module: "PAN™",
      action: "Data interpretation completed",
      hash: "0x7f9a8b...",
      encrypted: true,
      confidence: 98.4
    },
    {
      id: "2",
      timestamp: new Date(Date.now() - 120000),
      module: "ECM™",
      action: "Ethical calibration validated",
      hash: "0x3e5c2d...",
      encrypted: true,
      confidence: 96.7
    },
    {
      id: "3",
      timestamp: new Date(Date.now() - 240000),
      module: "TCO™",
      action: "Audit entry logged to blockchain",
      hash: "0x9b4f1a...",
      encrypted: true,
      confidence: 99.9
    },
    {
      id: "4",
      timestamp: new Date(Date.now() - 360000),
      module: "Legal Scanner",
      action: "Contract compliance verified",
      hash: "0x2c8e7f...",
      encrypted: true,
      confidence: 94.8
    },
    {
      id: "5",
      timestamp: new Date(Date.now() - 480000),
      module: "PFM™",
      action: "Predictive model updated",
      hash: "0x6d1a9c...",
      encrypted: true,
      confidence: 95.2
    }
  ];

  return (
    <Card className="bg-gradient-module border-border/50 shadow-module">
      <div className="p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-lg bg-encrypted/10 flex items-center justify-center">
            <Shield className="w-5 h-5 text-encrypted" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-foreground">Audit Trail</h3>
            <p className="text-sm text-muted-foreground">Immutable decision logging</p>
          </div>
        </div>

        <ScrollArea className="h-[400px] pr-4">
          <div className="space-y-3">
            {auditEntries.map((entry, index) => (
              <div
                key={entry.id}
                className="p-4 bg-background/50 rounded-lg border border-border/50 hover:border-primary/30 transition-all duration-300 animate-slide-up"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-sm font-semibold text-primary">
                        {entry.module}
                      </span>
                      {entry.encrypted && (
                        <Lock className="w-3 h-3 text-encrypted" />
                      )}
                    </div>
                    <p className="text-sm text-foreground">{entry.action}</p>
                  </div>
                  <Badge variant="outline" className="border-success/50 text-success">
                    <CheckCircle className="w-3 h-3 mr-1" />
                    {entry.confidence}%
                  </Badge>
                </div>
                
                <div className="flex items-center justify-between mt-3 pt-3 border-t border-border/30">
                  <code className="text-xs text-muted-foreground font-mono">
                    Hash: {entry.hash}
                  </code>
                  <span className="text-xs text-muted-foreground">
                    {entry.timestamp.toLocaleTimeString()}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </ScrollArea>
      </div>
    </Card>
  );
};
