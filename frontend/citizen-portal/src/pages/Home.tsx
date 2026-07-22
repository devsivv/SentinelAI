import { Link } from 'react-router-dom';
import { ShieldCheck, MessageSquare, Link as LinkIcon, FileSearch, ArrowRight, Lock } from 'lucide-react';

export default function Home() {
  return (
    <div className="space-y-16 py-8">
      {/* Hero section */}
      <div className="text-center max-w-3xl mx-auto space-y-6">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-300 text-xs font-semibold uppercase tracking-wider">
          <ShieldCheck className="h-3.5 w-3.5" aria-hidden="true" />
          Public Safety & Threat Reporting
        </div>
        
        <h1 className="text-4xl sm:text-5xl font-extrabold text-white tracking-tight leading-tight">
          Citizen Safety Portal
        </h1>
        
        <p className="text-lg text-gray-300 leading-relaxed">
          Report cyber fraud, verify suspicious communications, and track investigation progress using multi-agent artificial intelligence.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
          <Link
            to="/investigate"
            className="inline-flex items-center justify-center gap-2 px-8 py-3.5 rounded-xl font-bold text-white bg-blue-600 hover:bg-blue-500 shadow-lg shadow-blue-900/40 transition-all min-h-[48px] w-full sm:w-auto"
          >
            <FileSearch className="h-5 w-5" aria-hidden="true" />
            <span>Report Fraud / Scan SMS</span>
            <ArrowRight className="h-4 w-4" aria-hidden="true" />
          </Link>
        </div>
      </div>

      {/* Feature cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-card p-6 flex flex-col gap-4">
          <div className="w-12 h-12 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400">
            <MessageSquare className="h-6 w-6" aria-hidden="true" />
          </div>
          <h3 className="text-lg font-bold text-white">SMS & Communication Scan</h3>
          <p className="text-sm text-gray-400 leading-relaxed">
            Instantly evaluate suspicious text messages for scam patterns, social engineering, and fraudulent intent.
          </p>
        </div>

        <div className="glass-card p-6 flex flex-col gap-4">
          <div className="w-12 h-12 rounded-xl bg-purple-600/20 border border-purple-500/30 flex items-center justify-center text-purple-400">
            <LinkIcon className="h-6 w-6" aria-hidden="true" />
          </div>
          <h3 className="text-lg font-bold text-white">Phishing Link Verification</h3>
          <p className="text-sm text-gray-400 leading-relaxed">
            Scan web links and domains against AI models to detect phishing attempts before clicking.
          </p>
        </div>

        <div className="glass-card p-6 flex flex-col gap-4">
          <div className="w-12 h-12 rounded-xl bg-green-600/20 border border-green-500/30 flex items-center justify-center text-green-400">
            <Lock className="h-6 w-6" aria-hidden="true" />
          </div>
          <h3 className="text-lg font-bold text-white">Case Tracking & Status</h3>
          <p className="text-sm text-gray-400 leading-relaxed">
            Track your complaint status using your unique Case ID directly connected to police intelligence.
          </p>
        </div>
      </div>
    </div>
  );
}
