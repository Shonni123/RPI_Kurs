import React, { useState, useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import {
  X,
  Mail,
  Lock,
  User,
  ArrowRight,
  ShieldCheck,
  RefreshCw,
  AlertCircle,
  CheckCircle2,
  KeyRound,
  Plane,
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export const AuthModal: React.FC = () => {
  const {
    isAuthModalOpen,
    authModalTab,
    pendingEmail,
    closeAuthModal,
    setAuthModalTab,
    login,
    register,
    verifyEmail,
    resendVerificationCode,
    requestPasswordReset,
    confirmPasswordReset,
  } = useAuth();

  // Form states
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [newPasswordConfirm, setNewPasswordConfirm] = useState('');

  // 6-digit code inputs
  const [codeDigits, setCodeDigits] = useState<string[]>(['', '', '', '', '', '']);
  const codeInputsRef = useRef<(HTMLInputElement | null)[]>([]);

  // Timer & UI feedback
  const [timer, setTimer] = useState(60);
  const [canResend, setCanResend] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  // Reset or initialize state on tab change
  useEffect(() => {
    setErrorMsg(null);
    setSuccessMsg(null);
    if (authModalTab === 'verify_email' || authModalTab === 'reset_confirm') {
      setCodeDigits(['', '', '', '', '', '']);
      setTimer(60);
      setCanResend(false);
      setTimeout(() => codeInputsRef.current[0]?.focus(), 150);
    }
  }, [authModalTab]);

  // Countdown timer for resending code
  useEffect(() => {
    if (authModalTab !== 'verify_email' && authModalTab !== 'reset_confirm') return;
    if (timer <= 0) {
      setCanResend(true);
      return;
    }
    const interval = setInterval(() => {
      setTimer((prev) => prev - 1);
    }, 1000);
    return () => clearInterval(interval);
  }, [timer, authModalTab]);

  if (!isAuthModalOpen) return null;

  // Handle digit input & auto-focus next
  const handleDigitChange = (index: number, value: string) => {
    const char = value.slice(-1).replace(/\D/g, '');
    const newDigits = [...codeDigits];
    newDigits[index] = char;
    setCodeDigits(newDigits);

    if (char && index < 5) {
      codeInputsRef.current[index + 1]?.focus();
    }
  };

  const handleDigitKeyDown = (index: number, e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Backspace' && !codeDigits[index] && index > 0) {
      codeInputsRef.current[index - 1]?.focus();
    }
  };

  const handleDigitPaste = (e: React.ClipboardEvent) => {
    e.preventDefault();
    const pasted = e.clipboardData.getData('text').replace(/\D/g, '').slice(0, 6);
    if (!pasted) return;
    const newDigits = [...codeDigits];
    for (let i = 0; i < 6; i++) {
      newDigits[i] = pasted[i] || '';
    }
    setCodeDigits(newDigits);
    const nextIndex = Math.min(pasted.length, 5);
    codeInputsRef.current[nextIndex]?.focus();
  };

  // Form submissions
  const handleLoginSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (loading) return;
    setErrorMsg(null);
    setLoading(true);
    const res = await login({ emailOrUsername: email, password });
    setLoading(false);
    if (!res.success && res.error) {
      setErrorMsg(res.error);
    }
  };

  const handleRegisterSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (loading) return;
    setErrorMsg(null);
    if (password !== passwordConfirm) {
      setErrorMsg('Пароли не совпадают');
      return;
    }
    if (password.length < 6) {
      setErrorMsg('Пароль должен быть не менее 6 символов');
      return;
    }
    setLoading(true);
    const res = await register({ fullName, email, password, passwordConfirm });
    setLoading(false);
    if (!res.success) {
      if (res.error) setErrorMsg(res.error);
      else if (res.errors) {
        const first = Object.values(res.errors)[0];
        setErrorMsg(Array.isArray(first) ? first[0] : String(first));
      }
    }
  };

  const handleVerifySubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (loading) return;
    setErrorMsg(null);
    const fullCode = codeDigits.join('');
    if (fullCode.length !== 6) {
      setErrorMsg('Введите все 6 цифр кода');
      return;
    }
    setLoading(true);
    const res = await verifyEmail(fullCode);
    setLoading(false);
    if (!res.success && res.error) {
      setErrorMsg(res.error);
    }
  };

  const handleResendCode = async () => {
    if (!canResend || loading) return;
    setErrorMsg(null);
    setLoading(true);
    const purpose = authModalTab === 'reset_confirm' ? 'reset_password' : 'verify_email';
    const res = await resendVerificationCode(purpose);
    setLoading(false);
    if (res.success) {
      setSuccessMsg('Новый код отправлен на почту!');
      setTimer(60);
      setCanResend(false);
      setTimeout(() => setSuccessMsg(null), 4000);
    } else if (res.error) {
      setErrorMsg(res.error);
    }
  };

  const handleResetRequestSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (loading) return;
    setErrorMsg(null);
    if (!email) {
      setErrorMsg('Введите ваш email');
      return;
    }
    setLoading(true);
    const res = await requestPasswordReset(email);
    setLoading(false);
    if (!res.success && res.error) {
      setErrorMsg(res.error);
    }
  };

  const handleResetConfirmSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (loading) return;
    setErrorMsg(null);
    const fullCode = codeDigits.join('');
    if (fullCode.length !== 6) {
      setErrorMsg('Введите 6-значный код из письма');
      return;
    }
    if (newPassword !== newPasswordConfirm) {
      setErrorMsg('Пароли не совпадают');
      return;
    }
    if (newPassword.length < 6) {
      setErrorMsg('Пароль должен содержать минимум 6 символов');
      return;
    }
    setLoading(true);
    const res = await confirmPasswordReset({
      code: fullCode,
      newPassword,
      newPasswordConfirm,
    });
    setLoading(false);
    if (!res.success && res.error) {
      setErrorMsg(res.error);
    }
  };

  return createPortal(
    <div className="fixed inset-0 z-[999999] flex items-center justify-center p-4 isolate">
      {/* Backdrop */}
      <div
        onClick={closeAuthModal}
        className="fixed inset-0 bg-slate-950/60 backdrop-blur-xs transition-opacity animate-fadeIn"
      />

      {/* Modal Card */}
      <div className="relative z-10 w-full max-w-md bg-white rounded-3xl shadow-2xl border border-slate-100 overflow-hidden animate-fadeIn">
        {/* Header decoration */}
        <div className="bg-[#EFF7FE] border-b border-[#D5ECF8] px-6 py-5 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-white border border-[#D5ECF8] flex items-center justify-center text-sky-600 shadow-xs">
              <Plane className="w-5 h-5 -rotate-45" />
            </div>
            <div>
              <h2 className="font-benzin-bold text-xs uppercase tracking-tight text-slate-950">
                {authModalTab === 'login' && 'Вход в аккаунт'}
                {authModalTab === 'register' && 'Регистрация'}
                {authModalTab === 'verify_email' && 'Подтверждение почты'}
                {authModalTab === 'reset_request' && 'Восстановление пароля'}
                {authModalTab === 'reset_confirm' && 'Новый пароль'}
              </h2>
              <p className="text-[11px] text-slate-500 font-sans">
                Информационный сервис «Авиарейсы»
              </p>
            </div>
          </div>

          <button
            onClick={closeAuthModal}
            className="w-8 h-8 rounded-full bg-white hover:bg-slate-100 border border-slate-200 flex items-center justify-center text-slate-500 hover:text-slate-800 transition-colors cursor-pointer"
            aria-label="Закрыть окно"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Body content */}
        <div className="p-6 sm:p-7">
          {/* Global Alert messages */}
          {errorMsg && (
            <div className="mb-5 p-3.5 rounded-2xl bg-rose-50 border border-rose-200 flex items-start gap-2.5 text-xs text-rose-700 animate-fadeIn">
              <AlertCircle className="w-4 h-4 text-rose-600 flex-shrink-0 mt-0.5" />
              <span>{errorMsg}</span>
            </div>
          )}

          {successMsg && (
            <div className="mb-5 p-3.5 rounded-2xl bg-emerald-50 border border-emerald-200 flex items-start gap-2.5 text-xs text-emerald-700 animate-fadeIn">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0 mt-0.5" />
              <span>{successMsg}</span>
            </div>
          )}

          {/* 1. LOGIN TAB */}
          {authModalTab === 'login' && (
            <form onSubmit={handleLoginSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Электронная почта или логин
                </label>
                <div className="relative">
                  <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <input
                    type="text"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="user@example.com"
                    className="w-full pl-10 pr-4 py-2.5 rounded-2xl bg-[#F8FCFF] border border-slate-200 text-xs sm:text-sm text-slate-900 focus:outline-hidden focus:border-sky-500 focus:bg-white transition-all"
                  />
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <label className="text-xs font-semibold text-slate-700">Пароль</label>
                  <button
                    type="button"
                    onClick={() => setAuthModalTab('reset_request')}
                    className="text-[11px] font-semibold text-sky-600 hover:text-sky-700 cursor-pointer"
                  >
                    Забыли пароль?
                  </button>
                </div>
                <div className="relative">
                  <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <input
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    className="w-full pl-10 pr-4 py-2.5 rounded-2xl bg-[#F8FCFF] border border-slate-200 text-xs sm:text-sm text-slate-900 focus:outline-hidden focus:border-sky-500 focus:bg-white transition-all"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 px-4 rounded-2xl bg-sky-600 hover:bg-sky-700 active:scale-[0.99] text-white font-semibold text-xs sm:text-sm shadow-md shadow-sky-600/20 transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-60"
              >
                {loading ? (
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : (
                  <>
                    <span>Войти в аккаунт</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>

              <div className="pt-3 text-center text-xs text-slate-500">
                Нет учётной записи?{' '}
                <button
                  type="button"
                  onClick={() => setAuthModalTab('register')}
                  className="font-semibold text-sky-600 hover:text-sky-700 cursor-pointer underline"
                >
                  Зарегистрироваться
                </button>
              </div>
            </form>
          )}

          {/* 2. REGISTER TAB */}
          {authModalTab === 'register' && (
            <form onSubmit={handleRegisterSubmit} className="space-y-3.5">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Ваше имя и фамилия
                </label>
                <div className="relative">
                  <User className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <input
                    type="text"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="Алина Файзрахманова"
                    className="w-full pl-10 pr-4 py-2.5 rounded-2xl bg-[#F8FCFF] border border-slate-200 text-xs sm:text-sm text-slate-900 focus:outline-hidden focus:border-sky-500 focus:bg-white transition-all"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Электронная почта
                </label>
                <div className="relative">
                  <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="user@example.com"
                    className="w-full pl-10 pr-4 py-2.5 rounded-2xl bg-[#F8FCFF] border border-slate-200 text-xs sm:text-sm text-slate-900 focus:outline-hidden focus:border-sky-500 focus:bg-white transition-all"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1.5">Пароль</label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <input
                      type="password"
                      required
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="Минимум 6 знаков"
                      className="w-full pl-9 pr-3 py-2.5 rounded-2xl bg-[#F8FCFF] border border-slate-200 text-xs text-slate-900 focus:outline-hidden focus:border-sky-500 focus:bg-white transition-all"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                    Повтор пароля
                  </label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <input
                      type="password"
                      required
                      value={passwordConfirm}
                      onChange={(e) => setPasswordConfirm(e.target.value)}
                      placeholder="Повторите пароль"
                      className="w-full pl-9 pr-3 py-2.5 rounded-2xl bg-[#F8FCFF] border border-slate-200 text-xs text-slate-900 focus:outline-hidden focus:border-sky-500 focus:bg-white transition-all"
                    />
                  </div>
                </div>
              </div>

              <p className="text-[11px] text-slate-500 leading-relaxed">
                На указанную почту будет выслан 6-значный проверочный код для завершения регистрации.
              </p>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 px-4 rounded-2xl bg-sky-600 hover:bg-sky-700 active:scale-[0.99] text-white font-semibold text-xs sm:text-sm shadow-md shadow-sky-600/20 transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-60"
              >
                {loading ? (
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : (
                  <>
                    <span>Получить код подтверждения</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>

              <div className="pt-2 text-center text-xs text-slate-500">
                Уже зарегистрированы?{' '}
                <button
                  type="button"
                  onClick={() => setAuthModalTab('login')}
                  className="font-semibold text-sky-600 hover:text-sky-700 cursor-pointer underline"
                >
                  Войти
                </button>
              </div>
            </form>
          )}

          {/* 3. VERIFY EMAIL (6-digit code) TAB */}
          {authModalTab === 'verify_email' && (
            <form onSubmit={handleVerifySubmit} className="space-y-5">
              <div className="text-center space-y-1.5">
                <div className="w-12 h-12 rounded-2xl bg-sky-50 border border-sky-100 mx-auto flex items-center justify-center text-sky-600">
                  <ShieldCheck className="w-6 h-6" />
                </div>
                <h3 className="font-semibold text-sm text-slate-900">Проверьте вашу почту</h3>
                <p className="text-xs text-slate-500 max-w-xs mx-auto">
                  Мы отправили 6-значный код подтверждения на{' '}
                  <span className="font-semibold text-slate-800">{pendingEmail || email}</span>
                </p>
              </div>

              {/* 6 Digit Input Boxes */}
              <div className="flex items-center justify-center gap-2 sm:gap-2.5" onPaste={handleDigitPaste}>
                {codeDigits.map((digit, index) => (
                  <input
                    key={index}
                    ref={(el) => {
                      codeInputsRef.current[index] = el;
                    }}
                    type="text"
                    inputMode="numeric"
                    maxLength={1}
                    value={digit}
                    onChange={(e) => handleDigitChange(index, e.target.value)}
                    onKeyDown={(e) => handleDigitKeyDown(index, e)}
                    className="w-11 h-12 sm:w-12 sm:h-14 text-center text-lg sm:text-xl font-bold rounded-2xl bg-[#F8FCFF] border-2 border-slate-200 text-slate-900 focus:outline-hidden focus:border-sky-600 focus:bg-white transition-all shadow-xs"
                  />
                ))}
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 px-4 rounded-2xl bg-sky-600 hover:bg-sky-700 active:scale-[0.99] text-white font-semibold text-xs sm:text-sm shadow-md shadow-sky-600/20 transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-60"
              >
                {loading ? (
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : (
                  <>
                    <span>Подтвердить и войти</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>

              <div className="flex items-center justify-between pt-1 text-xs">
                <button
                  type="button"
                  onClick={() => setAuthModalTab('register')}
                  className="text-slate-500 hover:text-slate-700 cursor-pointer"
                >
                  ← Изменить email
                </button>

                <button
                  type="button"
                  disabled={!canResend || loading}
                  onClick={handleResendCode}
                  className={`font-semibold flex items-center gap-1 cursor-pointer transition-colors ${
                    canResend
                      ? 'text-sky-600 hover:text-sky-700'
                      : 'text-slate-400 cursor-not-allowed'
                  }`}
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
                  <span>
                    {canResend ? 'Отправить код ещё раз' : `Повтор через ${timer} сек`}
                  </span>
                </button>
              </div>
            </form>
          )}

          {/* 4. PASSWORD RESET REQUEST TAB */}
          {authModalTab === 'reset_request' && (
            <form onSubmit={handleResetRequestSubmit} className="space-y-4">
              <div className="text-center space-y-1">
                <div className="w-11 h-11 rounded-2xl bg-sky-50 border border-sky-100 mx-auto flex items-center justify-center text-sky-600">
                  <KeyRound className="w-5 h-5" />
                </div>
                <h3 className="font-semibold text-sm text-slate-900">Восстановление пароля</h3>
                <p className="text-xs text-slate-500">
                  Введите адрес вашей электронной почты, и мы пришлём 6-значный проверочный код для сброса.
                </p>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Электронная почта
                </label>
                <div className="relative">
                  <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="user@example.com"
                    className="w-full pl-10 pr-4 py-2.5 rounded-2xl bg-[#F8FCFF] border border-slate-200 text-xs sm:text-sm text-slate-900 focus:outline-hidden focus:border-sky-500 focus:bg-white transition-all"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 px-4 rounded-2xl bg-sky-600 hover:bg-sky-700 active:scale-[0.99] text-white font-semibold text-xs sm:text-sm shadow-md shadow-sky-600/20 transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-60"
              >
                {loading ? (
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : (
                  <>
                    <span>Получить код сброса</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>

              <div className="pt-2 text-center text-xs">
                <button
                  type="button"
                  onClick={() => setAuthModalTab('login')}
                  className="font-semibold text-slate-500 hover:text-slate-800 cursor-pointer"
                >
                  ← Вернуться ко входу
                </button>
              </div>
            </form>
          )}

          {/* 5. PASSWORD RESET CONFIRM (code + new password) TAB */}
          {authModalTab === 'reset_confirm' && (
            <form onSubmit={handleResetConfirmSubmit} className="space-y-4">
              <div className="text-center space-y-1">
                <h3 className="font-semibold text-sm text-slate-900">Новый пароль</h3>
                <p className="text-xs text-slate-500">
                  Введите 6-значный код из письма для <span className="font-semibold text-slate-700">{pendingEmail || email}</span> и задайте новый пароль.
                </p>
              </div>

              {/* 6 Digit Input Boxes */}
              <div className="flex items-center justify-center gap-2" onPaste={handleDigitPaste}>
                {codeDigits.map((digit, index) => (
                  <input
                    key={index}
                    ref={(el) => {
                      codeInputsRef.current[index] = el;
                    }}
                    type="text"
                    inputMode="numeric"
                    maxLength={1}
                    value={digit}
                    onChange={(e) => handleDigitChange(index, e.target.value)}
                    onKeyDown={(e) => handleDigitKeyDown(index, e)}
                    className="w-10 h-12 text-center text-lg font-bold rounded-xl bg-[#F8FCFF] border-2 border-slate-200 text-slate-900 focus:outline-hidden focus:border-sky-600 focus:bg-white transition-all"
                  />
                ))}
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Новый пароль
                </label>
                <div className="relative">
                  <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <input
                    type="password"
                    required
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    placeholder="Минимум 6 символов"
                    className="w-full pl-10 pr-4 py-2.5 rounded-2xl bg-[#F8FCFF] border border-slate-200 text-xs sm:text-sm text-slate-900 focus:outline-hidden focus:border-sky-500 focus:bg-white transition-all"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Повторите новый пароль
                </label>
                <div className="relative">
                  <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <input
                    type="password"
                    required
                    value={newPasswordConfirm}
                    onChange={(e) => setNewPasswordConfirm(e.target.value)}
                    placeholder="Повторите новый пароль"
                    className="w-full pl-10 pr-4 py-2.5 rounded-2xl bg-[#F8FCFF] border border-slate-200 text-xs sm:text-sm text-slate-900 focus:outline-hidden focus:border-sky-500 focus:bg-white transition-all"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 px-4 rounded-2xl bg-sky-600 hover:bg-sky-700 active:scale-[0.99] text-white font-semibold text-xs sm:text-sm shadow-md shadow-sky-600/20 transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-60"
              >
                {loading ? (
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : (
                  <>
                    <span>Сохранить пароль и войти</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>

              <div className="flex items-center justify-between pt-1 text-xs">
                <button
                  type="button"
                  onClick={() => setAuthModalTab('login')}
                  className="text-slate-500 hover:text-slate-700 cursor-pointer"
                >
                  ← Вернуться ко входу
                </button>

                <button
                  type="button"
                  disabled={!canResend || loading}
                  onClick={handleResendCode}
                  className={`font-semibold cursor-pointer ${
                    canResend ? 'text-sky-600 hover:text-sky-700' : 'text-slate-400'
                  }`}
                >
                  {canResend ? 'Выслать код снова' : `Повтор: ${timer} с`}
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>,
    document.body
  );
};
