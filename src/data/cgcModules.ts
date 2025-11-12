import { Module } from '@/types/cgc';

export const cgcModules: Module[] = [
  {
    id: 'pan',
    name: 'Perception & Analysis Node',
    code: 'PAN™',
    description: 'Data interpretation & context synthesis. Collects and interprets real-world inputs.',
    status: 'active',
    health: 98,
    lastUpdate: new Date(),
    metrics: {
      uptime: 99.9,
      processedItems: 1547832,
      accuracy: 97.8,
      responseTime: 127,
      errorRate: 0.02
    }
  },
  {
    id: 'ecm',
    name: 'Ethical Calibration Module',
    code: 'ECM™',
    description: 'Ethical normalization & scoring. Converts ethical principles into quantitative values.',
    status: 'active',
    health: 96,
    lastUpdate: new Date(),
    metrics: {
      uptime: 99.7,
      processedItems: 892453,
      accuracy: 96.4,
      responseTime: 215,
      errorRate: 0.04
    }
  },
  {
    id: 'pfm',
    name: 'Predictive Feedback Mechanism',
    code: 'PFM™',
    description: 'Predictive analytics & adaptive learning. Generates forecasts and monitors outcomes.',
    status: 'processing',
    health: 94,
    lastUpdate: new Date(),
    metrics: {
      uptime: 99.5,
      processedItems: 654321,
      accuracy: 94.2,
      responseTime: 342,
      errorRate: 0.06
    }
  },
  {
    id: 'sda',
    name: 'Smart Data Advisor',
    code: 'SDA™',
    description: 'Cognitive mentoring & data insight. Analyzes historical data for actionable improvements.',
    status: 'active',
    health: 97,
    lastUpdate: new Date(),
    metrics: {
      uptime: 99.8,
      processedItems: 1234567,
      accuracy: 95.9,
      responseTime: 189,
      errorRate: 0.03
    }
  },
  {
    id: 'tco',
    name: 'Traceability & Cognitive Oversight',
    code: 'TCO™ (AuditChain)',
    description: 'Immutable logging & decision auditability. Ensures traceable accountability.',
    status: 'active',
    health: 99,
    lastUpdate: new Date(),
    metrics: {
      uptime: 99.99,
      processedItems: 2847391,
      accuracy: 99.2,
      responseTime: 98,
      errorRate: 0.01
    }
  },
  {
    id: 'cgc',
    name: 'Governance Orchestrator',
    code: 'CGC™ Loop',
    description: 'Integrative control loop. Synchronizes all modules in real-time governance.',
    status: 'active',
    health: 98,
    lastUpdate: new Date(),
    metrics: {
      uptime: 99.9,
      processedItems: 3456789,
      accuracy: 98.1,
      responseTime: 156,
      errorRate: 0.02
    }
  }
];

export const legalModules = [
  {
    id: 'legal-scanner',
    name: 'LegalScanner',
    description: 'Scans contracts, statutes, and regulations for compliance indicators',
    status: 'active' as const,
    documentsScanned: 45892,
    complianceRate: 94.7
  },
  {
    id: 'doc-intelligence',
    name: 'Document Intelligence Engine',
    description: 'NLP-powered interpretation and classification of legal clauses',
    status: 'active' as const,
    documentsScanned: 38456,
    complianceRate: 96.2
  },
  {
    id: 'legal-reasoning',
    name: 'Legal Reasoning Layer',
    description: 'Structured reasoning on legal logic with ECM™ ethical calibration',
    status: 'processing' as const,
    documentsScanned: 29384,
    complianceRate: 95.8
  },
  {
    id: 'compliance-audit',
    name: 'Compliance Audit Sync',
    description: 'Synchronizes with TCO™ for immutable legal traceability',
    status: 'active' as const,
    documentsScanned: 52193,
    complianceRate: 98.4
  },
  {
    id: 'human-override',
    name: 'Human Override Mode',
    description: 'Forces human validation when confidence < 85%',
    status: 'idle' as const,
    documentsScanned: 12847,
    complianceRate: 99.1
  }
];
