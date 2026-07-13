import axios from 'axios';
import type { InvestigateRequest, AggregatedRiskResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const investigationService = {
  submitInvestigation: async (request: InvestigateRequest): Promise<AggregatedRiskResponse> => {
    try {
      const response = await axiosInstance.post<AggregatedRiskResponse>('/investigate', request);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.detail || error.message || 'An error occurred during investigation submission.');
      }
      throw error;
    }
  },
};
