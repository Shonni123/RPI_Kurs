import React from 'react';
import { ShieldCheck, Zap, Smartphone } from 'lucide-react';

export const AboutPage: React.FC = () => {
  const stack = [
    { title: 'Frontend Framework', tech: 'React 19 + TypeScript', desc: 'Строгая типизация компонентов, современный компонентный подход.' },
    { title: 'Build Tool & Bundler', tech: 'Vite 6', desc: 'Сверхбыстрый HMR и оптимизированная сборка с tree-shaking.' },
    { title: 'Styling & Tokens', tech: 'Tailwind CSS', desc: 'Утилитарный дизайн по дизайн-системе из Figma.' },
    { title: 'Routing', tech: 'React Router v7', desc: 'Динамические пути, вложенные лейауты и обработка 404.' },
    { title: 'Backend (Fullstack)', tech: 'Python 3 + Django REST Framework', desc: 'REST API, ORM, база данных SQLite/PostgreSQL.' },
    { title: 'Infrastructure', tech: 'Docker & Docker Compose', desc: 'Изоляция окружения и развертывание в один клик.' },
  ];

  return (
    <div className="min-h-screen pt-28 pb-20 px-4 sm:px-6 lg:px-8 bg-[#0B0F19] text-white">
      <div className="max-w-5xl mx-auto space-y-12">
        
        {/* Header */}
        <div className="border-b border-white/10 pb-6 text-center sm:text-left">
          <span className="text-xs font-semibold tracking-widest text-blue-400 uppercase">
            О проекте и архитектуре
          </span>
          <h1 className="font-display font-black text-2xl sm:text-4xl uppercase tracking-tight text-white mt-1">
            Курсовая работа РПИ
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-2 max-w-2xl">
            Тема: «Разработка веб-интерфейса для информационного сервиса об авиарейсах на React».
          </p>
        </div>

        {/* Project Goals */}
        <div className="p-8 rounded-3xl bg-[#161F30]/70 border border-white/10 space-y-4">
          <h2 className="font-display font-bold text-lg sm:text-xl text-white">
            Цели и ключевые задачи
          </h2>
          <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
            Сервис разработан для оперативного информирования пассажиров и встречающих об актуальном статусе авиаперелётов. Интерфейс адаптирован для мобильных устройств, планшетов и широкоформатных экранов, полностью повторяя макеты из Figma с сохранением авиационной эстетики.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2">
            <div className="p-4 rounded-2xl bg-black/30 border border-white/5 space-y-1">
              <Zap className="w-5 h-5 text-amber-400" />
              <h4 className="font-bold text-sm text-white">Высокая скорость</h4>
              <p className="text-xs text-slate-400">Быстрый отклик и мгновенная фильтрация рейсов.</p>
            </div>
            <div className="p-4 rounded-2xl bg-black/30 border border-white/5 space-y-1">
              <ShieldCheck className="w-5 h-5 text-emerald-400" />
              <h4 className="font-bold text-sm text-white">Надёжность</h4>
              <p className="text-xs text-slate-400">Обработка ошибок сети и сохранение закладок офлайн.</p>
            </div>
            <div className="p-4 rounded-2xl bg-black/30 border border-white/5 space-y-1">
              <Smartphone className="w-5 h-5 text-sky-400" />
              <h4 className="font-bold text-sm text-white">Адаптивность</h4>
              <p className="text-xs text-slate-400">Идеальная вёрстка на смартфонах, планшетах и ПК.</p>
            </div>
          </div>
        </div>

        {/* Tech Stack Grid */}
        <div className="space-y-6">
          <h2 className="font-display font-bold text-lg sm:text-xl text-white">
            Технологический стек проекта
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {stack.map((item, idx) => (
              <div key={idx} className="p-5 rounded-2xl bg-[#161F30]/60 border border-white/10 space-y-2">
                <span className="text-[11px] font-bold text-blue-400 uppercase">{item.title}</span>
                <h4 className="font-bold text-sm text-white">{item.tech}</h4>
                <p className="text-xs text-slate-400 leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
};
