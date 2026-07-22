import { useState, useCallback } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';
import Footer from './Footer';

export default function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const openSidebar = useCallback(() => setSidebarOpen(true), []);
  const closeSidebar = useCallback(() => setSidebarOpen(false), []);

  return (
    <div className="flex h-screen overflow-hidden bg-[#0B1220] text-white">
      {/* Sidebar — fixed on lg, off-canvas drawer on smaller screens */}
      <Sidebar isOpen={sidebarOpen} onClose={closeSidebar} />

      {/* Main content area */}
      <div className="flex flex-1 flex-col overflow-hidden min-w-0 bg-[#0B1220]">
        <Header onMenuClick={openSidebar} />
        <main
          className="flex-1 overflow-y-auto flex flex-col justify-between bg-[#0B1220]"
          id="main-content"
          aria-label="Main content"
        >
          <div className="mx-auto max-w-7xl w-full p-4 sm:p-6 lg:p-8">
            <Outlet />
          </div>
          <Footer />
        </main>
      </div>
    </div>
  );
}
