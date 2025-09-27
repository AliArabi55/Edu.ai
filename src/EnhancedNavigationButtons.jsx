import React, { useState } from 'react';

const EnhancedNavigationButtons = () => {
  const [activeButton, setActiveButton] = useState(null);

  // دالة إضافة تأثير الموجة عند الضغط
  const addRippleEffect = (e) => {
    const button = e.currentTarget;
    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;

    const ripple = document.createElement('span');
    ripple.style.cssText = `
      position: absolute;
      width: ${size}px;
      height: ${size}px;
      left: ${x}px;
      top: ${y}px;
      background: rgba(255, 255, 255, 0.6);
      border-radius: 50%;
      transform: scale(0);
      animation: ripple 0.6s linear;
      pointer-events: none;
    `;

    button.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
  };

  // دالة التعامل مع النقر
  const handleClick = (direction, e) => {
    addRippleEffect(e);
    setActiveButton(direction);
    setTimeout(() => setActiveButton(null), 200);
    console.log(`التنقل إلى: ${direction}`);
  };

  // كلاس الزر الأساسي - بدون تأثيرات على الحجم
  const baseButtonClass = `
    relative overflow-hidden
    flex items-center justify-center gap-3
    font-semibold text-white
    rounded-xl shadow-md
    transition-all duration-300 ease-out
    focus:outline-none focus:ring-4 focus:ring-opacity-50
    transform-gpu
  `;

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-gray-100 to-gray-200 p-8">
      
      {/* العنوان */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-800 mb-4">
          أزرار التنقل التفاعلية
        </h1>
        <p className="text-gray-600 text-lg">
          تفاعلية فقط على الأزرار - بدون تأثيرات على الشاشة
        </p>
      </div>

      {/* الأزرار الرئيسية */}
      <div className="flex gap-8 mb-12">
        {/* زر السابق */}
        <button
          onClick={(e) => handleClick('السابق', e)}
          className={`
            ${baseButtonClass}
            px-10 py-5 text-xl
            bg-gradient-to-r from-blue-500 to-blue-600
            hover:from-blue-600 hover:to-blue-700 hover:shadow-xl
            focus:ring-blue-300
            active:scale-95
            ${activeButton === 'السابق' ? 'scale-95' : ''}
          `}
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          السابق
        </button>

        {/* زر التالي */}
        <button
          onClick={(e) => handleClick('التالي', e)}
          className={`
            ${baseButtonClass}
            px-10 py-5 text-xl
            bg-gradient-to-r from-green-500 to-green-600
            hover:from-green-600 hover:to-green-700 hover:shadow-xl
            focus:ring-green-300
            active:scale-95
            ${activeButton === 'التالي' ? 'scale-95' : ''}
          `}
        >
          التالي
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      {/* أزرار الاتجاهات */}
      <div className="flex flex-col items-center gap-4 mb-12">
        {/* زر لأعلى */}
        <button
          onClick={(e) => handleClick('لأعلى', e)}
          className={`
            ${baseButtonClass}
            px-8 py-4 text-lg
            bg-gradient-to-r from-purple-500 to-purple-600
            hover:from-purple-600 hover:to-purple-700 hover:shadow-lg
            focus:ring-purple-300
            active:scale-95
            ${activeButton === 'لأعلى' ? 'scale-95' : ''}
          `}
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
          </svg>
          لأعلى
        </button>

        <div className="flex gap-6">
          {/* زر لليسار */}
          <button
            onClick={(e) => handleClick('لليسار', e)}
            className={`
              ${baseButtonClass}
              px-6 py-3
              bg-gradient-to-r from-orange-500 to-orange-600
              hover:from-orange-600 hover:to-orange-700 hover:shadow-lg
              focus:ring-orange-300
              active:scale-95
              ${activeButton === 'لليسار' ? 'scale-95' : ''}
            `}
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            يسار
          </button>

          {/* زر لليمين */}
          <button
            onClick={(e) => handleClick('لليمين', e)}
            className={`
              ${baseButtonClass}
              px-6 py-3
              bg-gradient-to-r from-teal-500 to-teal-600
              hover:from-teal-600 hover:to-teal-700 hover:shadow-lg
              focus:ring-teal-300
              active:scale-95
              ${activeButton === 'لليمين' ? 'scale-95' : ''}
            `}
          >
            يمين
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>

        {/* زر لأسفل */}
        <button
          onClick={(e) => handleClick('لأسفل', e)}
          className={`
            ${baseButtonClass}
            px-8 py-4 text-lg
            bg-gradient-to-r from-red-500 to-red-600
            hover:from-red-600 hover:to-red-700 hover:shadow-lg
            focus:ring-red-300
            active:scale-95
            ${activeButton === 'لأسفل' ? 'scale-95' : ''}
          `}
        >
          لأسفل
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>
      </div>

      {/* أزرار إضافية بتصميمات متنوعة */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl w-full">
        {[
          { name: 'الرئيسية', color: 'gray', icon: 'home' },
          { name: 'الإعدادات', color: 'yellow', icon: 'settings' },
          { name: 'المساعدة', color: 'indigo', icon: 'help' },
          { name: 'الخروج', color: 'pink', icon: 'exit' }
        ].map((btn) => (
          <button
            key={btn.name}
            onClick={(e) => handleClick(btn.name, e)}
            className={`
              ${baseButtonClass}
              px-5 py-4 text-sm
              bg-gradient-to-r from-${btn.color}-500 to-${btn.color}-600
              hover:from-${btn.color}-600 hover:to-${btn.color}-700 hover:shadow-lg
              focus:ring-${btn.color}-300
              active:scale-95
              ${activeButton === btn.name ? 'scale-95' : ''}
            `}
          >
            {/* الأيقونات */}
            {btn.icon === 'home' && (
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
            )}
            {btn.icon === 'settings' && (
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            )}
            {btn.icon === 'help' && (
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            )}
            {btn.icon === 'exit' && (
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
            )}
            {btn.name}
          </button>
        ))}
      </div>

      {/* تعليمات الاستخدام */}
      <div className="mt-12 text-center">
        <p className="text-gray-600 text-sm">
          الأزرار تفاعلية فقط - بدون تأثيرات على الشاشة �
        </p>
      </div>

      {/* إضافة CSS للموجة */}
      <style jsx>{`
        @keyframes ripple {
          to {
            transform: scale(4);
            opacity: 0;
          }
        }
      `}</style>
    </div>
  );
};

export default EnhancedNavigationButtons;