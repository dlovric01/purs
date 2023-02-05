#include <Arduino.h>
#include <Adafruit_BMP280.h>

#include <WiFi.h>
#include <WiFiClient.h>
#include <WiFiUdp.h>

const char *ssid = "BRANKO";
const char *password = "zagreb300";

const char *host = "192.168.1.3";
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

float getTargetedTemperature()
{
  String url = "/targeted_temperature";
  if (!client.connect(host, httpPort))
  {
    Serial.println("Connection failed");
    return 0;
  }

  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n");

  String line = client.readString();
  float value = line.substring(line.indexOf("\r\n\r\n")).toFloat();
  Serial.print(value);
  Serial.println();
  // Serial.println("Closing connection");
  client.stop();
  return value;
  delay(2500);
}

void storeCurrentTemp(float temp)
{
  String url = "/send-temp1?value=" + String(temp);
  if (!client.connect(host, httpPort))
  {
    Serial.println("Connection failed");
    return;
  }
  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n");
  client.stop();
  delay(2500);
}

void loop()
{
  // must call this to wake sensor up and get new measurement data
  // it blocks until measurement is complete
  if (bmp.takeForcedMeasurement())
  {
    // can now print out the new measurements
    float temp = bmp.readTemperature();
    // Serial.print(F("Temperature = "));
    // Serial.print(temp);
    // Serial.println(" *C");
    // Serial.println();

    storeCurrentTemp(temp);
    float targetedTemp = getTargetedTemperature();
    if (targetedTemp != 0)
    {
      if (targetedTemp > temp)
      {
        Serial.print("FAN: OFF");
        Serial.println();
        Serial.print("RADIATOR: ON");
        Serial.println();
      }
      else if (targetedTemp < temp)
      {
        Serial.print("FAN: OFF");
        Serial.println();
        Serial.print("RADIATOR: ON");
        Serial.println();
      }
      else if (targetedTemp == temp)
      {
        Serial.print("FAN: OFF");
        Serial.println();
        Serial.print("RADIATOR: OFF");
        Serial.println();
      }
    }
  }
  else
  {
    Serial.println("Forced measurement failed!");
  }
}