import type { CaseDetailsData } from '../types/case';

export const mockCaseDetails: Record<string, CaseDetailsData> = {
  'CAS-2026-001': {
    case_id: 'CAS-2026-001',
    title: 'Romance Scam Ring Detection',
    victim_name: 'John Doe',
    created_at: '2026-07-10T08:30:00Z',
    updated_at: '2026-07-11T09:15:00Z',
    risk_level: 'High',
    status: 'Open',
    assigned_officer: 'Officer Smith',
    fusion_verdict: 'High Confidence Romance Scam',
    overall_risk_score: 85,
    confidence_score: 92,
    investigation_summary: 'Multiple agents have corroborated behavior indicative of an organized romance scam. The suspect has engaged in deceptive communication patterns, provided phishing links via SMS, and requested fraudulent cryptocurrency transfers.',
    agent_results: [
      {
        agent_name: 'SMS Scam Agent',
        verdict: 'Fraudulent',
        risk_score: 90,
        confidence: 95,
        explanation: 'Identified urgent language patterns and romance scam scripts in message history.'
      },
      {
        agent_name: 'Phishing URL Agent',
        verdict: 'Fraudulent',
        risk_score: 95,
        confidence: 98,
        explanation: 'Extracted URL matches known malicious cryptocurrency credential harvesting domains.'
      },
      {
        agent_name: 'Transaction Fraud Agent',
        verdict: 'Suspicious',
        risk_score: 75,
        confidence: 80,
        explanation: 'Detected anomalous outward cryptocurrency flow to a high-risk wallet cluster.'
      }
    ],
    evidence: [
      { id: 'EV-1001', type: 'SMS', preview: '"Honey I need you to click this link to verify the transfer..."', status: 'Analyzed' },
      { id: 'EV-1002', type: 'URL', preview: 'http://crypto-secure-auth-update.net/login', status: 'Flagged' },
      { id: 'EV-1003', type: 'Transaction', preview: 'Outgoing transfer: 2.5 BTC to 1A1zP1...', status: 'Pending' },
      { id: 'EV-1004', type: 'Location', preview: '{"latitude":12.9716,"longitude":77.5946,"radius_km":5.0,"district":"Bengaluru Urban","state":"Karnataka"}', status: 'Analyzed' }
    ],
    recommended_actions: [
      'Freeze suspicious cryptocurrency wallet addresses',
      'Contact victim immediately to prevent further transfers',
      'Escalate to Cyber Crime Unit for cross-jurisdiction tracking',
      'Preserve all SMS logs as digital evidence'
    ],
    timeline: [
      { id: 'TL-1', event: 'Case automatically created by SentinelAI', timestamp: '2026-07-10T08:30:00Z', actor: 'System' },
      { id: 'TL-2', event: 'Initial evidence (SMS, URL) ingested', timestamp: '2026-07-10T08:31:00Z', actor: 'System' },
      { id: 'TL-3', event: 'Multi-Agent Analysis completed', timestamp: '2026-07-10T08:32:15Z', actor: 'Fusion Engine' },
      { id: 'TL-4', event: 'Assigned to Officer Smith for review', timestamp: '2026-07-11T09:15:00Z', actor: 'System Router' }
    ]
  },

  'CAS-2026-002': {
    case_id: 'CAS-2026-002',
    title: 'Investment Fraud Cryptocurrency',
    victim_name: 'Jane Smith',
    created_at: '2026-07-11T14:15:00Z',
    updated_at: '2026-07-12T10:00:00Z',
    risk_level: 'Critical',
    status: 'Under Review',
    assigned_officer: 'Detective Jones',
    fusion_verdict: 'Critical — Organized Cryptocurrency Investment Fraud',
    overall_risk_score: 96,
    confidence_score: 94,
    investigation_summary: 'Victim was defrauded via a fake cryptocurrency trading platform promising guaranteed returns. Analysis reveals coordinated phishing, fraudulent transaction patterns, and a domain registered days before the scam.',
    agent_results: [
      { agent_name: 'Phishing URL Agent', verdict: 'Fraudulent', risk_score: 98, confidence: 99, explanation: 'Domain is a clone of a legitimate exchange, registered 3 days before first contact with victim.' },
      { agent_name: 'Transaction Fraud Agent', verdict: 'Fraudulent', risk_score: 95, confidence: 92, explanation: 'Funds transferred to a known mule account cluster flagged in prior investigations.' },
      { agent_name: 'SMS Scam Agent', verdict: 'Suspicious', risk_score: 70, confidence: 78, explanation: 'Messages contain investment persuasion scripts consistent with pig butchering scams.' }
    ],
    evidence: [
      { id: 'EV-2001', type: 'URL', preview: 'https://cryptovest-secure-platform.io/register', status: 'Flagged' },
      { id: 'EV-2002', type: 'Transaction', preview: 'Wire: ₹4,80,000 to account ending 7734', status: 'Analyzed' },
      { id: 'EV-2003', type: 'SMS', preview: '"Your investment is ready. Withdraw profits now!"', status: 'Analyzed' }
    ],
    recommended_actions: [
      'Initiate a bank reversal request immediately',
      'Report domain to CERT-In for takedown',
      'Coordinate with Financial Intelligence Unit',
      'Notify national cybercrime portal (cybercrime.gov.in)'
    ],
    timeline: [
      { id: 'TL-1', event: 'Case created from citizen complaint', timestamp: '2026-07-11T14:15:00Z', actor: 'System' },
      { id: 'TL-2', event: 'URL and transaction evidence analyzed', timestamp: '2026-07-11T14:20:00Z', actor: 'Fusion Engine' },
      { id: 'TL-3', event: 'Escalated to Detective Jones', timestamp: '2026-07-12T10:00:00Z', actor: 'System Router' }
    ]
  },

  'CAS-2026-003': {
    case_id: 'CAS-2026-003',
    title: 'Phishing Email Campaign',
    victim_name: 'Alice Johnson',
    created_at: '2026-07-11T10:45:00Z',
    updated_at: '2026-07-11T12:30:00Z',
    risk_level: 'Medium',
    status: 'Open',
    assigned_officer: 'Officer Smith',
    fusion_verdict: 'Medium Risk — Mass Phishing Campaign Targeting Bank Customers',
    overall_risk_score: 68,
    confidence_score: 83,
    investigation_summary: 'Victim received a spoofed bank email directing them to a credential harvesting page. The URL was deactivated within hours of the report, suggesting an automated campaign.',
    agent_results: [
      { agent_name: 'Phishing URL Agent', verdict: 'Fraudulent', risk_score: 92, confidence: 90, explanation: 'URL matches a known phishing kit template targeting SBI customers.' },
      { agent_name: 'SMS Scam Agent', verdict: 'Clean', risk_score: 10, confidence: 88, explanation: 'No scam SMS patterns detected in provided evidence.' }
    ],
    evidence: [
      { id: 'EV-3001', type: 'URL', preview: 'http://sbi-secure-login-alert.tk/auth', status: 'Flagged' },
      { id: 'EV-3002', type: 'SMS', preview: 'Email header shows spoofed sender noreply@sbi-bank.co.in', status: 'Analyzed' }
    ],
    recommended_actions: [
      'Report phishing URL to Google Safe Browsing and PhishTank',
      'Advise victim to reset banking credentials immediately',
      'Monitor victim account for unauthorized access',
      'Investigate email hosting provider for sender identity'
    ],
    timeline: [
      { id: 'TL-1', event: 'Phishing report submitted by victim', timestamp: '2026-07-11T10:45:00Z', actor: 'Citizen Portal' },
      { id: 'TL-2', event: 'URL analysis flagged as phishing', timestamp: '2026-07-11T10:50:00Z', actor: 'Fusion Engine' },
      { id: 'TL-3', event: 'Assigned for officer follow-up', timestamp: '2026-07-11T12:30:00Z', actor: 'System Router' }
    ]
  },

  'CAS-2026-004': {
    case_id: 'CAS-2026-004',
    title: 'Tech Support Scam',
    victim_name: 'Robert Brown',
    created_at: '2026-07-09T09:20:00Z',
    updated_at: '2026-07-10T14:00:00Z',
    risk_level: 'Low',
    status: 'Closed',
    assigned_officer: 'Detective Miller',
    fusion_verdict: 'Low Risk — Tech Support Scam (Resolved)',
    overall_risk_score: 38,
    confidence_score: 79,
    investigation_summary: 'Victim was contacted by a fake Microsoft technician requesting remote access. No financial transfer was made. Victim disconnected before completing the scam. Case closed with advisory issued.',
    agent_results: [
      { agent_name: 'SMS Scam Agent', verdict: 'Suspicious', risk_score: 45, confidence: 72, explanation: 'Message pattern matches tech support social engineering scripts.' },
      { agent_name: 'Phishing URL Agent', verdict: 'Clean', risk_score: 15, confidence: 85, explanation: 'No malicious URLs found in the provided evidence.' }
    ],
    evidence: [
      { id: 'EV-4001', type: 'SMS', preview: '"Your Windows PC is compromised. Call 1-800-TECH now."', status: 'Analyzed' }
    ],
    recommended_actions: [
      'Issue victim advisory on tech support scam patterns',
      'No financial recovery required — no transfer was completed',
      'Log phone number to national scam registry'
    ],
    timeline: [
      { id: 'TL-1', event: 'Report filed by victim', timestamp: '2026-07-09T09:20:00Z', actor: 'Citizen Portal' },
      { id: 'TL-2', event: 'Evidence analyzed — no financial loss', timestamp: '2026-07-09T09:30:00Z', actor: 'Fusion Engine' },
      { id: 'TL-3', event: 'Advisory issued and case closed', timestamp: '2026-07-10T14:00:00Z', actor: 'Detective Miller' }
    ]
  },

  'CAS-2026-005': {
    case_id: 'CAS-2026-005',
    title: 'Grandparent Scam Pattern',
    victim_name: 'Mary Williams',
    created_at: '2026-07-12T16:50:00Z',
    updated_at: '2026-07-12T18:00:00Z',
    risk_level: 'High',
    status: 'Open',
    assigned_officer: 'Officer Davis',
    fusion_verdict: 'High Risk — Grandparent Impersonation Scam',
    overall_risk_score: 81,
    confidence_score: 87,
    investigation_summary: 'Elderly victim was called by someone impersonating their grandchild claiming to be in legal trouble. Victim was instructed to wire bail money urgently. SentinelAI detected the urgency manipulation pattern and emergency wire transfer signature.',
    agent_results: [
      { agent_name: 'SMS Scam Agent', verdict: 'Fraudulent', risk_score: 88, confidence: 91, explanation: 'Script contains classic grandparent scam urgency markers and impersonation structure.' },
      { agent_name: 'Transaction Fraud Agent', verdict: 'Suspicious', risk_score: 76, confidence: 80, explanation: 'Outgoing wire to an unregistered account flagged as a potential mule account.' }
    ],
    evidence: [
      { id: 'EV-5001', type: 'SMS', preview: '"Grandma please don\'t tell mom, I need bail money now..."', status: 'Flagged' },
      { id: 'EV-5002', type: 'Transaction', preview: 'Wire: ₹65,000 to account XB-0034-7821', status: 'Pending' }
    ],
    recommended_actions: [
      'Contact victim\'s family immediately to confirm grandchild is safe',
      'Initiate wire recall with victim\'s bank',
      'Trace receiving account to identify mule network',
      'Issue community alert about active grandparent scam pattern in area'
    ],
    timeline: [
      { id: 'TL-1', event: 'Emergency report filed', timestamp: '2026-07-12T16:50:00Z', actor: 'Citizen Portal' },
      { id: 'TL-2', event: 'High-risk verdict generated', timestamp: '2026-07-12T16:55:00Z', actor: 'Fusion Engine' },
      { id: 'TL-3', event: 'Assigned to Officer Davis', timestamp: '2026-07-12T18:00:00Z', actor: 'System Router' }
    ]
  },

  'CAS-2026-006': {
    case_id: 'CAS-2026-006',
    title: 'Fake E-commerce Store',
    victim_name: 'James Wilson',
    created_at: '2026-07-08T11:10:00Z',
    updated_at: '2026-07-09T09:45:00Z',
    risk_level: 'Medium',
    status: 'Under Review',
    assigned_officer: 'Officer Smith',
    fusion_verdict: 'Medium Risk — Fraudulent E-commerce Operation',
    overall_risk_score: 64,
    confidence_score: 80,
    investigation_summary: 'Victim ordered electronics from a website that appeared legitimate. No product was delivered. The domain was registered 12 days before the purchase and uses a cloned product catalog from a real retailer.',
    agent_results: [
      { agent_name: 'Phishing URL Agent', verdict: 'Suspicious', risk_score: 72, confidence: 81, explanation: 'Domain age is 12 days, uses free hosting, and has no valid SSL certificate for checkout.' },
      { agent_name: 'Transaction Fraud Agent', verdict: 'Suspicious', risk_score: 60, confidence: 74, explanation: 'Payment to an unregistered payment gateway with no consumer protection.' }
    ],
    evidence: [
      { id: 'EV-6001', type: 'URL', preview: 'https://bestelectronics-deals24.shop/checkout', status: 'Flagged' },
      { id: 'EV-6002', type: 'Transaction', preview: 'UPI payment: ₹14,500 to merchant_id@paydummy', status: 'Analyzed' }
    ],
    recommended_actions: [
      'File consumer complaint with National Consumer Helpline (1915)',
      'Request UPI chargeback through victim\'s bank',
      'Report domain to ICANN and hosting provider',
      'Check for other victims of the same domain on cybercrime portal'
    ],
    timeline: [
      { id: 'TL-1', event: 'Complaint submitted via citizen portal', timestamp: '2026-07-08T11:10:00Z', actor: 'Citizen Portal' },
      { id: 'TL-2', event: 'Domain and payment analysis completed', timestamp: '2026-07-08T11:20:00Z', actor: 'Fusion Engine' },
      { id: 'TL-3', event: 'Under review by Officer Smith', timestamp: '2026-07-09T09:45:00Z', actor: 'System Router' }
    ]
  },

  'CAS-2026-007': {
    case_id: 'CAS-2026-007',
    title: 'Employment Scam Network',
    victim_name: 'Patricia Taylor',
    created_at: '2026-07-13T09:05:00Z',
    updated_at: '2026-07-13T11:30:00Z',
    risk_level: 'Critical',
    status: 'Open',
    assigned_officer: 'Detective Jones',
    fusion_verdict: 'Critical — Organized Employment Scam with Money Mule Recruitment',
    overall_risk_score: 93,
    confidence_score: 89,
    investigation_summary: 'Victim was recruited through a fake job posting promising remote work. After a fake interview, they were asked to receive and forward money, making them an unwitting money mule. Organized ring suspected involving multiple victims.',
    agent_results: [
      { agent_name: 'SMS Scam Agent', verdict: 'Fraudulent', risk_score: 95, confidence: 92, explanation: 'Job offer SMS contains known money mule recruitment script patterns.' },
      { agent_name: 'Transaction Fraud Agent', verdict: 'Fraudulent', risk_score: 91, confidence: 88, explanation: 'Transaction flow matches money mule forwarding patterns — receive and rapidly re-transfer.' },
      { agent_name: 'Phishing URL Agent', verdict: 'Suspicious', risk_score: 65, confidence: 75, explanation: 'Fake company website has no business registration and cloned HR content.' }
    ],
    evidence: [
      { id: 'EV-7001', type: 'SMS', preview: '"Congratulations! You are selected for Work From Home. Process your first task."', status: 'Flagged' },
      { id: 'EV-7002', type: 'Transaction', preview: 'Received: ₹50,000 → Forwarded: ₹48,000 within 2 hrs', status: 'Analyzed' },
      { id: 'EV-7003', type: 'URL', preview: 'https://globalrecruitment-jobs.net/apply', status: 'Flagged' }
    ],
    recommended_actions: [
      'Immediately freeze victim\'s account to stop mule activity',
      'Educate victim — they may face legal risk as an unwitting mule',
      'Trace full transaction chain to upstream orchestrator accounts',
      'Coordinate with telecom to trace SIM behind recruitment number'
    ],
    timeline: [
      { id: 'TL-1', event: 'Victim self-reported after realizing scam', timestamp: '2026-07-13T09:05:00Z', actor: 'Citizen Portal' },
      { id: 'TL-2', event: 'Critical verdict generated — mule pattern detected', timestamp: '2026-07-13T09:12:00Z', actor: 'Fusion Engine' },
      { id: 'TL-3', event: 'Escalated to Detective Jones', timestamp: '2026-07-13T11:30:00Z', actor: 'System Router' }
    ]
  },

  'CAS-2026-008': {
    case_id: 'CAS-2026-008',
    title: 'Lottery Fraud Analysis',
    victim_name: 'Michael Anderson',
    created_at: '2026-07-05T14:30:00Z',
    updated_at: '2026-07-07T10:00:00Z',
    risk_level: 'Low',
    status: 'Closed',
    assigned_officer: 'Officer Davis',
    fusion_verdict: 'Low Risk — Classic Lottery Fraud (No Financial Loss)',
    overall_risk_score: 30,
    confidence_score: 91,
    investigation_summary: 'Victim received an SMS claiming they won a lottery prize and needed to pay processing fees to claim. Victim did not pay. Case categorized as low-risk; no financial loss occurred. Closed after advisory was issued.',
    agent_results: [
      { agent_name: 'SMS Scam Agent', verdict: 'Fraudulent', risk_score: 87, confidence: 96, explanation: 'Classic lottery advance-fee fraud script detected with prize claim urgency triggers.' }
    ],
    evidence: [
      { id: 'EV-8001', type: 'SMS', preview: '"CONGRATULATIONS! You have won ₹25 Lakh. Pay ₹500 processing fee to claim."', status: 'Analyzed' }
    ],
    recommended_actions: [
      'Log sender number to scam registry',
      'Issue standard advisory to victim',
      'No financial recovery needed — case closed'
    ],
    timeline: [
      { id: 'TL-1', event: 'Lottery SMS reported by victim', timestamp: '2026-07-05T14:30:00Z', actor: 'Citizen Portal' },
      { id: 'TL-2', event: 'SMS analyzed — fraud pattern confirmed', timestamp: '2026-07-05T14:35:00Z', actor: 'Fusion Engine' },
      { id: 'TL-3', event: 'Advisory issued, case closed', timestamp: '2026-07-07T10:00:00Z', actor: 'Officer Davis' }
    ]
  },

  'CAS-2026-009': {
    case_id: 'CAS-2026-009',
    title: 'Advance Fee Fraud',
    victim_name: 'Linda Thomas',
    created_at: '2026-07-12T13:40:00Z',
    updated_at: '2026-07-13T08:30:00Z',
    risk_level: 'High',
    status: 'Under Review',
    assigned_officer: 'Detective Miller',
    fusion_verdict: 'High Risk — Advance Fee Fraud with Repeated Payments',
    overall_risk_score: 84,
    confidence_score: 88,
    investigation_summary: 'Victim paid multiple advance fees over 3 weeks believing they were unlocking a foreign inheritance. Total loss: ₹2,10,000. Investigation reveals an organized advance fee fraud ring operating from multiple jurisdictions.',
    agent_results: [
      { agent_name: 'Transaction Fraud Agent', verdict: 'Fraudulent', risk_score: 91, confidence: 90, explanation: 'Repeated small payments to diverse accounts — pattern matches advance fee fraud drip strategy.' },
      { agent_name: 'SMS Scam Agent', verdict: 'Fraudulent', risk_score: 86, confidence: 89, explanation: 'SMS content uses classic Nigerian advance fee fraud narrative structure.' }
    ],
    evidence: [
      { id: 'EV-9001', type: 'SMS', preview: '"You have been selected as the beneficiary of $3M estate. Processing fee required."', status: 'Flagged' },
      { id: 'EV-9002', type: 'Transaction', preview: '7 transfers over 3 weeks totaling ₹2,10,000', status: 'Analyzed' }
    ],
    recommended_actions: [
      'Contact victim urgently to prevent additional payments',
      'Initiate reversal requests for all recent transactions',
      'File Interpol referral for cross-border investigation',
      'Freeze all receiving accounts pending investigation'
    ],
    timeline: [
      { id: 'TL-1', event: 'Victim filed complaint after 3rd payment', timestamp: '2026-07-12T13:40:00Z', actor: 'Citizen Portal' },
      { id: 'TL-2', event: 'High-risk verdict — repeat payment pattern detected', timestamp: '2026-07-12T13:50:00Z', actor: 'Fusion Engine' },
      { id: 'TL-3', event: 'Assigned to Detective Miller', timestamp: '2026-07-13T08:30:00Z', actor: 'System Router' }
    ]
  },

  'CAS-2026-010': {
    case_id: 'CAS-2026-010',
    title: 'Business Email Compromise',
    victim_name: 'Corporate Corp LLC',
    created_at: '2026-07-13T10:15:00Z',
    updated_at: '2026-07-13T14:45:00Z',
    risk_level: 'Critical',
    status: 'Open',
    assigned_officer: 'Officer Smith',
    fusion_verdict: 'Critical — Business Email Compromise with Large Wire Fraud',
    overall_risk_score: 97,
    confidence_score: 95,
    investigation_summary: 'Attacker compromised a vendor email account and sent fraudulent invoice payment instructions to the victim organization. A ₹38,00,000 wire was completed to an attacker-controlled account before the fraud was detected.',
    agent_results: [
      { agent_name: 'Phishing URL Agent', verdict: 'Fraudulent', risk_score: 96, confidence: 94, explanation: 'Email domain is a homograph attack (rn vs m substitution) of a trusted vendor domain.' },
      { agent_name: 'Transaction Fraud Agent', verdict: 'Fraudulent', risk_score: 98, confidence: 97, explanation: 'First-time large wire to a new account — matches BEC wire fraud signature.' },
      { agent_name: 'SMS Scam Agent', verdict: 'Clean', risk_score: 5, confidence: 90, explanation: 'No SMS evidence submitted — BEC occurred via email only.' }
    ],
    evidence: [
      { id: 'EV-10001', type: 'URL', preview: 'Sender: accounts@payrnents-vendor.com (spoofed)', status: 'Flagged' },
      { id: 'EV-10002', type: 'Transaction', preview: 'Wire: ₹38,00,000 to Axis Bank account 00912345672', status: 'Flagged' }
    ],
    recommended_actions: [
      'Initiate emergency wire recall with the originating bank immediately',
      'Notify RBI Financial Intelligence Unit for account freeze',
      'Preserve all email headers and forwarding rules as forensic evidence',
      'Conduct internal audit for additional compromised email accounts',
      'Engage cyber forensics team for email server investigation'
    ],
    timeline: [
      { id: 'TL-1', event: 'Organization filed urgent BEC complaint', timestamp: '2026-07-13T10:15:00Z', actor: 'Citizen Portal' },
      { id: 'TL-2', event: 'Critical verdict generated — BEC wire fraud confirmed', timestamp: '2026-07-13T10:22:00Z', actor: 'Fusion Engine' },
      { id: 'TL-3', event: 'Assigned to Officer Smith — priority escalation', timestamp: '2026-07-13T14:45:00Z', actor: 'System Router' }
    ]
  }
};
