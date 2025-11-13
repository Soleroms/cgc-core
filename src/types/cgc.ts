/**
 * TypeScript Type Definitions
 * OlympusMont Systems LLC
 */

// Module Status Types
export type ModuleStatus = 'active' | 'processing' | 'idle' | 'error';

// CGC Module Interface
export interface Module {
  id: string;
  code: string;
  name: string;
  description: string;
  status: ModuleStatus;
  health: number;
  metrics: {
    uptime: number;
    accuracy: number;
    responseTime: number;
    errorRate: number;
    processedItems: number;
  };
}

// System Metrics
export interface SystemMetrics {
  totalDecisions: string;
  encryptedTransactions: string;
  averageConfidence: string;
  activeModules: string;
  auditIntegrity: string;
  legalCompliance: string;
}

// API Health Response
export interface HealthResponse {
  status: string;
  service: string;
  version: string;
  cgc_loaded: boolean;
  modules: {
    cgc_core: boolean;
    contract_analyzer: boolean;
  };
}

// CGC Decision Request
export interface DecisionRequest {
  module: string;
  action: string;
  input_data: Record<string, any>;
  context?: Record<string, any>;
}

// CGC Decision Response
export interface DecisionResponse {
  decision_id: string;
  module: string;
  action: string;
  result: any;
  confidence: number;
  timestamp: string;
  audit_hash: string;
}

// Contract Analysis Request
export interface ContractAnalysisRequest {
  contract_text: string;
  metadata?: {
    contract_type?: string;
    parties?: string[];
    jurisdiction?: string;
  };
}

// Contract Analysis Response
export interface ContractAnalysisResponse {
  analysis_id: string;
  contract_summary: string;
  key_terms: string[];
  risks: Array<{
    severity: 'high' | 'medium' | 'low';
    description: string;
    recommendation: string;
  }>;
  compliance_score: number;
  legal_frameworks: string[];
  timestamp: string;
}

// Audit Trail Entry
export interface AuditEntry {
  id: string;
  timestamp: Date;
  module: string;
  action: string;
  hash: string;
  encrypted: boolean;
  confidence: number;
}

// Legal Module
export interface LegalModule {
  id: string;
  name: string;
  description: string;
  status: 'active' | 'processing' | 'inactive';
  documentsScanned: number;
  complianceRate: number;
}

export default {
  Module,
  SystemMetrics,
  HealthResponse,
  DecisionRequest,
  DecisionResponse,
  ContractAnalysisRequest,
  ContractAnalysisResponse,
  AuditEntry,
  LegalModule,
};
