import { useState, useEffect } from 'react';
import { Menu, X, ExternalLink } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import SentinelAILogo from './SentinelAILogo';

const CITIZEN_URL = import.meta.env.VITE_CITIZEN_URL || '#';
const POLICE_URL = import.meta.env.VITE_POLICE_URL || '#';

const navLinks = [
  { label: 'Platform', href: '#overview' },
  { label: 'Capabilities', href: '#capabilities' },
  { label: 'Architecture', href: '#architecture' },
  { label: 'How It Works', href: '#how-it-works' },
  { label: 'About', href: '#about' },
];

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 16);
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Close mobile menu on resize to desktop
  useEffect(() => {
    const handleResize = () => { if (window.innerWidth >= 1024) setIsOpen(false); };
    window.addEventListener('resize', handleResize, { passive: true });
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const handleNavClick = () => setIsOpen(false);

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? 'bg-[#0B1220]/95 backdrop-blur-md border-b border-blue-900/30 shadow-lg shadow-blue-950/30'
          : 'bg-transparent'
      }`}
      role="banner"
    >
      <nav
        className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16 lg:h-18"
        aria-label="Main navigation"
      >
        {/* Logo */}
        <a href="#" aria-label="SentinelAI — Home" className="shrink-0 focus-visible:outline-blue-500 rounded-md">
          <SentinelAILogo size="md" showIcon />
        </a>

        {/* Desktop nav links */}
        <div className="hidden lg:flex items-center gap-7">
          {navLinks.map((link) => (
            <a
              key={link.label}
              href={link.href}
              className="text-sm font-medium text-gray-300 hover:text-white transition-colors duration-200 focus-visible:outline-blue-500 rounded-sm"
            >
              {link.label}
            </a>
          ))}
        </div>

        {/* Desktop CTAs */}
        <div className="hidden lg:flex items-center gap-3">
          <a
            href={CITIZEN_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-semibold text-white border border-blue-600/60 rounded-lg hover:bg-blue-600/10 hover:border-blue-500 transition-all duration-200 focus-visible:outline-blue-500"
            aria-label="Open Citizen Portal in new tab"
          >
            Citizen Portal
            <ExternalLink className="h-3.5 w-3.5 opacity-70" aria-hidden="true" />
          </a>
          <a
            href={POLICE_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-500 transition-all duration-200 shadow-lg shadow-blue-900/40 focus-visible:outline-blue-500"
            aria-label="Open Police Dashboard in new tab"
          >
            Police Dashboard
            <ExternalLink className="h-3.5 w-3.5 opacity-70" aria-hidden="true" />
          </a>
        </div>

        {/* Mobile hamburger */}
        <button
          type="button"
          onClick={() => setIsOpen((v) => !v)}
          className="lg:hidden inline-flex items-center justify-center h-11 w-11 rounded-lg text-gray-300 hover:text-white hover:bg-white/10 transition-colors focus-visible:outline-blue-500"
          aria-label={isOpen ? 'Close navigation menu' : 'Open navigation menu'}
          aria-expanded={isOpen}
          aria-controls="mobile-menu"
        >
          {isOpen ? <X className="h-5 w-5" aria-hidden="true" /> : <Menu className="h-5 w-5" aria-hidden="true" />}
        </button>
      </nav>

      {/* Mobile menu */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            id="mobile-menu"
            role="dialog"
            aria-modal="true"
            aria-label="Mobile navigation menu"
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.18, ease: 'easeOut' }}
            className="lg:hidden bg-[#0D1628]/98 backdrop-blur-xl border-b border-blue-900/30"
          >
            <div className="mx-auto max-w-7xl px-4 sm:px-6 py-4 space-y-1">
              {navLinks.map((link) => (
                <a
                  key={link.label}
                  href={link.href}
                  onClick={handleNavClick}
                  className="block px-4 py-3 text-sm font-medium text-gray-300 hover:text-white hover:bg-white/5 rounded-lg transition-colors"
                >
                  {link.label}
                </a>
              ))}
              <div className="pt-3 pb-1 flex flex-col gap-2.5 border-t border-white/10 mt-3">
                <a
                  href={CITIZEN_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  onClick={handleNavClick}
                  className="flex items-center justify-center gap-2 px-4 py-3 text-sm font-semibold text-white border border-blue-600/60 rounded-lg hover:bg-blue-600/10 transition-all"
                >
                  Citizen Portal <ExternalLink className="h-3.5 w-3.5 opacity-70" aria-hidden="true" />
                </a>
                <a
                  href={POLICE_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  onClick={handleNavClick}
                  className="flex items-center justify-center gap-2 px-4 py-3 text-sm font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-500 transition-all"
                >
                  Police Dashboard <ExternalLink className="h-3.5 w-3.5 opacity-70" aria-hidden="true" />
                </a>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}
