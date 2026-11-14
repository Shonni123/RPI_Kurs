import React from 'react';
import { TopNav } from './TopNav';

export const Navbar: React.FC = () => {
  return (
    <header className="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-sky-100/70 px-4 sm:px-8 lg:px-12 py-3 shadow-xs transition-colors">
      <TopNav theme="light" className="max-w-[1440px] mx-auto" />
    </header>
  );
};
