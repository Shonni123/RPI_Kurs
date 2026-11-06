import React from 'react';

export const LoadingSkeleton: React.FC<{ count?: number }> = ({ count = 3 }) => {
  return (
    <div className="space-y-4 w-full">
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className="p-6 rounded-3xl bg-[#161F30]/60 border border-white/10 animate-pulse space-y-4"
        >
          <div className="flex items-center justify-between">
            <div className="h-6 w-32 bg-white/10 rounded-full" />
            <div className="h-6 w-24 bg-white/10 rounded-full" />
          </div>
          <div className="grid grid-cols-3 gap-4 py-2">
            <div className="space-y-2">
              <div className="h-4 w-16 bg-white/10 rounded" />
              <div className="h-8 w-24 bg-white/10 rounded" />
            </div>
            <div className="flex flex-col items-center justify-center space-y-2">
              <div className="h-2 w-full bg-white/10 rounded" />
              <div className="h-4 w-20 bg-white/10 rounded" />
            </div>
            <div className="space-y-2 text-right flex flex-col items-end">
              <div className="h-4 w-16 bg-white/10 rounded" />
              <div className="h-8 w-24 bg-white/10 rounded" />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

