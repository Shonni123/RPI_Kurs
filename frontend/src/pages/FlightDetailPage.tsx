import React from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  Plane,
  ArrowLeft,
  Heart,
  Gauge,
  Compass,
  CloudSun,
  ShieldCheck,
  Share2,
  Calendar,
} from 'lucide-react';
import { MOCK_FLIGHTS } from '../services/mockFlights';
import { StatusBadge } from '../components/flights/StatusBadge';
import { useFavorites } from '../hooks/useFavorites';
import { EmptyState } from '../components/common/EmptyState';

export const FlightDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { isFavorite, toggleFavorite } = useFavorites();

  const flight = MOCK_FLIGHTS.find((f) => f.id === id);

  if (!flight) {
    return (
      <div className="min-h-screen pt-32 pb-20 px-4 bg-[#0B0F19] text-white">
        <EmptyState
          title="Рейс не найден"
          description={`Рейс с идентификатором "${id}" не зарегистрирован в системе или перенесён в архив.`}
          actionText="Вернуться к табло рейсов"
          actionLink="/flights"
        />
      </div>
    );
  }

  const favorite = isFavorite(flight.id);

  return (
    <div className="min-h-screen pt-28 pb-20 px-4 sm:px-6 lg:px-8 bg-[#0B0F19] text-white">
      <div className="max-w-5xl mx-auto space-y-8">
        
        {/* Navigation Breadcrumb */}
        <div className="flex items-center justify-between">
          <Link
            to="/flights"
            className="inline-flex items-center gap-2 text-xs font-semibold text-slate-400 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Назад к табло рейсов</span>
          </Link>

          <div className="flex items-center gap-3">
            <button
              onClick={() => {
                if (navigator.clipboard) {
                  navigator.clipboard.writeText(window.location.href);
                  alert('Ссылка на рейс скопирована в буфер обмена!');
                }
              }}
              className="p-2.5 rounded-full bg-white/5 hover:bg-white/10 border border-white/10 text-slate-300 transition-colors"
              title="Поделиться"
            >
              <Share2 className="w-4 h-4" />
            </button>

            <button
              onClick={() => toggleFavorite(flight.id)}
              className={`p-2.5 rounded-full flex items-center justify-center transition-all ${
                favorite
                  ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                  : 'bg-white/5 hover:bg-white/10 border border-white/10 text-slate-300'
              }`}
              title={favorite ? 'Удалить из избранного' : 'Добавить в избранное'}
            >
              <Heart className={`w-4 h-4 ${favorite ? 'fill-rose-400' : ''}`} />
            </button>
          </div>
        </div>

        {/* Flight Main Header Card */}
        <div className="p-8 rounded-[2.5rem] bg-gradient-to-b from-[#161F30] to-[#0E1424] border border-white/15 space-y-8 shadow-2xl">
          
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/10 pb-6">
            <div>
              <div className="flex items-center gap-3">
                <span className="font-display font-black text-2xl sm:text-4xl text-white">
                  {flight.flightNumber}
                </span>
                <StatusBadge status={flight.status} statusText={flight.statusText} />
              </div>
              <p className="text-xs sm:text-sm text-slate-400 mt-1">
                Авиакомпания: <strong className="text-slate-200">{flight.airline}</strong> · Борт: <strong className="text-slate-200">{flight.aircraft}</strong>
              </p>
            </div>

            <div className="text-left sm:text-right">
              <span className="text-xs text-slate-400">Дата перелёта</span>
              <p className="font-semibold text-sm text-white flex items-center gap-1.5 sm:justify-end mt-0.5">
                <Calendar className="w-4 h-4 text-blue-400" />
                {flight.departureDate}
              </p>
            </div>
          </div>

          {/* Interactive Route Timeline */}
          <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-center py-4">
            
            {/* Origin */}
            <div className="md:col-span-4 space-y-2">
              <span className="text-xs font-semibold text-blue-400 uppercase tracking-wider">Вылет</span>
              <div className="font-display font-black text-4xl text-white">{flight.departureTime}</div>
              <div className="font-bold text-lg text-white">{flight.from.city} ({flight.from.code})</div>
              <p className="text-xs text-slate-400">
                {flight.from.name}
                <br />
                {flight.from.terminal ? `Терминал ${flight.from.terminal}` : ''} {flight.from.gate ? `· Гейт ${flight.from.gate}` : ''}
              </p>
            </div>

            {/* Flight In-Air Progress */}
            <div className="md:col-span-4 flex flex-col items-center justify-center space-y-2">
              <span className="text-xs text-slate-400 font-medium">Время в пути: {flight.duration}</span>
              <div className="w-full flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-blue-500 ring-4 ring-blue-500/20" />
                <div className="relative flex-1 h-1 bg-gradient-to-r from-blue-500 via-sky-400 to-blue-500 rounded-full">
                  <div className="absolute top-1/2 left-3/5 -translate-x-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center shadow-lg shadow-blue-500/50">
                    <Plane className="w-4 h-4 text-white -rotate-45" />
                  </div>
                </div>
                <span className="w-3 h-3 rounded-full bg-blue-500 ring-4 ring-blue-500/20" />
              </div>
              <span className="text-[11px] text-emerald-400 font-semibold">
                {flight.status === 'in_air' ? 'Самолёт находится на эшелоне' : flight.statusText}
              </span>
            </div>

            {/* Destination */}
            <div className="md:col-span-4 md:text-right space-y-2">
              <span className="text-xs font-semibold text-sky-400 uppercase tracking-wider">Прилёт</span>
              <div className="font-display font-black text-4xl text-white">{flight.arrivalTime}</div>
              <div className="font-bold text-lg text-white">{flight.to.city} ({flight.to.code})</div>
              <p className="text-xs text-slate-400">
                {flight.to.name}
                <br />
                {flight.to.terminal ? `Терминал ${flight.to.terminal}` : ''} {flight.to.gate ? `· Гейт ${flight.to.gate}` : ''}
              </p>
            </div>

          </div>

          {/* Telemetry / Live flight data blocks */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-4 border-t border-white/10">
            <div className="p-4 rounded-2xl bg-black/30 border border-white/5 space-y-1">
              <div className="flex items-center gap-1.5 text-slate-400 text-xs">
                <Gauge className="w-3.5 h-3.5 text-blue-400" />
                <span>Текущая высота</span>
              </div>
              <p className="font-display font-bold text-lg text-white">
                {flight.altitude ? `${flight.altitude.toLocaleString()} м` : 'На земле'}
              </p>
            </div>

            <div className="p-4 rounded-2xl bg-black/30 border border-white/5 space-y-1">
              <div className="flex items-center gap-1.5 text-slate-400 text-xs">
                <Compass className="w-3.5 h-3.5 text-sky-400" />
                <span>Путевая скорость</span>
              </div>
              <p className="font-display font-bold text-lg text-white">
                {flight.speed ? `${flight.speed} км/ч` : '0 км/ч'}
              </p>
            </div>

            <div className="p-4 rounded-2xl bg-black/30 border border-white/5 space-y-1">
              <div className="flex items-center gap-1.5 text-slate-400 text-xs">
                <CloudSun className="w-3.5 h-3.5 text-amber-400" />
                <span>Погода прилёта</span>
              </div>
              <p className="font-display font-bold text-lg text-white">+14°C, Ясно</p>
            </div>

            <div className="p-4 rounded-2xl bg-black/30 border border-white/5 space-y-1">
              <div className="flex items-center gap-1.5 text-slate-400 text-xs">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                <span>Безопасность</span>
              </div>
              <p className="font-display font-bold text-lg text-emerald-400">В штатном режиме</p>
            </div>
          </div>

        </div>

      </div>
    </div>
  );
};
