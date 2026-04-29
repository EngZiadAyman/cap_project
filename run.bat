@echo off
REM برنامج بدء تشغيل نظام مراقبة المستشعرات
REM Startup script for Sensor Monitoring System

echo.
echo ╔════════════════════════════════════════╗
echo ║  🌱 نظام مراقبة المستشعرات            ║
echo ║    Sensor Monitoring System            ║
echo ╚════════════════════════════════════════╝
echo.

REM فحص تثبيت Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت
    echo Python is not installed
    pause
    exit /b 1
)

echo ✓ Python مثبت
echo.

REM فحص وتثبيت المتطلبات
echo 📦 جاري فحص المتطلبات...
echo Checking requirements...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ حدث خطأ في تثبيت المتطلبات
    echo Error installing requirements
    pause
    exit /b 1
)

echo.
echo ✓ تم تثبيت جميع المتطلبات بنجاح
echo ✓ All requirements installed successfully
echo.

REM عرض القائمة
echo ╔════════════════════════════════════════╗
echo ║  اختر ما تريد تشغيله:                  ║
echo ║  Choose what to run:                   ║
echo ╚════════════════════════════════════════╝
echo.
echo 1️⃣  تشغيل خادم FastAPI      (Run FastAPI Server)
echo 2️⃣  قراءة بيانات ESP32       (Read ESP32 Data)
echo 3️⃣  عرض البيانات المحفوظة   (View Saved Data)
echo 4️⃣  عميل API التفاعلي      (Interactive API Client)
echo 5️⃣  خروج                    (Exit)
echo.

set /p choice="اختر (1-5) Choose (1-5): "

if "%choice%"=="1" (
    echo.
    echo 🚀 تشغيل خادم FastAPI...
    echo 🚀 Starting FastAPI Server...
    echo.
    echo الخادم متاح على: http://localhost:8000
    echo Server available at: http://localhost:8000
    echo Swagger Docs: http://localhost:8000/docs
    echo ReDoc Docs: http://localhost:8000/redoc
    echo.
    python api.py
) else if "%choice%"=="2" (
    echo.
    echo 📡 قراءة بيانات ESP32...
    echo 📡 Reading ESP32 Data...
    echo.
    python esp32_client.py
) else if "%choice%"=="3" (
    echo.
    echo 📊 عرض البيانات المحفوظة...
    echo 📊 Viewing Saved Data...
    echo.
    python view_data.py
) else if "%choice%"=="4" (
    echo.
    echo 🖥️  عميل API التفاعلي...
    echo 🖥️  Interactive API Client...
    echo.
    echo تأكد من تشغيل خادم FastAPI أولاً!
    echo Make sure FastAPI Server is running first!
    echo.
    python api_client.py
) else if "%choice%"=="5" (
    echo.
    echo 👋 وداعاً! Goodbye!
    exit /b 0
) else (
    echo.
    echo ❌ اختيار غير صحيح Invalid choice
    pause
    exit /b 1
)

pause
