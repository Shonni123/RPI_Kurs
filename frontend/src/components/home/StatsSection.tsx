import React from 'react';
import { Plus } from 'lucide-react';
import { IMAGES } from '../../assets/images';
import { TopNav } from '../layout/TopNav';

export const StatsSection: React.FC = () => {
  return (
    <section id="stats" className="pt-8 sm:pt-10 lg:pt-12 pb-6 sm:pb-8 px-4 sm:px-6 lg:px-8 xl:px-10 bg-white text-slate-900 overflow-hidden scroll-mt-6">
      <div className="w-full max-w-[1364px] mx-auto space-y-6 sm:space-y-8">
        
        {/* Top Header matching Figma in light theme */}
        <header className="w-full">
          <TopNav theme="light" />
        </header>

        {/* Massive "FLIGHTS" typography cutout with airplane flying out matching Figma */}
        <div className="mt-4 sm:mt-5 lg:mt-6 mb-5 sm:mb-7 w-full max-w-[1240px] xl:max-w-[1280px] mx-auto select-none">
          <img
            src="/assets/flights_title_figma.png?v=3"
            alt="FLIGHTS"
            className="w-full h-auto object-contain pointer-events-none select-none"
          />
        </div>

        {/* 2 Column Stats & Visual Showcase: aligned with FLIGHTS banner */}
        <div className="w-full max-w-[1240px] xl:max-w-[1280px] mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 xl:gap-12 items-center w-full">
            
            {/* Left Column: Metrics & Avatars exactly matching Figma */}
            <div className="lg:col-span-7 space-y-5 sm:space-y-6">
              
              {/* Title & Subtitle */}
              <div className="space-y-1.5 sm:space-y-2">
                <h3 className="font-tt-travels font-bold text-xl sm:text-2xl lg:text-[26px] text-slate-900 leading-tight">
                  Ваш полёт — под контролем.
                </h3>
                <p className="text-xs sm:text-[13px] text-slate-600 font-montserrat-alt leading-relaxed max-w-[500px]">
                  Мы создали сервис, который помогает<br className="hidden sm:inline" /> пассажирам не терять самолёты из вида.
                </p>
              </div>

              {/* Avatars with '+' circle and 'Связаться с нами' below */}
              <div className="space-y-2 pt-0.5">
                <div className="flex -space-x-3 items-center">
                  <img src={IMAGES.avatar1} alt="Аватар 1" className="w-10 h-10 sm:w-11 sm:h-11 rounded-full border-2 border-white object-cover shadow-sm" />
                  <img src={IMAGES.avatar2} alt="Аватар 2" className="w-10 h-10 sm:w-11 sm:h-11 rounded-full border-2 border-white object-cover shadow-sm" />
                  <img src={IMAGES.avatar3} alt="Аватар 3" className="w-10 h-10 sm:w-11 sm:h-11 rounded-full border-2 border-white object-cover shadow-sm" />
                  <div className="w-10 h-10 sm:w-11 sm:h-11 rounded-full border border-slate-300/80 bg-white shadow-sm flex items-center justify-center text-slate-700">
                    <Plus className="w-4 h-4 text-slate-700" strokeWidth={1.5} />
                  </div>
                </div>
                <div>
                  <span className="text-xs sm:text-[13px] font-medium text-slate-800 font-montserrat-alt">
                    Связаться с нами
                  </span>
                </div>
              </div>

              {/* 3 Metrics: Horizontal Inline Rows matching Figma with Benzin Medium */}
              <div className="space-y-3.5 sm:space-y-4 pt-1 max-w-[680px]">
                
                {/* Metric 1: 1K+ */}
                <div className="border-b border-slate-100 pb-3 sm:pb-3.5 flex items-center">
                  <div className="w-[145px] sm:w-[170px] flex-shrink-0">
                    <span className="font-benzin-medium text-3xl sm:text-4xl text-slate-950 inline-block scale-x-[1.12] origin-left">
                      1K+
                    </span>
                  </div>
                  <p className="text-xs sm:text-[12.5px] text-slate-600 font-montserrat-alt leading-[1.35]">
                    Пользователей ежедневно<br />отслеживают свои рейсы.
                  </p>
                </div>

                {/* Metric 2: 64% */}
                <div className="border-b border-slate-100 pb-3 sm:pb-3.5 flex items-center">
                  <div className="w-[145px] sm:w-[170px] flex-shrink-0">
                    <span className="font-benzin-medium text-3xl sm:text-4xl text-slate-950 inline-block scale-x-[1.12] origin-left">
                      64%
                    </span>
                  </div>
                  <p className="text-xs sm:text-[12.5px] text-slate-600 font-montserrat-alt leading-[1.35]">
                    Уменьшение стресса у пользователей<br />при задержках рейсов.
                  </p>
                </div>

                {/* Metric 3: 348 */}
                <div className="border-b border-slate-100 pb-3 sm:pb-3.5 flex items-center">
                  <div className="w-[145px] sm:w-[170px] flex-shrink-0">
                    <span className="font-benzin-medium text-3xl sm:text-4xl text-slate-950 inline-block scale-x-[1.12] origin-left">
                      348
                    </span>
                  </div>
                  <p className="text-xs sm:text-[12.5px] text-slate-600 font-montserrat-alt leading-[1.35]">
                    Рейсов отслеживается в реальном<br />времени каждую минуту.
                  </p>
                </div>

              </div>

            </div>

            {/* Right Column: Terminal Board Photo Card (near-square matching Figma) */}
            <div className="lg:col-span-5 flex justify-center lg:justify-end w-full">
              <div className="relative w-full max-w-[500px] xl:max-w-[520px] aspect-[1.12/1] rounded-[26px] sm:rounded-[30px] overflow-hidden shadow-xl border border-slate-100 bg-slate-900 select-none">
                <img
                  src={IMAGES.airportLoungeView}
                  alt="Зал аэропорта с табло рейсов"
                  className="w-full h-full object-cover object-center pointer-events-none select-none"
                />
                
                {/* Action buttons at bottom matching header pill size */}
                <div className="absolute bottom-3 sm:bottom-3.5 left-3 sm:left-3.5 right-3 sm:right-3.5 flex items-center justify-between pointer-events-auto">
                  <a
                    href="#contact"
                    className="inline-flex items-center justify-center rounded-full bg-white text-slate-900 font-semibold shadow-sm backdrop-blur-md font-montserrat-alt transition-none whitespace-nowrap"
                    style={{ height: '32px', fontSize: '12px', paddingLeft: '16px', paddingRight: '16px', lineHeight: '1' }}
                  >
                    Связаться с нами
                  </a>

                  <button
                    type="button"
                    aria-label="Справка"
                    className="rounded-full bg-white text-slate-900 font-bold flex items-center justify-center shadow-sm backdrop-blur-md transition-none"
                    style={{ width: '32px', height: '32px', fontSize: '13px', lineHeight: '1' }}
                  >
                    ?
                  </button>
                </div>
              </div>
            </div>

          </div>
        </div>

      </div>
    </section>
  );
};