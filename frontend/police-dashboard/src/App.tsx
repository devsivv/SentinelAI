import { Routes, Route } from 'react-router-dom';
import { AlertTriangle } from 'lucide-react';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Cases from './pages/Cases';
import CaseDetails from './pages/CaseDetails';
import Profile from './pages/Profile';
import NotFound from './components/NotFound';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="cases" element={<Cases />} />
        <Route path="cases/:id" element={<CaseDetails />} />
        <Route path="profile" element={<Profile />} />
        <Route path="alerts" element={
          <div className="space-y-6">
            <div className="border-b border-gray-200 pb-5">
              <h2 className="text-xl sm:text-2xl font-bold leading-7 text-gray-900 break-words">
                System Alerts
              </h2>
              <p className="mt-1 text-sm text-gray-500">
                Real-time notifications and high-priority case escalations.
              </p>
            </div>
            {/* Alerts empty state */}
            <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-gray-300 bg-white p-12 sm:p-16 text-center shadow-sm">
              <div className="mb-4 p-4 bg-gray-100 rounded-full">
                <AlertTriangle className="h-8 w-8 text-gray-400" aria-hidden="true" />
              </div>
              <h3 className="text-base font-semibold text-gray-900 mb-1">No active alerts</h3>
              <p className="text-sm text-gray-500 max-w-sm">
                There are no active system alerts at this time. High-priority case notifications will appear here when triggered.
              </p>
            </div>
          </div>
        } />
        {/* Global 404 catch-all for unmatched routes within the Layout */}
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}

export default App;
