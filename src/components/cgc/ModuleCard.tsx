import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Module } from "@/types/cgc";
import { Activity, TrendingUp, Clock, AlertTriangle } from "lucide-react";

interface ModuleCardProps {
  module: Module;
}

const getStatusColor = (status: Module['status']) => {
  const colors = {
    active: 'bg-module-active text-success-foreground',
    processing: 'bg-module-processing text-warning-foreground',
    idle: 'bg-module-idle text-muted-foreground',
    error: 'bg-module-error text-error-foreground'
  };
  return colors[status];
};

const getHealthColor = (health: number) => {
  if (health >= 95) return 'text-success';
  if (health >= 85) return 'text-warning';
  return 'text-error';
};

export const ModuleCard = ({ module }: ModuleCardProps) => {
  return (
    <Card className="bg-gradient-module border-border/50 hover:border-primary/50 transition-all duration-300 shadow-module hover:shadow-elevated group">
      <div className="p-6">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <span className="text-2xl font-bold text-gradient-cognitive">
                {module.code}
              </span>
              <Badge className={getStatusColor(module.status)}>
                {module.status}
              </Badge>
            </div>
            <h3 className="text-lg font-semibold text-foreground mb-1">
              {module.name}
            </h3>
            <p className="text-sm text-muted-foreground">
              {module.description}
            </p>
          </div>
          <div className="flex flex-col items-end">
            <span className={`text-3xl font-bold ${getHealthColor(module.health)}`}>
              {module.health}%
            </span>
            <span className="text-xs text-muted-foreground">Health</span>
          </div>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-2 gap-4 mt-6 pt-4 border-t border-border/50">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-primary" />
            <div>
              <div className="text-xs text-muted-foreground">Uptime</div>
              <div className="text-sm font-semibold text-foreground">
                {module.metrics.uptime}%
              </div>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-success" />
            <div>
              <div className="text-xs text-muted-foreground">Accuracy</div>
              <div className="text-sm font-semibold text-foreground">
                {module.metrics.accuracy}%
              </div>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <Clock className="w-4 h-4 text-info" />
            <div>
              <div className="text-xs text-muted-foreground">Response</div>
              <div className="text-sm font-semibold text-foreground">
                {module.metrics.responseTime}ms
              </div>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-warning" />
            <div>
              <div className="text-xs text-muted-foreground">Error Rate</div>
              <div className="text-sm font-semibold text-foreground">
                {module.metrics.errorRate}%
              </div>
            </div>
          </div>
        </div>

        {/* Processed Items */}
        <div className="mt-4 pt-4 border-t border-border/50">
          <div className="text-xs text-muted-foreground mb-1">Processed Items</div>
          <div className="text-2xl font-bold text-gradient-primary">
            {module.metrics.processedItems.toLocaleString()}
          </div>
        </div>
      </div>
    </Card>
  );
};
