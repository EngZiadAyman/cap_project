import requests
import time
from database import save_sensor_reading

# ─── غيّر هذا للـ IP اللي يطلع في Serial Monitor بعد الاتصال ───
ESP32_IP = "192.168.1.12"
URL      = f"http://{ESP32_IP}/data"
INTERVAL = 2  # ثواني بين كل قراءة
SAVE_INTERVAL = 60  # دقيقة واحدة = 60 ثانية


def soil_status(pct: int) -> str:
    if pct < 20: return "🔴 dry"
    if pct < 50: return "🟡 moderate"
    return "🟢 wet"

def light_status(pct: int) -> str:
    if pct < 20: return "🌑 dark"
    if pct < 60: return "🌤 dim"
    return "☀️ bright"

def main():
    print(f"متصل بـ ESP32 على {URL}\n")
    last_save_time = 0

    while True:
        try:
            resp = requests.get(URL, timeout=5)
            resp.raise_for_status()
            data = resp.json()

            if "error" in data:
                print(f"⚠️  error: {data['error']}")
            else:
                gas_warn = "🚨 GAS DETECTED!" if data["gas_alert"] else "✅ normal"
                print(
                    f"🌡  temp:     {data['temp']:.1f} °C\n"
                    f"💧 humidity: {data['humidity']:.1f} %\n"
                    f"🌱 soil:     {data['soil_pct']} % {soil_status(data['soil_pct'])} (raw: {data['soil_raw']})\n"
                    f"💨 gas:      {data['gas_raw']}  →  {gas_warn}\n"
                    f"💡 light:    {data['light_pct']} % {light_status(data['light_pct'])} (raw: {data['light_raw']})\n"
                    f"{'-'*50}"
                )
                
                # ─── حفظ البيانات كل دقيقة ───
                current_time = time.time()
                if current_time - last_save_time >= SAVE_INTERVAL:
                    try:
                        save_sensor_reading(data)
                        print("💾 تم حفظ القراءة في قاعدة البيانات")
                        last_save_time = current_time
                    except Exception as e:
                        print(f"❌ خطأ في حفظ البيانات: {e}")

        except requests.exceptions.ConnectionError:
            print("❌ لا يمكن الاتصال بـ ESP32. تأكد من أنه متصل بنفس الشبكة وأن IP صحيح.")
        except requests.exceptions.Timeout:
            print("⏱ انتهى وقت الاتصال")
        except Exception as e:
            print(f"خطأ غير متوقع: {e}")

        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
