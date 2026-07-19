import { Routes, Route } from 'react-router-dom';
import { AlertTriangle } from 'lucide-react';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Cases from './pages/Cases';
import CaseDetails from './pages/CaseDetails';
import Profile from './pages/Profile';
import PlaceholderCard from './components/PlaceholderCard';

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
              <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:truncate sm:tracking-tight">
                System Alerts
              </h2>
            </div>
            <PlaceholderCard 
              title="Real-time Notifications"
              description="Critical system alerts and high-priority case notifications."
              icon={<AlertTriangle className="h-10 w-10" />}
            />
          </div>
        } />
      </Route>
    </Routes>
  );
}

export default App;
