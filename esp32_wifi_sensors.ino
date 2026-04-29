#include <WiFi.h>
#include <WebServer.h>
#include <DHT.h>
#include <ArduinoJson.h>

// ─── WiFi ───────────────────────────────────────────────
const char* WIFI_SSID = "YOUR_SSID";
const char* WIFI_PASS = "YOUR_PASSWORD";

// ─── DHT11 ──────────────────────────────────────────────
#define DHTPIN    4
#define DHTTYPE   DHT11
DHT dht(DHTPIN, DHTTYPE);

// ─── Soil Moisture ──────────────────────────────────────
#define SOIL_PIN  34
#define SOIL_DRY  3200
#define SOIL_WET  1200

// ─── Gas Sensor ─────────────────────────────────────────
#define GAS_PIN       35
#define GAS_THRESHOLD 1500

// ─── LDR ────────────────────────────────────────────────
#define LDR_PIN   32

// ─── Web Server on port 80 ──────────────────────────────
WebServer server(80);

// ─── Sensor data (updated every 2 s) ───────────────────
float temperature, humidity;
int   soilPct, soilRaw, gasRaw, ldrPct, ldrRaw;
bool  gasAlert;
unsigned long lastRead = 0;

int soilPercent(int raw) {
  return constrain(map(raw, SOIL_DRY, SOIL_WET, 0, 100), 0, 100);
}
int lightPercent(int raw) {
  return constrain(map(raw, 0, 4095, 100, 0), 0, 100);
}

void readSensors() {
  humidity    = dht.readHumidity();
  temperature = dht.readTemperature();
  soilRaw     = analogRead(SOIL_PIN);
  soilPct     = soilPercent(soilRaw);
  gasRaw      = analogRead(GAS_PIN);
  gasAlert    = gasRaw > GAS_THRESHOLD;
  ldrRaw      = analogRead(LDR_PIN);
  ldrPct      = lightPercent(ldrRaw);
}

// ─── /data  →  JSON response ────────────────────────────
void handleData() {
  // CORS header so browser dashboards can fetch freely
  server.sendHeader("Access-Control-Allow-Origin", "*");

  if (isnan(humidity) || isnan(temperature)) {
    server.send(503, "application/json", "{\"error\":\"DHT read failed\"}");
    return;
  }

  StaticJsonDocument<256> doc;
  doc["temp"]      = temperature;
  doc["humidity"]  = humidity;
  doc["soil_pct"]  = soilPct;
  doc["soil_raw"]  = soilRaw;
  doc["gas_raw"]   = gasRaw;
  doc["gas_alert"] = gasAlert;
  doc["light_pct"] = ldrPct;
  doc["light_raw"] = ldrRaw;

  String json;
  serializeJson(doc, json);
  server.send(200, "application/json", json);
}

// ─── /  →  tiny status page ─────────────────────────────
void handleRoot() {
  String html = "<h2>ESP32 Sensor Server</h2>"
                "<p>IP: " + WiFi.localIP().toString() + "</p>"
                "<p><a href='/data'>/data</a> — JSON endpoint</p>";
  server.send(200, "text/html", html);
}

void setup() {
  Serial.begin(115200);
  dht.begin();

  // Connect to WiFi
  Serial.print("Connecting to WiFi");
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected! IP: " + WiFi.localIP().toString());

  // Register routes
  server.on("/",     handleRoot);
  server.on("/data", handleData);
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();

  // Read sensors every 2 seconds (non-blocking)
  if (millis() - lastRead >= 2000) {
    lastRead = millis();
    readSensors();
    Serial.println("T:" + String(temperature,1) +
                   " H:" + String(humidity,1) +
                   " S:" + String(soilPct) +
                   " G:" + String(gasRaw) +
                   " L:" + String(ldrPct));
  }
}
