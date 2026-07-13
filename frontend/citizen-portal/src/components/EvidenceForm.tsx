import React, { useState } from 'react';
import { EvidenceType } from '../types';
import type { EvidenceItem } from '../types';
import { Plus, Trash2, Loader2 } from 'lucide-react';
import ErrorState from './ErrorState';

interface EvidenceFormProps {
  onSubmit: (caseId: string, evidence: EvidenceItem[]) => void;
  isLoading: boolean;
  error?: string | null;
}

export default function EvidenceForm({ onSubmit, isLoading, error }: EvidenceFormProps) {
  const [caseId, setCaseId] = useState('');
  const [evidenceList, setEvidenceList] = useState<EvidenceItem[]>([
    { input_type: EvidenceType.SMS, payload: { text: '' } },
  ]);

  const handleAddEvidence = () => {
    setEvidenceList([...evidenceList, { input_type: EvidenceType.SMS, payload: { text: '' } }]);
  };

  const handleRemoveEvidence = (index: number) => {
    setEvidenceList(evidenceList.filter((_, i) => i !== index));
  };

  const handleTypeChange = (index: number, newType: string) => {
    const updated = [...evidenceList];
    updated[index].input_type = newType;
    
    // Reset payload with sensible defaults based on type
    if (newType === EvidenceType.SMS) {
      updated[index].payload = { text: '' };
    } else if (newType === EvidenceType.URL) {
      updated[index].payload = { url: '' };
    } else if (newType === EvidenceType.TRANSACTION) {
      updated[index].payload = { amount: 0, sender_id: '', receiver_id: '' };
    } else {
      updated[index].payload = {};
    }
    
    setEvidenceList(updated);
  };

  const handlePayloadChange = (index: number, key: string, value: string | number) => {
    const updated = [...evidenceList];
    updated[index].payload = { ...updated[index].payload, [key]: value };
    setEvidenceList(updated);
  };

  const isFormValid = () => {
    if (!caseId.trim()) return false;
    if (evidenceList.length === 0) return false;
    
    // Check if any payload has empty strings for its required fields
    for (const ev of evidenceList) {
      if (ev.input_type === EvidenceType.SMS && !(ev.payload.text as string)?.trim()) return false;
      if (ev.input_type === EvidenceType.URL && !(ev.payload.url as string)?.trim()) return false;
      if (ev.input_type === EvidenceType.TRANSACTION && (!ev.payload.sender_id || !ev.payload.receiver_id)) return false;
    }
    return true;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (isFormValid() && !isLoading) {
      onSubmit(caseId, evidenceList);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6 bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      
      {error && (
        <ErrorState 
          title="Submission Failed" 
          message={error} 
        />
      )}

      <div>
        <label htmlFor="caseId" className="block text-sm font-medium text-gray-700">Case ID</label>
        <input
          type="text"
          id="caseId"
          value={caseId}
          onChange={(e) => setCaseId(e.target.value)}
          placeholder="e.g. c-2026-0001"
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
          required
          disabled={isLoading}
          aria-required="true"
        />
      </div>

      <div className="space-y-4">
        <div className="flex justify-between items-center">
          <h3 className="text-lg font-medium text-gray-900" id="evidence-heading">Evidence Items</h3>
          <button
            type="button"
            onClick={handleAddEvidence}
            disabled={isLoading}
            className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 transition-colors"
            aria-label="Add new evidence item"
          >
            <Plus className="w-4 h-4 mr-1" aria-hidden="true" /> Add Evidence
          </button>
        </div>

        <div role="group" aria-labelledby="evidence-heading" className="space-y-4">
          {evidenceList.map((item, index) => (
            <div key={index} className="p-4 border border-gray-200 rounded-md bg-gray-50 relative">
              {evidenceList.length > 1 && (
                <button
                  type="button"
                  onClick={() => handleRemoveEvidence(index)}
                  disabled={isLoading}
                  className="absolute top-4 right-4 text-gray-400 hover:text-red-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 rounded p-1 disabled:opacity-50 transition-colors"
                  aria-label={`Remove evidence item ${index + 1}`}
                >
                  <Trash2 className="w-4 h-4" aria-hidden="true" />
                </button>
              )}
              
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="col-span-1">
                  <label htmlFor={`type-${index}`} className="block text-sm font-medium text-gray-700">Type</label>
                  <select
                    id={`type-${index}`}
                    value={item.input_type}
                    onChange={(e) => handleTypeChange(index, e.target.value)}
                    disabled={isLoading}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border bg-white disabled:bg-gray-100"
                  >
                    {Object.values(EvidenceType).map(type => (
                      <option key={type} value={type}>{type.toUpperCase()}</option>
                    ))}
                  </select>
                </div>

                <div className="col-span-1 md:col-span-3">
                  <label htmlFor={`payload-${index}`} className="block text-sm font-medium text-gray-700">Payload</label>
                  {item.input_type === EvidenceType.SMS && (
                    <textarea
                      id={`payload-${index}`}
                      value={(item.payload.text as string) || ''}
                      onChange={(e) => handlePayloadChange(index, 'text', e.target.value)}
                      disabled={isLoading}
                      placeholder="Enter SMS text..."
                      rows={2}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border disabled:bg-gray-100"
                      aria-required="true"
                    />
                  )}
                  {item.input_type === EvidenceType.URL && (
                    <input
                      id={`payload-${index}`}
                      type="url"
                      value={(item.payload.url as string) || ''}
                      onChange={(e) => handlePayloadChange(index, 'url', e.target.value)}
                      disabled={isLoading}
                      placeholder="https://example.com"
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border disabled:bg-gray-100"
                      aria-required="true"
                    />
                  )}
                  {item.input_type === EvidenceType.TRANSACTION && (
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 mt-1">
                      <input
                        type="number"
                        value={(item.payload.amount as number) || 0}
                        onChange={(e) => handlePayloadChange(index, 'amount', Number(e.target.value))}
                        disabled={isLoading}
                        placeholder="Amount"
                        className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border disabled:bg-gray-100"
                        aria-label="Transaction amount"
                      />
                      <input
                        type="text"
                        value={(item.payload.sender_id as string) || ''}
                        onChange={(e) => handlePayloadChange(index, 'sender_id', e.target.value)}
                        disabled={isLoading}
                        placeholder="Sender ID"
                        className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border disabled:bg-gray-100"
                        aria-label="Transaction sender ID"
                      />
                      <input
                        type="text"
                        value={(item.payload.receiver_id as string) || ''}
                        onChange={(e) => handlePayloadChange(index, 'receiver_id', e.target.value)}
                        disabled={isLoading}
                        placeholder="Receiver ID"
                        className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border disabled:bg-gray-100"
                        aria-label="Transaction receiver ID"
                      />
                    </div>
                  )}
                  {(item.input_type === EvidenceType.IMAGE || item.input_type === EvidenceType.AUDIO) && (
                    <div className="mt-1 p-3 border rounded-md bg-gray-100 text-sm text-gray-500 italic">
                      Media uploads are not supported in this MVP.
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="pt-4">
        <button
          type="submit"
          disabled={!isFormValid() || isLoading}
          className="w-full flex justify-center items-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          aria-busy={isLoading}
        >
          {isLoading ? (
            <>
              <Loader2 className="animate-spin -ml-1 mr-2 h-4 w-4" aria-hidden="true" />
              Submitting Investigation...
            </>
          ) : (
            'Submit Investigation'
          )}
        </button>
      </div>
    </form>
  );
}
