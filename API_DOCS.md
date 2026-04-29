# 🚀 FastAPI Documentation - نظام مراقبة المستشعرات

## البدء السريع

### تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

### تشغيل الخادم
```bash
python api.py
```

الخادم سيعمل على: `http://localhost:8000`

### فتح توثيق Swagger
```
http://localhost:8000/docs
```

### فتح توثيق ReDoc
```
http://localhost:8000/redoc
```

---

## API Endpoints

### 1️⃣ فحص صحة الخادم
```bash
curl http://localhost:8000/health
```

**الاستجابة:**
```json
{
  "status": "🟢 سليم",
  "timestamp": "2026-04-29T10:30:00",
  "api_version": "1.0.0"
}
```

---

### 2️⃣ الحصول على آخر قراءة
```bash
curl http://localhost:8000/api/readings/latest
```

**الاستجابة:**
```json
{
  "id": 1,
  "timestamp": "2026-04-29T10:25:00",
  "temp": 25.5,
  "humidity": 60.0,
  "gas_raw": 400,
  "gas_alert": false,
  "light_pct": 75,
  "light_raw": 800,
  "soil_pct": 50,
  "soil_raw": 500
}
```

---

### 3️⃣ الحصول على عدة قراءات
```bash
# آخر 20 قراءة (افتراضي)
curl http://localhost:8000/api/readings

# آخر 50 قراءة
curl http://localhost:8000/api/readings?limit=50
```

---

### 4️⃣ قراءات اليوم
```bash
curl http://localhost:8000/api/readings/today
```

---

### 5️⃣ قراءات في نطاق زمني
```bash
curl "http://localhost:8000/api/readings/range?start=2026-04-29%2000:00:00&end=2026-04-29%2023:59:59"
```

---

### 6️⃣ ملخص الحالة الحالية
```bash
curl http://localhost:8000/api/summary/current
```

**الاستجابة:**
```json
{
  "status": "🟢 نشط",
  "timestamp": "2026-04-29T10:25:00",
  "temperature": {
    "value": 25.5,
    "unit": "°C",
    "status": "🟢"
  },
  "humidity": {
    "value": 60.0,
    "unit": "%",
    "status": "🟢"
  },
  "soil": {
    "moisture": 50,
    "unit": "%",
    "raw": 500,
    "status": "🟢 رطب"
  },
  "light": {
    "intensity": 75,
    "unit": "%",
    "raw": 800,
    "status": "☀️ مشرق"
  },
  "gas": {
    "value": 400,
    "alert": false,
    "status": "✅ عادي"
  }
}
```

---

### 7️⃣ الإحصائيات
```bash
# آخر 24 ساعة (افتراضي)
curl http://localhost:8000/api/statistics

# آخر 7 أيام
curl http://localhost:8000/api/statistics?hours=168

# آخر ساعة
curl http://localhost:8000/api/statistics?hours=1
```

**الاستجابة:**
```json
{
  "period_hours": 24,
  "total_readings": 1440,
  "temperature": {
    "min": 20.5,
    "max": 30.2,
    "avg": 25.1
  },
  "humidity": {
    "min": 45.0,
    "max": 75.0,
    "avg": 60.0
  },
  "soil_moisture": {
    "min": 30,
    "max": 80,
    "avg": 55
  },
  "light_intensity": {
    "min": 10,
    "max": 100,
    "avg": 60
  },
  "gas": {
    "min": 300,
    "max": 600,
    "avg": 400
  }
}
```

---

### 8️⃣ تحليل ذكي بـ Gemini AI
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "query": "تحليل حالة المستشعرات الحالية وإعطاء توصيات",
    "limit": 10
  }'
```

**الاستجابة:**
```json
{
  "analysis": "بناءً على البيانات المجمعة في آخر ساعة:\n\n🌡️ درجة الحرارة: مستقرة عند 25.5°C وهي مثالية...",
  "readings_count": 10,
  "timestamp": "2026-04-29T10:30:00"
}
```

---

### 9️⃣ التحكم بـ Relay
```bash
# تشغيل
curl -X POST "http://localhost:8000/api/control/relay?action=on"

# إيقاف
curl -X POST "http://localhost:8000/api/control/relay?action=off"
```

---

### 🔟 إضافة قراءة يدويًا
```bash
curl -X POST http://localhost:8000/api/readings/add \
  -H "Content-Type: application/json" \
  -d '{
    "temp": 26.0,
    "humidity": 61.0,
    "gas_raw": 410,
    "gas_alert": false,
    "light_pct": 76,
    "light_raw": 810,
    "soil_pct": 51,
    "soil_raw": 510
  }'
```

---

## Python Client Examples

### مثال 1: قراءة البيانات
```python
import requests

BASE_URL = "http://localhost:8000"

# آخر قراءة
response = requests.get(f"{BASE_URL}/api/readings/latest")
data = response.json()
print(data)

# آخر 50 قراءة
response = requests.get(f"{BASE_URL}/api/readings?limit=50")
readings = response.json()
for reading in readings:
    print(f"{reading['timestamp']}: {reading['temp']}°C")
```

### مثال 2: التحليل الذكي
```python
import requests
import json

BASE_URL = "http://localhost:8000"

response = requests.post(
    f"{BASE_URL}/api/analyze",
    json={
        "query": "هل هناك أي مشاكل في البيانات؟ وما التوصيات؟",
        "limit": 20
    }
)

analysis = response.json()
print("🤖 تحليل Gemini:")
print(analysis['analysis'])
```

### مثال 3: الإحصائيات
```python
import requests

BASE_URL = "http://localhost:8000"

response = requests.get(f"{BASE_URL}/api/statistics?hours=24")
stats = response.json()

print(f"عدد القراءات: {stats['total_readings']}")
print(f"درجة الحرارة المتوسطة: {stats['temperature']['avg']:.1f}°C")
print(f"الرطوبة المتوسطة: {stats['humidity']['avg']:.1f}%")
```

### مثال 4: مراقبة حية
```python
import requests
import time

BASE_URL = "http://localhost:8000"

print("🔄 مراقبة حية للمستشعرات:")
while True:
    response = requests.get(f"{BASE_URL}/api/summary/current")
    data = response.json()
    
    print(f"""
🌡️  درجة الحرارة: {data['temperature']['value']}°C {data['temperature']['status']}
💧 الرطوبة: {data['humidity']['value']}% {data['humidity']['status']}
🌱 التربة: {data['soil']['moisture']}% {data['soil']['status']}
💡 الضوء: {data['light']['intensity']}% {data['light']['status']}
💨 الغاز: {data['gas']['status']}
    """)
    
    time.sleep(5)  # تحديث كل 5 ثوان
```

---

## JavaScript/Node.js Client

```javascript
const BASE_URL = 'http://localhost:8000';

// قراءة البيانات
async function getLatestReading() {
    const response = await fetch(`${BASE_URL}/api/readings/latest`);
    const data = await response.json();
    console.log(data);
}

// التحليل الذكي
async function analyzeData() {
    const response = await fetch(`${BASE_URL}/api/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            query: 'تحليل كامل للبيانات',
            limit: 20
        })
    });
    const data = await response.json();
    console.log('تحليل Gemini:', data.analysis);
}

// الإحصائيات
async function getStatistics() {
    const response = await fetch(`${BASE_URL}/api/statistics?hours=24`);
    const data = await response.json();
    console.log(data);
}

getLatestReading();
```

---

## HTML Dashboard Example

```html
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>لوحة تحكم المستشعرات</title>
    <style>
        body { font-family: Arial; background: #f0f0f0; margin: 20px; }
        .card { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; }
        .stat { display: inline-block; width: 23%; margin: 1%; padding: 15px; background: #e3f2fd; border-radius: 8px; }
        .analysis { background: #fff9c4; padding: 15px; border-radius: 8px; }
    </style>
</head>
<body>
    <h1>📊 لوحة تحكم المستشعرات</h1>
    
    <div id="current-status" class="card"></div>
    <div id="stats" class="card"></div>
    <div id="analysis" class="card analysis"></div>

    <script>
        const BASE_URL = 'http://localhost:8000';

        async function updateDashboard() {
            // الحالة الحالية
            const summary = await fetch(`${BASE_URL}/api/summary/current`).then(r => r.json());
            document.getElementById('current-status').innerHTML = `
                <h2>الحالة الحالية</h2>
                <div class="stat">🌡️ ${summary.temperature.value}°C ${summary.temperature.status}</div>
                <div class="stat">💧 ${summary.humidity.value}% ${summary.humidity.status}</div>
                <div class="stat">🌱 ${summary.soil.moisture}% ${summary.soil.status}</div>
                <div class="stat">💡 ${summary.light.intensity}% ${summary.light.status}</div>
            `;

            // الإحصائيات
            const stats = await fetch(`${BASE_URL}/api/statistics?hours=24`).then(r => r.json());
            document.getElementById('stats').innerHTML = `
                <h2>إحصائيات آخر 24 ساعة</h2>
                <p>عدد القراءات: ${stats.total_readings}</p>
                <p>درجة الحرارة: ${stats.temperature.min}°C - ${stats.temperature.max}°C (متوسط: ${stats.temperature.avg.toFixed(1)}°C)</p>
                <p>الرطوبة: ${stats.humidity.min}% - ${stats.humidity.max}% (متوسط: ${stats.humidity.avg.toFixed(1)}%)</p>
            `;

            // التحليل الذكي
            const analysis = await fetch(`${BASE_URL}/api/analyze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: 'تحليل سريع', limit: 10 })
            }).then(r => r.json());
            document.getElementById('analysis').innerHTML = `
                <h2>🤖 تحليل ذكي</h2>
                <p>${analysis.analysis}</p>
            `;
        }

        updateDashboard();
        setInterval(updateDashboard, 60000); // تحديث كل دقيقة
    </script>
</body>
</html>
```

---

## متغيرات البيئة (اختياري)

إنشاء ملف `.env`:
```
GEMINI_API_KEY=AIzaSyAUT6q8rHN-WbqgS8zNu4Gu5FzYHDcCjrQ
ESP32_IP=192.168.1.17
API_PORT=8000
```

---

## ملاحظات مهمة

⚠️ **الأمان:**
- استخدم متغيرات البيئة بدلاً من حفظ المفاتيح في الكود
- أضف مصادقة OAuth2 للإنتاج
- استخدم HTTPS في الإنتاج

💡 **التطوير:**
- الخادم يعمل على جميع الواجهات (0.0.0.0:8000)
- استخدم Gunicorn في الإنتاج: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app`
- أضف قاعدة بيانات PostgreSQL بدلاً من SQLite للإنتاج

---

## استكشاف الأخطاء

### الخادم لا يعمل
```bash
python api.py
# يجب أن ترى:
# INFO:     Application startup complete [uvicorn]
```

### خطأ في Gemini API
- تأكد من أن المفتاح صحيح
- تحقق من الاتصال بالإنترنت

### خطأ في قاعدة البيانات
- احذف `sensor_data.db` لإنشاء قاعدة جديدة
- تأكد من صلاحيات الكتابة في المجلد
