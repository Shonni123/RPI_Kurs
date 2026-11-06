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
    <div className="py-16 px-6 text-center max-w-md mx-auto rounded-3xl bg-[#161F30]/60 border border-red-500/20 space-y-4">
      <div className="w-14 h-14 rounded-2xl bg-red-500/10 border border-red-500/20 text-red-400 flex items-center justify-center mx-auto">
        <AlertTriangle className="w-7 h-7" />
      </div>
      <h3 className="font-display font-bold text-lg text-white">
        Ошибка получения данных
      </h3>
      <p className="text-xs sm:text-sm text-slate-300">
        {message}
      </p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold shadow-lg shadow-blue-600/30 transition-all hover:scale-102"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Повторить попытку</span>
        </button>
      )}
    </div>
  );
};

