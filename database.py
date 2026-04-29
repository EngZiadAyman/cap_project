from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# ─── إعدادات قاعدة البيانات ───
DATABASE_URL = "sqlite:///sensor_data.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class SensorReading(Base):
    """نموذج لحفظ قراءات المستشعرات"""
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # DHT (درجة الحرارة والرطوبة)
    temp = Column(Float)
    humidity = Column(Float)
    
    # Gas (الغاز)
    gas_raw = Column(Integer)
    gas_alert = Column(Boolean, default=False)
    
    # Light (الضوء)
    light_pct = Column(Integer)
    light_raw = Column(Integer)
    
    # Soil (التربة)
    soil_pct = Column(Integer)
    soil_raw = Column(Integer)

    def __repr__(self):
        return (
            f"<SensorReading(timestamp={self.timestamp}, "
            f"temp={self.temp}°C, humidity={self.humidity}%, "
            f"gas={self.gas_raw}, light={self.light_pct}%, soil={self.soil_pct}%)>"
        )


# ─── إنشاء الجداول ───
Base.metadata.create_all(bind=engine)


# ─── دوال مساعدة ───
def save_sensor_reading(data: dict):
    """حفظ قراءة مستشعر جديدة في قاعدة البيانات"""
    db = SessionLocal()
    try:
        reading = SensorReading(
            temp=data.get("temp"),
            humidity=data.get("humidity"),
            gas_raw=data.get("gas_raw"),
            gas_alert=data.get("gas_alert", False),
            light_pct=data.get("light_pct"),
            light_raw=data.get("light_raw"),
            soil_pct=data.get("soil_pct"),
            soil_raw=data.get("soil_raw"),
        )
        db.add(reading)
        db.commit()
        db.refresh(reading)
        return reading
    finally:
        db.close()


def get_latest_readings(limit: int = 10):
    """الحصول على آخر قراءات"""
    db = SessionLocal()
    try:
        return db.query(SensorReading).order_by(SensorReading.timestamp.desc()).limit(limit).all()
    finally:
        db.close()


def get_readings_by_date_range(start_time: datetime, end_time: datetime):
    """الحصول على قراءات بين تاريخين"""
    db = SessionLocal()
    try:
        return (
            db.query(SensorReading)
            .filter(SensorReading.timestamp >= start_time)
            .filter(SensorReading.timestamp <= end_time)
            .order_by(SensorReading.timestamp)
            .all()
        )
    finally:
        db.close()
