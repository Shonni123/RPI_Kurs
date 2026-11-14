export interface AuthUser {
  id: number;
  username: string;
  email: string;
  fullName: string;
  isEmailVerified: boolean;
  phone?: string;
  date_joined?: string;
}

export interface AuthResponse {
  success: boolean;
  message?: string;
  token?: string;
  user?: AuthUser;
  error?: string;
  errors?: Record<string, string | string[]>;
  email?: string;
  emailSent?: boolean;
  debugCode?: string;
  requiresVerification?: boolean;
}

export type AuthModalTab = 'login' | 'register' | 'verify_email' | 'reset_request' | 'reset_confirm';

