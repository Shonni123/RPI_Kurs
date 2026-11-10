import React from 'react';
import { Link } from 'react-router-dom';
import { Plane, Heart, ArrowRight, ExternalLink } from 'lucide-react';
import { Flight } from '../../types/flight';
import { StatusBadge } from './StatusBadge';

interface FlightCardProps {
  flight: Flight;
  isFavorite: boolean;
  onToggleFavorite: (id: string) => void;
}

export const FlightCard: React.FC<FlightCardProps> = ({
  flight,
  isFavorite,
  onToggleFavorite,
}) => {
  return (
    <div className="group relative rounded-[24px] sm:rounded-[28px] bg-white border border-[#E2EEF8] hover:border-[#B7DAF4] p-5 sm:p-6 transition-all duration-300 shadow-sm hover:shadow-xl hover:shadow-sky-100/70">
      
      {/* Top Header: Airline, Flight Number, Status & Favorite Button */}
      <div className="flex items-center justify-between border-b border-slate-100 pb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-[#EFF7FE] border border-[#D5ECF8] flex items-center justify-center text-sky-600 group-hover:bg-black group-hover:text-white transition-colors duration-200">
            <Plane className="w-5 h-5 -rotate-45" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-benzin-bold text-sm tracking-wide text-slate-950">
                {flight.flightNumber}
              </span>
              <span className="text-xs text-slate-500 font-tt-travels">· {flight.airline}</span>
              {flight.isRealApi && (
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 hidden sm:inline-flex items-center gap-1" title="Синхронизировано из Aviationstack API">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                  <span>Aviationstack</span>
                </span>
              )}
            </div>
            <span className="text-[11px] text-slate-400 font-sans">{flight.aircraft}</span>
          </div>
        </div>

        <div className="flex items-center gap-2.5">
          <StatusBadge status={flight.status} statusText={flight.statusText} />
          <button
            onClick={(e) => {
              e.preventDefault();
              e.stopPropagation();
              onToggleFavorite(flight.id);
            }}
            className={`w-9 h-9 rounded-full flex items-center justify-center transition-all cursor-pointer ${
              isFavorite
                ? 'bg-rose-50 text-rose-500 border border-rose-200 shadow-xs scale-105'
                : 'bg-[#F8FCFF] text-slate-400 hover:text-rose-500 hover:bg-rose-50/50 border border-[#E2EEF8]'
            }`}
            title={isFavorite ? 'Удалить из избранного' : 'Добавить в избранное'}
          >
            <Heart className={`w-4 h-4 transition-transform active:scale-125 ${isFavorite ? 'fill-rose-500 text-rose-500' : ''}`} />
          </button>
        </div>
      </div>

      {/* Main Route Info */}
      <div className="py-5 sm:py-6 grid grid-cols-1 md:grid-cols-12 gap-4 items-center">
        
        {/* Origin */}
        <div className="md:col-span-4 space-y-1">
          <div className="font-benzin-bold text-2xl sm:text-3xl text-slate-950 tracking-tight">
            {flight.departureTime}
          </div>
          <div className="flex items-center gap-2">
            <span className="font-tt-travels font-bold text-sm sm:text-base text-slate-800">
              {flight.from.city}
            </span>
            <span className="text-xs font-semibold px-2 py-0.5 rounded-md bg-[#EFF7FE] text-sky-700 border border-[#D5ECF8]">
              {flight.from.code}
            </span>
          </div>
          <div className="text-xs text-slate-500 font-sans">
            {flight.from.name} {flight.from.terminal ? `· Терм. ${flight.from.terminal}` : ''}
          </div>
        </div>

        {/* Flight duration & progress route line */}
        <div className="md:col-span-4 flex flex-col items-center justify-center py-2">
          <span className="text-xs font-semibold text-slate-500 font-tt-travels mb-1.5">
            {flight.duration}
          </span>
          <div className="w-full flex items-center gap-2 px-2">
            <span className="w-2.5 h-2.5 rounded-full bg-sky-500 ring-4 ring-sky-100 flex-shrink-0" />
            <div className="relative flex-1 h-[2px] bg-gradient-to-r from-sky-400 via-blue-500 to-sky-400">
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-6 h-6 rounded-full bg-white border border-[#D5ECF8] shadow-xs flex items-center justify-center">
                <Plane className="w-3.5 h-3.5 text-sky-600 rotate-90" />
              </div>
            </div>
            <span className="w-2.5 h-2.5 rounded-full bg-blue-600 ring-4 ring-blue-100 flex-shrink-0" />
          </div>
          <span className="text-[11px] text-slate-400 mt-2 font-sans">Прямой рейс</span>
        </div>

        {/* Destination */}
        <div className="md:col-span-4 md:text-right space-y-1">
          <div className="font-benzin-bold text-2xl sm:text-3xl text-slate-950 tracking-tight">
            {flight.arrivalTime}
          </div>
          <div className="flex items-center md:justify-end gap-2">
            <span className="font-tt-travels font-bold text-sm sm:text-base text-slate-800">
              {flight.to.city}
            </span>
            <span className="text-xs font-semibold px-2 py-0.5 rounded-md bg-[#EFF7FE] text-sky-700 border border-[#D5ECF8]">
              {flight.to.code}
            </span>
          </div>
          <div className="text-xs text-slate-500 font-sans">
            {flight.to.name} {flight.to.terminal ? `· Терм. ${flight.to.terminal}` : ''}
          </div>
        </div>

      </div>

      {/* Footer Info & CTA with Aviasales ticket link and Aviationstack API source */}
      <div className="border-t border-slate-100 pt-4 flex flex-wrap items-center justify-between gap-3">
        <div className="flex flex-wrap items-center gap-3 sm:gap-4 text-xs text-slate-600 font-sans">
          {flight.from.gate && (
            <span>
              Гейт: <strong className="text-slate-900 font-semibold">{flight.from.gate}</strong>
            </span>
          )}
          {flight.price && (
            <div className="flex items-center gap-2">
              <span>
                Билеты от <strong className="font-benzin-medium text-slate-950 text-xs sm:text-sm">{flight.price.toLocaleString('ru-RU')} ₽</strong>
              </span>
              <a
                href={`https://www.aviasales.ru/search/${flight.from.code || 'MOW'}${flight.to.code || 'LED'}1`}
                target="_blank"
                rel="noopener noreferrer"
                onClick={(e) => e.stopPropagation()}
                className="inline-flex items-center gap-1 text-[11px] font-semibold text-sky-600 hover:text-sky-800 hover:underline px-2 py-0.5 rounded-md bg-[#EFF7FE] border border-[#D5ECF8] transition-colors"
                title="Купить или проверить цену на Aviasales"
              >
                <span>Купить билет</span>
                <ExternalLink className="w-2.5 h-2.5" />
              </a>
            </div>
          )}
        </div>

        <div className="flex items-center gap-2.5">
          <a
            href="https://aviationstack.com/"
            target="_blank"
            rel="noopener noreferrer"
            onClick={(e) => e.stopPropagation()}
            className="text-[11px] text-slate-400 hover:text-sky-700 transition-colors hidden sm:inline-flex items-center gap-1"
            title="Источник данных: Aviationstack Global Aviation API"
          >
            <span>Aviationstack API</span>
            <ExternalLink className="w-2.5 h-2.5" />
          </a>

          <Link
            to={`/flights/${flight.id}`}
            className="inline-flex items-center gap-2 px-5 py-2 rounded-full bg-black hover:bg-slate-800 text-white text-xs font-semibold transition-all hover:scale-[1.02] shadow-sm cursor-pointer"
          >
            <span>Детали рейса</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>

    </div>
  );
};
