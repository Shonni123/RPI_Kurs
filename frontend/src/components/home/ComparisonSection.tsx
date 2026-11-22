import React, { useState } from 'react';
import { Check, X, Minus, ArrowRight, Sparkles, Shield, Zap, Eye, Bell, Compass } from 'lucide-react';
import { Link } from 'react-router-dom';

interface ComparisonFeature {
  id: string;
  category: string;
  name: string;
  description: string;
  icon: React.ElementType;
  ourService: {
    status: 'full' | 'partial' | 'none';
    label: string;
    detail?: string;
  };
  flightradar: {
    status: 'full' | 'partial' | 'none';
    label: string;
    detail?: string;
  };
  flightaware: {
    status: 'full' | 'partial' | 'none';
    label: string;
    detail?: string;
  };
  yandex: {
    status: 'full' | 'partial' | 'none';
    label: string;
    detail?: string;
  };
  aviasales: {
    status: 'full' | 'partial' | 'none';
    label: string;
    detail?: string;
  };
}

const COMPARISON_DATA: ComparisonFeature[] = [
  {
    id: 'clean_ui',
    category: 'Пользовательский опыт',
    name: 'Интерфейс без рекламы и баннеров',
    description: 'Отсутствие коммерческих баннеров, всплывающих окон и предложений отелей',
    icon: Eye,
    ourService: {
      status: 'full',
      label: '100% без рекламы',
      detail: 'Фокус только на полётах',
    },
    flightradar: {
      status: 'none',
      label: 'Много рекламы',
      detail: 'Баннеры каждые 3 минуты',
    },
    flightaware: {
      status: 'none',
      label: 'Рекламные блоки',
      detail: 'Перегружен промо',
    },
    yandex: {
      status: 'partial',
      label: 'Частично',
      detail: 'Партнёрские блоки Яндекс',
    },
    aviasales: {
      status: 'none',
      label: 'Агрессивные продажи',
      detail: 'Отели, страховки, авто',
    },
  },
  {
    id: 'telemetry',
    category: 'Функциональность',
    name: 'Телеметрия полёта (высота и скорость)',
    description: 'Отображение текущей высоты полета (в метрах) и путевой скорости (км/ч)',
    icon: Zap,
    ourService: {
      status: 'full',
      label: 'В реальном времени',
      detail: 'Мгновенно в карточке',
    },
    flightradar: {
      status: 'full',
      label: 'Есть',
      detail: 'ADS-B радары (футы/узлы)',
    },
    flightaware: {
      status: 'full',
      label: 'Есть',
      detail: 'Техническая телеметрия',
    },
    yandex: {
      status: 'none',
      label: 'Нет',
      detail: 'Только время прилёта',
    },
    aviasales: {
      status: 'none',
      label: 'Нет',
      detail: 'Только расписание',
    },
  },
  {
    id: 'terminal_gate',
    category: 'Информация для пассажиров',
    name: 'Терминалы и гейты вылета / прилёта',
    description: 'Точное указание номера терминала и выхода на посадку для аэропортов',
    icon: Compass,
    ourService: {
      status: 'full',
      label: 'Терминал + Гейт',
      detail: 'Выделены в табло',
    },
    flightradar: {
      status: 'partial',
      label: 'Частично',
      detail: 'Гейты по платной подписке',
    },
    flightaware: {
      status: 'full',
      label: 'Есть',
      detail: 'Для большинства хабов',
    },
    yandex: {
      status: 'partial',
      label: 'Только терминал',
      detail: 'Гейты часто отсутствуют',
    },
    aviasales: {
      status: 'none',
      label: 'Нет',
      detail: 'Не отображает гейты',
    },
  },
  {
    id: 'simplicity',
    category: 'Пользовательский опыт',
    name: 'Простота и понятность для пассажира',
    description: 'Интуитивная навигация, крупные шрифты, карточки рейсов без сложных авиа-кодов',
    icon: Shield,
    ourService: {
      status: 'full',
      label: 'Максимальная',
      detail: 'Адаптивный эргономичный UI',
    },
    flightradar: {
      status: 'partial',
      label: 'Сложный',
      detail: 'Интерфейс для споттеров',
    },
    flightaware: {
      status: 'partial',
      label: 'B2B перегруз',
      detail: 'Много технических графиков',
    },
    yandex: {
      status: 'partial',
      label: 'Стандартный',
      detail: 'Простой табличный список',
    },
    aviasales: {
      status: 'partial',
      label: 'Коммерческий',
      detail: 'Фокус на покупке билетов',
    },
  },
  {
    id: 'notifications',
    category: 'Сервисные функции',
    name: 'Email-уведомления и рассылка',
    description: 'Оперативные уведомления об изменениях расписания и полезные советы',
    icon: Bell,
    ourService: {
      status: 'full',
      label: 'Бесплатно по email',
      detail: 'Без спама и без паролей',
    },
    flightradar: {
      status: 'partial',
      label: 'Платная подписка',
      detail: 'Тариф Silver / Gold',
    },
    flightaware: {
      status: 'partial',
      label: 'Сложная настройка',
      detail: 'Нужна полная регистрация',
    },
    yandex: {
      status: 'partial',
      label: 'Только в приложении',
      detail: 'Push-уведомления',
    },
    aviasales: {
      status: 'partial',
      label: 'Только о ценах',
      detail: 'Уведомления о скидках',
    },
  },
  {
    id: 'free_access',
    category: 'Доступность',
    name: '100% бесплатный полный доступ',
    description: 'Все функции, детали рейса, телеметрия и поиск доступны бесплатно без тарифов',
    icon: Sparkles,
    ourService: {
      status: 'full',
      label: 'Полностью бесплатно',
      detail: 'Все функции открыты',
    },
    flightradar: {
      status: 'partial',
      label: 'От $1.49 / месяц',
      detail: 'Платные тарифные планы',
    },
    flightaware: {
      status: 'partial',
      label: 'B2B подписки',
      detail: 'Ограничения free-аккаунта',
    },
    yandex: {
      status: 'full',
      label: 'Бесплатно',
      detail: 'Базовый функционал',
    },
    aviasales: {
      status: 'full',
      label: 'Бесплатно',
      detail: 'Монетизация на билетах',
    },
  },
];

export const ComparisonSection: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'all' | 'experience' | 'functionality'>('all');

  const filteredData = COMPARISON_DATA.filter((item) => {
    if (activeTab === 'experience') return item.category === 'Пользовательский опыт';
    if (activeTab === 'functionality') return item.category !== 'Пользовательский опыт';
    return true;
  });

  const renderStatusBadge = (
    item: { status: 'full' | 'partial' | 'none'; label: string; detail?: string },
    isOur = false
  ) => {
    if (isOur) {
      return (
        <div className="flex flex-col items-center justify-center p-2 rounded-xl bg-sky-500/10 border border-sky-300/40 text-center">
          <div className="flex items-center gap-1.5 font-semibold text-xs sm:text-sm text-sky-900">
            <div className="w-5 h-5 rounded-full bg-sky-600 text-white flex items-center justify-center flex-shrink-0 shadow-xs">
              <Check className="w-3.5 h-3.5" strokeWidth={2.5} />
            </div>
            <span>{item.label}</span>
          </div>
          {item.detail && (
            <span className="text-[11px] text-sky-700/80 font-normal mt-0.5">{item.detail}</span>
          )}
        </div>
      );
    }

    if (item.status === 'full') {
      return (
        <div className="flex flex-col items-center justify-center p-2 text-center">
          <div className="flex items-center gap-1.5 font-medium text-xs sm:text-sm text-slate-800">
            <div className="w-4 h-4 rounded-full bg-emerald-500 text-white flex items-center justify-center flex-shrink-0">
              <Check className="w-3 h-3" strokeWidth={2.5} />
            </div>
            <span>{item.label}</span>
          </div>
          {item.detail && <span className="text-[10.5px] text-slate-500 mt-0.5">{item.detail}</span>}
        </div>
      );
    }

    if (item.status === 'partial') {
      return (
        <div className="flex flex-col items-center justify-center p-2 text-center">
          <div className="flex items-center gap-1.5 font-medium text-xs sm:text-sm text-amber-700">
            <div className="w-4 h-4 rounded-full bg-amber-400 text-amber-950 flex items-center justify-center flex-shrink-0 font-bold text-[10px]">
              <Minus className="w-3 h-3" strokeWidth={2.5} />
            </div>
            <span>{item.label}</span>
          </div>
          {item.detail && <span className="text-[10.5px] text-slate-500 mt-0.5">{item.detail}</span>}
        </div>
      );
    }

    return (
      <div className="flex flex-col items-center justify-center p-2 text-center">
        <div className="flex items-center gap-1.5 font-medium text-xs sm:text-sm text-slate-400">
          <div className="w-4 h-4 rounded-full bg-slate-200 text-slate-500 flex items-center justify-center flex-shrink-0">
            <X className="w-3 h-3" strokeWidth={2.5} />
          </div>
          <span>{item.label}</span>
        </div>
        {item.detail && <span className="text-[10.5px] text-slate-400 mt-0.5">{item.detail}</span>}
      </div>
    );
  };

  return (
    <section id="comparison" className="pt-10 sm:pt-14 pb-12 sm:pb-16 px-4 sm:px-6 lg:px-8 xl:px-10 bg-white text-slate-900 w-full overflow-hidden scroll-mt-6">
      <div className="w-full max-w-[1364px] mx-auto space-y-8 sm:space-y-10">
        
        {/* Header Block */}
        <div className="w-full max-w-[1240px] xl:max-w-[1280px] mx-auto">
          <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 border-b border-[#E2EEF8] pb-6 sm:pb-8">
            <div className="space-y-2.5 max-w-2xl">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#EFF7FE] border border-[#D5ECF8] text-[11px] font-semibold text-sky-700">
                <Sparkles className="w-3.5 h-3.5 text-sky-600" />
                <span>СРАВНИТЕЛЬНЫЙ АНАЛИЗ СЕРВИСОВ</span>
              </div>
              <h2
                className="text-[22px] sm:text-[28px] lg:text-[34px] font-medium tracking-tight text-slate-950 uppercase leading-tight font-benzin"
                style={{ fontFamily: "'Benzin-Bold', 'Benzin-Medium', 'Benzin', sans-serif" }}
              >
                КАК МЫ ВЫГЛЯДИМ НА ФОНЕ АНАЛОГОВ?
              </h2>
              <p className="text-xs sm:text-sm text-slate-600 font-tt-travels leading-relaxed">
                Честное сравнение сервиса «Авиарейсы» с мировыми и российскими трекерами полётов. Мы объединили удобство для пассажиров, отсутствие навязчивой рекламы и точность данных.
              </p>
            </div>

            {/* Filter Pills */}
            <div className="flex items-center gap-2 bg-[#F8FCFF] border border-[#E2EEF8] p-1.5 rounded-full select-none">
              <button
                onClick={() => setActiveTab('all')}
                className={`px-4 py-2 rounded-full text-xs font-semibold transition-all cursor-pointer ${
                  activeTab === 'all'
                    ? 'bg-black text-white shadow-xs'
                    : 'text-slate-600 hover:text-slate-950'
                }`}
              >
                Все критерии
              </button>
              <button
                onClick={() => setActiveTab('experience')}
                className={`px-4 py-2 rounded-full text-xs font-semibold transition-all cursor-pointer ${
                  activeTab === 'experience'
                    ? 'bg-black text-white shadow-xs'
                    : 'text-slate-600 hover:text-slate-950'
                }`}
              >
                Интерфейс и UX
              </button>
              <button
                onClick={() => setActiveTab('functionality')}
                className={`px-4 py-2 rounded-full text-xs font-semibold transition-all cursor-pointer ${
                  activeTab === 'functionality'
                    ? 'bg-black text-white shadow-xs'
                    : 'text-slate-600 hover:text-slate-950'
                }`}
              >
                Функции и данные
              </button>
            </div>
          </div>
        </div>

        {/* Comparison Table Card */}
        <div className="w-full max-w-[1240px] xl:max-w-[1280px] mx-auto overflow-hidden rounded-[30px] sm:rounded-[36px] bg-[#F8FCFF] border border-[#E2EEF8] shadow-sm">
          <div className="overflow-x-auto">
            <table className="w-full min-w-[900px] border-collapse text-left">
              <thead>
                <tr className="border-b border-[#E2EEF8] bg-white/70">
                  <th className="py-5 px-6 font-tt-travels font-bold text-xs sm:text-sm text-slate-600 uppercase tracking-wider w-[320px]">
                    Возможность / Параметр
                  </th>
                  
                  {/* Our Service Highlight Header */}
                  <th className="py-5 px-5 bg-sky-500/10 border-x border-sky-300/40 text-center w-[230px] relative">
                    <div className="absolute -top-2 left-1/2 -translate-x-1/2 px-2.5 py-0.5 rounded-full bg-sky-600 text-white text-[9.5px] font-bold uppercase tracking-wider shadow-xs">
                      Наш сервис
                    </div>
                    <div className="font-benzin-bold text-sm sm:text-base text-sky-950 uppercase pt-1">
                      Авиарейсы
                    </div>
                    <span className="text-[10.5px] text-sky-700 font-sans block mt-0.5">
                      React + Django + Live API
                    </span>
                  </th>

                  <th className="py-5 px-4 text-center w-[180px]">
                    <div className="font-tt-travels font-bold text-xs sm:text-sm text-slate-900">
                      Flightradar24
                    </div>
                    <span className="text-[10px] text-slate-400 font-sans block mt-0.5">
                      ADS-B Радар
                    </span>
                  </th>

                  <th className="py-5 px-4 text-center w-[180px]">
                    <div className="font-tt-travels font-bold text-xs sm:text-sm text-slate-900">
                      FlightAware
                    </div>
                    <span className="text-[10px] text-slate-400 font-sans block mt-0.5">
                      Корпоративный трекер
                    </span>
                  </th>

                  <th className="py-5 px-4 text-center w-[180px]">
                    <div className="font-tt-travels font-bold text-xs sm:text-sm text-slate-900">
                      Яндекс Расписания
                    </div>
                    <span className="text-[10px] text-slate-400 font-sans block mt-0.5">
                      Текстовое табло
                    </span>
                  </th>

                  <th className="py-5 px-4 text-center w-[180px]">
                    <div className="font-tt-travels font-bold text-xs sm:text-sm text-slate-900">
                      Aviasales
                    </div>
                    <span className="text-[10px] text-slate-400 font-sans block mt-0.5">
                      Агрегатор билетов
                    </span>
                  </th>
                </tr>
              </thead>
              
              <tbody className="divide-y divide-[#E2EEF8]/70">
                {filteredData.map((feature, idx) => {
                  const Icon = feature.icon;
                  return (
                    <tr
                      key={feature.id}
                      className={idx % 2 === 0 ? 'bg-white/40' : 'bg-transparent'}
                    >
                      {/* Feature Name & Description */}
                      <td className="py-4 px-6 align-middle">
                        <div className="flex items-start gap-3">
                          <div className="w-8 h-8 rounded-xl bg-white border border-[#E2EEF8] flex items-center justify-center text-sky-600 flex-shrink-0 mt-0.5 shadow-xs">
                            <Icon className="w-4 h-4" />
                          </div>
                          <div>
                            <span className="font-tt-travels font-bold text-xs sm:text-sm text-slate-950 block">
                              {feature.name}
                            </span>
                            <span className="text-[11px] text-slate-500 font-sans leading-tight block mt-0.5">
                              {feature.description}
                            </span>
                          </div>
                        </div>
                      </td>

                      {/* Our Service Column */}
                      <td className="py-3 px-4 bg-sky-500/[0.07] border-x border-sky-300/40 align-middle">
                        {renderStatusBadge(feature.ourService, true)}
                      </td>

                      {/* Flightradar24 */}
                      <td className="py-3 px-3 align-middle">
                        {renderStatusBadge(feature.flightradar)}
                      </td>

                      {/* FlightAware */}
                      <td className="py-3 px-3 align-middle">
                        {renderStatusBadge(feature.flightaware)}
                      </td>

                      {/* Яндекс Расписания */}
                      <td className="py-3 px-3 align-middle">
                        {renderStatusBadge(feature.yandex)}
                      </td>

                      {/* Aviasales */}
                      <td className="py-3 px-3 align-middle">
                        {renderStatusBadge(feature.aviasales)}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {/* Table Bottom Footer CTA */}
          <div className="p-5 sm:p-6 bg-white border-t border-[#E2EEF8] flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="text-xs sm:text-[13px] text-slate-600 font-sans text-center sm:text-left">
              Оцените удобство и скорость работы нашего онлайн-табло прямо сейчас.
            </div>
            <Link
              to="/flights"
              className="px-6 py-2.5 rounded-full bg-black hover:bg-slate-900 active:scale-95 text-white font-medium text-xs sm:text-sm transition-all flex items-center gap-2 shadow-xs cursor-pointer whitespace-nowrap"
            >
              <span>Открыть онлайн-табло</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>

      </div>
    </section>
  );
};
