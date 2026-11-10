import React, { useState, useEffect } from 'react';
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
  Clock,
  Check,
  ExternalLink,
  Ticket,
  Building2,
} from 'lucide-react';
import { Flight } from '../types/flight';
import { flightApi } from '../services/api';
import { StatusBadge } from '../components/flights/StatusBadge';
import { useFavorites } from '../hooks/useFavorites';
import { EmptyState } from '../components/common/EmptyState';

export const FlightDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { isFavorite, toggleFavorite } = useFavorites();
  const [copied, setCopied] = useState(false);
  const [flight, setFlight] = useState<Flight | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    if (id) {
      flightApi.getFlightById(id).then((data) => {
        if (mounted) {
          setFlight(data);
          setLoading(false);
        }
      });
    }
    return () => {
      mounted = false;
    };
  }, [id]);

  if (loading) {
    return (
      <div className="min-h-screen pt-20 pb-20 px-4 bg-[#F8FCFF] text-slate-900 flex items-center justify-center">
        <div className="w-8 h-8 rounded-full border-2 border-sky-600 border-t-transparent animate-spin" />
      </div>
    );
  }

  if (!flight) {
    return (
      <div className="min-h-screen pt-12 pb-20 px-4 bg-[#F8FCFF] text-slate-900">
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

  const handleShare = () => {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(window.location.href);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="min-h-screen bg-[#F8FCFF] text-slate-900 pt-6 sm:pt-8 pb-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto space-y-6 sm:space-y-8">
        
        {/* Navigation Breadcrumb */}
        <div className="flex items-center justify-between">
          <Link
            to="/flights"
            className="inline-flex items-center gap-2 text-xs font-semibold text-slate-600 hover:text-slate-950 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Назад к онлайн-табло</span>
          </Link>

          <div className="flex items-center gap-2.5">
            <button
              onClick={handleShare}
              className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-white hover:bg-slate-50 border border-[#E2EEF8] text-xs font-semibold text-slate-700 transition-all shadow-xs cursor-pointer"
              title="Поделиться рейсом"
            >
              {copied ? (
                <>
                  <Check className="w-3.5 h-3.5 text-emerald-600" />
                  <span className="text-emerald-700">Скопировано!</span>
                </>
              ) : (
                <>
                  <Share2 className="w-3.5 h-3.5" />
                  <span>Поделиться</span>
                </>
              )}
            </button>

            <button
              onClick={() => toggleFavorite(flight.id)}
              className={`p-2 rounded-full flex items-center justify-center transition-all cursor-pointer ${
                favorite
                  ? 'bg-rose-50 text-rose-500 border border-rose-200 shadow-xs'
                  : 'bg-white hover:bg-rose-50/50 border border-[#E2EEF8] text-slate-500 hover:text-rose-500'
              }`}
              title={favorite ? 'Удалить из избранного' : 'Добавить в избранное'}
            >
              <Heart className={`w-4 h-4 ${favorite ? 'fill-rose-500 text-rose-500' : ''}`} />
            </button>
          </div>
        </div>

        {/* Flight Main Card */}
        <div className="p-6 sm:p-8 rounded-[30px] sm:rounded-[36px] bg-white border border-[#E2EEF8] shadow-sm space-y-8">
          
          {/* Header Info */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-6">
            <div>
              <div className="flex items-center gap-3">
                <span className="font-benzin-bold text-2xl sm:text-4xl text-slate-950 tracking-tight">
                  {flight.flightNumber}
                </span>
                <StatusBadge status={flight.status} statusText={flight.statusText} />
              </div>
              <p className="font-tt-travels text-xs sm:text-sm text-slate-600 mt-1.5">
                Авиакомпания: <strong className="text-slate-900 font-semibold">{flight.airline}</strong> · Воздушное судно: <strong className="text-slate-900 font-semibold">{flight.aircraft}</strong>
              </p>
            </div>

            <div className="text-left sm:text-right">
              <span className="text-xs text-slate-500 font-sans">Дата рейса</span>
              <p className="font-tt-travels font-semibold text-sm text-slate-900 flex items-center gap-1.5 sm:justify-end mt-0.5">
                <Calendar className="w-4 h-4 text-sky-600" />
                <span>{flight.departureDate}</span>
              </p>
            </div>
          </div>

          {/* Interactive Route Timeline */}
          <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-center py-4">
            
            {/* Origin */}
            <div className="md:col-span-4 space-y-2">
              <span className="text-[11px] font-semibold text-sky-700 uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-[#EFF7FE] border border-[#D5ECF8] inline-block">
                Вылет
              </span>
              <div className="font-benzin-bold text-3xl sm:text-4xl text-slate-950 tracking-tight">
                {flight.departureTime}
              </div>
              <div className="font-tt-travels font-bold text-lg text-slate-900">
                {flight.from.city} ({flight.from.code})
              </div>
              <p className="text-xs text-slate-500 font-sans leading-relaxed">
                {flight.from.name}
                <br />
                {flight.from.terminal ? `Терминал ${flight.from.terminal}` : ''} {flight.from.gate ? `· Гейт ${flight.from.gate}` : ''}
              </p>
            </div>

            {/* Flight In-Air Progress Route Bar */}
            <div className="md:col-span-4 flex flex-col items-center justify-center space-y-2.5">
              <span className="text-xs font-semibold text-slate-600 font-tt-travels flex items-center gap-1.5">
                <Clock className="w-3.5 h-3.5 text-sky-600" />
                <span>В пути: {flight.duration}</span>
              </span>
              
              <div className="w-full flex items-center gap-2 px-2">
                <span className="w-3 h-3 rounded-full bg-sky-500 ring-4 ring-sky-100 flex-shrink-0" />
                <div className="relative flex-1 h-[3px] bg-gradient-to-r from-sky-400 via-blue-500 to-sky-400 rounded-full">
                  <div className="absolute top-1/2 left-3/5 -translate-x-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-black text-white flex items-center justify-center shadow-md">
                    <Plane className="w-4 h-4 rotate-90" />
                  </div>
                </div>
                <span className="w-3 h-3 rounded-full bg-blue-600 ring-4 ring-blue-100 flex-shrink-0" />
              </div>

              <span className="text-xs font-semibold text-emerald-700 bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200">
                {flight.status === 'in_air' ? 'Самолёт находится на эшелоне' : flight.statusText}
              </span>
            </div>

            {/* Destination */}
            <div className="md:col-span-4 md:text-right space-y-2">
              <span className="text-[11px] font-semibold text-blue-700 uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-blue-50 border border-blue-200 inline-block">
                Прилёт
              </span>
              <div className="font-benzin-bold text-3xl sm:text-4xl text-slate-950 tracking-tight">
                {flight.arrivalTime}
              </div>
              <div className="font-tt-travels font-bold text-lg text-slate-900">
                {flight.to.city} ({flight.to.code})
              </div>
              <p className="text-xs text-slate-500 font-sans leading-relaxed">
                {flight.to.name}
                <br />
                {flight.to.terminal ? `Терминал ${flight.to.terminal}` : ''} {flight.to.gate ? `· Гейт ${flight.to.gate}` : ''}
              </p>
            </div>

          </div>

          {/* Telemetry / Live Flight Data Blocks */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4 pt-4 border-t border-slate-100">
            <div className="p-4 rounded-2xl bg-[#F8FCFF] border border-[#E2EEF8] space-y-1">
              <div className="flex items-center gap-1.5 text-slate-500 text-xs">
                <Gauge className="w-3.5 h-3.5 text-sky-600" />
                <span>Высота</span>
              </div>
              <p className="font-benzin-medium text-base sm:text-lg text-slate-950">
                {flight.altitude ? `${flight.altitude.toLocaleString('ru-RU')} м` : 'На земле'}
              </p>
            </div>

            <div className="p-4 rounded-2xl bg-[#F8FCFF] border border-[#E2EEF8] space-y-1">
              <div className="flex items-center gap-1.5 text-slate-500 text-xs">
                <Compass className="w-3.5 h-3.5 text-blue-600" />
                <span>Скорость</span>
              </div>
              <p className="font-benzin-medium text-base sm:text-lg text-slate-950">
                {flight.speed ? `${flight.speed} км/ч` : '0 км/ч'}
              </p>
            </div>

            <div className="p-4 rounded-2xl bg-[#F8FCFF] border border-[#E2EEF8] space-y-1">
              <div className="flex items-center gap-1.5 text-slate-500 text-xs">
                <CloudSun className="w-3.5 h-3.5 text-amber-600" />
                <span>Погода прилёта</span>
              </div>
              <p className="font-benzin-medium text-base sm:text-lg text-slate-950">+16°C, Ясно</p>
            </div>

            <div className="p-4 rounded-2xl bg-[#F8FCFF] border border-[#E2EEF8] space-y-1">
              <div className="flex items-center gap-1.5 text-slate-500 text-xs">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                <span>Безопасность</span>
              </div>
              <p className="font-benzin-medium text-base sm:text-lg text-emerald-700">Штатно</p>
            </div>
          </div>

          {/* Ticket Booking & Pricing Section */}
          <div className="p-6 rounded-[28px] bg-[#F8FCFF] border border-[#E2EEF8] space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#E2EEF8] pb-4">
              <div>
                <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block font-sans">
                  Стоимость перелёта
                </span>
                <div className="flex items-baseline gap-2 mt-0.5">
                  <span className="font-benzin-bold text-2xl sm:text-3xl text-slate-950">
                    {flight.price ? `${flight.price.toLocaleString('ru-RU')} ₽` : 'от 12 500 ₽'}
                  </span>
                  <span className="text-xs text-slate-500 font-sans">эконом-класс / в одну сторону</span>
                </div>
              </div>

              <div className="flex flex-wrap items-center gap-2.5">
                <a
                  href={`https://www.aviasales.ru/search/${flight.from.code || 'MOW'}${flight.to.code || 'LED'}1`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-black hover:bg-slate-800 text-white text-xs font-semibold shadow-sm transition-all hover:scale-[1.02]"
                >
                  <Ticket className="w-3.5 h-3.5" />
                  <span>Купить на Aviasales</span>
                  <ExternalLink className="w-3 h-3 text-white/70" />
                </a>

                <a
                  href={`https://travel.yandex.ru/avia/search/result/?fromName=${encodeURIComponent(flight.from.city)}&toName=${encodeURIComponent(flight.to.city)}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-4 py-2.5 rounded-full bg-white hover:bg-slate-50 border border-[#D5ECF8] text-slate-800 text-xs font-semibold shadow-xs transition-all"
                >
                  <span>Яндекс Путешествия</span>
                  <ExternalLink className="w-3 h-3 text-slate-400" />
                </a>
              </div>
            </div>

            {/* Data Source & External Verification Links */}
            <div className="pt-1 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs text-slate-500 font-sans">
              <div className="flex items-center gap-2">
                <Building2 className="w-3.5 h-3.5 text-sky-600 flex-shrink-0" />
                <span>
                  Источник статуса и телеметрии: 
                  <a
                    href="https://aviationstack.com/"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="font-semibold text-sky-600 hover:text-sky-800 hover:underline ml-1 inline-flex items-center gap-0.5"
                  >
                    <span>Aviationstack Global Flight API</span>
                    <ExternalLink className="w-2.5 h-2.5" />
                  </a>
                </span>
              </div>

              <div className="flex items-center gap-3">
                <a
                  href={`https://www.google.com/search?q=${encodeURIComponent('Авиакомпания ' + flight.airline + ' официальный сайт')}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-slate-500 hover:text-slate-800 hover:underline inline-flex items-center gap-1"
                >
                  <span>Сайт {flight.airline}</span>
                  <ExternalLink className="w-2.5 h-2.5 text-slate-400" />
                </a>
                <span>·</span>
                <a
                  href={`https://www.google.com/search?q=${encodeURIComponent('Аэропорт ' + flight.from.name + ' онлайн табло')}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-slate-500 hover:text-slate-800 hover:underline inline-flex items-center gap-1"
                >
                  <span>Табло {flight.from.code}</span>
                  <ExternalLink className="w-2.5 h-2.5 text-slate-400" />
                </a>
              </div>
            </div>
          </div>

        </div>

      </div>
    </div>
  );
};
