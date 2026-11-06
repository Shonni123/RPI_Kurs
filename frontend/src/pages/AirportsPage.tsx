import React, { useState } from 'react';
import { PlaneTakeoff, PlaneLanding, MapPin, Search, ArrowLeft, ArrowRight, X } from 'lucide-react';
import { Link } from 'react-router-dom';

interface AirportCardData {
  code: string;
  name: string;
  city: string;
  country: string;
  departuresCount: number;
  arrivalsCount: number;
  timezone: string;
}

const AIRPORTS: AirportCardData[] = [
  {
    code: 'SVO',
    name: 'Шереметьево имени А. С. Пушкина',
    city: 'Москва',
    country: 'Россия',
    departuresCount: 142,
    arrivalsCount: 138,
    timezone: 'UTC+3',
  },
  {
    code: 'DME',
    name: 'Домодедово имени М. В. Ломоносова',
    city: 'Москва',
    country: 'Россия',
    departuresCount: 98,
    arrivalsCount: 95,
    timezone: 'UTC+3',
  },
  {
    code: 'VKO',
    name: 'Внуково имени А. Н. Туполева',
    city: 'Москва',
    country: 'Россия',
    departuresCount: 64,
    arrivalsCount: 61,
    timezone: 'UTC+3',
  },
  {
    code: 'LED',
    name: 'Пулково',
    city: 'Санкт-Петербург',
    country: 'Россия',
    departuresCount: 88,
    arrivalsCount: 84,
    timezone: 'UTC+3',
  },
  {
    code: 'AER',
    name: 'Международный аэропорт Сочи',
    city: 'Сочи',
    country: 'Россия',
    departuresCount: 76,
    arrivalsCount: 72,
    timezone: 'UTC+3',
  },
  {
    code: 'KZN',
    name: 'Международный аэропорт Казань',
    city: 'Казань',
    country: 'Россия',
    departuresCount: 45,
    arrivalsCount: 42,
    timezone: 'UTC+3',
  },
  {
    code: 'DXB',
    name: 'Международный аэропорт Дубай',
    city: 'Дубай',
    country: 'ОАЭ',
    departuresCount: 310,
    arrivalsCount: 305,
    timezone: 'UTC+4',
  },
  {
    code: 'IST',
    name: 'Новый аэропорт Стамбула',
    city: 'Стамбул',
    country: 'Турция',
    departuresCount: 260,
    arrivalsCount: 254,
    timezone: 'UTC+3',
  },
  {
    code: 'DOH',
    name: 'Международный аэропорт Хамад',
    city: 'Доха',
    country: 'Катар',
    departuresCount: 185,
    arrivalsCount: 180,
    timezone: 'UTC+3',
  },
];

export const AirportsPage: React.FC = () => {
  const [search, setSearch] = useState('');

  const filtered = AIRPORTS.filter(
    (a) =>
      a.city.toLowerCase().includes(search.toLowerCase()) ||
      a.name.toLowerCase().includes(search.toLowerCase()) ||
      a.code.toLowerCase().includes(search.toLowerCase()) ||
      a.country.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-[#F8FCFF] text-slate-900 pt-6 sm:pt-8 pb-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto space-y-6 sm:space-y-8">
        
        {/* Navigation Breadcrumb */}
        <div className="flex items-center justify-between">
          <Link
            to="/"
            className="inline-flex items-center gap-2 text-xs font-semibold text-slate-600 hover:text-slate-950 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Вернуться на главную</span>
          </Link>
        </div>

        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-[#E2EEF8] pb-6">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#EFF7FE] border border-[#D5ECF8] text-[11px] font-semibold text-sky-700 mb-2">
              <MapPin className="w-3.5 h-3.5 text-sky-600" />
              <span>ГЕОГРАФИЯ И ХАБЫ</span>
            </div>
            <h1 className="font-benzin-bold text-2xl sm:text-3xl lg:text-4xl uppercase tracking-tight text-slate-950">
              Аэропорты и хабы
            </h1>
            <p className="font-tt-travels text-xs sm:text-sm text-slate-600 mt-1.5 max-w-xl">
              Справочник узловых аэропортов с актуальной статистикой вылетов, прилётов и часовых поясов.
            </p>
          </div>

          <div className="text-xs text-slate-500 font-sans">
            Всего аэропортов в базе: <strong className="font-benzin-medium text-slate-950">{AIRPORTS.length}</strong>
          </div>
        </div>

        {/* Search */}
        <div className="relative max-w-md">
          <Search className="w-4 h-4 sm:w-5 sm:h-5 text-slate-400 absolute top-1/2 left-4 -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Поиск по городу, названию или коду (SVO, LED, Дубай)..."
            className="w-full pl-11 pr-10 py-3 rounded-2xl bg-white border border-[#E2EEF8] text-slate-900 placeholder:text-slate-400 text-xs sm:text-sm focus:outline-none focus:border-sky-400 transition-colors shadow-xs font-sans"
          />
          {search && (
            <button
              onClick={() => setSearch('')}
              className="absolute top-1/2 right-4 -translate-y-1/2 text-slate-400 hover:text-slate-700 p-1 cursor-pointer"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>

        {/* Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {filtered.map((airport) => (
            <div
              key={airport.code}
              className="p-6 rounded-[28px] bg-white border border-[#E2EEF8] hover:border-[#BCE0F8] transition-all duration-300 shadow-sm hover:shadow-xl hover:shadow-sky-100/70 space-y-5 flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="font-benzin-bold text-3xl text-sky-700 tracking-tight">
                    {airport.code}
                  </span>
                  <span className="text-[11px] px-3 py-1 rounded-full bg-[#EFF7FE] border border-[#D5ECF8] text-sky-800 font-semibold">
                    {airport.timezone}
                  </span>
                </div>

                <div>
                  <h3 className="font-tt-travels font-bold text-base text-slate-900 flex items-center gap-1.5">
                    <MapPin className="w-4 h-4 text-sky-600" />
                    <span>{airport.city}, {airport.country}</span>
                  </h3>
                  <p className="text-xs text-slate-500 font-sans mt-1 leading-relaxed">{airport.name}</p>
                </div>
              </div>

              <div className="pt-4 border-t border-slate-100 grid grid-cols-2 gap-3 text-xs">
                <div className="p-3 rounded-2xl bg-[#F8FCFF] border border-[#E2EEF8] flex items-center gap-2.5">
                  <PlaneTakeoff className="w-4 h-4 text-sky-600" />
                  <div>
                    <span className="text-slate-500 block text-[10px] font-sans">Вылетов</span>
                    <strong className="text-slate-950 font-benzin-medium text-sm">{airport.departuresCount}</strong>
                  </div>
                </div>

                <div className="p-3 rounded-2xl bg-[#F8FCFF] border border-[#E2EEF8] flex items-center gap-2.5">
                  <PlaneLanding className="w-4 h-4 text-emerald-600" />
                  <div>
                    <span className="text-slate-500 block text-[10px] font-sans">Прилётов</span>
                    <strong className="text-slate-950 font-benzin-medium text-sm">{airport.arrivalsCount}</strong>
                  </div>
                </div>
              </div>

              <Link
                to={`/flights`}
                className="w-full text-center py-2.5 rounded-full bg-black hover:bg-slate-800 text-xs font-semibold text-white transition-all shadow-xs flex items-center justify-center gap-1.5"
              >
                <span>Смотреть рейсы</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          ))}
        </div>

      </div>
    </div>
  );
};
