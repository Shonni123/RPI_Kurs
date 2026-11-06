import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { LogOut, Settings, X } from 'lucide-react';

interface TopNavProps {
  theme?: 'dark' | 'light';
  className?: string;
}

export const TopNav: React.FC<TopNavProps> = ({ theme = 'dark', className = '' }) => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const isDark = theme === 'dark';

  const navLinks = [
    { name: 'Главная', path: '/' },
    { name: 'Мобильная версия', path: '/#newsletter' },
    { name: 'О сервисе', path: '/#why-us' },
    { name: 'Как это работает', path: '/#features' },
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
    }
  };

  return (
    <nav className={`w-full flex items-center justify-between ${className}`}>
      {/* Left: 3-line hamburger menu - 3 identical parallel lines matching Figma */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex flex-col justify-center items-start gap-1.5 p-1 rounded-lg hover:opacity-80 transition-opacity cursor-pointer"
        aria-label="Меню"
      >
        <span className={`w-6 h-0.5 rounded-full transition-all ${isDark ? 'bg-white' : 'bg-slate-900'}`} />
        <span className={`w-6 h-0.5 rounded-full transition-all ${isDark ? 'bg-white' : 'bg-slate-900'}`} />
        <span className={`w-6 h-0.5 rounded-full transition-all ${isDark ? 'bg-white' : 'bg-slate-900'}`} />
      </button>

      {/* Center: Frosted capsule navigation pills matching Figma reference */}
      <div className="hidden md:flex items-center gap-3 lg:gap-3.5">
        {navLinks.map((link) => (
          <Link
            key={link.name}
            to={link.path}
            onClick={(e) => handleLinkClick(e, link.path)}
            className={`px-5 py-2 rounded-full text-xs sm:text-[13px] font-semibold transition-all duration-200 hover:scale-[1.02] whitespace-nowrap shadow-sm ${
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
          to="/login"
          className={`p-1.5 rounded-full hover:opacity-80 transition-all ${
            isDark ? 'text-white' : 'text-slate-900'
          }`}
          title="Вход / Выход"
        >
          <LogOut className="w-5 h-5 stroke-[2]" />
        </Link>
        <Link
          to="/settings"
          className={`p-1.5 rounded-full hover:opacity-80 transition-all ${
            isDark ? 'text-white' : 'text-slate-900'
          }`}
          title="Настройки"
        >
          <Settings className="w-5 h-5 stroke-[2]" />
        </Link>
      </div>

      {/* Mobile Dropdown */}
      {isOpen && (
        <div className="md:hidden fixed inset-x-4 top-20 z-50 bg-slate-950/95 backdrop-blur-2xl border border-white/20 rounded-3xl p-5 shadow-2xl flex flex-col gap-2.5 animate-fadeIn">
          <div className="flex justify-between items-center pb-2 border-b border-white/10">
            <span className="text-white text-xs font-semibold uppercase tracking-wider font-display">Навигация</span>
            <button onClick={() => setIsOpen(false)} className="text-white/70 hover:text-white p-1">
              <X className="w-5 h-5" />
            </button>
          </div>
          {navLinks.map((link) => (
            <Link
              key={link.name}
              to={link.path}
              onClick={(e) => handleLinkClick(e, link.path)}
              className="px-4 py-3 rounded-2xl text-xs font-medium text-white hover:bg-white/10 transition-all"
            >
              {link.name}
            </Link>
          ))}
          <div className="pt-2 border-t border-white/10 flex items-center justify-around">
            <Link
              to="/flights"
              onClick={() => setIsOpen(false)}
              className="text-white/80 hover:text-white text-xs py-2 px-3 rounded-xl bg-white/10"
            >
              Табло рейсов
            </Link>
            <Link
              to="/about"
              onClick={() => setIsOpen(false)}
              className="text-white/80 hover:text-white text-xs py-2 px-3 rounded-xl bg-white/10"
            >
              О проекте
            </Link>
          </div>
        </div>
      )}
    </nav>
  );
};
