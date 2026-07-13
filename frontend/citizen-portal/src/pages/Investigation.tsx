import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import EvidenceForm from '../components/EvidenceForm';
import { investigationService } from '../services/api';
import type { EvidenceItem } from '../types';

export default function Investigation() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (caseId: string, evidence: EvidenceItem[]) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await investigationService.submitInvestigation({
        case_id: caseId,
        evidence,
      });
      // Navigate to Results page, passing the response data in route state
      navigate(`/results/${caseId}`, { state: { response } });
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unexpected error occurred.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900">New Investigation</h2>
        <p className="mt-1 text-sm text-gray-500">
          Provide the case details and evidence below to initiate an AI-assisted analysis.
        </p>
      </div>
      
      <EvidenceForm 
        onSubmit={handleSubmit} 
        isLoading={isLoading} 
        error={error} 
      />
    </div>
  );
}
