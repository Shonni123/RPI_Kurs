import React from 'react';
import { Plane, Compass, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';

export const NotFoundPage: React.FC = () => {
  return (
    <div className="min-h-screen pt-20 pb-20 px-4 flex items-center justify-center bg-[#F8FCFF] text-slate-900">
      <div className="max-w-md w-full text-center p-8 sm:p-10 rounded-[32px] bg-white border border-[#E2EEF8] space-y-6 shadow-sm">
        
        {/* Plane icon with radar circle */}
        <div className="relative w-20 h-20 mx-auto rounded-full bg-[#EFF7FE] border border-[#D5ECF8] flex items-center justify-center text-sky-600">
          <Plane className="w-10 h-10 -rotate-45" />
          <div className="absolute inset-0 rounded-full border border-sky-400/40 animate-ping pointer-events-none" />
        </div>

        <div className="space-y-2">
          <span className="font-benzin-bold text-6xl sm:text-7xl text-slate-950 tracking-tight block">
            404
          </span>
          <h2 className="font-benzin-medium text-lg sm:text-xl text-slate-950 uppercase tracking-tight">
            Маршрут отклонился от курса
          </h2>
          <p className="font-tt-travels text-xs sm:text-sm text-slate-600 leading-relaxed">
            Запрашиваемая страница не существует или была перемещена в другой терминал.
          </p>
        </div>

        <div className="pt-2 flex flex-col sm:flex-row items-center justify-center gap-3">
          <Link
            to="/"
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 rounded-full bg-black hover:bg-slate-800 text-white text-xs font-semibold shadow-sm transition-all hover:scale-102"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>На главную</span>
          </Link>

          <Link
            to="/flights"
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 rounded-full bg-[#ECF9FF] hover:bg-[#DDF2FD] border border-[#D5ECF8] text-slate-800 text-xs font-semibold transition-all"
          >
            <Compass className="w-4 h-4 text-sky-600" />
            <span>Онлайн-табло</span>
          </Link>
        </div>

      </div>
    </div>
  );
};
