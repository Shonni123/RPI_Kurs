import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

interface ErrorStateProps {
  message?: string;
  onRetry?: () => void;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  message = 'Произошла ошибка при загрузке данных о рейсах.',
  onRetry,
}) => {
  return (
    <div className="py-14 px-6 text-center max-w-md mx-auto rounded-[28px] bg-white border border-rose-200 space-y-4 shadow-sm">
      <div className="w-14 h-14 rounded-2xl bg-rose-50 border border-rose-200 text-rose-500 flex items-center justify-center mx-auto">
        <AlertTriangle className="w-7 h-7" />
      </div>
      <h3 className="font-benzin-bold text-base sm:text-lg text-slate-950 uppercase tracking-tight">
        Ошибка получения данных
      </h3>
      <p className="text-xs sm:text-sm text-slate-600 font-tt-travels leading-relaxed">
        {message}
      </p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-black hover:bg-slate-800 text-white text-xs font-semibold shadow-sm transition-all hover:scale-102 cursor-pointer"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Повторить попытку</span>
        </button>
      )}
    </div>
  );
};
