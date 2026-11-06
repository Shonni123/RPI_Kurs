import React, { useState } from 'react';
import { PlaneTakeoff, PlaneLanding, MapPin, Search } from 'lucide-react';
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
];

export const AirportsPage: React.FC = () => {
  const [search, setSearch] = useState('');

  const filtered = AIRPORTS.filter(
    (a) =>
      a.city.toLowerCase().includes(search.toLowerCase()) ||
      a.name.toLowerCase().includes(search.toLowerCase()) ||
      a.code.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="min-h-screen pt-28 pb-20 px-4 sm:px-6 lg:px-8 bg-[#0B0F19] text-white">
      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Title */}
        <div className="border-b border-white/10 pb-6">
          <span className="text-xs font-semibold tracking-widest text-blue-400 uppercase">
            База знаний и направлений
          </span>
          <h1 className="font-display font-black text-2xl sm:text-4xl uppercase tracking-tight text-white mt-1">
            Аэропорты и хабы
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Справочник узловых аэропортов с актуальным числом вылетов и прилётов.
          </p>
        </div>

        {/* Search */}
        <div className="relative max-w-md">
          <Search className="w-5 h-5 text-slate-400 absolute top-1/2 left-4 -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Поиск по названию или коду (SVO, LED, Дубай)..."
            className="w-full pl-12 pr-4 py-3 rounded-2xl bg-[#161F30]/70 border border-white/10 text-white placeholder:text-slate-400 text-xs sm:text-sm focus:outline-none focus:border-blue-500"
          />
        </div>

        {/* Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map((airport) => (
            <div
              key={airport.code}
              className="p-6 rounded-3xl bg-[#161F30]/80 border border-white/10 hover:border-blue-500/50 transition-all duration-300 hover:shadow-xl space-y-5 flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="font-display font-black text-3xl text-blue-400">
                    {airport.code}
                  </span>
                  <span className="text-[11px] px-3 py-1 rounded-full bg-white/5 border border-white/10 text-slate-300 font-medium">
                    {airport.timezone}
                  </span>
                </div>

                <div>
                  <h3 className="font-bold text-base text-white flex items-center gap-1.5">
                    <MapPin className="w-4 h-4 text-blue-400" />
                    {airport.city}, {airport.country}
                  </h3>
                  <p className="text-xs text-slate-400 mt-1">{airport.name}</p>
                </div>
              </div>

              <div className="pt-4 border-t border-white/5 grid grid-cols-2 gap-3 text-xs">
                <div className="p-3 rounded-2xl bg-black/30 border border-white/5 flex items-center gap-2.5">
                  <PlaneTakeoff className="w-4 h-4 text-sky-400" />
                  <div>
                    <span className="text-slate-400 block text-[10px]">Вылетов</span>
                    <strong className="text-white text-sm">{airport.departuresCount}</strong>
                  </div>
                </div>

                <div className="p-3 rounded-2xl bg-black/30 border border-white/5 flex items-center gap-2.5">
                  <PlaneLanding className="w-4 h-4 text-emerald-400" />
                  <div>
                    <span className="text-slate-400 block text-[10px]">Прилётов</span>
                    <strong className="text-white text-sm">{airport.arrivalsCount}</strong>
                  </div>
                </div>
              </div>

              <Link
                to={`/flights?search=${airport.code}`}
                className="w-full text-center py-2.5 rounded-full bg-white/5 hover:bg-blue-600 border border-white/10 hover:border-blue-500 text-xs font-semibold text-white transition-all"
              >
                Смотреть рейсы аэропорта
              </Link>
            </div>
          ))}
        </div>

      </div>
    </div>
  );
};
