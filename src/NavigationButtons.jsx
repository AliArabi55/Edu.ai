import React from 'react';

const NavigationButtons = () => {
  // دالة للتعامل مع النقر على الأزرار
  const handleNavigation = (direction) => {
    console.log(`التنقل إلى: ${direction}`);
    // هنا يمكنك إضافة منطق التنقل الفعلي
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-8">
      {/* عنوان المكون */}
      <h1 className="text-3xl font-bold text-gray-800 mb-12">
        أزرار التنقل التفاعلية
      </h1>

      {/* مجموعة الأزرار الأفقية */}
      <div className="flex gap-6 mb-8">
        {/* زر السابق */}
        <button
          onClick={() => handleNavigation('السابق')}
          className="
            flex items-center justify-center gap-3 
            px-8 py-4 
            bg-blue-500 text-white font-semibold text-lg
            rounded-xl shadow-md
            transition-all duration-300 ease-in-out
            hover:bg-blue-600 hover:shadow-lg hover:scale-105
            active:scale-95 active:shadow-sm
            transform
          "
        >
          <svg 
            className="w-5 h-5" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M15 19l-7-7 7-7" 
            />
          </svg>
          السابق
        </button>

        {/* زر التالي */}
        <button
          onClick={() => handleNavigation('التالي')}
          className="
            flex items-center justify-center gap-3 
            px-8 py-4 
            bg-green-500 text-white font-semibold text-lg
            rounded-xl shadow-md
            transition-all duration-300 ease-in-out
            hover:bg-green-600 hover:shadow-lg hover:scale-105
            active:scale-95 active:shadow-sm
            transform
          "
        >
          التالي
          <svg 
            className="w-5 h-5" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M9 5l7 7-7 7" 
            />
          </svg>
        </button>
      </div>

      {/* مجموعة الأزرار العمودية */}
      <div className="flex flex-col gap-4 mb-8">
        {/* زر لأعلى */}
        <button
          onClick={() => handleNavigation('لأعلى')}
          className="
            flex items-center justify-center gap-3 
            px-6 py-3 
            bg-purple-500 text-white font-medium
            rounded-xl shadow-md
            transition-all duration-300 ease-in-out
            hover:bg-purple-600 hover:shadow-lg hover:-translate-y-1
            active:translate-y-0 active:shadow-sm
            transform
          "
        >
          <svg 
            className="w-4 h-4" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M5 15l7-7 7 7" 
            />
          </svg>
          لأعلى
        </button>

        {/* زر لأسفل */}
        <button
          onClick={() => handleNavigation('لأسفل')}
          className="
            flex items-center justify-center gap-3 
            px-6 py-3 
            bg-red-500 text-white font-medium
            rounded-xl shadow-md
            transition-all duration-300 ease-in-out
            hover:bg-red-600 hover:shadow-lg hover:translate-y-1
            active:translate-y-0 active:shadow-sm
            transform
          "
        >
          لأسفل
          <svg 
            className="w-4 h-4" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M19 9l-7 7-7-7" 
            />
          </svg>
        </button>
      </div>

      {/* أزرار إضافية بتصميمات مختلفة */}
      <div className="grid grid-cols-2 gap-4 max-w-md w-full">
        {/* زر الرئيسية */}
        <button
          onClick={() => handleNavigation('الرئيسية')}
          className="
            flex items-center justify-center gap-2 
            px-5 py-3 
            bg-gray-700 text-white font-medium text-sm
            rounded-xl shadow-md
            transition-all duration-200 ease-in-out
            hover:bg-gray-800 hover:shadow-lg
            active:scale-95 active:shadow-sm
            transform
          "
        >
          <svg 
            className="w-4 h-4" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" 
            />
          </svg>
          الرئيسية
        </button>

        {/* زر الإعدادات */}
        <button
          onClick={() => handleNavigation('الإعدادات')}
          className="
            flex items-center justify-center gap-2 
            px-5 py-3 
            bg-yellow-500 text-white font-medium text-sm
            rounded-xl shadow-md
            transition-all duration-200 ease-in-out
            hover:bg-yellow-600 hover:shadow-lg
            active:scale-95 active:shadow-sm
            transform
          "
        >
          <svg 
            className="w-4 h-4" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" 
            />
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" 
            />
          </svg>
          الإعدادات
        </button>

        {/* زر الخروج */}
        <button
          onClick={() => handleNavigation('الخروج')}
          className="
            flex items-center justify-center gap-2 
            px-5 py-3 
            bg-orange-500 text-white font-medium text-sm
            rounded-xl shadow-md
            transition-all duration-200 ease-in-out
            hover:bg-orange-600 hover:shadow-lg
            active:scale-95 active:shadow-sm
            transform
          "
        >
          <svg 
            className="w-4 h-4" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" 
            />
          </svg>
          خروج
        </button>

        {/* زر المساعدة */}
        <button
          onClick={() => handleNavigation('المساعدة')}
          className="
            flex items-center justify-center gap-2 
            px-5 py-3 
            bg-indigo-500 text-white font-medium text-sm
            rounded-xl shadow-md
            transition-all duration-200 ease-in-out
            hover:bg-indigo-600 hover:shadow-lg
            active:scale-95 active:shadow-sm
            transform
          "
        >
          <svg 
            className="w-4 h-4" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" 
            />
          </svg>
          مساعدة
        </button>
      </div>
    </div>
  );
};

export default NavigationButtons;