/**
 * CGC Modules Data
 * OlympusMont Systems LLC
 */

import { Module, LegalModule } from '@/types/cgc';

export const cgcModules: Module[] = [
  {
    id: 'pan',
    code: 'PAN™',
    name: 'Perception & Analysis Node',
    description: 'Data interpretation & context synthesis. Collects and interprets real-world inputs.',
    status: 'active',
    health: 98,
    metrics: {
      uptime: 99.9,
      accuracy: 97.8,
      responseTime: 127,
      errorRate: 0.02,
      processedItems: 1547832,
    },
  },
  {
    id: 'ecm',
    code: 'ECM™',
    name: 'Ethical Calibration Module',
    description: 'Ethical normalization & scoring. Converts ethical principles into quantitative values.',
    status: 'active',
    health: 96,
    metrics: {
      uptime: 99.7,
      accuracy: 96.4,
      responseTime: 215,
      errorRate: 0.04,
      processedItems: 892453,
    },
  },
  {
    id: 'pfm',
    code: 'PFM™',
    name: 'Predictive Feedback Mechanism',
    description: 'Predictive analytics & adaptive learning. Generates forecasts and monitors outcomes.',
    status: 'processing',
    health: 94,
    metrics: {
      uptime: 99.5,
      accuracy: 94.2,
      responseTime: 342,
      errorRate: 0.06,
      processedItems: 654321,
    },
  },
  {
    id: 'sda',
    code: 'SDA™',
    name: 'Smart Data Advisor',
    description: 'Cognitive mentoring & data insight. Analyzes historical data for actionable improvements.',
    status: 'active',
    health: 97,
    metrics: {
      uptime: 99.8,
      accuracy: 95.9,
      responseTime: 189,
      errorRate: 0.03,
      processedItems: 1234567,
    },
  },
  {
    id: 'tco',
    code: 'TCO™ (AuditChain)',
    name: 'Traceability & Cognitive Oversight',
    description: 'Immutable logging & decision auditability. Ensures traceable accountability.',
    status: 'active',
    health: 99,
    metrics: {
      uptime: 99.99,
      accuracy: 99.2,
      responseTime: 98,
      errorRate: 0.01,
      processedItems: 2847391,
    },
  },
  {
    id: 'cgc-loop',
    code: 'CGC™ Loop',
    name: 'Governance Orchestrator',
    description: 'Integrative control loop. Synchronizes all modules in real-time governance.',
    status: 'active',
    health: 98,
    metrics: {
      uptime: 99.9,
      accuracy: 98.1,
      responseTime: 156,
      errorRate: 0.02,
      processedItems: 3456789,
    },
  },
];

export const legalModules: LegalModule[] = [
  {
    id: 'legal-scanner',
    name: 'Legal Compliance Scanner',
    description: 'Real-time contract analysis and compliance verification',
    status: 'active',
    documentsScanned: 15243,
    complianceRate: 98.2,
  },
  {
    id: 'risk-analyzer',
    name: 'Risk Assessment Engine',
    description: 'Automated risk detection and mitigation recommendations',
    status: 'active',
    documentsScanned: 8965,
    complianceRate: 96.8,
  },
  {
    id: 'regulatory-monitor',
    name: 'Regulatory Compliance Monitor',
    description: 'Multi-jurisdiction compliance tracking (GDPR, HIPAA, CCPA)',
    status: 'processing',
    documentsScanned: 12789,
    complianceRate: 97.5,
  },
];

export default {
  cgcModules,
  legalModules,
};
