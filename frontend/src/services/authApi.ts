import { AuthResponse, AuthUser } from '../types/auth';

const CANDIDATE_AUTH_URLS = [
  'http://127.0.0.1:8000/api/auth',
  'http://127.0.0.1:8001/api/auth',
];

let activeAuthBaseUrl = CANDIDATE_AUTH_URLS[0];

async function fetchAuth(endpoint: string, options?: RequestInit): Promise<Response> {
  const headers = {
    'Content-Type': 'application/json',
    ...(options?.headers || {}),
  };

  const isMutation = options?.method && options.method.toUpperCase() !== 'GET';
  // Allow plenty of time for SMTP email delivery (25s) without prematurely aborting
  const timeoutMs = isMutation ? 25000 : 5000;

  try {
    const res = await fetch(`${activeAuthBaseUrl}${endpoint}`, {
      ...options,
      headers,
      signal: AbortSignal.timeout(timeoutMs),
    });
    if (res.status < 500) return res;
  } catch (err: any) {
    // If it's a mutation, DO NOT retry on error/timeout to prevent duplicate operations (such as sending two emails)
    if (isMutation) {
      throw err;
    }
  }

  // Only GET requests or connection setup can try fallback port
  const altUrl = CANDIDATE_AUTH_URLS.find((u) => u !== activeAuthBaseUrl) || CANDIDATE_AUTH_URLS[0];
  const res = await fetch(`${altUrl}${endpoint}`, {
    ...options,
    headers,
    signal: AbortSignal.timeout(timeoutMs),
  });
  if (res.status < 500) {
    activeAuthBaseUrl = altUrl;
  }
  return res;
}

export const authApi = {
  async register(data: { fullName?: string; email: string; password: string; passwordConfirm: string }): Promise<AuthResponse> {
    try {
      const res = await fetchAuth('/register/', {
        method: 'POST',
        body: JSON.stringify(data),
      });
      return await res.json();
    } catch (e: any) {
      return { success: false, error: e?.message || 'Не удалось связаться с сервером.' };
    }
  },

  async verifyCode(email: string, code: string, purpose = 'verify_email'): Promise<AuthResponse> {
    try {
      const res = await fetchAuth('/verify-code/', {
        method: 'POST',
        body: JSON.stringify({ email, code, purpose }),
      });
      return await res.json();
    } catch (e: any) {
      return { success: false, error: e?.message || 'Не удалось проверить код.' };
    }
  },

  async resendCode(email: string, purpose = 'verify_email'): Promise<AuthResponse> {
    try {
      const res = await fetchAuth('/resend-code/', {
        method: 'POST',
        body: JSON.stringify({ email, purpose }),
      });
      return await res.json();
    } catch (e: any) {
      return { success: false, error: e?.message || 'Не удалось отправить код повторно.' };
    }
  },

  async login(data: { emailOrUsername: string; password: string }): Promise<AuthResponse> {
    try {
      const res = await fetchAuth('/login/', {
        method: 'POST',
        body: JSON.stringify(data),
      });
      return await res.json();
    } catch (e: any) {
      return { success: false, error: e?.message || 'Ошибка подключения к серверу.' };
    }
  },

  async requestPasswordReset(email: string): Promise<AuthResponse> {
    try {
      const res = await fetchAuth('/password-reset/request/', {
        method: 'POST',
        body: JSON.stringify({ email }),
      });
      return await res.json();
    } catch (e: any) {
      return { success: false, error: e?.message || 'Ошибка запроса на сброс пароля.' };
    }
  },

  async confirmPasswordReset(data: {
    email: string;
    code: string;
    newPassword: string;
    newPasswordConfirm: string;
  }): Promise<AuthResponse> {
    try {
      const res = await fetchAuth('/password-reset/confirm/', {
        method: 'POST',
        body: JSON.stringify(data),
      });
      return await res.json();
    } catch (e: any) {
      return { success: false, error: e?.message || 'Ошибка подтверждения пароля.' };
    }
  },

  async getMe(token: string): Promise<{ success: boolean; user?: AuthUser; error?: string }> {
    try {
      const res = await fetchAuth('/me/', {
        method: 'GET',
        headers: { Authorization: `Token ${token}` },
      });
      if (res.ok) {
        return await res.json();
      }
      return { success: false, error: 'Сессия устарела.' };
    } catch (e: any) {
      return { success: false, error: e?.message || 'Ошибка запроса профиля.' };
    }
  },

  async updateMe(token: string, data: { fullName?: string; phone?: string }): Promise<AuthResponse> {
    try {
      const res = await fetchAuth('/me/', {
        method: 'PUT',
        headers: { Authorization: `Token ${token}` },
        body: JSON.stringify(data),
      });
      return await res.json();
    } catch (e: any) {
      return { success: false, error: e?.message || 'Не удалось обновить профиль.' };
    }
  },

  async changePassword(token: string, data: { oldPassword: string; newPassword: string }): Promise<AuthResponse> {
    try {
      const res = await fetchAuth('/change-password/', {
        method: 'POST',
        headers: { Authorization: `Token ${token}` },
        body: JSON.stringify(data),
      });
      return await res.json();
    } catch (e: any) {
      return { success: false, error: e?.message || 'Ошибка смены пароля.' };
    }
  },

  async logout(token?: string): Promise<void> {
    try {
      if (token) {
        await fetchAuth('/logout/', {
          method: 'POST',
          headers: { Authorization: `Token ${token}` },
        });
      }
    } catch {
      // ignore
    }
  },
};

