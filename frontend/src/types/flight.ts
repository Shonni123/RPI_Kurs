export type FlightStatus = 'scheduled' | 'boarding' | 'in_air' | 'delayed' | 'landed' | 'cancelled';

export interface Airport {
  code: string;       // SVO, LED, DXB, etc.
  name: string;       // Шереметьево, Пулково
  city: string;       // Москва, Санкт-Петербург
  terminal?: string;  // B, C, 1, 2
  gate?: string;      // 12A, 34
}

export interface Flight {
  id: string;
  flightNumber: string; // SU 1702
  airline: string;      // Аэрофлот, S7 Airlines, Emirates
  airlineLogo?: string;
  aircraft: string;     // Airbus A350-900, Boeing 787 Dreamliner
  from: Airport;
  to: Airport;
  departureTime: string; // 14:30
  arrivalTime: string;   // 18:45
  departureDate: string; // 2026-11-04
  duration: string;      // 4 ч 15 мин
  status: FlightStatus;
  statusText: string;    // Ожидает взлёта, В полёте, Прибыл
  altitude?: number;     // 10600 м
  speed?: number;        // 860 км/ч
  price?: number;        // 14 500 ₽
  isFavorite?: boolean;
  isRealApi?: boolean;
}

export interface FlightFiltersState {
  searchQuery: string;
  status: string;
  airline: string;
  sortBy: 'time' | 'price' | 'status';
}

