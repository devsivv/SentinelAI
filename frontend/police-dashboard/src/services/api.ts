import axios from 'axios';
import type { InvestigateRequest, AggregatedRiskResponse } from '../types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Single shared timeout — 2 minutes to accommodate cold-start inference on Render free tier
const REQUEST_TIMEOUT_MS = 120_000;

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: REQUEST_TIMEOUT_MS,
  headers: {
    'Content-Type': 'application/json',
  },
});

/** Classifies an Axios error into a human-readable, differentiated message. */
export function classifyApiError(error: unknown): string {
  if (!axios.isAxiosError(error)) {
    return error instanceof Error ? error.message : 'An unexpected error occurred.';
  }

  // Timeout
  if (error.code === 'ECONNABORTED' || error.message?.toLowerCase().includes('timeout')) {
    return 'timeout';
  }

  // Network disconnected (no response received)
  if (!error.response) {
    return 'network';
  }

  const status = error.response.status;

  if (status === 404) return 'not_found';
  if (status === 503 || status === 502) return 'unavailable';
  if (status >= 500) return 'server_error';

  // Fallback: use backend detail if present
  return error.response?.data?.detail || error.message || 'An error occurred.';
}

export const investigationService = {
  submitInvestigation: async (request: InvestigateRequest): Promise<AggregatedRiskResponse> => {
    try {
      const response = await axiosInstance.post<AggregatedRiskResponse>('/investigate', request);
      return response.data;
    } catch (error) {
      throw new Error(classifyApiError(error));
    }
  },
};

export const caseService = {
  getCases: async () => {
    try {
      const response = await axiosInstance.get('/cases');
      return response.data;
    } catch (error) {
      throw new Error(classifyApiError(error));
    }
  },
  getCaseById: async (id: string) => {
    try {
      const response = await axiosInstance.get(`/cases/${id}`);
      return response.data;
    } catch (error) {
      throw new Error(classifyApiError(error));
    }
  },
};
