import React from 'react';
import { Send, Globe } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-white border-t border-slate-100 py-12 px-4 sm:px-6 lg:px-8 text-slate-500 text-xs">
      <div className="max-w-7xl mx-auto flex flex-col items-center justify-center gap-6 text-center">
        
        {/* Social Icons matching Figma (VK, Telegram, YouTube) */}
        <div className="flex items-center gap-4">
          <a
            href="https://vk.com"
            target="_blank"
            rel="noreferrer"
            className="w-10 h-10 rounded-full bg-slate-900 hover:bg-blue-600 text-white flex items-center justify-center transition-all hover:scale-105 shadow-md"
            title="ВКонтакте"
          >
            <span className="font-bold text-xs">VK</span>
          </a>
          <a
            href="https://t.me"
            target="_blank"
            rel="noreferrer"
            className="w-10 h-10 rounded-full bg-slate-900 hover:bg-sky-500 text-white flex items-center justify-center transition-all hover:scale-105 shadow-md"
            title="Telegram"
          >
            <Send className="w-4 h-4 -rotate-12" />
          </a>
          <a
            href="https://youtube.com"
            target="_blank"
            rel="noreferrer"
            className="w-10 h-10 rounded-full bg-slate-900 hover:bg-red-600 text-white flex items-center justify-center transition-all hover:scale-105 shadow-md"
            title="YouTube"
          >
            <Globe className="w-4 h-4" />
          </a>
        </div>

        {/* Copyright matching Figma text */}
        <p className="text-slate-400">
          © 2026 Файзрахманова. Все права защищены. Курсовая работа РПИ.
        </p>
      </div>
    </footer>
  );
};
