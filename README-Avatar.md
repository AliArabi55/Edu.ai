# 🎓 Edu.ai - منصة التعلم بالذكاء الاصطناعي

## نظرة عامة
Edu.ai هي منصة تعليمية تفاعلية مصممة لتعليم الأطفال والمراهقين (6-18 سنة) مهارات البرمجة والذكاء الاصطناعي باستخدام أحدث التقنيات.

## 🚀 المميزات الجديدة

### 🤖 المساعد الصوتي الذكي (Avatar.py)
- مساعد ذكي مدعوم بـ Azure OpenAI VoiceLive
- تفاعل صوتي طبيعي باللغة الإنجليزية
- إرشادات تعليمية مخصصة
- دعم للدروس التفاعلية

## 📁 هيكل المشروع

```
Edu.ai/
├── .env                    # متغيرات البيئة (Azure Keys)
├── index.html             # الصفحة الرئيسية الجديدة
├── launch_avatar.py       # سكريبت تشغيل Avatar
├── Edu.ai/
│   ├── 1.Land page/       # صفحة الهبوط الأساسية
│   ├── 2.Login/          # صفحة تسجيل الدخول
│   ├── 3.Sign up/        # صفحة التسجيل
│   ├── 4.select language/ # اختيار اللغة
│   ├── 5.courses/        # الدورات التعليمية
│   ├── 6.1.Start Lesson/ # بداية الدرس (محدثة بـ Avatar)
│   ├── 6.2/              # يحتوي على Avatar.py
│   ├── 7.Quiz 1/         # الاختبارات
│   └── 8.Score/          # النتائج
└── src/                  # ملفات React (اختيارية)
```

## ⚡ التشغيل السريع

### 1. بدء الخادم
```bash
cd "C:\Users\aliar\OneDrive\Documents\GitHub\Edu.ai"
python -m http.server 8000
```

### 2. الوصول للتطبيق
- **الصفحة الرئيسية**: http://localhost:8000
- **صفحة الهبوط**: http://localhost:8000/Edu.ai/1.Land%20page/
- **المساعد الذكي**: http://localhost:8000/Edu.ai/6.1.Start%20Lesson/

## 🤖 تشغيل المساعد الصوتي

### المتطلبات المثبتة:
- ✅ Python 3.12.6
- ✅ azure-ai-voicelive
- ✅ pyaudio
- ✅ python-dotenv
- ✅ azure-core
- ✅ azure-identity

### تشغيل Avatar يدوياً:
```bash
cd "C:\Users\aliar\OneDrive\Documents\GitHub\Edu.ai\Edu.ai\6.2"
python Avatar.py --endpoint https://your-resource-name.cognitiveservices.azure.com/ --api-key [YOUR_KEY] --model gpt-4o-realtime-preview --voice alloy
```

### أو استخدام السكريبت المساعد:
```bash
cd "C:\Users\aliar\OneDrive\Documents\GitHub\Edu.ai"
python launch_avatar.py
```

## 🔐 الإعدادات

### ملف .env:
```env
AZURE_OPENAI_ENDPOINT=https://your-resource-name.cognitiveservices.azure.com/
AZURE_OPENAI_KEY=your_azure_openai_key_here
AZURE_OPENAI_REGION=your_region

AZURE_VOICELIVE_ENDPOINT=https://your-resource-name.cognitiveservices.azure.com/
AZURE_VOICELIVE_API_KEY=your_azure_openai_key_here
AZURE_VOICELIVE_REGION=your_region
```

## 🎯 كيفية استخدام المساعد الصوتي

1. **ابدأ التطبيق**: افتح http://localhost:8000
2. **اذهب للدروس**: اضغط على "ابدأ رحلة التعلم" أو انتقل مباشرة للمساعد الذكي
3. **في صفحة 6.1.Start Lesson**: اضغط على "Start Avatar Lesson"
4. **اتبع التعليمات**: سيبدأ المساعد الصوتي تلقائياً
5. **ابدأ التحدث**: تحدث باللغة الإنجليزية مع المساعد

## 🛠️ الإصلاحات المطبقة

### في Avatar.py:
- ✅ إصلاح أخطاء السلاسل النصية (`\n` بدلاً من أسطر جديدة مكسورة)
- ✅ تحديث استيراد `AudioFormat` إلى `InputAudioFormat`
- ✅ إعداد متغيرات البيئة الصحيحة

### في 6.1.Start Lesson:
- ✅ إضافة واجهة تحكم بـ Avatar
- ✅ إضافة مؤشرات التحميل والحالة
- ✅ ربط الزر بتشغيل Avatar

## 🔧 استكشاف الأخطاء

### إذا لم يعمل المساعد الصوتي:
1. تأكد من وجود الميكروفون والسماعات
2. تحقق من مفاتيح Azure في ملف `.env`
3. تأكد من تشغيل الخادم على المنفذ 8000
4. جرب تشغيل Avatar.py مباشرة من Terminal

### إذا كانت هناك مشاكل في الصوت:
```bash
# اختبار PyAudio
python -c "import pyaudio; print('PyAudio works!')"

# اختبار Azure VoiceLive
python -c "from azure.ai.voicelive.models import *; print('VoiceLive works!')"
```

## 📞 الدعم الفني

- **المطور**: تم التطوير بواسطة GitHub Copilot
- **التاريخ**: سبتمبر 2025
- **الإصدار**: v2.0 مع دعم Avatar AI

## 🎨 التخصيص

يمكنك تخصيص المساعد الصوتي من خلال:
- تغيير الصوت (`--voice` parameter)
- تعديل التعليمات (`--instructions` parameter)
- تغيير نموذج AI (`--model` parameter)

## 🚀 التطوير المستقبلي

- [ ] دعم اللغة العربية في المساعد الصوتي
- [ ] إضافة المزيد من الأصوات
- [ ] تكامل أعمق مع صفحات الاختبار
- [ ] حفظ جلسات التعلم
- [ ] تتبع التقدم الصوتي

---
**استمتع بتجربة التعلم التفاعلية مع Edu.ai! 🎓✨**