import React from 'react';
import { ShieldCheck, Zap, Smartphone, ArrowLeft, Layers, CheckCircle2 } from 'lucide-react';
import { Link } from 'react-router-dom';

export const AboutPage: React.FC = () => {
  const stack = [
    { title: 'Frontend Framework', tech: 'React 19 + TypeScript', desc: 'Строгая типизация компонентов, хуки, современный компонентный подход.' },
    { title: 'Build Tool & Bundler', tech: 'Vite 6', desc: 'Сверхбыстрый HMR и оптимизированная сборка с tree-shaking.' },
    { title: 'Styling & Tokens', tech: 'Tailwind CSS', desc: 'Дизайн-система по макетам из Figma: Benzin, TT Travels, frosted glass.' },
    { title: 'Routing', tech: 'React Router v7', desc: 'Клиентская маршрутизация, плавный якорный скроллинг, обработка 404.' },
    { title: 'Architecture', tech: 'Component-Driven UI', desc: 'Модульная структура, переиспользуемые виджеты, адаптивность.' },
    { title: 'Data Management', tech: 'Mock API + LocalStorage', desc: 'Имитация асинхронной загрузки, фильтрация и сохранение избранного.' },
  ];

  return (
    <div className="min-h-screen bg-[#F8FCFF] text-slate-900 pt-6 sm:pt-8 pb-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto space-y-8 sm:space-y-10">
        
        {/* Navigation Breadcrumb */}
        <div className="flex items-center justify-between">
          <Link
            to="/"
            className="inline-flex items-center gap-2 text-xs font-semibold text-slate-600 hover:text-slate-950 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Вернуться на главную</span>
          </Link>
        </div>

        {/* Header */}
        <div className="border-b border-[#E2EEF8] pb-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#EFF7FE] border border-[#D5ECF8] text-[11px] font-semibold text-sky-700 mb-2">
            <Layers className="w-3.5 h-3.5 text-sky-600" />
            <span>КУРСОВАЯ РАБОТА РПИ</span>
          </div>
          <h1 className="font-benzin-bold text-2xl sm:text-3xl lg:text-4xl uppercase tracking-tight text-slate-950">
            О сервисе и архитектуре
          </h1>
          <p className="font-tt-travels text-xs sm:text-sm text-slate-600 mt-2 max-w-2xl leading-relaxed">
            Тема: «Разработка веб-интерфейса для информационного сервиса об авиарейсах на React».
          </p>
        </div>

        {/* Project Goals */}
        <div className="p-6 sm:p-8 rounded-[30px] sm:rounded-[36px] bg-white border border-[#E2EEF8] shadow-sm space-y-6">
          <h2 className="font-benzin-bold text-lg sm:text-xl text-slate-950 uppercase tracking-tight">
            Цели и ключевые задачи
          </h2>
          <p className="font-tt-travels text-xs sm:text-sm text-slate-700 leading-relaxed">
            Сервис разработан для оперативного информирования пассажиров и встречающих об актуальном статусе авиаперелётов в режиме реального времени. Интерфейс адаптирован для мобильных устройств, планшетов и широкоформатных экранов, полностью повторяя макеты из Figma с соблюдением требований к дизайну и юзабилити.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2">
            <div className="p-4 rounded-2xl bg-[#F8FCFF] border border-[#E2EEF8] space-y-1.5">
              <Zap className="w-5 h-5 text-amber-500" />
              <h4 className="font-tt-travels font-bold text-sm text-slate-900">Высокая скорость</h4>
              <p className="text-xs text-slate-500 font-sans leading-relaxed">Быстрый отклик и мгновенная фильтрация рейсов без перезагрузки страниц.</p>
            </div>
            <div className="p-4 rounded-2xl bg-[#F8FCFF] border border-[#E2EEF8] space-y-1.5">
              <ShieldCheck className="w-5 h-5 text-emerald-600" />
              <h4 className="font-tt-travels font-bold text-sm text-slate-900">Надёжность данных</h4>
              <p className="text-xs text-slate-500 font-sans leading-relaxed">Обработка ошибок сети, пустого поиска и локальное сохранение закладок.</p>
            </div>
            <div className="p-4 rounded-2xl bg-[#F8FCFF] border border-[#E2EEF8] space-y-1.5">
              <Smartphone className="w-5 h-5 text-sky-600" />
              <h4 className="font-tt-travels font-bold text-sm text-slate-900">Адаптивность</h4>
              <p className="text-xs text-slate-500 font-sans leading-relaxed">Комфортное использование на смартфонах, планшетах и компьютерах.</p>
            </div>
          </div>
        </div>

        {/* Tech Stack Grid */}
        <div className="space-y-5">
          <h2 className="font-benzin-bold text-lg sm:text-xl text-slate-950 uppercase tracking-tight">
            Технологический стек проекта
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {stack.map((item, idx) => (
              <div key={idx} className="p-5 rounded-[24px] bg-white border border-[#E2EEF8] space-y-2 shadow-xs hover:border-[#BCE0F8] transition-colors">
                <span className="text-[11px] font-bold text-sky-700 uppercase tracking-wider block font-sans">{item.title}</span>
                <h4 className="font-tt-travels font-bold text-sm text-slate-950 flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0" />
                  <span>{item.tech}</span>
                </h4>
                <p className="text-xs text-slate-600 leading-relaxed font-sans">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
};
