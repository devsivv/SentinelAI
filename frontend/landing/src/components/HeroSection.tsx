import { ExternalLink, ChevronDown } from 'lucide-react';
import { motion } from 'framer-motion';
import SentinelAILogo from './SentinelAILogo';

const CITIZEN_URL = import.meta.env.VITE_CITIZEN_URL || '#';
const POLICE_URL = import.meta.env.VITE_POLICE_URL || '#';

const fadeUp = {
  hidden: { opacity: 0, y: 24 },
  show: (delay: number = 0) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: [0.22, 1, 0.36, 1], delay },
  }),
};

export default function HeroSection() {
  return (
    <section
      className="relative min-h-screen flex flex-col items-center justify-center pt-20 pb-16 px-4 sm:px-6 lg:px-8 overflow-hidden"
      aria-labelledby="hero-heading"
    >
      {/* Background layers */}
      <div className="absolute inset-0 bg-grid opacity-60 pointer-events-none" aria-hidden="true" />
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background:
            'radial-gradient(ellipse 80% 50% at 50% -10%, rgba(37,99,235,0.18) 0%, transparent 70%)',
        }}
        aria-hidden="true"
      />
      <div
        className="absolute bottom-0 left-0 right-0 h-64 pointer-events-none"
        style={{
          background: 'linear-gradient(to top, #0B1220, transparent)',
        }}
        aria-hidden="true"
      />

      {/* Floating orb accents */}
      <div
        className="absolute top-1/4 left-1/4 w-72 h-72 rounded-full pointer-events-none"
        style={{
          background: 'radial-gradient(circle, rgba(37,99,235,0.06) 0%, transparent 70%)',
          filter: 'blur(40px)',
        }}
        aria-hidden="true"
      />
      <div
        className="absolute bottom-1/4 right-1/4 w-96 h-96 rounded-full pointer-events-none"
        style={{
          background: 'radial-gradient(circle, rgba(124,58,237,0.06) 0%, transparent 70%)',
          filter: 'blur(60px)',
        }}
        aria-hidden="true"
      />

      {/* Content */}
      <div className="relative z-10 flex flex-col items-center text-center max-w-4xl mx-auto">
        {/* Status badge */}
        <motion.div
          variants={fadeUp}
          initial="hidden"
          animate="show"
          custom={0}
          className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-blue-500/30 bg-blue-500/8 text-blue-300 text-xs font-semibold tracking-widest uppercase mb-8"
        >
          <span className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-pulse" aria-hidden="true" />
          AI-Powered Cybercrime Intelligence
        </motion.div>

        {/* Logo — hero-sized */}
        <motion.div
          variants={fadeUp}
          initial="hidden"
          animate="show"
          custom={0.1}
          className="mb-8"
        >
          <SentinelAILogo size="xl" showIcon subtitle="Digital Safety Platform" />
        </motion.div>

        {/* Headline */}
        <motion.h1
          id="hero-heading"
          variants={fadeUp}
          initial="hidden"
          animate="show"
          custom={0.2}
          className="text-4xl sm:text-5xl lg:text-6xl font-extrabold leading-tight tracking-tight text-white mb-6"
        >
          AI-Powered{' '}
          <span className="gradient-text">Digital Safety</span>{' '}
          Platform
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          variants={fadeUp}
          initial="hidden"
          animate="show"
          custom={0.3}
          className="text-lg sm:text-xl text-gray-300 max-w-2xl leading-relaxed mb-10"
        >
          Protecting citizens, empowering investigators, and accelerating cybercrime
          intelligence through multi-agent artificial intelligence.
        </motion.p>

        {/* CTA Buttons */}
        <motion.div
          variants={fadeUp}
          initial="hidden"
          animate="show"
          custom={0.4}
          className="flex flex-col sm:flex-row items-center gap-4"
        >
          <motion.a
            href={CITIZEN_URL}
            target="_blank"
            rel="noopener noreferrer"
            whileHover={{ scale: 1.03, y: -2 }}
            whileTap={{ scale: 0.97 }}
            transition={{ type: 'spring', stiffness: 300, damping: 20 }}
            className="inline-flex items-center gap-2.5 px-8 py-4 rounded-xl text-base font-bold text-white bg-blue-600 hover:bg-blue-500 shadow-xl shadow-blue-900/40 transition-colors duration-200 min-h-[52px] w-full sm:w-auto justify-center focus-visible:outline-blue-500"
            aria-label="Open Citizen Portal in new tab"
          >
            Citizen Portal
            <ExternalLink className="h-4 w-4 opacity-80" aria-hidden="true" />
          </motion.a>

          <motion.a
            href={POLICE_URL}
            target="_blank"
            rel="noopener noreferrer"
            whileHover={{ scale: 1.03, y: -2 }}
            whileTap={{ scale: 0.97 }}
            transition={{ type: 'spring', stiffness: 300, damping: 20 }}
            className="inline-flex items-center gap-2.5 px-8 py-4 rounded-xl text-base font-bold text-white border border-blue-600/60 hover:border-blue-500 hover:bg-blue-600/10 transition-all duration-200 backdrop-blur-sm min-h-[52px] w-full sm:w-auto justify-center focus-visible:outline-blue-500"
            aria-label="Open Police Dashboard in new tab"
          >
            Police Dashboard
            <ExternalLink className="h-4 w-4 opacity-80" aria-hidden="true" />
          </motion.a>
        </motion.div>

        {/* Trust indicators */}
        <motion.div
          variants={fadeUp}
          initial="hidden"
          animate="show"
          custom={0.5}
          className="mt-14 flex flex-wrap items-center justify-center gap-6 sm:gap-10 text-xs text-gray-500 font-medium tracking-wide uppercase"
        >
          {['Multi-Agent AI', 'Real-Time Detection', 'Explainable Results', 'Law Enforcement Ready'].map((item) => (
            <span key={item} className="flex items-center gap-2">
              <span className="w-1 h-1 rounded-full bg-blue-500 shrink-0" aria-hidden="true" />
              {item}
            </span>
          ))}
        </motion.div>
      </div>

      {/* Scroll indicator */}
      <motion.a
        href="#overview"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.2, duration: 0.6 }}
        className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-1 text-gray-600 hover:text-gray-400 transition-colors focus-visible:outline-blue-500 rounded-md"
        aria-label="Scroll to Platform Overview"
      >
        <span className="text-xs font-medium tracking-widest uppercase">Explore</span>
        <motion.div
          animate={{ y: [0, 4, 0] }}
          transition={{ duration: 1.4, repeat: Infinity, ease: 'easeInOut' }}
        >
          <ChevronDown className="h-5 w-5" aria-hidden="true" />
        </motion.div>
      </motion.a>
    </section>
  );
}
