import React, { useState, useMemo, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { Search, RefreshCw, Heart, X, SlidersHorizontal, ArrowLeft, Radio, Globe, CheckCircle } from 'lucide-react';
import { Flight } from '../types/flight';
import { MOCK_FLIGHTS } from '../services/mockFlights';
import { flightApi } from '../services/api';
import { FlightCard } from '../components/flights/FlightCard';
import { LoadingSkeleton } from '../components/common/LoadingSkeleton';
import { ErrorState } from '../components/common/ErrorState';
import { EmptyState } from '../components/common/EmptyState';
import { useFavorites } from '../hooks/useFavorites';

export const FlightsPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialStatus = searchParams.get('status') || 'all';

  const [flights, setFlights] = useState<Flight[]>(MOCK_FLIGHTS);
  const [isLiveServer, setIsLiveServer] = useState(false);
  const [isSyncing, setIsSyncing] = useState(false);
  const [syncMessage, setSyncMessage] = useState<string | null>(null);

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedStatus, setSelectedStatus] = useState<string>(initialStatus);
  const [selectedAirline, setSelectedAirline] = useState<string>('all');
  const [sortBy, setSortBy] = useState<'time' | 'price'>('time');
  const [lastUpdated, setLastUpdated] = useState<string>('только что');

  // Loading & Error states
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);

  const { favorites, isFavorite, toggleFavorite } = useFavorites();

  const loadFlightsData = async () => {
    setIsLoading(true);
    setHasError(false);
    try {
      const res = await flightApi.getFlights();
      setFlights(res.flights);
      setIsLiveServer(res.isLiveServer);
      const now = new Date();
      setLastUpdated(`${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`);
    } catch {
      setHasError(true);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadFlightsData();
  }, []);

  // Status counts based on loaded flights
  const statusCounts = useMemo(() => {
    const counts: Record<string, number> = {
      all: flights.length,
      in_air: 0,
      scheduled: 0,
      delayed: 0,
      landed: 0,
    };
    flights.forEach((f) => {
      if (counts[f.status] !== undefined) {
        counts[f.status]++;
      }
    });
    return counts;
  }, [flights]);

  const airlines = useMemo(() => {
    return ['all', ...Array.from(new Set(flights.map((f) => f.airline)))];
  }, [flights]);

  const statuses = [
    { key: 'all', label: 'Все рейсы', count: statusCounts.all },
    { key: 'in_air', label: 'В полёте', count: statusCounts.in_air },
    { key: 'scheduled', label: 'Ожидают взлёта', count: statusCounts.scheduled },
    { key: 'delayed', label: 'Задержаны', count: statusCounts.delayed },
    { key: 'landed', label: 'Прибыли', count: statusCounts.landed },
  ];

  const handleRefresh = () => {
    loadFlightsData();
  };

  const handleSyncAviationstack = async () => {
    setIsSyncing(true);
    setSyncMessage(null);
    const res = await flightApi.syncAviationstack(15);
    setIsSyncing(false);
    if (res.success) {
      setSyncMessage(res.message || 'Синхронизировано из Aviationstack API!');
      loadFlightsData();
      setTimeout(() => setSyncMessage(null), 5000);
    } else {
      setSyncMessage(res.error || 'Ошибка синхронизации с API');
      setTimeout(() => setSyncMessage(null), 5000);
    }
  };

  const handleResetFilters = () => {
    setSearchQuery('');
    setSelectedStatus('all');
    setSelectedAirline('all');
    setSortBy('time');
    setSearchParams({});
  };

  const hasActiveFilters = searchQuery.trim() !== '' || selectedStatus !== 'all' || selectedAirline !== 'all' || sortBy !== 'time';

  const filteredFlights = useMemo(() => {
    let result = [...flights];

    // Status filter
    if (selectedStatus !== 'all') {
      result = result.filter((f) => f.status === selectedStatus);
    }

    // Airline filter
    if (selectedAirline !== 'all') {
      result = result.filter((f) => f.airline === selectedAirline);
    }

    // Search query filter (flightNumber, from city/code, to city/code, aircraft)
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase().trim();
      result = result.filter(
        (f) =>
          f.flightNumber.toLowerCase().includes(q) ||
          f.from.city.toLowerCase().includes(q) ||
          f.from.code.toLowerCase().includes(q) ||
          f.to.city.toLowerCase().includes(q) ||
          f.to.code.toLowerCase().includes(q) ||
          f.airline.toLowerCase().includes(q) ||
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
  }, [flights, searchQuery, selectedStatus, selectedAirline, sortBy]);

  return (
    <div className="min-h-screen bg-[#F8FCFF] text-slate-900 pt-6 sm:pt-8 pb-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto space-y-6 sm:space-y-8">
        
        {/* Top Breadcrumb & Favorites Shortcut */}
        <div className="flex items-center justify-between text-xs font-semibold">
          <Link
            to="/"
            className="inline-flex items-center gap-1.5 text-slate-600 hover:text-slate-950 transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Вернуться на главную</span>
          </Link>

          <Link
            to="/favorites"
            className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-white border border-[#E2EEF8] text-slate-700 hover:text-rose-600 hover:border-rose-200 transition-all shadow-xs"
          >
            <Heart className={`w-3.5 h-3.5 ${favorites.length > 0 ? 'fill-rose-500 text-rose-500' : 'text-slate-400'}`} />
            <span>Избранное</span>
            <span className="w-5 h-5 rounded-full bg-slate-100 text-slate-900 text-[11px] font-bold flex items-center justify-center">
              {favorites.length}
            </span>
          </Link>
        </div>

        {/* Header with real API connection indicator */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-[#E2EEF8] pb-6">
          <div>
            <div className="flex flex-wrap items-center gap-2 mb-2">
              <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#EFF7FE] border border-[#D5ECF8] text-[11px] font-semibold text-sky-700">
                <span className="w-1.5 h-1.5 rounded-full bg-sky-500 animate-pulse" />
                <span>ОНЛАЙН-МОНИТОРИНГ РЕЙСОВ</span>
              </div>

              {isLiveServer ? (
                <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-[11px] font-semibold text-emerald-700">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                  <span>Django REST API + Aviationstack</span>
                </div>
              ) : (
                <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-100 border border-slate-200 text-[11px] font-medium text-slate-600">
                  <Radio className="w-3 h-3 text-slate-400" />
                  <span>Локальный кэш</span>
                </div>
              )}
            </div>

            <h1 className="font-benzin-bold text-2xl sm:text-3xl lg:text-4xl uppercase tracking-tight text-slate-950">
              Табло авиарейсов
            </h1>
            <p className="font-tt-travels text-xs sm:text-sm text-slate-600 mt-1.5 max-w-xl">
              Точные статусы вылетов, прибытий, терминалов и гейтов. Данные синхронизируются с сервером Django и мировым API Aviationstack.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2.5">
            <span className="text-[11px] text-slate-500 hidden sm:inline">
              Обновлено: {lastUpdated}
            </span>

            {/* Sync Aviationstack Button */}
            <button
              onClick={handleSyncAviationstack}
              disabled={isSyncing}
              className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-full bg-[#EFF7FE] hover:bg-[#DDF2FD] border border-[#D5ECF8] text-xs font-semibold text-sky-800 transition-all shadow-xs cursor-pointer disabled:opacity-60"
              title="Запросить свежие реальные рейсы через сервер Django"
            >
              <Globe className={`w-3.5 h-3.5 text-sky-600 ${isSyncing ? 'animate-spin' : ''}`} />
              <span>{isSyncing ? 'Синхронизация API...' : 'Подтянуть API'}</span>
            </button>

            <button
              onClick={handleRefresh}
              disabled={isLoading}
              className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-full bg-white hover:bg-slate-50 border border-[#D5ECF8] text-xs font-semibold text-slate-800 transition-all shadow-xs cursor-pointer disabled:opacity-60"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin text-sky-600' : 'text-slate-600'}`} />
              <span>Обновить</span>
            </button>
          </div>
        </div>

        {/* Sync notification message banner */}
        {syncMessage && (
          <div className="p-3.5 rounded-2xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-medium flex items-center justify-between animate-fadeIn">
            <div className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-emerald-600 flex-shrink-0" />
              <span>{syncMessage}</span>
            </div>
            <button onClick={() => setSyncMessage(null)} className="text-emerald-600 hover:text-emerald-900">
              <X className="w-4 h-4" />
            </button>
          </div>
        )}

        {/* Search & Filter Control Card */}
        <div className="p-5 sm:p-6 rounded-[28px] bg-white border border-[#E2EEF8] shadow-sm space-y-4">
          
          {/* Search Input Bar */}
          <div className="relative w-full">
            <Search className="w-4 h-4 sm:w-5 sm:h-5 text-slate-400 absolute top-1/2 left-4 sm:left-5 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Поиск рейса: номер (SU 1702, QF7343), город (Москва, Сочи, Дубай, Сидней) или код аэропорта (SVO, MEL)..."
              className="w-full pl-11 sm:pl-13 pr-10 py-3 sm:py-3.5 rounded-2xl bg-[#F8FCFF] border border-[#E2EEF8] text-slate-900 placeholder:text-slate-400 text-xs sm:text-sm focus:outline-none focus:border-sky-400 focus:bg-white transition-all font-sans"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute top-1/2 right-4 -translate-y-1/2 text-slate-400 hover:text-slate-700 p-1 cursor-pointer"
                title="Очистить"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>

          {/* Filter Pills & Selectors */}
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pt-1">
            
            {/* Status Pills */}
            <div className="flex flex-wrap items-center gap-2">
              {statuses.map((s) => {
                const isActive = selectedStatus === s.key;
                return (
                  <button
                    key={s.key}
                    onClick={() => {
                      setSelectedStatus(s.key);
                      setSearchParams(s.key === 'all' ? {} : { status: s.key });
                    }}
                    className={`px-3.5 sm:px-4 py-1.5 sm:py-2 rounded-full text-xs font-semibold transition-all duration-200 cursor-pointer flex items-center gap-1.5 whitespace-nowrap ${
                      isActive
                        ? 'bg-black text-white shadow-sm scale-[1.02]'
                        : 'bg-[#ECF9FF] hover:bg-[#DDF2FD] text-slate-700 border border-[#D5ECF8]'
                    }`}
                  >
                    <span>{s.label}</span>
                    <span className={`text-[10px] px-1.5 py-0.2 rounded-full ${isActive ? 'bg-white/20 text-white' : 'bg-white text-slate-600'}`}>
                      {s.count}
                    </span>
                  </button>
                );
              })}
            </div>

            {/* Dropdowns for Airlines & Sorting */}
            <div className="flex items-center gap-2.5 w-full lg:w-auto">
              <div className="flex-1 lg:flex-initial">
                <select
                  value={selectedAirline}
                  onChange={(e) => setSelectedAirline(e.target.value)}
                  className="w-full lg:w-auto px-4 py-2 rounded-full bg-[#ECF9FF] border border-[#D5ECF8] text-xs font-semibold text-slate-800 focus:outline-none focus:border-sky-400 cursor-pointer"
                >
                  <option value="all">Все авиакомпании</option>
                  {airlines.filter((a) => a !== 'all').map((airline) => (
                    <option key={airline} value={airline}>
                      {airline}
                    </option>
                  ))}
                </select>
              </div>

              <div className="flex-1 lg:flex-initial">
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value as 'time' | 'price')}
                  className="w-full lg:w-auto px-4 py-2 rounded-full bg-[#ECF9FF] border border-[#D5ECF8] text-xs font-semibold text-slate-800 focus:outline-none focus:border-sky-400 cursor-pointer"
                >
                  <option value="time">По времени вылета</option>
                  <option value="price">По цене билета</option>
                </select>
              </div>
            </div>

          </div>

          {/* Active Filter Indicators Bar */}
          {hasActiveFilters && (
            <div className="flex items-center justify-between pt-2 border-t border-slate-100 text-xs">
              <div className="flex items-center gap-2 text-slate-600">
                <SlidersHorizontal className="w-3.5 h-3.5 text-sky-600" />
                <span>Активны фильтры поиска</span>
              </div>
              <button
                onClick={handleResetFilters}
                className="text-xs font-semibold text-sky-600 hover:text-sky-800 underline cursor-pointer"
              >
                Сбросить всё
              </button>
            </div>
          )}

        </div>

        {/* Results Area with Loading, Error, Empty & List States */}
        {isLoading ? (
          <LoadingSkeleton count={4} />
        ) : hasError ? (
          <ErrorState onRetry={loadFlightsData} />
        ) : filteredFlights.length === 0 ? (
          <EmptyState
            title="Рейсы не найдены"
            description="По заданным критериям поиска рейсов не обнаружено. Попробуйте сбросить фильтры или изменить поисковый запрос."
            actionText="Сбросить фильтры"
            onReset={handleResetFilters}
          />
        ) : (
          <div className="space-y-4">
            <div className="flex items-center justify-between text-xs text-slate-600 px-1">
              <span>
                Найдено рейсов: <strong className="text-slate-950 font-bold">{filteredFlights.length}</strong>
              </span>
              <span className="text-[11px] text-slate-400 hidden sm:inline">
                Нажмите на рейс для подробной информации о маршруте и самолёте
              </span>
            </div>

            <div className="grid grid-cols-1 gap-3.5 sm:gap-4">
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
