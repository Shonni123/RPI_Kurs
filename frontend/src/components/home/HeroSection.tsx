import React from 'react';
import { TopNav } from '../layout/TopNav';
import { IMAGES } from '../../assets/images';

export const HeroSection: React.FC = () => {
  return (
    <section className="relative min-h-screen flex flex-col justify-between overflow-hidden rounded-none shadow-2xl">
      {/* Background Plane Image directly from Figma (sharp, unrounded corners at bottom) */}
      <div className="absolute inset-0 z-0">
        <img
          src={IMAGES.heroPlane}
          alt="Авиарейсы онлайн — фон"
          className="w-full h-full object-cover object-center"
        />
      </div>

      {/* Top Bar: ≡ | Главная Посмотреть рейс О сервисе Как это работает | [-> ⚙ */}
      <header className="relative z-20 pt-5 sm:pt-6 px-6 sm:px-10 lg:px-14 w-full">
        <TopNav theme="dark" className="max-w-[1440px] mx-auto" />
      </header>

      {/* Bottom Content: online + АВИАРЕЙСЫ and 4+ Frosted Card */}
      <div className="relative z-20 w-full max-w-[1440px] mx-auto px-6 sm:px-10 lg:px-14 flex flex-col xl:flex-row items-end justify-between gap-6 pb-6 sm:pb-8 lg:pb-10 pt-8">
        
        {/* Main Title Group: Combined vector of online in High Summit font + АВИАРЕЙСЫ in Benzin with exact spacing */}
        <div className="relative w-full max-w-[940px] select-none">
          <img
            src="/assets/hero_title_combined.svg"
            alt="АВИАРЕЙСЫ online"
            className="w-full h-auto drop-shadow-2xl"
          />
        </div>

        {/* Right Badge Widget: HTML Frosted Glass matching Figma exactly */}
        <div
          className="w-[301px] h-[171px] rounded-[22px] backdrop-blur-md border border-white/30 p-5 shadow-2xl flex flex-col justify-between flex-shrink-0 self-start xl:self-end mb-2 transition-all hover:bg-white/[0.22]"
          style={{ backgroundColor: 'rgba(209, 209, 209, 0.24)' }}
        >
          <div className="flex items-center justify-between gap-3">
            <span className="font-sans font-light italic text-[60px] leading-none text-white tracking-tight pl-0.5 select-none">
              4+
            </span>
            <div className="flex items-center -space-x-2.5">
              <img
                src={IMAGES.avatar1}
                alt="Пользователь 1"
                className="w-9 h-9 rounded-full object-cover ring-1 ring-white/25 shadow-sm"
              />
              <img
                src={IMAGES.avatar2}
                alt="Пользователь 2"
                className="w-9 h-9 rounded-full object-cover ring-1 ring-white/25 shadow-sm"
              />
              <img
                src={IMAGES.avatar3}
                alt="Пользователь 3"
                className="w-9 h-9 rounded-full object-cover ring-1 ring-white/25 shadow-sm"
              />
              <div className="w-9 h-9 rounded-full bg-white/[0.25] backdrop-blur-sm border border-white/30 flex items-center justify-center text-white ring-1 ring-white/20 shadow-sm">
                <svg
                  className="w-3.5 h-3.5 stroke-white"
                  viewBox="0 0 12 12"
                  fill="none"
                  strokeWidth="1.6"
                  strokeLinecap="round"
                >
                  <line x1="6" y1="2" x2="6" y2="10" />
                  <line x1="2" y1="6" x2="10" y2="6" />
                </svg>
              </div>
            </div>
          </div>

          <div className="text-white/75 text-[13.5px] leading-[1.38] font-light italic tracking-normal pl-0.5 select-none">
            <p>Отслеживаем рейсы с 2021 года.</p>
            <p>Присоединяйтесь к тысячам</p>
            <p>пользователей!</p>
          </div>
        </div>

      </div>
    </section>
  );
};
