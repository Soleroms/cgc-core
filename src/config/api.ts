/**
 * API Service - Handles all backend communication
 * OlympusMont Systems LLC
 */

import axios, { AxiosInstance, AxiosError } from 'axios';
import { API_CONFIG, API_ENDPOINTS } from '@/config/api';

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
  headers: API_CONFIG.headers,
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// API Service
export const apiService = {
  /**
   * Health Check
   */
  async getHealth() {
    const response = await apiClient.get(API_ENDPOINTS.health);
    return response.data;
  },

  /**
   * Get System Metrics
   */
  async getMetrics() {
    const response = await apiClient.get(API_ENDPOINTS.metrics);
    return response.data;
  },

  /**
   * Get System Status
   */
  async getStatus() {
    const response = await apiClient.get(API_ENDPOINTS.status);
    return response.data;
  },

  /**
   * Execute CGC Decision
   */
  async executeDecision(data: {
    module: string;
    action: string;
    input_data: Record<string, any>;
    context?: Record<string, any>;
  }) {
    const response = await apiClient.post(API_ENDPOINTS.decision, data);
    return response.data;
  },

  /**
   * Analyze Contract (DiscipleAI Legal)
   */
  async analyzeContract(data: {
    contract_text: string;
    metadata?: Record<string, any>;
  }) {
    const response = await apiClient.post(API_ENDPOINTS.analyzeContract, data);
    return response.data;
  },
};

export default apiService;
