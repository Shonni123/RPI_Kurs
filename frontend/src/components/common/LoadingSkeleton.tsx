import React from 'react';

export const LoadingSkeleton: React.FC<{ count?: number }> = ({ count = 3 }) => {
  return (
    <div className="space-y-4 w-full">
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className="p-6 rounded-[26px] bg-white border border-[#E2EEF8] animate-pulse space-y-4 shadow-sm"
        >
          <div className="flex items-center justify-between">
            <div className="h-6 w-36 bg-slate-100 rounded-full" />
            <div className="h-6 w-24 bg-slate-100 rounded-full" />
          </div>
          <div className="grid grid-cols-3 gap-4 py-3">
            <div className="space-y-2">
              <div className="h-7 w-28 bg-slate-100 rounded-lg" />
              <div className="h-4 w-20 bg-slate-100 rounded" />
            </div>
            <div className="flex flex-col items-center justify-center space-y-2">
              <div className="h-2 w-full bg-slate-100 rounded-full" />
              <div className="h-4 w-16 bg-slate-100 rounded" />
            </div>
            <div className="space-y-2 text-right flex flex-col items-end">
              <div className="h-7 w-28 bg-slate-100 rounded-lg" />
              <div className="h-4 w-20 bg-slate-100 rounded" />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};
