import React from 'react';
import { HeroSection } from '../components/home/HeroSection';
import { WhyUsSection } from '../components/home/WhyUsSection';
import { FeaturesGridSection } from '../components/home/FeaturesGridSection';
import { ComparisonSection } from '../components/home/ComparisonSection';
import { StatsSection } from '../components/home/StatsSection';
import { NewsletterSection } from '../components/home/NewsletterSection';
import { FaqAccordion } from '../components/home/FaqAccordion';

export const HomePage: React.FC = () => {
  return (
    <main className="w-full">
      <HeroSection />
      <WhyUsSection />
      <FeaturesGridSection />
      <ComparisonSection />
      <StatsSection />
      <NewsletterSection />
      <FaqAccordion />
    </main>
  );
};

