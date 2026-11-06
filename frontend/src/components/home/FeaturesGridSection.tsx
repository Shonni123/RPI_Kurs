import React from 'react';
import { IMAGES } from '../../assets/images';
import { TopNav } from '../layout/TopNav';

export const FeaturesGridSection: React.FC = () => {
  const features = [
    {
      id: 1,
      title: (
        <>
          УПРАВЛЯЙТЕ<br />ПОЛЁТОМ
        </>
      ),
      desc: (
        <>
          Настройте уведомления, выберите<br />
          нужные рейсы и получайте только<br />
          ту информацию, которая важна<br />
          именно вам.
        </>
      ),
      iconSrc: '/assets/benefit_icon_1.png',
    },
    {
      id: 2,
      title: (
        <>
          БЫСТРО И<br />НАДЁЖНО
        </>
      ),
      desc: (
        <>
          Данные обновляются каждые 15<br />
          секунд. Никаких задержек, никаких<br />
          ошибок — только точная информация<br />
          в режиме реального времени.
        </>
      ),
      iconSrc: '/assets/benefit_icon_2.png',
    },
    {
      id: 3,
      title: (
        <>
          УМНЫЙ<br />ИНТЕРФЕЙС
        </>
      ),
      desc: (
        <>
          Система сама анализирует данные и<br />
          предлагает вам лучшие варианты —<br />
          от оптимального времени вылета до<br />
          лучших мест в аэропорту.
        </>
      ),
      iconSrc: '/assets/benefit_icon_3.png',
    },
    {
      id: 4,
      title: (
        <>
          БЕЗОПАСНОСТЬ<br />ДАННЫХ
        </>
      ),
      desc: (
        <>
          Ваши личные данные защищены. Мы не<br />
          передаём их третьим лицам и не<br />
          используем для рекламы.
        </>
      ),
      iconSrc: '/assets/benefit_icon_4.png',
    },
  ];

  return (
    <section id="features" className="pt-3 sm:pt-4 pb-6 sm:pb-8 px-4 sm:px-6 lg:px-8 xl:px-10 bg-white text-slate-900 scroll-mt-6">
      <div className="w-full max-w-[1364px] mx-auto">
        
        {/* Top Header matching Figma in light theme */}
        <header className="w-full">
          <TopNav theme="light" />
        </header>

        {/* Title matching Figma in Benzin-Bold font */}
        <div className="select-none mt-2.5 sm:mt-3 mb-4 sm:mb-5">
          <h2
            className="text-[22px] sm:text-[26px] lg:text-[32px] tracking-tight uppercase text-slate-950 leading-tight"
            style={{ fontFamily: "'Benzin-Bold', sans-serif", fontWeight: 700 }}
          >
            ВАШ ПОЛЁТ — ПОД КОНТРОЛЕМ
          </h2>
        </div>

        {/* 2-column layout: Left authentic airplane image, Right 2x2 grid (1:1 split, comfortably filling viewport) */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 sm:gap-6 items-stretch lg:h-[555px] xl:h-[585px]">
          
          {/* Left: Authentic Airplane on Wet Tarmac from Figma */}
          <div className="relative h-[340px] sm:h-[450px] lg:h-full rounded-[28px] sm:rounded-[32px] overflow-hidden group">
            <img
              src={IMAGES.controlPlane}
              alt="Самолёт на мокром перроне"
              className="w-full h-full object-cover rounded-[28px] sm:rounded-[32px] group-hover:scale-105 transition-transform duration-700"
            />
          </div>

          {/* Right: 2x2 Grid with Light Ice-Blue Cards & Authentic Figma Graphics */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5 sm:gap-6 h-full">
            {features.map((item) => (
              <div
                key={item.id}
                className="pt-6 sm:pt-7 px-5 sm:px-6 pb-4 sm:pb-5 rounded-[28px] sm:rounded-[32px] bg-[#F8FCFF] border border-[#E4ECF5] hover:border-blue-300 transition-all duration-300 flex flex-col justify-between"
              >
                <div>
                  {/* Title Container: Locked exact height so titles are on the exact same horizontal level */}
                  <div className="h-[46px] sm:h-[48px] flex flex-col justify-start">
                    <h3
                      className="text-[15px] sm:text-[16px] lg:text-[17px] uppercase tracking-normal text-[#161C30] leading-[21px] sm:leading-[23px]"
                      style={{ fontFamily: "'Benzin-Bold', sans-serif", fontWeight: 700 }}
                    >
                      {item.title}
                    </h3>
                  </div>

                  {/* Description Container: Locked exact height so description text starts at the exact same horizontal level */}
                  <div className="mt-3 sm:mt-3.5 h-[66px] sm:h-[70px] flex flex-col justify-start">
                    <p
                      className="text-[11.5px] sm:text-[12px] lg:text-[12.5px] text-[#565A74] leading-[16.5px] sm:leading-[17.5px] font-normal not-italic"
                      style={{ fontFamily: "'Montserrat Alternates', sans-serif", fontWeight: 400 }}
                    >
                      {item.desc}
                    </p>
                  </div>
                </div>

                {/* Authentic Figma Blue Line-Art Graphic: Aligned to bottom */}
                <div className="mt-auto pt-2 flex items-end justify-start h-[100px] sm:h-[115px]">
                  <img
                    src={item.iconSrc}
                    alt=""
                    className="h-[85px] sm:h-[100px] lg:h-[108px] w-auto object-contain pointer-events-none select-none"
                  />
                </div>
              </div>
            ))}
          </div>

        </div>

      </div>
    </section>
  );
};
