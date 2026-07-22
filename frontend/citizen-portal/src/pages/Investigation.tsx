import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import EvidenceForm from '../components/EvidenceForm';
import { investigationService } from '../services/api';
import type { EvidenceItem } from '../types';
import { ShieldCheck } from 'lucide-react';

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
    <div className="max-w-4xl mx-auto py-6 space-y-8">
      {/* Page Header */}
      <div className="text-center sm:text-left space-y-2">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-300 text-xs font-semibold uppercase tracking-wider mb-2">
          <ShieldCheck className="h-3.5 w-3.5" aria-hidden="true" />
          AI Multi-Agent Investigation
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          New Investigation
        </h1>
        <p className="text-gray-300 text-base leading-relaxed max-w-2xl">
          Provide the Case ID and attach evidence payloads (SMS, URL, or Transaction) to run real-time multi-agent intelligence analysis.
        </p>
      </div>

      {/* Form Container */}
      <EvidenceForm
        onSubmit={handleSubmit}
        isLoading={isLoading}
        error={error}
      />
    </div>
  );
}
