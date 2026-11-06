import React from 'react';
import { PlaneTakeoff, RotateCcw } from 'lucide-react';
import { Link } from 'react-router-dom';

interface EmptyStateProps {
  title?: string;
  description?: string;
  actionText?: string;
  actionLink?: string;
  onReset?: () => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title = 'Рейсы не найдены',
  description = 'По вашему запросу нет активных рейсов. Попробуйте изменить параметры поиска или фильтры.',
  actionText,
  actionLink,
  onReset,
}) => {
  return (
    <div className="py-14 px-6 text-center max-w-md mx-auto rounded-[28px] bg-white border border-[#E2EEF8] space-y-4 shadow-sm">
      <div className="w-14 h-14 rounded-2xl bg-[#EFF7FE] border border-[#D5ECF8] text-sky-600 flex items-center justify-center mx-auto">
        <PlaneTakeoff className="w-7 h-7" />
      </div>
      <h3 className="font-benzin-bold text-base sm:text-lg text-slate-950 uppercase tracking-tight">
        {title}
      </h3>
      <p className="text-xs sm:text-sm text-slate-600 font-tt-travels leading-relaxed">
        {description}
      </p>
      {onReset && (
        <button
          onClick={onReset}
          className="inline-flex items-center gap-2 px-6 py-2.5 rounded-full bg-black hover:bg-slate-800 text-white text-xs font-semibold shadow-sm transition-all hover:scale-102 cursor-pointer"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>{actionText || 'Сбросить фильтры'}</span>
        </button>
      )}
      {!onReset && actionText && actionLink && (
        <Link
          to={actionLink}
          className="inline-flex items-center gap-2 px-6 py-2.5 rounded-full bg-black hover:bg-slate-800 text-white text-xs font-semibold shadow-sm transition-all hover:scale-102 cursor-pointer"
        >
          {actionText}
        </Link>
      )}
    </div>
  );
};
