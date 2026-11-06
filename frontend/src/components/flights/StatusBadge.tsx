import React from 'react';
import { FlightStatus } from '../../types/flight';

interface StatusBadgeProps {
  status: FlightStatus;
  statusText?: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, statusText }) => {
  const getBadgeConfig = () => {
    switch (status) {
      case 'in_air':
        return {
          bg: 'bg-sky-50',
          border: 'border-sky-200',
          text: 'text-sky-700',
          dot: 'bg-sky-500',
          defaultText: 'В полёте',
        };
      case 'boarding':
        return {
          bg: 'bg-purple-50',
          border: 'border-purple-200',
          text: 'text-purple-700',
          dot: 'bg-purple-500',
          defaultText: 'Посадка',
        };
      case 'delayed':
        return {
          bg: 'bg-amber-50',
          border: 'border-amber-200',
          text: 'text-amber-800',
          dot: 'bg-amber-500',
          defaultText: 'Задержан',
        };
      case 'landed':
        return {
          bg: 'bg-emerald-50',
          border: 'border-emerald-200',
          text: 'text-emerald-700',
          dot: 'bg-emerald-500',
          defaultText: 'Прибыл',
        };
      case 'cancelled':
        return {
          bg: 'bg-rose-50',
          border: 'border-rose-200',
          text: 'text-rose-700',
          dot: 'bg-rose-500',
          defaultText: 'Отменён',
        };
      case 'scheduled':
      default:
        return {
          bg: 'bg-blue-50',
          border: 'border-blue-200',
          text: 'text-blue-700',
          dot: 'bg-blue-500',
          defaultText: 'По расписанию',
        };
    }
  };

  const config = getBadgeConfig();

  return (
    <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-semibold border ${config.bg} ${config.border} ${config.text} shadow-xs whitespace-nowrap`}>
      <span className={`w-1.5 h-1.5 rounded-full ${config.dot} animate-pulse`} />
      <span>{statusText || config.defaultText}</span>
    </span>
  );
};
