/**
 * API Configuration for CGC CORE Dashboard
 * OlympusMont Systems LLC - olympusmont.com
 */

const isDevelopment = import.meta.env.MODE === 'development';

export const API_CONFIG = {
  baseURL: isDevelopment 
    ? 'http://localhost:8000'
    : 'https://cgc-core-production.up.railway.app',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
};

export const API_ENDPOINTS = {
  health: '/api/health',
  metrics: '/api/metrics',
  status: '/api/status',
  decision: '/api/decision',
  analyzeContract: '/api/analyze-contract',
};

export const SITE_URLS = {
  main: 'https://olympusmont.com',
  app: 'https://cgc-core-production.up.railway.app',
  api: 'https://cgc-core-production.up.railway.app',
};

export default API_CONFIG;