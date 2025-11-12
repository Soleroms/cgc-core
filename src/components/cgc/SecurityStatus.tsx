import { Card } from "@/components/ui/card";
import { Shield, Lock, Key, CheckCircle } from "lucide-react";

export const SecurityStatus = () => {
  const securityFeatures = [
    {
      label: "End-to-End Encryption",
      status: "Active",
      icon: Lock,
      level: "AES-256"
    },
    {
      label: "Blockchain Verification",
      status: "Active",
      icon: Shield,
      level: "SHA-256"
    },
    {
      label: "Zero-Knowledge Proofs",
      status: "Active",
      icon: Key,
      level: "ZK-SNARK"
    },
    {
      label: "Audit Trail Integrity",
      status: "Verified",
      icon: CheckCircle,
      level: "99.99%"
    }
  ];

  return (
    <Card className="bg-gradient-module border-encrypted/30 shadow-encrypted">
      <div className="p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-12 h-12 rounded-lg bg-encrypted/10 flex items-center justify-center animate-pulse-glow">
            <Shield className="w-6 h-6 text-encrypted" />
          </div>
          <div>
            <h3 className="text-xl font-bold text-foreground">Security Status</h3>
            <p className="text-sm text-muted-foreground">Enterprise-grade protection</p>
          </div>
        </div>

        <div className="space-y-4">
          {securityFeatures.map((feature, index) => (
            <div
              key={feature.label}
              className="flex items-center justify-between p-3 bg-background/50 rounded-lg border border-encrypted/20 animate-slide-up"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-encrypted/10 flex items-center justify-center">
                  <feature.icon className="w-4 h-4 text-encrypted" />
                </div>
                <div>
                  <div className="text-sm font-semibold text-foreground">
                    {feature.label}
                  </div>
                  <div className="text-xs text-muted-foreground">
                    {feature.level}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-encrypted animate-pulse-glow" />
                <span className="text-xs font-semibold text-encrypted">
                  {feature.status}
                </span>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-6 p-4 bg-encrypted/5 rounded-lg border border-encrypted/20">
          <div className="text-center">
            <div className="text-2xl font-bold text-encrypted mb-1">
              100%
            </div>
            <div className="text-xs text-muted-foreground">
              All transactions encrypted & verified
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
};
