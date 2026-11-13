import { Flight } from '../types/flight';
import { MOCK_FLIGHTS } from './mockFlights';

// Backend port fallback (8001 if 8000 is occupied by another project, or 8000)
const CANDIDATE_API_URLS = [
  'http://127.0.0.1:8001/api',
  'http://127.0.0.1:8000/api',
];

let activeApiBaseUrl = CANDIDATE_API_URLS[0];

async function fetchFromApi(endpoint: string, options?: RequestInit): Promise<Response> {
  // First attempt with currently active URL
  try {
    const res = await fetch(`${activeApiBaseUrl}${endpoint}`, {
      ...options,
      signal: AbortSignal.timeout(2000),
    });
    if (res.ok) return res;
  } catch {
    // Ignore and try alternative candidate
  }

  // Try the other candidate URL
  const altUrl = CANDIDATE_API_URLS.find((u) => u !== activeApiBaseUrl) || CANDIDATE_API_URLS[0];
  try {
    const res = await fetch(`${altUrl}${endpoint}`, {
      ...options,
      signal: AbortSignal.timeout(2000),
    });
    if (res.ok) {
      activeApiBaseUrl = altUrl;
      return res;
    }
    return res;
  } catch (err) {
    throw err;
  }
}

export interface SyncApiResponse {
  success: boolean;
  message?: string;
  count?: number;
  error?: string;
}

export const flightApi = {
  /**
   * Fetches flights from Django REST API with fallback to local mock data.
   */
  async getFlights(params?: { search?: string; status?: string; airline?: string; ordering?: string }): Promise<{ flights: Flight[]; isLiveServer: boolean }> {
    try {
      const query = new URLSearchParams();
      if (params?.search) query.append('search', params.search);
      if (params?.status && params.status !== 'all') query.append('status', params.status);
      if (params?.airline && params.airline !== 'all') query.append('airline', params.airline);
      if (params?.ordering) query.append('ordering', params.ordering);

      const endpoint = `/flights/${query.toString() ? '?' + query.toString() : ''}`;
      const response = await fetchFromApi(endpoint);

      if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
      }

      const data = await response.json();
      if (Array.isArray(data) && data.length > 0) {
        return { flights: data, isLiveServer: true };
      }
      return { flights: MOCK_FLIGHTS, isLiveServer: true };
    } catch {
      // Fallback to local data if backend is offline
      return { flights: MOCK_FLIGHTS, isLiveServer: false };
    }
  },

  /**
   * Fetches single flight by ID
   */
  async getFlightById(id: string): Promise<Flight | null> {
    try {
      const response = await fetchFromApi(`/flights/${id}/`);
      if (response.ok) {
        return await response.json();
      }
    } catch {
      // Fallback to local
    }
    return MOCK_FLIGHTS.find((f) => f.id === id) || null;
  },

  /**
   * Triggers real-time sync with Aviationstack API via Django backend
   */
  async syncAviationstack(limit = 15): Promise<SyncApiResponse> {
    try {
      const response = await fetchFromApi(`/sync-aviationstack/?limit=${limit}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        signal: AbortSignal.timeout(12000),
      });
      return await response.json();
    } catch (e: any) {
      return { success: false, error: e?.message || 'Не удалось связаться с Django бэкендом' };
    }
  },

  /**
   * Check backend status
   */
  async checkBackendStatus(): Promise<boolean> {
    try {
      const res = await fetchFromApi('/status/', { signal: AbortSignal.timeout(1500) });
      return res.ok;
    } catch {
      return false;
    }
  }
};
