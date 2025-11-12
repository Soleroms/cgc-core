// CGC_CORE™ Type Definitions
// Version: v2.1.4

export type ModuleStatus = 'active' | 'processing' | 'idle' | 'error';

export interface Module {
  id: string;
  name: string;
  code: string;
  description: string;
  status: ModuleStatus;
  health: number;
  lastUpdate: Date;
  metrics: ModuleMetrics;
}

export interface ModuleMetrics {
  uptime: number;
  processedItems: number;
  accuracy: number;
  responseTime: number;
  errorRate: number;
}

export interface AuditEntry {
  id: string;
  timestamp: Date;
  module: string;
  action: string;
  hash: string;
  encrypted: boolean;
  confidence: number;
  userId?: string;
}

export interface LegalDocument {
  id: string;
  title: string;
  type: 'contract' | 'statute' | 'regulation' | 'case-law';
  status: 'compliant' | 'non-compliant' | 'review-required';
  confidence: number;
  riskLevel: 'low' | 'medium' | 'high';
  scannedAt: Date;
  findings: string[];
}

export interface SystemMetrics {
  totalDecisions: number;
  encryptedTransactions: number;
  averageConfidence: number;
  activeModules: number;
  auditTrailIntegrity: number;
  legalComplianceRate: number;
}
