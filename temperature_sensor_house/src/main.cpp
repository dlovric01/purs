#include <Arduino.h>
#include <Adafruit_BMP280.h>

#include <WiFi.h>
#include <WiFiClient.h>
#include <WiFiUdp.h>

const char *ssid = "Metalmania1";
const char *password = "ik090669";

const char *host = "192.168.0.104";
const int httpPort = 80;

Adafruit_BMP280 bmp; // I2C
WiFiClient client;

void setup()
{
  Serial.begin(9600);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  Serial.println(F("BMP280 Forced Mode Test."));

  // if (!bmp.begin(BMP280_ADDRESS_ALT, BMP280_CHIPID)) {
  if (!bmp.begin(0x76))
  {
    Serial.println(F("Could not find a valid BMP280 sensor, check wiring or "
                     "try a different address!"));
    while (1)
      delay(10);
  }

  /* Default settings from datasheet. */
  bmp.setSampling(Adafruit_BMP280::MODE_FORCED,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
}

void storeCurrentTemp(float temp)
{
  String url = "/temp_sensor_one?value=" + String(temp);
  if (!client.connect(host, httpPort))
  {
    Serial.println("Connection failed");
    return;
  }
  client.print(String("POST ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n");
  client.stop();
}

void loop()
{
  // must call this to wake sensor up and get new measurement data
  // it blocks until measurement is complete
  if (bmp.takeForcedMeasurement())
  {
    float temp = bmp.readTemperature();

    storeCurrentTemp(temp);
  }
  else
  {
    Serial.println("Forced measurement failed!");
  }
  delay(5000);
}