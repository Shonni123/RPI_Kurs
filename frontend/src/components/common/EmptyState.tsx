import React from 'react';
import { PlaneTakeoff } from 'lucide-react';
import { Link } from 'react-router-dom';

interface EmptyStateProps {
  title?: string;
  description?: string;
  actionText?: string;
  actionLink?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title = 'Рейсы не найдены',
  description = 'По вашему запросу нет активных рейсов. Попробуйте изменить параметры поиска или фильтры.',
  actionText,
  actionLink,
}) => {
  return (
    <div className="py-16 px-6 text-center max-w-md mx-auto rounded-3xl bg-[#161F30]/60 border border-white/10 space-y-4">
      <div className="w-14 h-14 rounded-2xl bg-blue-500/10 border border-blue-500/20 text-blue-400 flex items-center justify-center mx-auto">
        <PlaneTakeoff className="w-7 h-7" />
      </div>
      <h3 className="font-display font-bold text-lg text-white">
        {title}
      </h3>
      <p className="text-xs sm:text-sm text-slate-300">
        {description}
      </p>
      {actionText && actionLink && (
        <Link
          to={actionLink}
          className="inline-flex items-center gap-2 px-6 py-2.5 rounded-full bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold shadow-lg shadow-blue-600/30 transition-all hover:scale-102"
        >
          {actionText}
        </Link>
      )}
    </div>
  );
};

