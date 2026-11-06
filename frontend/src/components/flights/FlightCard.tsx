import React from 'react';
import { Link } from 'react-router-dom';
import { Plane, Heart, ArrowRight } from 'lucide-react';
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
    <div className="group relative rounded-3xl bg-[#161F30]/80 hover:bg-[#161F30] border border-white/10 hover:border-blue-500/50 p-6 transition-all duration-300 shadow-xl hover:shadow-2xl hover:shadow-blue-900/20">
      
      {/* Top Header: Airline, Flight Number, Status & Favorite Button */}
      <div className="flex items-center justify-between border-b border-white/5 pb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-blue-600/15 border border-blue-500/25 flex items-center justify-center text-blue-400 group-hover:bg-blue-600 group-hover:text-white transition-colors">
            <Plane className="w-5 h-5 -rotate-45" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-display font-bold text-sm tracking-wide text-white">
                {flight.flightNumber}
              </span>
              <span className="text-xs text-slate-400">· {flight.airline}</span>
            </div>
            <span className="text-[11px] text-slate-500">{flight.aircraft}</span>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <StatusBadge status={flight.status} statusText={flight.statusText} />
          <button
            onClick={(e) => {
              e.preventDefault();
              onToggleFavorite(flight.id);
            }}
            className={`w-9 h-9 rounded-full flex items-center justify-center transition-all ${
              isFavorite
                ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                : 'bg-white/5 text-slate-400 hover:text-white hover:bg-white/10'
            }`}
            title={isFavorite ? 'Удалить из избранного' : 'Добавить в избранное'}
          >
            <Heart className={`w-4 h-4 ${isFavorite ? 'fill-rose-400' : ''}`} />
          </button>
        </div>
      </div>

      {/* Main Route Info */}
      <div className="py-6 grid grid-cols-1 md:grid-cols-12 gap-4 items-center">
        
        {/* Origin */}
        <div className="md:col-span-4 space-y-1">
          <div className="font-display font-extrabold text-2xl sm:text-3xl text-white">
            {flight.departureTime}
          </div>
          <div className="font-bold text-sm text-slate-200">
            {flight.from.city} ({flight.from.code})
          </div>
          <div className="text-xs text-slate-400">
            {flight.from.name} {flight.from.terminal ? `· Терминал ${flight.from.terminal}` : ''}
          </div>
        </div>

        {/* Flight duration & progress line */}
        <div className="md:col-span-4 flex flex-col items-center justify-center py-2">
          <span className="text-[11px] font-medium text-slate-400 mb-1">
            {flight.duration}
          </span>
          <div className="w-full flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-blue-500 flex-shrink-0" />
            <div className="relative flex-1 h-[2px] bg-gradient-to-r from-blue-500 via-sky-400 to-blue-500">
              <Plane className="w-4 h-4 text-sky-400 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2" />
            </div>
            <span className="w-2 h-2 rounded-full bg-blue-500 flex-shrink-0" />
          </div>
          <span className="text-[10px] text-slate-500 mt-1">Прямой рейс</span>
        </div>

        {/* Destination */}
        <div className="md:col-span-4 md:text-right space-y-1">
          <div className="font-display font-extrabold text-2xl sm:text-3xl text-white">
            {flight.arrivalTime}
          </div>
          <div className="font-bold text-sm text-slate-200">
            {flight.to.city} ({flight.to.code})
          </div>
          <div className="text-xs text-slate-400">
            {flight.to.name} {flight.to.terminal ? `· Терминал ${flight.to.terminal}` : ''}
          </div>
        </div>

      </div>

      {/* Footer info & CTA */}
      <div className="border-t border-white/5 pt-4 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-4 text-xs text-slate-400">
          {flight.from.gate && (
            <span>Гейт: <strong className="text-white">{flight.from.gate}</strong></span>
          )}
          {flight.price && (
            <span>От <strong className="text-blue-400 font-semibold">{flight.price.toLocaleString('ru-RU')} ₽</strong></span>
          )}
        </div>

        <Link
          to={`/flights/${flight.id}`}
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-white/10 hover:bg-blue-600 text-white text-xs font-semibold transition-all group-hover:scale-102"
        >
          <span>Детали рейса</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>

    </div>
  );
};

