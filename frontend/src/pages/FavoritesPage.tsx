import React from 'react';
import { ArrowLeft, Heart } from 'lucide-react';
import { Link } from 'react-router-dom';
import { MOCK_FLIGHTS } from '../services/mockFlights';
import { FlightCard } from '../components/flights/FlightCard';
import { EmptyState } from '../components/common/EmptyState';
import { useFavorites } from '../hooks/useFavorites';

export const FavoritesPage: React.FC = () => {
  const { favorites, toggleFavorite, isFavorite } = useFavorites();

  const favoriteFlights = MOCK_FLIGHTS.filter((f) => favorites.includes(f.id));

  return (
    <div className="min-h-screen bg-[#F8FCFF] text-slate-900 pt-6 sm:pt-8 pb-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto space-y-6 sm:space-y-8">
        
        {/* Navigation Breadcrumb */}
        <div className="flex items-center justify-between">
          <Link
            to="/flights"
            className="inline-flex items-center gap-2 text-xs font-semibold text-slate-600 hover:text-slate-950 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Назад к поиску рейсов</span>
          </Link>
        </div>

        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 border-b border-[#E2EEF8] pb-6">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-50 border border-rose-200 text-[11px] font-semibold text-rose-700 mb-2">
              <Heart className="w-3 h-3 fill-rose-500 text-rose-500" />
              <span>ЛИЧНЫЕ ЗАКЛАДКИ</span>
            </div>
            <h1 className="font-benzin-bold text-2xl sm:text-3xl lg:text-4xl uppercase tracking-tight text-slate-950">
              Избранные рейсы
            </h1>
            <p className="font-tt-travels text-xs sm:text-sm text-slate-600 mt-1.5 max-w-xl">
              Быстрый доступ к сохранённым рейсам для оперативного отслеживания статуса вылета и прилёта.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-500 font-sans">
              Сохранено: <strong className="font-benzin-medium text-slate-950">{favoriteFlights.length}</strong>
            </span>
          </div>
        </div>

        {/* List or Empty State */}
        {favoriteFlights.length === 0 ? (
          <EmptyState
            title="У вас пока нет сохранённых рейсов"
            description="Чтобы отслеживать важный рейс, нажмите на иконку сердечка в карточке любого рейса на онлайн-табло."
            actionText="Перейти к табло рейсов"
            actionLink="/flights"
          />
        ) : (
          <div className="space-y-4">
            <div className="flex items-center justify-between text-xs text-slate-500 px-1">
              <span>Сохранено рейсов: <strong className="text-slate-950 font-bold">{favoriteFlights.length}</strong></span>
              <span>Данные сохраняются в памяти вашего браузера</span>
            </div>

            <div className="grid grid-cols-1 gap-3.5 sm:gap-4">
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
