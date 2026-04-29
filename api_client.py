"""
🌱 Python Client for Sensor Monitoring API
عميل Python لنظام مراقبة المستشعرات
"""

import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json


class SensorAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    # ─── فحص الخادم ───
    def health_check(self) -> dict:
        """فحص صحة الخادم"""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    # ─── قراءات المستشعرات ───
    def get_latest_reading(self) -> dict:
        """الحصول على آخر قراءة"""
        response = self.session.get(f"{self.base_url}/api/readings/latest")
        response.raise_for_status()
        return response.json()
    
    def get_readings(self, limit: int = 20) -> List[dict]:
        """الحصول على عدة قراءات"""
        response = self.session.get(f"{self.base_url}/api/readings", params={"limit": limit})
        response.raise_for_status()
        return response.json()
    
    def get_today_readings(self) -> List[dict]:
        """الحصول على قراءات اليوم"""
        response = self.session.get(f"{self.base_url}/api/readings/today")
        response.raise_for_status()
        return response.json()
    
    def get_readings_by_date_range(self, start: datetime, end: datetime) -> List[dict]:
        """الحصول على قراءات في نطاق زمني"""
        params = {
            "start": start.strftime("%Y-%m-%d %H:%M:%S"),
            "end": end.strftime("%Y-%m-%d %H:%M:%S")
        }
        response = self.session.get(f"{self.base_url}/api/readings/range", params=params)
        response.raise_for_status()
        return response.json()
    
    # ─── الملخص والإحصائيات ───
    def get_current_summary(self) -> dict:
        """الحصول على ملخص الحالة الحالية"""
        response = self.session.get(f"{self.base_url}/api/summary/current")
        response.raise_for_status()
        return response.json()
    
    def get_statistics(self, hours: int = 24) -> dict:
        """الحصول على الإحصائيات"""
        response = self.session.get(f"{self.base_url}/api/statistics", params={"hours": hours})
        response.raise_for_status()
        return response.json()
    
    # ─── التحليل الذكي ───
    def analyze_data(self, query: str = "تحليل حالة المستشعرات الحالية", limit: int = 10) -> dict:
        """تحليل البيانات باستخدام Gemini AI"""
        payload = {"query": query, "limit": limit}
        response = self.session.post(f"{self.base_url}/api/analyze", json=payload)
        response.raise_for_status()
        return response.json()
    
    # ─── التحكم ───
    def control_relay(self, action: str = "on") -> dict:
        """التحكم بـ Relay (on/off)"""
        if action not in ["on", "off"]:
            raise ValueError("Action must be 'on' or 'off'")
        response = self.session.post(f"{self.base_url}/api/control/relay", params={"action": action})
        response.raise_for_status()
        return response.json()
    
    # ─── إضافة القراءات ───
    def add_reading(self, temp: float, humidity: float, gas_raw: int, gas_alert: bool,
                   light_pct: int, light_raw: int, soil_pct: int, soil_raw: int) -> dict:
        """إضافة قراءة جديدة يدويًا"""
        payload = {
            "temp": temp,
            "humidity": humidity,
            "gas_raw": gas_raw,
            "gas_alert": gas_alert,
            "light_pct": light_pct,
            "light_raw": light_raw,
            "soil_pct": soil_pct,
            "soil_raw": soil_raw
        }
        response = self.session.post(f"{self.base_url}/api/readings/add", json=payload)
        response.raise_for_status()
        return response.json()


# ─── وظائف مساعدة للعرض ───
def print_reading(reading: dict):
    """طباعة قراءة بصيغة منسقة"""
    print(f"""
    ⏰ الوقت: {reading['timestamp']}
    🌡️  درجة الحرارة: {reading['temp']}°C
    💧 الرطوبة: {reading['humidity']}%
    🌱 رطوبة التربة: {reading['soil_pct']}% (خام: {reading['soil_raw']})
    💡 الضوء: {reading['light_pct']}% (خام: {reading['light_raw']})
    💨 الغاز: {reading['gas_raw']} {'🚨' if reading['gas_alert'] else '✅'}
    """)


def print_summary(summary: dict):
    """طباعة الملخص بصيغة منسقة"""
    print(f"""
    ╔════════════════════════════════════════╗
    ║       📊 ملخص الحالة الحالية          ║
    ╚════════════════════════════════════════╝
    
    🌡️  درجة الحرارة: {summary['temperature']['value']}°C {summary['temperature']['status']}
    💧 الرطوبة: {summary['humidity']['value']}% {summary['humidity']['status']}
    🌱 التربة: {summary['soil']['moisture']}% {summary['soil']['status']}
    💡 الضوء: {summary['light']['intensity']}% {summary['light']['status']}
    💨 الغاز: {summary['gas']['status']}
    ⏰ الوقت: {summary['timestamp']}
    """)


def print_statistics(stats: dict):
    """طباعة الإحصائيات بصيغة منسقة"""
    print(f"""
    ╔════════════════════════════════════════╗
    ║      📈 الإحصائيات ({stats['period_hours']} ساعة)      ║
    ╚════════════════════════════════════════╝
    
    عدد القراءات: {stats['total_readings']}
    
    🌡️  درجة الحرارة:
        • الحد الأدنى: {stats['temperature']['min']}°C
        • الحد الأقصى: {stats['temperature']['max']}°C
        • المتوسط: {stats['temperature']['avg']:.1f}°C
    
    💧 الرطوبة:
        • الحد الأدنى: {stats['humidity']['min']}%
        • الحد الأقصى: {stats['humidity']['max']}%
        • المتوسط: {stats['humidity']['avg']:.1f}%
    
    🌱 رطوبة التربة:
        • الحد الأدنى: {stats['soil_moisture']['min']}%
        • الحد الأقصى: {stats['soil_moisture']['max']}%
        • المتوسط: {stats['soil_moisture']['avg']:.1f}%
    
    💡 الضوء:
        • الحد الأدنى: {stats['light_intensity']['min']}%
        • الحد الأقصى: {stats['light_intensity']['max']}%
        • المتوسط: {stats['light_intensity']['avg']:.1f}%
    
    💨 الغاز:
        • الحد الأدنى: {stats['gas']['min']}
        • الحد الأقصى: {stats['gas']['max']}
        • المتوسط: {stats['gas']['avg']:.1f}
    """)


# ─── البرنامج الرئيسي ───
def main():
    """برنامج تفاعلي"""
    client = SensorAPIClient()
    
    print("🌱 عميل نظام مراقبة المستشعرات")
    print("=" * 50)
    
    try:
        # فحص الخادم
        print("✓ فحص الخادم...")
        health = client.health_check()
        print(f"✓ الخادم: {health['status']}")
        
    except requests.exceptions.ConnectionError:
        print("❌ لا يمكن الاتصال بالخادم. تأكد من تشغيل API")
        print("تشغيل الخادم: python api.py")
        return
    
    # القائمة الرئيسية
    while True:
        print("\n" + "=" * 50)
        print("1️⃣  عرض آخر قراءة")
        print("2️⃣  عرض آخر 20 قراءة")
        print("3️⃣  عرض قراءات اليوم")
        print("4️⃣  عرض ملخص الحالة الحالية")
        print("5️⃣  عرض إحصائيات آخر 24 ساعة")
        print("6️⃣  تحليل ذكي بـ Gemini")
        print("7️⃣  إضافة قراءة يدويًا")
        print("8️⃣  التحكم بـ Relay")
        print("9️⃣  خروج")
        print("=" * 50)
        
        choice = input("اختر رقم الخيار: ").strip()
        
        try:
            if choice == "1":
                print("\n📖 آخر قراءة:")
                reading = client.get_latest_reading()
                print_reading(reading)
                
            elif choice == "2":
                limit = input("عدد القراءات (افتراضي 20): ").strip()
                limit = int(limit) if limit else 20
                print(f"\n📖 آخر {limit} قراءة:")
                readings = client.get_readings(limit)
                for reading in readings[:10]:  # عرض أول 10 فقط
                    print_reading(reading)
                if len(readings) > 10:
                    print(f"... و {len(readings) - 10} قراءات أخرى")
                
            elif choice == "3":
                print("\n📖 قراءات اليوم:")
                readings = client.get_today_readings()
                print(f"عدد القراءات: {len(readings)}")
                if readings:
                    print_reading(readings[-1])
                
            elif choice == "4":
                print("\n📊 ملخص الحالة الحالية:")
                summary = client.get_current_summary()
                print_summary(summary)
                
            elif choice == "5":
                hours = input("عدد الساعات (افتراضي 24): ").strip()
                hours = int(hours) if hours else 24
                print(f"\n📈 الإحصائيات:")
                stats = client.get_statistics(hours)
                print_statistics(stats)
                
            elif choice == "6":
                query = input("أدخل السؤال (اتركه فارغاً للسؤال الافتراضي): ").strip()
                query = query if query else "تحليل حالة المستشعرات الحالية وإعطاء توصيات"
                limit = input("عدد القراءات (افتراضي 10): ").strip()
                limit = int(limit) if limit else 10
                
                print("\n🤖 جاري التحليل...")
                analysis = client.analyze_data(query, limit)
                print(f"\n✓ التحليل:")
                print(analysis['analysis'])
                print(f"\nعدد القراءات المستخدمة: {analysis['readings_count']}")
                
            elif choice == "7":
                print("\nإدخال بيانات القراءة الجديدة:")
                temp = float(input("درجة الحرارة (°C): "))
                humidity = float(input("الرطوبة (%): "))
                gas_raw = int(input("قيمة الغاز الخام: "))
                gas_alert = input("تنبيه الغاز (yes/no): ").lower() == "yes"
                light_pct = int(input("كثافة الضوء (%): "))
                light_raw = int(input("قيمة الضوء الخام: "))
                soil_pct = int(input("رطوبة التربة (%): "))
                soil_raw = int(input("قيمة التربة الخام: "))
                
                reading = client.add_reading(temp, humidity, gas_raw, gas_alert,
                                            light_pct, light_raw, soil_pct, soil_raw)
                print("\n✓ تم إضافة القراءة بنجاح")
                print_reading(reading)
                
            elif choice == "8":
                action = input("الإجراء (on/off): ").strip().lower()
                if action in ["on", "off"]:
                    result = client.control_relay(action)
                    print(f"\n✓ {result['message']}")
                else:
                    print("❌ إجراء غير صحيح")
                
            elif choice == "9":
                print("🔚 وداعاً!")
                break
                
            else:
                print("❌ اختيار غير صحيح")
                
        except Exception as e:
            print(f"❌ حدث خطأ: {str(e)}")


if __name__ == "__main__":
    main()
