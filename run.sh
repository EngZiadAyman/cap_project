#!/bin/bash

# برنامج بدء تشغيل نظام مراقبة المستشعرات
# Startup script for Sensor Monitoring System

echo ""
echo "╔════════════════════════════════════════╗"
echo "║  🌱 نظام مراقبة المستشعرات            ║"
echo "║    Sensor Monitoring System            ║"
echo "╚════════════════════════════════════════╝"
echo ""

# فحص تثبيت Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python غير مثبت"
    echo "Python is not installed"
    exit 1
fi

echo "✓ Python مثبت"
echo ""

# فحص وتثبيت المتطلبات
echo "📦 جاري فحص المتطلبات..."
echo "Checking requirements..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ حدث خطأ في تثبيت المتطلبات"
    echo "Error installing requirements"
    exit 1
fi

echo ""
echo "✓ تم تثبيت جميع المتطلبات بنجاح"
echo "✓ All requirements installed successfully"
echo ""

# عرض القائمة
echo "╔════════════════════════════════════════╗"
echo "║  اختر ما تريد تشغيله:                  ║"
echo "║  Choose what to run:                   ║"
echo "╚════════════════════════════════════════╝"
echo ""
echo "1️⃣  تشغيل خادم FastAPI      (Run FastAPI Server)"
echo "2️⃣  قراءة بيانات ESP32       (Read ESP32 Data)"
echo "3️⃣  عرض البيانات المحفوظة   (View Saved Data)"
echo "4️⃣  عميل API التفاعلي      (Interactive API Client)"
echo "5️⃣  خروج                    (Exit)"
echo ""

read -p "اختر (1-5) Choose (1-5): " choice

case $choice in
    1)
        echo ""
        echo "🚀 تشغيل خادم FastAPI..."
        echo "🚀 Starting FastAPI Server..."
        echo ""
        echo "الخادم متاح على: http://localhost:8000"
        echo "Server available at: http://localhost:8000"
        echo "Swagger Docs: http://localhost:8000/docs"
        echo "ReDoc Docs: http://localhost:8000/redoc"
        echo ""
        python3 api.py
        ;;
    2)
        echo ""
        echo "📡 قراءة بيانات ESP32..."
        echo "📡 Reading ESP32 Data..."
        echo ""
        python3 esp32_client.py
        ;;
    3)
        echo ""
        echo "📊 عرض البيانات المحفوظة..."
        echo "📊 Viewing Saved Data..."
        echo ""
        python3 view_data.py
        ;;
    4)
        echo ""
        echo "🖥️  عميل API التفاعلي..."
        echo "🖥️  Interactive API Client..."
        echo ""
        echo "تأكد من تشغيل خادم FastAPI أولاً!"
        echo "Make sure FastAPI Server is running first!"
        echo ""
        python3 api_client.py
        ;;
    5)
        echo ""
        echo "👋 وداعاً! Goodbye!"
        exit 0
        ;;
    *)
        echo ""
        echo "❌ اختيار غير صحيح Invalid choice"
        exit 1
        ;;
esac
