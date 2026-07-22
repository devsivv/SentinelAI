import { lazy, Suspense } from 'react';
import Navbar from './components/Navbar';
import HeroSection from './components/HeroSection';
import Footer from './components/Footer';

// Lazy-load below-the-fold sections for performance
const PlatformOverview = lazy(() => import('./components/PlatformOverview'));
const CapabilitiesSection = lazy(() => import('./components/CapabilitiesSection'));
const ArchitectureSection = lazy(() => import('./components/ArchitectureSection'));
const TechStackSection = lazy(() => import('./components/TechStackSection'));
const HowItWorksSection = lazy(() => import('./components/HowItWorksSection'));
const PortalSelection = lazy(() => import('./components/PortalSelection'));
const AboutSection = lazy(() => import('./components/AboutSection'));
const TeamSection = lazy(() => import('./components/TeamSection'));

function SectionFallback() {
  return (
    <div className="w-full py-24 flex items-center justify-center">
      <div className="w-6 h-6 rounded-full border-2 border-blue-500 border-t-transparent animate-spin" aria-label="Loading section" />
    </div>
  );
}

export default function App() {
  return (
    <div className="min-h-screen bg-[#0B1220] text-white overflow-x-hidden">
      <Navbar />
      <main id="main-content">
        <HeroSection />
        <Suspense fallback={<SectionFallback />}>
          <PlatformOverview />
        </Suspense>
        <Suspense fallback={<SectionFallback />}>
          <CapabilitiesSection />
        </Suspense>
        <Suspense fallback={<SectionFallback />}>
          <ArchitectureSection />
        </Suspense>
        <Suspense fallback={<SectionFallback />}>
          <TechStackSection />
        </Suspense>
        <Suspense fallback={<SectionFallback />}>
          <HowItWorksSection />
        </Suspense>
        <Suspense fallback={<SectionFallback />}>
          <PortalSelection />
        </Suspense>
        <Suspense fallback={<SectionFallback />}>
          <AboutSection />
        </Suspense>
        <Suspense fallback={<SectionFallback />}>
          <TeamSection />
        </Suspense>
      </main>
      <Footer />
    </div>
  );
}
