# 🌱 نظام مراقبة المستشعرات - Sensor Monitoring System

نظام متكامل لقراءة ومراقبة مستشعرات ESP32 مع واجهة API قوية وتحليل ذكي باستخدام Gemini AI.

An integrated system for reading and monitoring ESP32 sensors with a powerful API interface and intelligent analysis using Gemini AI.

---

## ✨ المميزات / Features

### 🔄 قراءة البيانات
- ✅ قراءة مستمرة من مستشعرات ESP32 عبر الشبكة
- ✅ حفظ تلقائي للبيانات كل دقيقة في SQLite
- ✅ معالجة الأخطاء والإعادة التلقائية

### 📊 التخزين والقاعدة البيانات
- ✅ قاعدة بيانات SQLite محلية
- ✅ نموذج SQLAlchemy لإدارة البيانات
- ✅ تخزين آخر 4 أسابيع من البيانات (قابل للتخصيص)

### 🚀 واجهة API
- ✅ 10+ endpoints لعرض والتحكم بالبيانات
- ✅ توثيق تلقائي بـ Swagger و ReDoc
- ✅ CORS مفعّل للعمل مع جميع التطبيقات

### 🤖 التحليل الذكي
- ✅ تحليل البيانات باستخدام Gemini Flash
- ✅ توصيات تلقائية حول حالة المستشعرات
- ✅ كشف الحالات الشاذة والتنبيهات

### 📈 الإحصائيات
- ✅ حساب الحد الأدنى والأقصى والمتوسط
- ✅ تحليل الاتجاهات الزمنية
- ✅ مقارنة الفترات الزمنية

---

## 🔧 المكونات / Components

| الملف | الوصف |
|------|-------|
| **esp32_client.py** | برنامج قراءة بيانات ESP32 وحفظها |
| **database.py** | نموذج SQLAlchemy وعمليات قاعدة البيانات |
| **api.py** | خادم FastAPI (الجزء الرئيسي) |
| **api_client.py** | عميل Python تفاعلي للـ API |
| **view_data.py** | برنامج عرض البيانات المحفوظة |
| **requirements.txt** | المكتبات المطلوبة |

---

## 🚀 البدء السريع

### 1. تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

### 2. تشغيل البرنامج (Windows)
```bash
python run.bat
```

أو على Linux/Mac:
```bash
chmod +x run.sh
./run.sh
```

### 3. اختيار الخيار المطلوب
```
1️⃣  تشغيل خادم FastAPI
2️⃣  قراءة بيانات ESP32
3️⃣  عرض البيانات المحفوظة
4️⃣  عميل API التفاعلي
```

---

## 📡 قراءة بيانات ESP32

```bash
python esp32_client.py
```

**الإخراج:**
```
متصل بـ ESP32 على http://192.168.1.17/data

🌡️  temp:     25.5 °C
💧 humidity: 60.0 %
🌱 soil:     50 % 🟢 wet (raw: 500)
💨 gas:      400  →  ✅ normal
💡 light:    75 % ☀️ bright (raw: 800)
--------------------------------------------------
💾 تم حفظ القراءة في قاعدة البيانات
```

---

## 🚀 API Server

تشغيل الخادم:
```bash
python api.py
```

الخادم متاح على:
- **Base URL**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc Docs**: http://localhost:8000/redoc

### أمثلة على الاستخدام

#### الحصول على آخر قراءة
```bash
curl http://localhost:8000/api/readings/latest
```

#### الحصول على آخر 50 قراءة
```bash
curl http://localhost:8000/api/readings?limit=50
```

#### الحصول على ملخص الحالة الحالية
```bash
curl http://localhost:8000/api/summary/current
```

#### الإحصائيات (آخر 24 ساعة)
```bash
curl http://localhost:8000/api/statistics?hours=24
```

#### تحليل ذكي بـ Gemini
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "query": "تحليل حالة المستشعرات",
    "limit": 10
  }'
```

---

## 🖥️ عميل API التفاعلي

```bash
python api_client.py
```

يوفر واجهة تفاعلية لـ:
- ✅ عرض البيانات
- ✅ الإحصائيات
- ✅ التحليل الذكي
- ✅ التحكم بـ Relay
- ✅ إضافة بيانات يدويًا

---

## 📊 عرض البيانات المحفوظة

```bash
python view_data.py
```

الخيارات:
1. آخر 20 قراءة
2. قراءات اليوم
3. آخر 24 ساعة
4. آخر 7 أيام

---

## 🤖 تحليل Gemini AI

يتم التحليل تلقائياً على المنصات التالية:

### عبر API
```bash
POST /api/analyze
{
  "query": "أي سؤال عن البيانات",
  "limit": 10
}
```

### عبر عميل Python
```python
from api_client import SensorAPIClient

client = SensorAPIClient()
analysis = client.analyze_data("هل المستشعرات تعمل بشكل صحيح؟")
print(analysis['analysis'])
```

---

## 📈 البيانات المحفوظة

كل قراءة تحتوي على:

```json
{
  "id": 1,
  "timestamp": "2026-04-29T10:25:00",
  "temp": 25.5,           // درجة الحرارة °C
  "humidity": 60.0,       // الرطوبة %
  "gas_raw": 400,         // قيمة الغاز الخام
  "gas_alert": false,     // تنبيه الغاز
  "light_pct": 75,        // كثافة الضوء %
  "light_raw": 800,       // قيمة الضوء الخام
  "soil_pct": 50,         // رطوبة التربة %
  "soil_raw": 500         // قيمة التربة الخام
}
```

---

## ⚙️ التكوين

### تغيير عنوان IP للـ ESP32
في `esp32_client.py`:
```python
ESP32_IP = "192.168.1.YOUR_IP"
```

### تغيير فترة الحفظ
في `esp32_client.py`:
```python
SAVE_INTERVAL = 60  # كل 60 ثانية
```

### تغيير مفتاح Gemini API
في `api.py`:
```python
GEMINI_API_KEY = "YOUR_API_KEY"
```

أو استخدم متغيرات البيئة:
```bash
export GEMINI_API_KEY=your_key
```

---

## 📚 التوثيق الكاملة

اقرأ [API_DOCS.md](API_DOCS.md) للحصول على:
- ✅ جميع الـ Endpoints المتاحة
- ✅ أمثلة مفصلة بـ curl و Python
- ✅ أمثلة JavaScript/Node.js
- ✅ لوحة تحكم HTML

---

## 🔐 الأمان

⚠️ **ملاحظات أمان مهمة:**

1. **المفاتيح الحساسة**: استخدم متغيرات البيئة بدلاً من حفظها في الكود
   ```bash
   export GEMINI_API_KEY=your_key
   ```

2. **المصادقة**: أضف OAuth2 في الإنتاج
   ```python
   from fastapi.security import OAuth2PasswordBearer
   ```

3. **HTTPS**: استخدم HTTPS في الإنتاج
   ```bash
   gunicorn --certfile=cert.pem --keyfile=key.pem api:app
   ```

4. **CORS**: حدد النطاقات المسموحة:
   ```python
   allow_origins=["https://yourdomain.com"]
   ```

---

## 🔧 استكشاف الأخطاء

### ❌ الخادم لا يعمل
```bash
python api.py
# يجب أن ترى:
# INFO:     Application startup complete [uvicorn]
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

### ❌ خطأ في قاعدة البيانات
```bash
# احذف قاعدة البيانات وأنشئها من جديد
rm sensor_data.db
python esp32_client.py
```

### ❌ خطأ في الاتصال بـ ESP32
- تحقق من عنوان IP الصحيح
- تأكد من اتصال الـ Wi-Fi
- اختبر الاتصال:
  ```bash
  curl http://192.168.1.YOUR_IP/data
  ```

### ❌ خطأ في Gemini API
- تحقق من صحة المفتاح
- تأكد من الاتصال بالإنترنت
- اختبر الاتصال:
  ```bash
  curl https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent
  ```

---

## 📦 المتطلبات

```
requests==2.31.0           # HTTP requests
SQLAlchemy==2.0.25         # ORM
tabulate==0.9.0            # جداول بصيغة جميلة
fastapi==0.109.0           # Web framework
uvicorn==0.27.0            # ASGI server
pydantic==2.6.0            # Data validation
google-generativeai==0.3.0 # Gemini AI
```

---

## 🌟 الميزات المستقبلية

- [ ] لوحة تحكم ويب تفاعلية
- [ ] تصدير البيانات إلى CSV/Excel
- [ ] رسوم بيانية والعروض المرئية
- [ ] إرسال تنبيهات عند تجاوز القيم الحدية
- [ ] التكامل مع قواعد بيانات سحابية
- [ ] تطبيق mobile
- [ ] المزيد من الحسابات الإحصائية

---

## 📞 الدعم

في حالة وجود مشاكل:
1. اقرأ الأسئلة الشائعة في API_DOCS.md
2. تحقق من سجلات الأخطاء
3. تأكد من تثبيت جميع المتطلبات

---

## 📄 الرخصة

تحقق من ملف LICENSE

---

## 👨‍💻 المؤلف

نظام مراقبة المستشعرات - Sensor Monitoring System
عام 2026

---

## 🎯 الخطوات الأولى الموصى بها

1. **ابدأ بقراءة البيانات**:
   ```bash
   python esp32_client.py
   ```

2. **شغّل خادم API**:
   ```bash
   python api.py
   ```

3. **اختبر الـ API** في متصفح:
   ```
   http://localhost:8000/docs
   ```

4. **استخدم عميل Python**:
   ```bash
   python api_client.py
   ```

5. **اقرأ التوثيق الكاملة**:
   - [API_DOCS.md](API_DOCS.md)
   - [README_AR.md](README_AR.md)

---

**Happy Monitoring! 🌱📊**
