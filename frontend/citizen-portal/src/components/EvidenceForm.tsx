import React, { useState } from 'react';
import { EvidenceType } from '../types';
import type { EvidenceItem } from '../types';
import { Plus, Trash2, Loader2, FileText, Send } from 'lucide-react';
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
    <form
      onSubmit={handleSubmit}
      className="glass-card p-6 sm:p-8 space-y-8 shadow-[0_0_40px_rgba(37,99,235,0.12)] border border-white/10 rounded-2xl bg-[#111827]/70 backdrop-blur-md"
    >
      {error && (
        <ErrorState
          title="Submission Failed"
          message={error}
        />
      )}

      {/* Case ID input section */}
      <div className="space-y-2">
        <label htmlFor="caseId" className="block text-sm font-semibold text-gray-200">
          Case ID <span className="text-blue-400">*</span>
        </label>
        <input
          type="text"
          id="caseId"
          value={caseId}
          onChange={(e) => setCaseId(e.target.value)}
          placeholder="e.g. CAS-2026-0001"
          className="w-full min-h-[44px] px-4 py-2.5 rounded-xl bg-[#0F172A] border border-white/10 text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 text-sm font-mono transition-all disabled:opacity-50"
          required
          disabled={isLoading}
          aria-required="true"
        />
        <p className="text-xs text-gray-400">Enter a unique identifier for this investigation tracking file.</p>
      </div>

      {/* Evidence Items Section */}
      <div className="space-y-5 pt-2 border-t border-white/10">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <FileText className="h-5 w-5 text-blue-400" aria-hidden="true" />
            <h3 className="text-lg font-bold text-white" id="evidence-heading">
              Evidentiary Payload Items
            </h3>
          </div>

          <button
            type="button"
            onClick={handleAddEvidence}
            disabled={isLoading}
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold text-blue-300 bg-blue-600/20 border border-blue-500/30 hover:bg-blue-600/30 transition-all disabled:opacity-50 min-h-[40px] focus-visible:outline-blue-500"
            aria-label="Add new evidence item"
          >
            <Plus className="w-4 h-4" aria-hidden="true" />
            <span>Add Evidence</span>
          </button>
        </div>

        <div role="group" aria-labelledby="evidence-heading" className="space-y-5">
          {evidenceList.map((item, index) => (
            <div
              key={index}
              className="p-5 rounded-xl border border-white/10 bg-[#0F172A]/60 relative transition-all hover:border-blue-500/30"
            >
              {evidenceList.length > 1 && (
                <button
                  type="button"
                  onClick={() => handleRemoveEvidence(index)}
                  disabled={isLoading}
                  className="absolute top-4 right-4 text-gray-400 hover:text-red-400 p-2 rounded-lg hover:bg-red-500/10 focus:outline-none focus-visible:ring-2 focus-visible:ring-red-500 disabled:opacity-50 transition-colors"
                  aria-label={`Remove evidence item ${index + 1}`}
                >
                  <Trash2 className="w-4 h-4" aria-hidden="true" />
                </button>
              )}

              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                {/* Type select */}
                <div className="col-span-1 space-y-1.5">
                  <label htmlFor={`type-${index}`} className="block text-xs font-semibold text-gray-300 uppercase tracking-wider">
                    Evidence Type
                  </label>
                  <select
                    id={`type-${index}`}
                    value={item.input_type}
                    onChange={(e) => handleTypeChange(index, e.target.value)}
                    disabled={isLoading}
                    className="w-full min-h-[44px] px-3 py-2.5 rounded-xl bg-[#0F172A] border border-white/10 text-white focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 text-sm font-semibold transition-all disabled:opacity-50 cursor-pointer"
                  >
                    {Object.values(EvidenceType).map((type) => (
                      <option key={type} value={type} className="bg-[#0F172A] text-white">
                        {type.toUpperCase()}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Payload inputs */}
                <div className="col-span-1 md:col-span-3 space-y-1.5">
                  <label htmlFor={`payload-${index}`} className="block text-xs font-semibold text-gray-300 uppercase tracking-wider">
                    Payload Content
                  </label>
                  {item.input_type === EvidenceType.SMS && (
                    <textarea
                      id={`payload-${index}`}
                      value={(item.payload.text as string) || ''}
                      onChange={(e) => handlePayloadChange(index, 'text', e.target.value)}
                      disabled={isLoading}
                      placeholder="Paste suspicious SMS text or communication log..."
                      rows={3}
                      className="w-full p-3 rounded-xl bg-[#0F172A] border border-white/10 text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 text-sm font-mono transition-all disabled:opacity-50"
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
                      placeholder="https://suspicious-phishing-link.com"
                      className="w-full min-h-[44px] px-4 py-2.5 rounded-xl bg-[#0F172A] border border-white/10 text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 text-sm font-mono transition-all disabled:opacity-50"
                      aria-required="true"
                    />
                  )}
                  {item.input_type === EvidenceType.TRANSACTION && (
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                      <div>
                        <label className="text-[10px] font-medium text-gray-400 mb-1 block">Amount ($)</label>
                        <input
                          type="number"
                          value={(item.payload.amount as number) || 0}
                          onChange={(e) => handlePayloadChange(index, 'amount', Number(e.target.value))}
                          disabled={isLoading}
                          placeholder="Amount"
                          className="w-full min-h-[44px] px-3 py-2 rounded-xl bg-[#0F172A] border border-white/10 text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 text-sm font-mono transition-all disabled:opacity-50"
                          aria-label="Transaction amount"
                        />
                      </div>
                      <div>
                        <label className="text-[10px] font-medium text-gray-400 mb-1 block">Sender ID</label>
                        <input
                          type="text"
                          value={(item.payload.sender_id as string) || ''}
                          onChange={(e) => handlePayloadChange(index, 'sender_id', e.target.value)}
                          disabled={isLoading}
                          placeholder="ACC-ORIGIN"
                          className="w-full min-h-[44px] px-3 py-2 rounded-xl bg-[#0F172A] border border-white/10 text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 text-sm font-mono transition-all disabled:opacity-50"
                          aria-label="Transaction sender ID"
                        />
                      </div>
                      <div>
                        <label className="text-[10px] font-medium text-gray-400 mb-1 block">Receiver ID</label>
                        <input
                          type="text"
                          value={(item.payload.receiver_id as string) || ''}
                          onChange={(e) => handlePayloadChange(index, 'receiver_id', e.target.value)}
                          disabled={isLoading}
                          placeholder="ACC-DEST"
                          className="w-full min-h-[44px] px-3 py-2 rounded-xl bg-[#0F172A] border border-white/10 text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 text-sm font-mono transition-all disabled:opacity-50"
                          aria-label="Transaction receiver ID"
                        />
                      </div>
                    </div>
                  )}
                  {item.input_type === EvidenceType.IMAGE && (
                    <div className="p-3.5 rounded-xl border border-white/10 bg-[#0F172A] text-xs text-gray-400 italic">
                      Image analysis is currently reserved for currency banknote verification models.
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Submit button */}
      <div className="pt-4 border-t border-white/10">
        <button
          type="submit"
          disabled={!isFormValid() || isLoading}
          className="w-full inline-flex justify-center items-center gap-2 py-3.5 px-6 rounded-xl font-bold text-base text-white bg-blue-600 hover:bg-blue-500 shadow-lg shadow-blue-900/40 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all min-h-[48px]"
          aria-busy={isLoading}
        >
          {isLoading ? (
            <>
              <Loader2 className="animate-spin h-5 w-5 text-white" aria-hidden="true" />
              <span>Analyzing Multi-Agent Intelligence...</span>
            </>
          ) : (
            <>
              <Send className="h-4 w-4" aria-hidden="true" />
              <span>Submit Investigation</span>
            </>
          )}
        </button>
      </div>
    </form>
  );
}
