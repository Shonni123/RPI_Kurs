import React from 'react';
import { Plane, Compass, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';

export const NotFoundPage: React.FC = () => {
  return (
    <div className="min-h-screen pt-32 pb-20 px-4 flex items-center justify-center bg-[#0B0F19] text-white">
      <div className="max-w-md w-full text-center p-8 rounded-3xl bg-[#161F30]/80 border border-white/10 space-y-6 shadow-2xl">
        
        {/* Plane icon with radar circle */}
        <div className="relative w-24 h-24 mx-auto rounded-full bg-blue-600/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
          <Plane className="w-12 h-12 -rotate-45" />
          <div className="absolute inset-0 rounded-full border border-blue-400/30 animate-ping pointer-events-none" />
        </div>

        <div className="space-y-2">
          <span className="font-display font-black text-6xl sm:text-7xl text-blue-500 tracking-tight">
            404
          </span>
          <h2 className="font-display font-bold text-xl text-white">
            Маршрут отклонился от курса
          </h2>
          <p className="text-xs sm:text-sm text-slate-400 leading-relaxed">
            Запрашиваемая страница не существует или была перемещена в другой терминал.
          </p>
        </div>

        <div className="pt-2 flex flex-col sm:flex-row items-center justify-center gap-3">
          <Link
            to="/"
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 rounded-full bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold shadow-lg shadow-blue-600/30 transition-all hover:scale-102"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>На главную страницу</span>
          </Link>

          <Link
            to="/flights"
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 rounded-full bg-white/5 hover:bg-white/10 border border-white/10 text-white text-xs font-semibold transition-all"
          >
            <Compass className="w-4 h-4 text-blue-400" />
            <span>Онлайн-табло</span>
          </Link>
        </div>

      </div>
    </div>
  );
};

