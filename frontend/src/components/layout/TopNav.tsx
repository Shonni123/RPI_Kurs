import React, { useState, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import {
  LogOut,
  Settings,
  X,
  Plane,
  Building2,
  Heart,
  HelpCircle,
  Info,
  ChevronRight,
  ExternalLink,
} from 'lucide-react';
import { useFavorites } from '../../hooks/useFavorites';

interface TopNavProps {
  theme?: 'dark' | 'light';
  className?: string;
}

export const TopNav: React.FC<TopNavProps> = ({ theme = 'dark', className = '' }) => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const { favorites } = useFavorites();
  const isDark = theme === 'dark';

  // Prevent background scroll and handle Escape key when drawer is open
  useEffect(() => {
    if (isOpen) {
      const originalOverflow = document.body.style.overflow;
      document.body.style.overflow = 'hidden';

      const handleKeyDown = (e: KeyboardEvent) => {
        if (e.key === 'Escape') {
          setIsOpen(false);
        }
      };

      window.addEventListener('keydown', handleKeyDown);
      return () => {
        document.body.style.overflow = originalOverflow;
        window.removeEventListener('keydown', handleKeyDown);
      };
    }
  }, [isOpen]);

  const navLinks = [
    { name: 'Главная', path: '/' },
    { name: 'Посмотреть рейс', path: '/flights' },
    { name: 'О сервисе', path: '/#why-us' },
    { name: 'Как это работает', path: '/#features' },
  ];

  const drawerLinks = [
    { name: 'Онлайн-табло рейсов', path: '/flights', icon: Plane, badge: 'Live' },
    { name: 'Аэропорты и хабы', path: '/airports', icon: Building2 },
    { name: 'Избранные рейсы', path: '/favorites', icon: Heart, count: favorites.length },
    { name: 'О сервисе', path: '/#why-us', icon: Info },
    { name: 'Архитектура и стек', path: '/about', icon: ExternalLink },
    { name: 'Вопросы и ответы (FAQ)', path: '/#faq', icon: HelpCircle },
  ];

  const handleLinkClick = (e: React.MouseEvent<HTMLAnchorElement>, path: string) => {
    if (path === '/') {
      if (location.pathname === '/') {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
      setIsOpen(false);
      return;
    }

    if (path.includes('#')) {
      const [route, hash] = path.split('#');
      const targetRoute = route || '/';
      if (location.pathname === targetRoute) {
        e.preventDefault();
        const element = document.getElementById(hash);
        if (element) {
          element.scrollIntoView({ behavior: 'smooth' });
        }
      } else {
        e.preventDefault();
        navigate(path);
      }
      setIsOpen(false);
      return;
    }

    setIsOpen(false);
  };

  return (
    <>
      <nav className={`w-full flex items-center justify-between ${className}`}>
        {/* Left: 3-line hamburger menu - 3 identical parallel lines matching Figma */}
        <button
          onClick={() => setIsOpen(true)}
          className="flex flex-col justify-center items-start gap-1.5 p-1 rounded-lg hover:opacity-80 transition-opacity cursor-pointer group"
          aria-label="Меню навигации"
          title="Открыть меню"
        >
          <span className={`w-6 h-0.5 rounded-full transition-all group-hover:w-7 ${isDark ? 'bg-white' : 'bg-slate-900'}`} />
          <span className={`w-6 h-0.5 rounded-full transition-all group-hover:w-5 ${isDark ? 'bg-white' : 'bg-slate-900'}`} />
          <span className={`w-6 h-0.5 rounded-full transition-all group-hover:w-6 ${isDark ? 'bg-white' : 'bg-slate-900'}`} />
        </button>

        {/* Center: Frosted capsule navigation pills matching Figma reference */}
        <div className="hidden md:flex items-center gap-3 lg:gap-3.5">
          {navLinks.map((link) => (
            <Link
              key={link.name}
              to={link.path}
              onClick={(e) => handleLinkClick(e, link.path)}
              className={`px-5 py-2 rounded-full text-xs sm:text-[13px] font-semibold transition-all duration-200 hover:scale-[1.02] whitespace-nowrap shadow-sm cursor-pointer ${
                isDark
                  ? 'text-slate-950 bg-white/[0.22] hover:bg-white/[0.38] backdrop-blur-[6px] border border-white/[0.35]'
                  : 'text-slate-900 bg-[#ECF9FF] hover:bg-[#DDF2FD] border border-[#D5ECF8]'
              }`}
            >
              {link.name}
            </Link>
          ))}
        </div>

        {/* Right: Exit [-> and Settings ⚙ icons matching Figma */}
        <div className="flex items-center gap-3.5">
          <Link
            to="/flights"
            className={`p-1.5 rounded-full hover:opacity-80 transition-all ${
              isDark ? 'text-white' : 'text-slate-900'
            }`}
            title="Табло рейсов"
          >
            <LogOut className="w-5 h-5 stroke-[2]" />
          </Link>
          <button
            onClick={() => setIsOpen(true)}
            className={`relative p-1.5 rounded-full hover:opacity-80 transition-all cursor-pointer ${
              isDark ? 'text-white' : 'text-slate-900'
            }`}
            title="Настройки и меню"
          >
            <Settings className="w-5 h-5 stroke-[2]" />
            {favorites.length > 0 && (
              <span className="absolute -top-0.5 -right-0.5 w-4 h-4 rounded-full bg-rose-500 text-white text-[9px] font-bold flex items-center justify-center">
                {favorites.length}
              </span>
            )}
          </button>
        </div>
      </nav>

      {/* Global Slide-Over Navigation Drawer rendered directly in document.body via Portal */}
      {isOpen &&
        createPortal(
          <div className="fixed inset-0 z-[999999] flex isolate" role="dialog" aria-modal="true">
            {/* Backdrop */}
            <div
              onClick={() => setIsOpen(false)}
              className="fixed inset-0 bg-slate-950/60 backdrop-blur-xs transition-opacity cursor-pointer animate-fadeIn"
              aria-label="Закрыть меню"
            />

            {/* Drawer Content */}
            <aside className="relative z-10 w-[300px] sm:w-[340px] h-screen bg-white text-slate-900 shadow-2xl flex flex-col justify-between p-6 overflow-y-auto animate-slideInLeft border-r border-slate-200">
              {/* Header */}
              <div>
                <div className="flex items-center justify-between pb-5 border-b border-slate-100">
                  <div className="flex items-center gap-2">
                    <div className="w-8 h-8 rounded-xl bg-[#EFF7FE] border border-[#D5ECF8] flex items-center justify-center text-sky-600">
                      <Plane className="w-4 h-4 -rotate-45" />
                    </div>
                    <div>
                      <h3 className="font-benzin-bold text-xs uppercase tracking-tight text-slate-950">
                        АВИАРЕЙСЫ
                      </h3>
                      <p className="text-[10px] text-slate-400 font-sans">Информационный сервис</p>
                    </div>
                  </div>

                  <button
                    onClick={() => setIsOpen(false)}
                    className="w-8 h-8 rounded-full bg-slate-100 hover:bg-slate-200 flex items-center justify-center text-slate-600 transition-colors cursor-pointer"
                    aria-label="Закрыть меню"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>

                {/* Navigation List */}
                <div className="py-5 space-y-1.5">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block px-3 mb-2 font-sans">
                    Разделы сервиса
                  </span>

                  {drawerLinks.map((item) => {
                    const Icon = item.icon;
                    return (
                      <Link
                        key={item.name}
                        to={item.path}
                        onClick={(e) => handleLinkClick(e, item.path)}
                        className="w-full flex items-center justify-between px-3.5 py-3 rounded-2xl hover:bg-[#EFF7FE] text-slate-800 hover:text-sky-700 transition-colors group text-xs font-semibold"
                      >
                        <div className="flex items-center gap-3">
                          <Icon className="w-4 h-4 text-slate-500 group-hover:text-sky-600 transition-colors" />
                          <span>{item.name}</span>
                        </div>

                        <div className="flex items-center gap-1.5">
                          {item.badge && (
                            <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-sky-100 text-sky-700">
                              {item.badge}
                            </span>
                          )}
                          {item.count !== undefined && item.count > 0 && (
                            <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-rose-100 text-rose-600">
                              {item.count}
                            </span>
                          )}
                          <ChevronRight className="w-3.5 h-3.5 text-slate-400 group-hover:translate-x-0.5 transition-transform" />
                        </div>
                      </Link>
                    );
                  })}
                </div>
              </div>

              {/* Drawer Footer */}
              <div className="pt-4 border-t border-slate-100 text-[11px] text-slate-500 space-y-2">
                <div className="p-3 rounded-2xl bg-[#F8FCFF] border border-[#E2EEF8] space-y-1">
                  <span className="text-slate-900 font-semibold block">Курсовая работа РПИ</span>
                  <p className="text-[10px] text-slate-500">
                    Разработка веб-интерфейса сервиса об авиарейсах на React.
                  </p>
                </div>
                <p className="text-center text-[10px] text-slate-400">
                  © 2026 Файзрахманова. Все права защищены.
                </p>
              </div>
            </aside>
          </div>,
          document.body
        )}
    </>
  );
};
