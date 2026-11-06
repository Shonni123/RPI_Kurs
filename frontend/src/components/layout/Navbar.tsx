import React from 'react';
import { useLocation } from 'react-router-dom';
import { TopNav } from './TopNav';

export const Navbar: React.FC = () => {
  const location = useLocation();

  // On HomePage, HeroSection and WhyUsSection have their own integrated headers matching Figma frames
  if (location.pathname === '/') {
    return null;
  }

  return (
    <header className="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-slate-100 px-4 sm:px-8 py-3.5 shadow-sm">
      <TopNav theme="light" />
    </header>
  );
};
