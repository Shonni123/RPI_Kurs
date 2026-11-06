import { Flight } from '../types/flight';

export const MOCK_FLIGHTS: Flight[] = [
  {
    id: 'su-1702',
    flightNumber: 'SU 1702',
    airline: 'Аэрофлот',
    aircraft: 'Airbus A350-900',
    from: {
      code: 'SVO',
      name: 'Шереметьево',
      city: 'Москва',
      terminal: 'B',
      gate: '115'
    },
    to: {
      code: 'VVO',
      name: 'Кневичи',
      city: 'Владивосток',
      terminal: 'A',
      gate: '04'
    },
    departureTime: '15:40',
    arrivalTime: '07:15',
    departureDate: '2026-11-04',
    duration: '8 ч 35 мин',
    status: 'in_air',
    statusText: 'В полёте',
    altitude: 10800,
    speed: 890,
    price: 18400,
  },
  {
    id: 's7-2041',
    flightNumber: 'S7 2041',
    airline: 'S7 Airlines',
    aircraft: 'Boeing 737-800',
    from: {
      code: 'DME',
      name: 'Домодедово',
      city: 'Москва',
      terminal: '1',
      gate: '22'
    },
    to: {
      code: 'AER',
      name: 'Сочи (Адлер)',
      city: 'Сочи',
      terminal: '1',
      gate: '08'
    },
    departureTime: '17:10',
    arrivalTime: '21:00',
    departureDate: '2026-11-04',
    duration: '3 ч 50 мин',
    status: 'scheduled',
    statusText: 'Ожидает взлёта',
    altitude: 0,
    speed: 0,
    price: 9200,
  },
  {
    id: 'dp-6511',
    flightNumber: 'DP 6511',
    airline: 'Победа',
    aircraft: 'Boeing 737-800',
    from: {
      code: 'VKO',
      name: 'Внуково',
      city: 'Москва',
      terminal: 'A',
      gate: '16'
    },
    to: {
      code: 'LED',
      name: 'Пулково',
      city: 'Санкт-Петербург',
      terminal: '1',
      gate: '12'
    },
    departureTime: '14:20',
    arrivalTime: '15:45',
    departureDate: '2026-11-04',
    duration: '1 ч 25 мин',
    status: 'delayed',
    statusText: 'Задержан до 16:00',
    altitude: 0,
    speed: 0,
    price: 3600,
  },
  {
    id: 'ek-134',
    flightNumber: 'EK 134',
    airline: 'Emirates',
    aircraft: 'Boeing 777-300ER',
    from: {
      code: 'DME',
      name: 'Домодедово',
      city: 'Москва',
      terminal: '2',
      gate: '45'
    },
    to: {
      code: 'DXB',
      name: 'Дубай',
      city: 'Дубай',
      terminal: '3',
      gate: 'B12'
    },
    departureTime: '16:45',
    arrivalTime: '23:15',
    departureDate: '2026-11-04',
    duration: '5 ч 30 мин',
    status: 'boarding',
    statusText: 'Посадка завершается',
    altitude: 0,
    speed: 0,
    price: 42800,
  },
  {
    id: 'tk-414',
    flightNumber: 'TK 414',
    airline: 'Turkish Airlines',
    aircraft: 'Airbus A330-300',
    from: {
      code: 'VKO',
      name: 'Внуково',
      city: 'Москва',
      terminal: 'A',
      gate: '24'
    },
    to: {
      code: 'IST',
      name: 'Стамбул',
      city: 'Стамбул',
      terminal: '1',
      gate: 'F07'
    },
    departureTime: '11:00',
    arrivalTime: '15:30',
    departureDate: '2026-11-04',
    duration: '4 ч 30 мин',
    status: 'landed',
    statusText: 'Прибыл в 15:24',
    altitude: 0,
    speed: 0,
    price: 29500,
  },
  {
    id: 'su-1110',
    flightNumber: 'SU 1110',
    airline: 'Аэрофлот',
    aircraft: 'Sukhoi Superjet 100',
    from: {
      code: 'SVO',
      name: 'Шереметьево',
      city: 'Москва',
      terminal: 'B',
      gate: '102'
    },
    to: {
      code: 'KZN',
      name: 'Казань',
      city: 'Казань',
      terminal: '1A',
      gate: '02'
    },
    departureTime: '18:30',
    arrivalTime: '20:05',
    departureDate: '2026-11-04',
    duration: '1 ч 35 мин',
    status: 'scheduled',
    statusText: 'По расписанию',
    altitude: 0,
    speed: 0,
    price: 5400,
  }
];

