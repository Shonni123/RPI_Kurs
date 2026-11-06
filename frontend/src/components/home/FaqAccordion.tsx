import React, { useState } from 'react';
import { Plus, Minus } from 'lucide-react';

interface FaqItem {
  id: number;
  question: string;
  answer: string;
}

const FAQ_DATA: FaqItem[] = [
  {
    id: 1,
    question: 'КАК РАБОТАЕТ ОТСЛЕЖИВАНИЕ РЕЙСОВ?',
    answer:
      'Мы получаем данные напрямую от аэропортов и авиакомпаний. Информация обновляется каждые 15 секунд — вы видите точное местоположение самолёта, статус рейса, высоту полёта и погоду в аэропорту.',
  },
  {
    id: 2,
    question: 'МОЖНО ЛИ ИСПОЛЬЗОВАТЬ СЕРВИС БЕСПЛАТНО?',
    answer:
      'Да, базовый функционал поиска и отслеживания рейсов полностью бесплатен для всех пользователей. Мы предоставляем актуальную информацию без скрытых комиссий и обязательных подписок.',
  },
  {
    id: 3,
    question: 'МОЖНО ЛИ ИСПОЛЬЗОВАТЬ СЕРВИС БЕЗ ИНТЕРНЕТА?',
    answer:
      'Базовые функции просмотра сохранённых рейсов доступны офлайн из кэша. Для обновления статусов и перемещений самолётов в реальном времени требуется подключение к сети.',
  },
];

export const FaqAccordion: React.FC = () => {
  const [openIds, setOpenIds] = useState<number[]>([1]);

  const toggle = (id: number) => {
    setOpenIds((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  return (
    <section className="pt-4 sm:pt-6 pb-20 sm:pb-24 px-4 sm:px-6 lg:px-8 xl:px-10 bg-white text-slate-900 w-full overflow-hidden">
      <div className="w-full max-w-[1240px] xl:max-w-[1243px] mx-auto space-y-6 sm:space-y-8 select-none">
        
        {/* Title matching Figma in Benzin font */}
        <div className="text-center">
          <h2 className="font-benzin-medium text-[24px] sm:text-[28px] lg:text-[30px] uppercase tracking-normal text-slate-950">
            FAQ
          </h2>
        </div>

        {/* 3 Accordion items matching Figma */}
        <div className="space-y-3 sm:space-y-3.5">
          {FAQ_DATA.map((item) => {
            const isOpen = openIds.includes(item.id);
            return (
              <div
                key={item.id}
                className="rounded-[19px] sm:rounded-[20px] bg-[#F8FCFF] border border-[#E2EEF8] overflow-hidden transition-all duration-200"
              >
                <button
                  type="button"
                  onClick={() => toggle(item.id)}
                  className="w-full px-6 sm:px-8 py-5 sm:py-6 text-left flex items-center justify-between gap-4 cursor-pointer focus:outline-none"
                >
                  <span
                    className="font-benzin-bold text-[12px] sm:text-[14px] lg:text-[15px] tracking-[0.05em] uppercase text-[#4F566B]"
                    style={{ fontFamily: "'Benzin-Bold', 'Benzin', sans-serif" }}
                  >
                    {item.question}
                  </span>

                  {/* Compact circle toggle button matching Figma (~38px with clean icon) */}
                  <div
                    className="w-[36px] h-[36px] sm:w-[38px] sm:h-[38px] rounded-full bg-[#DFEDF8] hover:bg-[#D4E8F5] text-slate-900 flex items-center justify-center transition-colors flex-shrink-0"
                  >
                    {isOpen ? (
                      <Minus className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-slate-900" strokeWidth={2.2} />
                    ) : (
                      <Plus className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-slate-900" strokeWidth={2.2} />
                    )}
                  </div>
                </button>

                {isOpen && (
                  <div
                    className="px-6 sm:px-8 pb-6 pt-0 text-slate-600 text-xs sm:text-[14px] leading-relaxed font-montserrat-alt animate-fadeIn"
                    style={{ fontFamily: "'Montserrat Alternates', sans-serif" }}
                  >
                    {item.answer}
                  </div>
                )}
              </div>
            );
          })}
        </div>

      </div>
    </section>
  );
};
