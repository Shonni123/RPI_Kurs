import React from 'react';
import { ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';
import { MOCK_FLIGHTS } from '../services/mockFlights';
import { FlightCard } from '../components/flights/FlightCard';
import { EmptyState } from '../components/common/EmptyState';
import { useFavorites } from '../hooks/useFavorites';

export const FavoritesPage: React.FC = () => {
  const { favoriteIds, toggleFavorite, isFavorite } = useFavorites();

  const favoriteFlights = MOCK_FLIGHTS.filter((f) => favoriteIds.includes(f.id));

  return (
    <div className="min-h-screen pt-28 pb-20 px-4 sm:px-6 lg:px-8 bg-[#0B0F19] text-white">
      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 border-b border-white/10 pb-6">
          <div>
            <span className="text-xs font-semibold tracking-widest text-rose-400 uppercase">
              Личные закладки
            </span>
            <h1 className="font-display font-black text-2xl sm:text-4xl uppercase tracking-tight text-white mt-1">
              Избранные рейсы
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 mt-1">
              Отслеживайте важные для вас рейсы без необходимости постоянного поиска.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Link
              to="/flights"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 hover:bg-white/10 border border-white/10 text-xs text-slate-300 transition-colors"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>К поиску рейсов</span>
            </Link>
          </div>
        </div>

        {/* List or Empty State */}
        {favoriteFlights.length === 0 ? (
          <EmptyState
            title="У вас пока нет сохранённых рейсов"
            description="Чтобы отслеживать рейс, нажмите на иконку сердечка в карточке любого рейса на онлайн-табло."
            actionText="Перейти к табло рейсов"
            actionLink="/flights"
          />
        ) : (
          <div className="space-y-4">
            <div className="flex items-center justify-between text-xs text-slate-400 px-2">
              <span>Сохранено рейсов: <strong className="text-white">{favoriteFlights.length}</strong></span>
              <span>Сохраняется локально в браузере</span>
            </div>

            <div className="grid grid-cols-1 gap-4">
              {favoriteFlights.map((flight) => (
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
