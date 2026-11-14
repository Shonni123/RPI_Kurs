import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  User,
  Mail,
  Phone,
  ShieldCheck,
  Calendar,
  Heart,
  Lock,
  LogOut,
  Save,
  CheckCircle2,
  AlertCircle,
  Plane,
  ChevronRight,
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useFavorites } from '../hooks/useFavorites';

export const UserProfilePage: React.FC = () => {
  const { user, isAuthenticated, updateProfile, changePassword, logout, openAuthModal } = useAuth();
  const { favorites } = useFavorites();
  const navigate = useNavigate();

  // Profile edit form
  const [fullName, setFullName] = useState(user?.fullName || '');
  const [phoneNumber, setPhoneNumber] = useState(user?.phone || '');
  const [profileLoading, setProfileLoading] = useState(false);
  const [profileMsg, setProfileMsg] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  // Password change form
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [newPasswordConfirm, setNewPasswordConfirm] = useState('');
  const [passLoading, setPassLoading] = useState(false);
  const [passMsg, setPassMsg] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  if (!isAuthenticated || !user) {
    return (
      <div className="min-h-[80vh] bg-[#F8FCFF] text-slate-900 flex items-center justify-center px-4 py-16">
        <div className="max-w-md w-full bg-white rounded-3xl p-8 border border-slate-100 shadow-xl text-center space-y-4">
          <div className="w-16 h-16 rounded-2xl bg-[#EFF7FE] border border-[#D5ECF8] mx-auto flex items-center justify-center text-sky-600">
            <User className="w-8 h-8" />
          </div>
          <h2 className="text-xl font-bold font-benzin uppercase tracking-tight text-slate-900">
            Личный кабинет
          </h2>
          <p className="text-xs sm:text-sm text-slate-500 leading-relaxed">
            Для доступа к профилю, настройкам безопасности и персональным данным войдите в свою учётную запись.
          </p>
          <div className="pt-2 flex flex-col sm:flex-row gap-3 justify-center">
            <button
              onClick={() => openAuthModal('login')}
              className="px-6 py-2.5 rounded-full bg-sky-600 hover:bg-sky-700 text-white font-semibold text-xs transition-all shadow-md cursor-pointer"
            >
              Войти
            </button>
            <button
              onClick={() => openAuthModal('register')}
              className="px-6 py-2.5 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold text-xs transition-all cursor-pointer"
            >
              Зарегистрироваться
            </button>
          </div>
        </div>
      </div>
    );
  }

  const handleProfileSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setProfileMsg(null);
    setProfileLoading(true);
    const res = await updateProfile({ fullName, phone: phoneNumber });
    setProfileLoading(false);
    if (res.success) {
      setProfileMsg({ type: 'success', text: 'Данные профиля успешно сохранены!' });
      setTimeout(() => setProfileMsg(null), 4000);
    } else {
      setProfileMsg({ type: 'error', text: res.error || 'Ошибка при сохранении профиля' });
    }
  };

  const handlePasswordSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setPassMsg(null);
    if (newPassword !== newPasswordConfirm) {
      setPassMsg({ type: 'error', text: 'Новые пароли не совпадают' });
      return;
    }
    if (newPassword.length < 6) {
      setPassMsg({ type: 'error', text: 'Новый пароль должен содержать минимум 6 знаков' });
      return;
    }
    setPassLoading(true);
    const res = await changePassword({ oldPassword, newPassword });
    setPassLoading(false);
    if (res.success) {
      setPassMsg({ type: 'success', text: 'Пароль успешно обновлён!' });
      setOldPassword('');
      setNewPassword('');
      setNewPasswordConfirm('');
      setTimeout(() => setPassMsg(null), 4000);
    } else {
      setPassMsg({ type: 'error', text: res.error || 'Ошибка смены пароля' });
    }
  };

  const handleLogoutClick = async () => {
    await logout();
    navigate('/');
  };

  const formattedDate = user.date_joined
    ? new Date(user.date_joined).toLocaleDateString('ru-RU', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
      })
    : 'Ноябрь 2026';

  const userInitials = (user.fullName || user.username || 'У')
    .split(' ')
    .map((w) => w[0])
    .join('')
    .slice(0, 2)
    .toUpperCase();

  return (
    <div className="min-h-screen bg-[#F8FCFF] text-slate-900 pt-6 sm:pt-10 pb-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-6 sm:space-y-8">
        {/* Breadcrumb navigation */}
        <div className="flex items-center gap-2 text-xs text-slate-400">
          <Link to="/" className="hover:text-slate-600 transition-colors">
            Главная
          </Link>
          <ChevronRight className="w-3.5 h-3.5" />
          <span className="text-slate-800 font-semibold">Личный кабинет</span>
        </div>

        {/* Profile Hero Header Card */}
        <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-100 shadow-md flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="flex items-center gap-4 sm:gap-5">
            <div className="w-16 h-16 sm:w-20 sm:h-20 rounded-2xl bg-gradient-to-tr from-sky-600 to-blue-500 text-white font-benzin font-bold text-xl sm:text-2xl flex items-center justify-center shadow-lg shadow-sky-600/20 flex-shrink-0">
              {userInitials}
            </div>
            <div className="space-y-1">
              <h1 className="text-lg sm:text-2xl font-bold font-benzin uppercase tracking-tight text-slate-950">
                {user.fullName || user.username}
              </h1>
              <p className="text-xs sm:text-sm text-slate-500 flex items-center gap-1.5">
                <Mail className="w-3.5 h-3.5 text-slate-400" />
                <span>{user.email}</span>
              </p>
              <div className="flex flex-wrap items-center gap-2 pt-1">
                {user.isEmailVerified ? (
                  <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 text-[11px] font-semibold">
                    <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                    <span>Email подтверждён</span>
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-amber-50 text-amber-700 border border-amber-200 text-[11px] font-semibold">
                    <span>Email не подтверждён</span>
                  </span>
                )}
                <span className="inline-flex items-center gap-1 text-[11px] text-slate-400">
                  <Calendar className="w-3.5 h-3.5" />
                  <span>В сервисе с {formattedDate}</span>
                </span>
              </div>
            </div>
          </div>

          <button
            onClick={handleLogoutClick}
            className="flex items-center gap-2 px-4 py-2 rounded-2xl border border-rose-200 text-rose-600 hover:bg-rose-50 text-xs font-semibold transition-all cursor-pointer self-stretch md:self-auto justify-center"
          >
            <LogOut className="w-4 h-4" />
            <span>Выйти</span>
          </button>
        </div>

        {/* 2 Quick Summary Stats */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Link
            to="/favorites"
            className="p-5 rounded-3xl bg-white border border-slate-100 shadow-sm hover:shadow-md transition-all flex items-center justify-between group"
          >
            <div className="flex items-center gap-3.5">
              <div className="w-11 h-11 rounded-2xl bg-rose-50 border border-rose-100 flex items-center justify-center text-rose-500 group-hover:scale-105 transition-transform">
                <Heart className="w-5 h-5 fill-rose-500" />
              </div>
              <div>
                <span className="text-xs text-slate-500 block">Избранные рейсы</span>
                <span className="text-xl font-bold text-slate-900">{favorites.length}</span>
              </div>
            </div>
            <ChevronRight className="w-4 h-4 text-slate-400 group-hover:translate-x-1 transition-transform" />
          </Link>

          <Link
            to="/flights"
            className="p-5 rounded-3xl bg-white border border-slate-100 shadow-sm hover:shadow-md transition-all flex items-center justify-between group"
          >
            <div className="flex items-center gap-3.5">
              <div className="w-11 h-11 rounded-2xl bg-sky-50 border border-sky-100 flex items-center justify-center text-sky-600 group-hover:scale-105 transition-transform">
                <Plane className="w-5 h-5 -rotate-45" />
              </div>
              <div>
                <span className="text-xs text-slate-500 block">Онлайн-табло рейсов</span>
                <span className="text-xs font-semibold text-sky-700">Перейти к расписанию</span>
              </div>
            </div>
            <ChevronRight className="w-4 h-4 text-slate-400 group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>

        {/* Settings Sections Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Left: Edit Personal Data */}
          <div className="bg-white rounded-3xl p-6 sm:p-7 border border-slate-100 shadow-sm space-y-5">
            <div className="flex items-center gap-2.5 pb-3 border-b border-slate-100">
              <User className="w-5 h-5 text-sky-600" />
              <h2 className="font-bold text-sm text-slate-900">Личные данные</h2>
            </div>

            {profileMsg && (
              <div
                className={`p-3 rounded-2xl text-xs flex items-center gap-2 ${
                  profileMsg.type === 'success'
                    ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                    : 'bg-rose-50 text-rose-700 border border-rose-200'
                }`}
              >
                {profileMsg.type === 'success' ? (
                  <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
                ) : (
                  <AlertCircle className="w-4 h-4 flex-shrink-0" />
                )}
                <span>{profileMsg.text}</span>
              </div>
            )}

            <form onSubmit={handleProfileSave} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Имя и фамилия
                </label>
                <input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="Алина Файзрахманова"
                  className="w-full px-3.5 py-2.5 rounded-2xl bg-[#F8FCFF] border border-slate-200 text-xs sm:text-sm text-slate-900 focus:outline-hidden focus:border-sky-500 focus:bg-white transition-all"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Электронная почта
                </label>
                <div className="relative">
                  <input
                    type="email"
                    disabled
                    value={user.email}
                    className="w-full px-3.5 py-2.5 rounded-2xl bg-slate-50 border border-slate-200 text-xs sm:text-sm text-slate-500 cursor-not-allowed"
                  />
                  <span className="absolute right-3.5 top-1/2 -translate-y-1/2 text-[10px] text-emerald-600 font-semibold bg-emerald-50 px-2 py-0.5 rounded-full">
                    Подтверждена
                  </span>
                </div>
                <p className="text-[10px] text-slate-400 mt-1">
                  Для смены email обратитесь к администратору.
                </p>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Контактный телефон
                </label>
                <div className="relative">
                  <Phone className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <input
                    type="tel"
                    value={phoneNumber}
                    onChange={(e) => setPhoneNumber(e.target.value)}
                    placeholder="+7 (999) 000-00-00"
                    className="w-full pl-10 pr-3.5 py-2.5 rounded-2xl bg-[#F8FCFF] border border-slate-200 text-xs sm:text-sm text-slate-900 focus:outline-hidden focus:border-sky-500 focus:bg-white transition-all"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={profileLoading}
                className="w-full py-2.5 px-4 rounded-2xl bg-sky-600 hover:bg-sky-700 text-white font-semibold text-xs transition-all shadow-sm flex items-center justify-center gap-2 cursor-pointer disabled:opacity-60"
              >
                <Save className="w-3.5 h-3.5" />
                <span>{profileLoading ? 'Сохранение...' : 'Сохранить изменения'}</span>
              </button>
            </form>
          </div>

          {/* Right: Security & Change Password */}
          <div className="bg-white rounded-3xl p-6 sm:p-7 border border-slate-100 shadow-sm space-y-5">
            <div className="flex items-center gap-2.5 pb-3 border-b border-slate-100">
              <Lock className="w-5 h-5 text-sky-600" />
              <h2 className="font-bold text-sm text-slate-900">Безопасность и пароль</h2>
            </div>

            {passMsg && (
              <div
                className={`p-3 rounded-2xl text-xs flex items-center gap-2 ${
                  passMsg.type === 'success'
                    ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                    : 'bg-rose-50 text-rose-700 border border-rose-200'
                }`}
              >
                {passMsg.type === 'success' ? (
                  <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
                ) : (
                  <AlertCircle className="w-4 h-4 flex-shrink-0" />
                )}
                <span>{passMsg.text}</span>
              </div>
            )}

            <form onSubmit={handlePasswordSave} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Текущий пароль
                </label>
                <input
                  type="password"
                  required
                  value={oldPassword}
                  onChange={(e) => setOldPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full px-3.5 py-2.5 rounded-2xl bg-[#F8FCFF] border border-slate-200 text-xs sm:text-sm text-slate-900 focus:outline-hidden focus:border-sky-500 focus:bg-white transition-all"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Новый пароль
                </label>
                <input
                  type="password"
                  required
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  placeholder="Минимум 6 знаков"
                  className="w-full px-3.5 py-2.5 rounded-2xl bg-[#F8FCFF] border border-slate-200 text-xs sm:text-sm text-slate-900 focus:outline-hidden focus:border-sky-500 focus:bg-white transition-all"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Подтвердите новый пароль
                </label>
                <input
                  type="password"
                  required
                  value={newPasswordConfirm}
                  onChange={(e) => setNewPasswordConfirm(e.target.value)}
                  placeholder="Повторите новый пароль"
                  className="w-full px-3.5 py-2.5 rounded-2xl bg-[#F8FCFF] border border-slate-200 text-xs sm:text-sm text-slate-900 focus:outline-hidden focus:border-sky-500 focus:bg-white transition-all"
                />
              </div>

              <button
                type="submit"
                disabled={passLoading}
                className="w-full py-2.5 px-4 rounded-2xl bg-slate-900 hover:bg-slate-800 text-white font-semibold text-xs transition-all shadow-sm flex items-center justify-center gap-2 cursor-pointer disabled:opacity-60"
              >
                <Lock className="w-3.5 h-3.5" />
                <span>{passLoading ? 'Обновление...' : 'Обновить пароль'}</span>
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};
