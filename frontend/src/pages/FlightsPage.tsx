import React, { useState, useMemo, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Search, RefreshCw } from 'lucide-react';
import { MOCK_FLIGHTS } from '../services/mockFlights';
import { FlightCard } from '../components/flights/FlightCard';
import { LoadingSkeleton } from '../components/common/LoadingSkeleton';
import { ErrorState } from '../components/common/ErrorState';
import { EmptyState } from '../components/common/EmptyState';
import { useFavorites } from '../hooks/useFavorites';

export const FlightsPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialStatus = searchParams.get('status') || 'all';

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedStatus, setSelectedStatus] = useState<string>(initialStatus);
  const [selectedAirline, setSelectedAirline] = useState<string>('all');
  const [sortBy, setSortBy] = useState<'time' | 'price'>('time');

  // Simulated Async Loading & Error states for coursework requirements
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);

  const { isFavorite, toggleFavorite } = useFavorites();

  useEffect(() => {
    // Simulate real network fetch
    setIsLoading(true);
    setHasError(false);
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 400);
    return () => clearTimeout(timer);
  }, [selectedStatus, selectedAirline]);

  const airlines = useMemo(() => {
    return ['all', ...Array.from(new Set(MOCK_FLIGHTS.map((f) => f.airline)))];
  }, []);

  const statuses = [
    { key: 'all', label: 'Все рейсы' },
    { key: 'in_air', label: 'В полёте' },
    { key: 'scheduled', label: 'Ожидает взлёта' },
    { key: 'delayed', label: 'Задержаны' },
    { key: 'landed', label: 'Прибыли' },
  ];

  const filteredFlights = useMemo(() => {
    let result = [...MOCK_FLIGHTS];

    // Status filter
    if (selectedStatus !== 'all') {
      result = result.filter((f) => f.status === selectedStatus);
    }

    // Airline filter
    if (selectedAirline !== 'all') {
      result = result.filter((f) => f.airline === selectedAirline);
    }

    // Search query filter (flightNumber, from city/code, to city/code)
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase().trim();
      result = result.filter(
        (f) =>
          f.flightNumber.toLowerCase().includes(q) ||
          f.from.city.toLowerCase().includes(q) ||
          f.from.code.toLowerCase().includes(q) ||
          f.to.city.toLowerCase().includes(q) ||
          f.to.code.toLowerCase().includes(q) ||
          f.aircraft.toLowerCase().includes(q)
      );
    }

    // Sort
    result.sort((a, b) => {
      if (sortBy === 'price') {
        return (a.price || 0) - (b.price || 0);
      }
      return a.departureTime.localeCompare(b.departureTime);
    });

    return result;
  }, [searchQuery, selectedStatus, selectedAirline, sortBy]);

  return (
    <div className="min-h-screen pt-28 pb-20 px-4 sm:px-6 lg:px-8 bg-[#0B0F19] text-white">
      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 border-b border-white/10 pb-6">
          <div>
            <span className="text-xs font-semibold tracking-widest text-blue-400 uppercase">
              Мониторинг рейсов
            </span>
            <h1 className="font-display font-black text-2xl sm:text-4xl uppercase tracking-tight text-white mt-1">
              Онлайн-табло авиарейсов
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 mt-1">
              Актуальные данные о статусах, гейтах и времени вылета в реальном времени.
            </p>
          </div>

          <button
            onClick={() => {
              setIsLoading(true);
              setTimeout(() => setIsLoading(false), 300);
            }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 hover:bg-white/10 border border-white/10 text-xs text-slate-300 transition-all self-start sm:self-auto"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />
            <span>Обновить табло</span>
          </button>
        </div>

        {/* Search & Filter Bar */}
        <div className="p-6 rounded-3xl bg-[#161F30]/70 border border-white/10 space-y-5">
          
          {/* Search Input */}
          <div className="relative">
            <Search className="w-5 h-5 text-slate-400 absolute top-1/2 left-4 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Поиск по номеру рейса, городу, аэропорту (например: SU 1702, Москва, SVO)..."
              className="w-full pl-12 pr-4 py-3.5 rounded-2xl bg-black/40 border border-white/10 text-white placeholder:text-slate-400 text-xs sm:text-sm focus:outline-none focus:border-blue-500 transition-colors"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute top-1/2 right-4 -translate-y-1/2 text-xs text-slate-400 hover:text-white"
              >
                Очистить
              </button>
            )}
          </div>

          {/* Filter Pills & Selectors */}
          <div className="flex flex-wrap items-center justify-between gap-4">
            
            {/* Status Pills */}
            <div className="flex flex-wrap items-center gap-2">
              {statuses.map((s) => (
                <button
                  key={s.key}
                  onClick={() => {
                    setSelectedStatus(s.key);
                    setSearchParams(s.key === 'all' ? {} : { status: s.key });
                  }}
                  className={`px-4 py-2 rounded-full text-xs font-semibold transition-all ${
                    selectedStatus === s.key
                      ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/30'
                      : 'bg-white/5 hover:bg-white/10 text-slate-300'
                  }`}
                >
                  {s.label}
                </button>
              ))}
            </div>

            {/* Airline Dropdown & Sort */}
            <div className="flex items-center gap-3 w-full sm:w-auto">
              <select
                value={selectedAirline}
                onChange={(e) => setSelectedAirline(e.target.value)}
                className="px-4 py-2 rounded-full bg-black/40 border border-white/10 text-xs text-slate-200 focus:outline-none focus:border-blue-500"
              >
                <option value="all">Все авиакомпании</option>
                {airlines.filter((a) => a !== 'all').map((airline) => (
                  <option key={airline} value={airline}>
                    {airline}
                  </option>
                ))}
              </select>

              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as 'time' | 'price')}
                className="px-4 py-2 rounded-full bg-black/40 border border-white/10 text-xs text-slate-200 focus:outline-none focus:border-blue-500"
              >
                <option value="time">По времени</option>
                <option value="price">По цене</option>
              </select>
            </div>

          </div>
        </div>

        {/* Results Area with Loading, Error, Empty & List States */}
        {isLoading ? (
          <LoadingSkeleton count={4} />
        ) : hasError ? (
          <ErrorState onRetry={() => setIsLoading(true)} />
        ) : filteredFlights.length === 0 ? (
          <EmptyState
            title="Рейсы не найдены"
            description="Попробуйте сбросить фильтры или ввести другой поисковый запрос."
            actionText="Сбросить фильтры"
            actionLink="/flights"
          />
        ) : (
          <div className="space-y-4">
            <div className="flex items-center justify-between text-xs text-slate-400 px-2">
              <span>Найдено рейсов: <strong className="text-white">{filteredFlights.length}</strong></span>
              <span>Обновление в реальном времени</span>
            </div>

            <div className="grid grid-cols-1 gap-4">
              {filteredFlights.map((flight) => (
                <FlightCard
                  key={flight.id}
                  flight={flight}
                  isFavorite={isFavorite(flight.id)}
                  onToggleFavorite={toggleFavorite}
                />
              ))}
            </div>
          </div>
        )}

      </div>
    </div>
  );
};
