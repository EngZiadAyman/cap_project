from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests
import google.generativeai as genai
from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, field_serializer

from database import (
    SensorReading, 
    SessionLocal, 
    get_latest_readings, 
    get_readings_by_date_range,
    save_sensor_reading
)

# ─── إعدادات Gemini API ───
GEMINI_API_KEY = "AIzaSyAUT6q8rHN-WbqgS8zNu4Gu5FzYHDcCjrQ"
genai.configure(api_key=GEMINI_API_KEY)

# ─── إنشاء تطبيق FastAPI ───
app = FastAPI(
    title="🌱 نظام مراقبة المستشعرات",
    description="API لعرض والتحكم بمستشعرات ESP32 مع تحليل ذكي من Gemini",
    version="1.0.0"
)

# ─── السماح بـ CORS ───
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── نماذج Pydantic ───
class SensorReadingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    timestamp: datetime
    temp: float
    humidity: float
    gas_raw: int
    gas_alert: bool
    light_pct: int
    light_raw: int
    soil_pct: int
    soil_raw: int
    
    @field_serializer('timestamp')
    def serialize_timestamp(self, value: datetime):
        return value.isoformat()


class AnalysisRequest(BaseModel):
    query: str = "تحليل حالة المستشعرات الحالية وإعطاء توصيات"
    limit: int = 10


class AnalysisResponse(BaseModel):
    analysis: str
    readings_count: int
    timestamp: datetime
    
    @field_serializer('timestamp')
    def serialize_timestamp(self, value: datetime):
        return value.isoformat()


class ControlResponse(BaseModel):
    status: str
    message: str
    timestamp: datetime
    
    @field_serializer('timestamp')
    def serialize_timestamp(self, value: datetime):
        return value.isoformat()


# ─── دوال مساعدة ───
def reading_to_dict(reading: SensorReading) -> dict:
    """تحويل قراءة قاعدة البيانات إلى قاموس"""
    return {
        "id": reading.id,
        "timestamp": reading.timestamp.isoformat(),
        "temp": reading.temp,
        "humidity": reading.humidity,
        "gas_raw": reading.gas_raw,
        "gas_alert": reading.gas_alert,
        "light_pct": reading.light_pct,
        "light_raw": reading.light_raw,
        "soil_pct": reading.soil_pct,
        "soil_raw": reading.soil_raw,
    }


def format_readings_for_gemini(readings: List[SensorReading]) -> str:
    """تنسيق القراءات لإرسالها إلى Gemini"""
    text = "📊 بيانات المستشعرات:\n\n"
    for reading in readings:
        text += f"""
⏰ الوقت: {reading.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
🌡️  درجة الحرارة: {reading.temp}°C
💧 الرطوبة: {reading.humidity}%
🌱 رطوبة التربة: {reading.soil_pct}% (خام: {reading.soil_raw})
💡 الضوء: {reading.light_pct}% (خام: {reading.light_raw})
💨 الغاز: {reading.gas_raw} {'🚨 تنبيه!' if reading.gas_alert else '✅'}
───────────────────────────
"""
    return text


async def call_gemini_api(prompt: str) -> str:
    """استدعاء Gemini API للتحليل الذكي"""
    try:
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في Gemini API: {str(e)}")


# ─── Endpoints ───

@app.get("/health", tags=["System"])
async def health_check():
    """فحص صحة الخادم"""
    return {
        "status": "🟢 سليم",
        "timestamp": datetime.utcnow().isoformat(),
        "api_version": "1.0.0"
    }


@app.get("/api/readings/latest", response_model=SensorReadingResponse, tags=["Readings"])
async def get_latest_single():
    """الحصول على آخر قراءة"""
    db = SessionLocal()
    try:
        reading = db.query(SensorReading).order_by(SensorReading.timestamp.desc()).first()
        if not reading:
            raise HTTPException(status_code=404, detail="لا توجد قراءات محفوظة")
        return reading
    finally:
        db.close()


@app.get("/api/readings", response_model=List[SensorReadingResponse], tags=["Readings"])
async def get_readings(limit: int = Query(20, ge=1, le=1000)):
    """الحصول على آخر قراءات"""
    readings = get_latest_readings(limit)
    if not readings:
        raise HTTPException(status_code=404, detail="لا توجد قراءات محفوظة")
    return readings


@app.get("/api/readings/today", response_model=List[SensorReadingResponse], tags=["Readings"])
async def get_today_readings():
    """الحصول على قراءات اليوم"""
    now = datetime.utcnow()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    readings = get_readings_by_date_range(start_of_day, now)
    
    if not readings:
        raise HTTPException(status_code=404, detail="لا توجد قراءات لهذا اليوم")
    return readings


@app.get("/api/readings/range", response_model=List[SensorReadingResponse], tags=["Readings"])
async def get_readings_range(
    start: str = Query(..., description="تاريخ البداية (YYYY-MM-DD HH:MM:SS)"),
    end: str = Query(..., description="تاريخ النهاية (YYYY-MM-DD HH:MM:SS)")
):
    """الحصول على قراءات في نطاق زمني"""
    try:
        start_time = datetime.fromisoformat(start)
        end_time = datetime.fromisoformat(end)
    except ValueError:
        raise HTTPException(status_code=400, detail="صيغة التاريخ غير صحيحة. استخدم: YYYY-MM-DD HH:MM:SS")
    
    readings = get_readings_by_date_range(start_time, end_time)
    
    if not readings:
        raise HTTPException(status_code=404, detail="لا توجد قراءات في هذا النطاق الزمني")
    return readings


@app.post("/api/analyze", response_model=AnalysisResponse, tags=["Analysis"])
async def analyze_sensor_data(request: AnalysisRequest):
    """تحليل بيانات المستشعرات باستخدام Gemini AI"""
    readings = get_latest_readings(request.limit)
    
    if not readings:
        raise HTTPException(status_code=404, detail="لا توجد بيانات للتحليل")
    
    # تنسيق البيانات للـ Gemini
    readings_text = format_readings_for_gemini(readings)
    prompt = f"{readings_text}\n\n{request.query}\n\nيرجى تقديم تحليل مفصل بالعربية."
    
    # استدعاء Gemini
    analysis = await call_gemini_api(prompt)
    
    return {
        "analysis": analysis,
        "readings_count": len(readings),
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/summary/current", tags=["Summary"])
async def get_current_summary():
    """ملخص الحالة الحالية للمستشعرات"""
    db = SessionLocal()
    try:
        reading = db.query(SensorReading).order_by(SensorReading.timestamp.desc()).first()
        if not reading:
            raise HTTPException(status_code=404, detail="لا توجد بيانات")
        
        return {
            "status": "🟢 نشط",
            "timestamp": reading.timestamp.isoformat(),
            "temperature": {
                "value": reading.temp,
                "unit": "°C",
                "status": "🟢" if 15 <= reading.temp <= 30 else "🟡" if 10 <= reading.temp <= 35 else "🔴"
            },
            "humidity": {
                "value": reading.humidity,
                "unit": "%",
                "status": "🟢" if 40 <= reading.humidity <= 60 else "🟡" if 30 <= reading.humidity <= 80 else "🔴"
            },
            "soil": {
                "moisture": reading.soil_pct,
                "unit": "%",
                "raw": reading.soil_raw,
                "status": "🟢 رطب" if reading.soil_pct > 50 else "🟡 معتدل" if reading.soil_pct > 20 else "🔴 جاف"
            },
            "light": {
                "intensity": reading.light_pct,
                "unit": "%",
                "raw": reading.light_raw,
                "status": "☀️ مشرق" if reading.light_pct > 60 else "🌤 خافت" if reading.light_pct > 20 else "🌑 مظلم"
            },
            "gas": {
                "value": reading.gas_raw,
                "alert": reading.gas_alert,
                "status": "🚨 تنبيه!" if reading.gas_alert else "✅ عادي"
            }
        }
    finally:
        db.close()


@app.get("/api/statistics", tags=["Analytics"])
async def get_statistics(hours: int = Query(24, ge=1, le=720)):
    """إحصائيات المستشعرات في آخر X ساعة"""
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        start_time = now - timedelta(hours=hours)
        
        readings = db.query(SensorReading).filter(
            SensorReading.timestamp >= start_time,
            SensorReading.timestamp <= now
        ).all()
        
        if not readings:
            raise HTTPException(status_code=404, detail="لا توجد بيانات في هذا الوقت")
        
        temps = [r.temp for r in readings if r.temp is not None]
        humidities = [r.humidity for r in readings if r.humidity is not None]
        soils = [r.soil_pct for r in readings if r.soil_pct is not None]
        lights = [r.light_pct for r in readings if r.light_pct is not None]
        gases = [r.gas_raw for r in readings if r.gas_raw is not None]
        
        return {
            "period_hours": hours,
            "total_readings": len(readings),
            "temperature": {
                "min": min(temps) if temps else None,
                "max": max(temps) if temps else None,
                "avg": sum(temps) / len(temps) if temps else None,
            },
            "humidity": {
                "min": min(humidities) if humidities else None,
                "max": max(humidities) if humidities else None,
                "avg": sum(humidities) / len(humidities) if humidities else None,
            },
            "soil_moisture": {
                "min": min(soils) if soils else None,
                "max": max(soils) if soils else None,
                "avg": sum(soils) / len(soils) if soils else None,
            },
            "light_intensity": {
                "min": min(lights) if lights else None,
                "max": max(lights) if lights else None,
                "avg": sum(lights) / len(lights) if lights else None,
            },
            "gas": {
                "min": min(gases) if gases else None,
                "max": max(gases) if gases else None,
                "avg": sum(gases) / len(gases) if gases else None,
            },
        }
    finally:
        db.close()


@app.post("/api/control/relay", response_model=ControlResponse, tags=["Control"])
async def control_relay(action: str = Query("on", pattern="^(on|off)$")):
    """التحكم بـ Relay (تشغيل/إيقاف)"""
    # هذه دالة placeholder للتحكم
    # يمكن توسيعها لاحقاً للتحكم الفعلي بأجهزة ESP32
    return {
        "status": "success",
        "message": f"تم تشغيل Relay: {action.upper()}",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/readings/add", response_model=SensorReadingResponse, tags=["Readings"])
async def add_reading(reading_data: dict):
    """إضافة قراءة جديدة يدويًا"""
    try:
        new_reading = save_sensor_reading(reading_data)
        return new_reading
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"خطأ في حفظ القراءة: {str(e)}")


@app.get("/api/docs-ar", tags=["Documentation"])
async def docs_arabic():
    """توثيق API بالعربية"""
    return {
        "title": "📚 توثيق API",
        "endpoints": {
            "/health": "فحص صحة الخادم",
            "/api/readings/latest": "آخر قراءة",
            "/api/readings": "عدة قراءات (مع limit)",
            "/api/readings/today": "قراءات اليوم",
            "/api/readings/range": "قراءات في نطاق زمني",
            "/api/summary/current": "ملخص الحالة الحالية",
            "/api/statistics": "إحصائيات",
            "/api/analyze": "تحليل ذكي باستخدام Gemini",
            "/api/control/relay": "التحكم بـ Relay",
            "/api/readings/add": "إضافة قراءة جديدة"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
