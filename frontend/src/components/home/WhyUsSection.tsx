import React, { useRef } from 'react';
import { ArrowUpRight, ArrowRight, ChevronRight } from 'lucide-react';
import { IMAGES } from '../../assets/images';
import { Link } from 'react-router-dom';
import { TopNav } from '../layout/TopNav';

export const WhyUsSection: React.FC = () => {
  const scrollRef = useRef<HTMLDivElement>(null);

  const cards = [
    {
      id: 1,
      title: (
        <>
          В РЕАЛЬНОМ<br />ВРЕМЕНИ
        </>
      ),
      desc: (
        <>
          Следите за любым рейсом — от вылета до<br className="hidden lg:inline" />
          {' '}посадки. Точное местоположение, высота,<br className="hidden lg:inline" />
          {' '}скорость и статус обновляются каждые 15 секунд.
        </>
      ),
      image: IMAGES.why1RealTime,
      isRightArrow: true, // Card 1 has horizontal right arrow → in Figma
      isWide: true, // Card 1 is ~1.61x wider than cards 2-4 in Figma (460px vs 285px)
      link: '/flights',
    },
    {
      id: 2,
      title: (
        <>
          ДЛЯ<br />ВСЕХ
        </>
      ),
      desc: (
        <>
          Путешествуете сами,<br />
          встречаете близких или<br />
          планируете командировку.
        </>
      ),
      image: IMAGES.why2ForAll,
      isRightArrow: false, // Card 2 has diagonal ↗ arrow in Figma
      isWide: false,
      link: '/flights',
    },
    {
      id: 3,
      title: (
        <>
          БЕЗ<br />РЕКЛАМЫ
        </>
      ),
      desc: (
        <>
          Никаких баннеров,<br />
          всплывающих окон — только<br />
          нужная информация.
        </>
      ),
      image: IMAGES.why3NoAds,
      isRightArrow: false, // Card 3 has diagonal ↗ arrow in Figma
      isWide: false,
      link: '/about',
    },
    {
      id: 4,
      title: (
        <>
          НАДЁЖНЫЕ<br />ДАННЫЕ
        </>
      ),
      desc: (
        <>
          Информация поступает<br />
          напрямую от аэропортов и<br />
          авиакомпаний.
        </>
      ),
      image: IMAGES.why4Reliable,
      isRightArrow: false, // Card 4 has diagonal ↗ arrow in Figma
      isWide: false,
      link: '/airports',
    },
  ];

  return (
    <section id="why-us" className="pt-6 sm:pt-8 pb-3 sm:pb-4 px-4 sm:px-6 lg:px-8 xl:px-10 bg-white text-slate-900 w-full overflow-hidden">
      <div className="w-full max-w-[1364px] mx-auto">
        
        {/* Top Header matching Figma in light theme */}
        <header className="w-full">
          <TopNav theme="light" />
        </header>

        {/* Section Title matching Figma in Benzin-Medium - tight spacing to header */}
        <div className="select-none mt-2 sm:mt-2.5">
          <h2
            className="text-[22px] sm:text-[28px] lg:text-[34px] font-medium tracking-tight text-slate-950 uppercase leading-tight font-benzin"
            style={{ fontFamily: "'Benzin-Bold', 'Benzin-Medium', 'Benzin', sans-serif" }}
          >
            ПОЧЕМУ ВЫБИРАЮТ НАС?
          </h2>
        </div>

        {/* 4 Cards Grid: Card 1 is 1.614x wider (460px vs 285px in Figma 1364px canvas) */}
        <div
          ref={scrollRef}
          className="mt-5 sm:mt-6 flex lg:grid lg:grid-cols-[1.614fr_1fr_1fr_1fr] gap-4 overflow-x-auto lg:overflow-visible pb-4 lg:pb-0 scrollbar-none"
        >
          {cards.map((card) => (
            <div
              key={card.id}
              className={`group relative h-[609px] rounded-[36px] overflow-hidden shadow-xl flex-shrink-0 transition-transform duration-300 ${
                card.isWide
                  ? 'w-[360px] sm:w-[420px] lg:w-auto'
                  : 'w-[260px] sm:w-[285px] lg:w-auto'
              }`}
            >
              {/* Background Photo from Figma */}
              <div className="absolute inset-0 z-0">
                <img
                  src={card.image}
                  alt="Преимущество сервиса"
                  className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
                />
                {/* Soft natural vignette matching Figma - keeping tarmac, plane, and lights bright and clear */}
                <div className="absolute inset-0 bg-gradient-to-t from-black/65 via-black/20 to-transparent" />
              </div>

              {/* Top-Right Arrow Circle: Frosted translucent glass on ALL cards (no white hover on card 3) */}
              <div className="absolute top-6 right-6 z-10">
                <div className="w-[50px] h-[50px] rounded-full bg-black/40 backdrop-blur-md border border-white/20 flex items-center justify-center text-white transition-all shadow-md group-hover:scale-105">
                  {card.isRightArrow ? (
                    <ArrowRight className="w-5 h-5 text-white stroke-[2]" />
                  ) : (
                    <ArrowUpRight className="w-5 h-5 text-white stroke-[2]" />
                  )}
                </div>
              </div>

              {/* Bottom Content Container - Locked vertical levels across all 4 cards */}
              <div className="absolute inset-x-0 bottom-0 z-10 px-5 sm:px-6 pb-[30px] flex flex-col justify-end">
                {/* Titles in Benzin: exactly 2 lines at identical horizontal level */}
                <div className="h-[64px] flex flex-col justify-end">
                  <h3
                    className="font-benzin text-[21px] sm:text-[23px] lg:text-[25px] font-bold uppercase text-white leading-[27px] sm:leading-[29px] tracking-normal"
                    style={{ fontFamily: "'Benzin-Bold', 'Benzin-Medium', 'Benzin', sans-serif" }}
                  >
                    {card.title}
                  </h3>
                </div>

                {/* Description: Montserrat Alternates matching Figma */}
                <div className="h-[64px] mt-3.5 flex items-start">
                  <p
                    className="font-montserrat-alt text-[12.5px] sm:text-[13px] text-white/90 leading-[19px] sm:leading-[20px] font-normal not-italic tracking-normal"
                    style={{ fontFamily: "'Montserrat Alternates', sans-serif" }}
                  >
                    {card.desc}
                  </p>
                </div>

                {/* Full-width White Pill Button matching Figma */}
                <div className="mt-5">
                  <Link
                    to={card.link}
                    className="flex items-center justify-between w-full h-[48px] bg-white hover:bg-slate-100 text-slate-900 font-semibold text-xs sm:text-sm px-6 rounded-full transition-all shadow-md group-hover:shadow-lg cursor-pointer"
                  >
                    <span>Подробнее</span>
                    <ChevronRight className="w-4 h-4 text-slate-600 stroke-[2.2]" />
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
};
