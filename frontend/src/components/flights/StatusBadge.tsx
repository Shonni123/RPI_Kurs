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
          bg: 'bg-sky-500/15',
          border: 'border-sky-500/30',
          text: 'text-sky-300',
          dot: 'bg-sky-400',
          defaultText: 'В полёте',
        };
      case 'boarding':
        return {
          bg: 'bg-purple-500/15',
          border: 'border-purple-500/30',
          text: 'text-purple-300',
          dot: 'bg-purple-400',
          defaultText: 'Посадка',
        };
      case 'delayed':
        return {
          bg: 'bg-amber-500/15',
          border: 'border-amber-500/30',
          text: 'text-amber-300',
          dot: 'bg-amber-400',
          defaultText: 'Задержан',
        };
      case 'landed':
        return {
          bg: 'bg-slate-500/15',
          border: 'border-slate-500/30',
          text: 'text-slate-300',
          dot: 'bg-slate-400',
          defaultText: 'Прибыл',
        };
      case 'cancelled':
        return {
          bg: 'bg-red-500/15',
          border: 'border-red-500/30',
          text: 'text-red-300',
          dot: 'bg-red-400',
          defaultText: 'Отменён',
        };
      case 'scheduled':
      default:
        return {
          bg: 'bg-emerald-500/15',
          border: 'border-emerald-500/30',
          text: 'text-emerald-300',
          dot: 'bg-emerald-400',
          defaultText: 'По расписанию',
        };
    }
  };

  const config = getBadgeConfig();

  return (
    <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-semibold border ${config.bg} ${config.border} ${config.text}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${config.dot} animate-pulse`} />
      <span>{statusText || config.defaultText}</span>
    </span>
  );
};

