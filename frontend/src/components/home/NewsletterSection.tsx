import React, { useState } from 'react';
import { TopNav } from '../layout/TopNav';

export const NewsletterSection: React.FC = () => {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !email.includes('@')) return;
    setSubmitted(true);
    setEmail('');
  };

  return (
    <section id="newsletter" className="pt-2 sm:pt-3 pb-12 sm:pb-16 px-4 sm:px-6 lg:px-8 xl:px-10 bg-white text-slate-900 w-full overflow-hidden scroll-mt-6">
      <div className="w-full max-w-[1364px] mx-auto space-y-6 sm:space-y-8">
        
        {/* Top Header matching other sections in light theme */}
        <header className="w-full">
          <TopNav theme="light" />
        </header>

        {/* Newsletter Card matching Figma exactly */}
        <div className="w-full max-w-[1240px] xl:max-w-[1243px] mx-auto">
          <div className="relative w-full rounded-[33px] bg-[#F8FCFF] border border-[#E2EEF8] overflow-hidden min-h-[420px] sm:min-h-[453px] flex flex-col items-center justify-between pt-10 sm:pt-11 pb-10 sm:pb-12 px-6 sm:px-10 select-none">
            
            {/* Background concentric dome arches from Figma (Ellipse 17 & 16) */}
            <div className="absolute inset-0 overflow-hidden pointer-events-none select-none">
              <div
                className="absolute left-1/2 -translate-x-1/2 rounded-full"
                style={{
                  width: '848px',
                  height: '848px',
                  top: '156px',
                  backgroundColor: '#EFF7FE',
                }}
              />
              <div
                className="absolute left-1/2 -translate-x-1/2 rounded-full"
                style={{
                  width: '679px',
                  height: '679px',
                  top: '233px',
                  backgroundColor: '#E5F0FF',
                }}
              />
            </div>

            {/* 4 Floating Circular Photo Bubbles from Figma */}
            {/* 1. Top-Left: Mountain in pink/morning clouds */}
            <div className="hidden lg:block absolute left-[140px] xl:left-[150px] top-[85px] xl:top-[87px] w-[68px] h-[68px] rounded-full overflow-hidden shadow-sm pointer-events-none select-none z-10">
              <img src="/assets/newsletter_bubble_1.jpg" alt="Горы" className="w-full h-full object-cover" />
            </div>

            {/* 2. Bottom-Left: Airplane on wet tarmac */}
            <div className="hidden lg:block absolute left-[35px] xl:left-[39px] top-[165px] xl:top-[171px] w-[110px] h-[110px] rounded-full overflow-hidden shadow-sm pointer-events-none select-none z-10">
              <img src="/assets/newsletter_bubble_2.jpg" alt="Самолёт на взлётной полосе" className="w-full h-full object-cover" />
            </div>

            {/* 3. Top-Right: Person walking to airplane */}
            <div className="hidden lg:block absolute right-[140px] xl:right-[150px] top-[85px] xl:top-[87px] w-[68px] h-[68px] rounded-full overflow-hidden shadow-sm pointer-events-none select-none z-10">
              <img src="/assets/newsletter_bubble_3.jpg" alt="Пассажир" className="w-full h-full object-cover" />
            </div>

            {/* 4. Bottom-Right: Airport lounge terminal seats */}
            <div className="hidden lg:block absolute right-[35px] xl:right-[40px] top-[165px] xl:top-[171px] w-[110px] h-[110px] rounded-full overflow-hidden shadow-sm pointer-events-none select-none z-10">
              <img src="/assets/newsletter_bubble_4.jpg" alt="Зал ожидания" className="w-full h-full object-cover" />
            </div>

            {/* Title & Subtitle */}
            <div className="relative z-10 text-center w-full max-w-[840px] mx-auto space-y-3">
              <h2 className="font-benzin-medium text-[18px] sm:text-[23px] md:text-[26px] lg:text-[29.5px] uppercase tracking-normal text-slate-950 leading-tight whitespace-normal md:whitespace-nowrap">
                ПОДПИШИТЕСЬ НА НАШУ РАССЫЛКУ
              </h2>
              <p className="text-slate-700 text-xs sm:text-[14.8px] leading-[1.3] font-tt-travels font-normal max-w-[460px] mx-auto">
                Получайте уведомления о задержках, новые функции и<br className="hidden sm:inline" /> советы для путешественников
              </p>
            </div>

            {/* Pill Form: 467 x 62 with black button matching Figma */}
            <div className="relative z-10 w-full flex justify-center mt-8 sm:mt-12">
              {submitted ? (
                <div className="w-full max-w-[467px] h-[58px] sm:h-[62px] bg-white rounded-full shadow-md px-6 flex items-center justify-center text-emerald-700 text-xs sm:text-sm font-semibold border border-emerald-300">
                  Спасибо! Вы успешно подписаны.
                </div>
              ) : (
                <form
                  onSubmit={handleSubmit}
                  className="w-full max-w-[467px] h-[58px] sm:h-[62px] bg-white rounded-full shadow-sm pl-5 sm:pl-6 pr-1.5 py-1.5 flex items-center justify-between border border-slate-200/60"
                >
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Ваш email..."
                    required
                    className="flex-1 bg-transparent text-slate-900 placeholder:text-slate-400 text-sm sm:text-base focus:outline-none pr-3 font-sans"
                  />
                  <button
                    type="submit"
                    className="h-[48px] sm:h-[52px] px-6 sm:px-7 rounded-full bg-black hover:bg-slate-900 text-white font-medium text-sm sm:text-[15px] transition-all whitespace-nowrap flex items-center justify-center cursor-pointer"
                  >
                    Подписаться
                  </button>
                </form>
              )}
            </div>

          </div>
        </div>

      </div>
    </section>
  );
};
