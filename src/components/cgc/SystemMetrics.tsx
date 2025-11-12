import { Card } from "@/components/ui/card";
import { Shield, Lock, CheckCircle, Activity, Database, Scale } from "lucide-react";

export const SystemMetrics = () => {
  const metrics = [
    {
      label: "Total Decisions",
      value: "12.4M",
      icon: Activity,
      color: "text-primary",
      bgColor: "bg-primary/10"
    },
    {
      label: "Encrypted Transactions",
      value: "100%",
      icon: Lock,
      color: "text-encrypted",
      bgColor: "bg-encrypted/10",
      glow: true
    },
    {
      label: "Average Confidence",
      value: "96.8%",
      icon: CheckCircle,
      color: "text-success",
      bgColor: "bg-success/10"
    },
    {
      label: "Active Modules",
      value: "6/6",
      icon: Database,
      color: "text-info",
      bgColor: "bg-info/10"
    },
    {
      label: "Audit Trail Integrity",
      value: "99.99%",
      icon: Shield,
      color: "text-encrypted",
      bgColor: "bg-encrypted/10"
    },
    {
      label: "Legal Compliance",
      value: "98.4%",
      icon: Scale,
      color: "text-primary",
      bgColor: "bg-primary/10"
    }
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
      {metrics.map((metric) => (
        <Card
          key={metric.label}
          className={`bg-card border-border/50 hover:border-primary/50 transition-all duration-300 ${
            metric.glow ? 'shadow-encrypted' : 'shadow-module'
          }`}
        >
          <div className="p-4">
            <div className={`w-10 h-10 rounded-lg ${metric.bgColor} flex items-center justify-center mb-3`}>
              <metric.icon className={`w-5 h-5 ${metric.color}`} />
            </div>
            <div className="text-2xl font-bold text-foreground mb-1">
              {metric.value}
            </div>
            <div className="text-xs text-muted-foreground">
              {metric.label}
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
};
