import axios from 'axios';
import type { InvestigateRequest, AggregatedRiskResponse } from '../types/api';

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

export const caseService = {
  getCases: async () => {
    try {
      const response = await axiosInstance.get('/cases');
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.detail || error.message || 'Failed to fetch cases from database.');
      }
      throw error;
    }
  },
  getCaseById: async (id: string) => {
    try {
      const response = await axiosInstance.get(`/cases/${id}`);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.detail || error.message || `Failed to fetch case ${id} from database.`);
      }
      throw error;
    }
  },
};

