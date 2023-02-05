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

void sendRequest(String path)
{
  String url = path;

  if (!client.connect(host, httpPort))
  {
    Serial.println("Connection failed");
    return;
  }

  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n");

  String line = client.readStringUntil('\n');
  Serial.println(line);

  Serial.println();
  Serial.print(client.readString());

  Serial.println();
  Serial.println("Closing connection");
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
    Serial.print(F("Temperature = "));
    Serial.print(temp);
    Serial.println(" *C");
    Serial.println();

    sendRequest("/send-temp1?value=" + String(temp));
    sendRequest("targeted_temperature");
  }
  else
  {
    Serial.println("Forced measurement failed!");
  }
}