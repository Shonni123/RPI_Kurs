import React, { createContext, useContext, useState, useEffect } from 'react';
import { AuthUser, AuthModalTab, AuthResponse } from '../types/auth';
import { authApi } from '../services/authApi';

interface AuthContextType {
  user: AuthUser | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  isAuthModalOpen: boolean;
  authModalTab: AuthModalTab;
  pendingEmail: string;
  debugCode: string | null;
  openAuthModal: (tab?: AuthModalTab, email?: string) => void;
  closeAuthModal: () => void;
  setAuthModalTab: (tab: AuthModalTab) => void;
  setPendingEmail: (email: string) => void;
  login: (data: { emailOrUsername: string; password: string }) => Promise<AuthResponse>;
  register: (data: { fullName?: string; email: string; password: string; passwordConfirm: string }) => Promise<AuthResponse>;
  verifyEmail: (code: string) => Promise<AuthResponse>;
  resendVerificationCode: (purpose?: string) => Promise<AuthResponse>;
  requestPasswordReset: (email: string) => Promise<AuthResponse>;
  confirmPasswordReset: (data: { code: string; newPassword: string; newPasswordConfirm: string }) => Promise<AuthResponse>;
  logout: () => Promise<void>;
  updateProfile: (data: { fullName?: string; phone?: string }) => Promise<AuthResponse>;
  changePassword: (data: { oldPassword: string; newPassword: string }) => Promise<AuthResponse>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const TOKEN_KEY = 'aviaraces_auth_token';
const USER_KEY = 'aviaraces_auth_user';

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem(TOKEN_KEY));
  const [user, setUser] = useState<AuthUser | null>(() => {
    const saved = localStorage.getItem(USER_KEY);
    try {
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Modal state
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [authModalTab, setAuthModalTab] = useState<AuthModalTab>('login');
  const [pendingEmail, setPendingEmail] = useState<string>('');
  const [debugCode, setDebugCode] = useState<string | null>(null);

  // Sync session on mount
  useEffect(() => {
    const initAuth = async () => {
      const savedToken = localStorage.getItem(TOKEN_KEY);
      if (savedToken) {
        const res = await authApi.getMe(savedToken);
        if (res.success && res.user) {
          setUser(res.user);
          localStorage.setItem(USER_KEY, JSON.stringify(res.user));
        } else {
          // Token invalid or expired
          setToken(null);
          setUser(null);
          localStorage.removeItem(TOKEN_KEY);
          localStorage.removeItem(USER_KEY);
        }
      }
      setIsLoading(false);
    };

    initAuth();
  }, []);

  const openAuthModal = (tab: AuthModalTab = 'login', email = '') => {
    setAuthModalTab(tab);
    if (email) setPendingEmail(email);
    setIsAuthModalOpen(true);
  };

  const closeAuthModal = () => {
    setIsAuthModalOpen(false);
    setDebugCode(null);
  };

  const handleAuthSuccess = (newToken: string, newUser: AuthUser) => {
    setToken(newToken);
    setUser(newUser);
    localStorage.setItem(TOKEN_KEY, newToken);
    localStorage.setItem(USER_KEY, JSON.stringify(newUser));
    closeAuthModal();
  };

  const login = async (data: { emailOrUsername: string; password: string }): Promise<AuthResponse> => {
    const res = await authApi.login(data);
    if (res.success && res.token && res.user) {
      handleAuthSuccess(res.token, res.user);
    } else if (res.requiresVerification && res.email) {
      setPendingEmail(res.email);
      setAuthModalTab('verify_email');
    }
    return res;
  };

  const register = async (data: { fullName?: string; email: string; password: string; passwordConfirm: string }): Promise<AuthResponse> => {
    const res = await authApi.register(data);
    if (res.success && res.email) {
      setPendingEmail(res.email);
      setAuthModalTab('verify_email');
    }
    return res;
  };

  const verifyEmail = async (code: string): Promise<AuthResponse> => {
    const res = await authApi.verifyCode(pendingEmail, code, 'verify_email');
    if (res.success && res.token && res.user) {
      handleAuthSuccess(res.token, res.user);
    }
    return res;
  };

  const resendVerificationCode = async (purpose = 'verify_email'): Promise<AuthResponse> => {
    const res = await authApi.resendCode(pendingEmail, purpose);
    return res;
  };

  const requestPasswordReset = async (email: string): Promise<AuthResponse> => {
    setPendingEmail(email);
    const res = await authApi.requestPasswordReset(email);
    if (res.success) {
      setAuthModalTab('reset_confirm');
    }
    return res;
  };

  const confirmPasswordReset = async (data: { code: string; newPassword: string; newPasswordConfirm: string }): Promise<AuthResponse> => {
    const res = await authApi.confirmPasswordReset({
      email: pendingEmail,
      code: data.code,
      newPassword: data.newPassword,
      newPasswordConfirm: data.newPasswordConfirm,
    });
    if (res.success && res.token && res.user) {
      handleAuthSuccess(res.token, res.user);
    }
    return res;
  };

  const logout = async () => {
    if (token) {
      await authApi.logout(token);
    }
    setToken(null);
    setUser(null);
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  };

  const updateProfile = async (data: { fullName?: string; phone?: string }): Promise<AuthResponse> => {
    if (!token) return { success: false, error: 'Не авторизован' };
    const res = await authApi.updateMe(token, data);
    if (res.success && res.user) {
      setUser(res.user);
      localStorage.setItem(USER_KEY, JSON.stringify(res.user));
    }
    return res;
  };

  const changePassword = async (data: { oldPassword: string; newPassword: string }): Promise<AuthResponse> => {
    if (!token) return { success: false, error: 'Не авторизован' };
    const res = await authApi.changePassword(token, data);
    if (res.success && res.token) {
      setToken(res.token);
      localStorage.setItem(TOKEN_KEY, res.token);
    }
    return res;
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!user && !!token,
        isLoading,
        isAuthModalOpen,
        authModalTab,
        pendingEmail,
        debugCode,
        openAuthModal,
        closeAuthModal,
        setAuthModalTab,
        setPendingEmail,
        login,
        register,
        verifyEmail,
        resendVerificationCode,
        requestPasswordReset,
        confirmPasswordReset,
        logout,
        updateProfile,
        changePassword,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

