#include <Arduino.h>

#include <WiFi.h>
#include <WiFiClient.h>
#include <WiFiUdp.h>

const char *ssid = "BRANKO_EXT";
const char *password = "zagreb300";

const char *host = "192.168.1.100";
const int httpPort = 80;

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

  pinMode(2, OUTPUT);
  pinMode(4, OUTPUT);
}

void blinkNoConnection()
{
  digitalWrite(2, HIGH);
  digitalWrite(4, HIGH);
  delay(100);
  digitalWrite(2, LOW);
  digitalWrite(4, LOW);
  delay(100);
  digitalWrite(2, HIGH);
  digitalWrite(4, HIGH);
  delay(100);
  digitalWrite(2, LOW);
  digitalWrite(4, LOW);
  delay(2000);
}

void blinkNoWifi()
{
  {
    digitalWrite(2, HIGH);
    digitalWrite(4, HIGH);
    delay(500);
    digitalWrite(2, LOW);
    digitalWrite(4, LOW);
    delay(500);
    digitalWrite(2, HIGH);
    digitalWrite(4, HIGH);
    delay(500);
    digitalWrite(2, LOW);
    digitalWrite(4, LOW);
    delay(5000);
  }
}

float getTargetedTemp()
{
  String url = "/targeted_temperature";
  if (!client.connect(host, httpPort))
  {
    Serial.println("Connection failed");
    blinkNoConnection();
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
}

float getCurrentTemp()
{
  String url = "/temp_sensor_one";
  if (!client.connect(host, httpPort))
  {
    Serial.println("Connection failed");
    return -1;
  }

  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n");

  String line = client.readString();
  String bla = (line.substring(line.indexOf("\r\n\r\n")));
  bla.trim();
  float value;
  if (bla == "Sensor not connected")
  {
    value = -1;
  }
  else
  {
    value = line.substring(line.indexOf("\r\n\r\n")).toFloat();
  }
  Serial.print(value);
  Serial.println();
  // Serial.println("Closing connection");
  client.stop();
  return value;
}

void updateDeviceStatus(String fan, String radiator)
{
  String url = "/devices?fan=" + String(fan) + "&radiator=" + String(radiator);
  if (!client.connect(host, httpPort))
  {
    Serial.println("Connection failed");
    delay(10000);
    return;
  }

  client.print(String("POST ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n");
  client.stop();
}

void loop()
{
  if (WiFi.status() == WL_CONNECTED)
  {

    float targetedTemp = getTargetedTemp();
    float currentTemp = getCurrentTemp();

    if (targetedTemp != 0 && currentTemp != -1 && currentTemp != 0.00)
    {

      if (targetedTemp > currentTemp)
      {
        Serial.print("FAN: OFF");
        Serial.println();
        Serial.print("RADIATOR: ON");
        Serial.println();
        digitalWrite(2, LOW);
        digitalWrite(4, HIGH);
        updateDeviceStatus("OFF", "ON");
      }
      else if (targetedTemp < currentTemp)
      {
        Serial.print("FAN: ON");
        Serial.println();
        Serial.print("RADIATOR: OFF");
        Serial.println();
        digitalWrite(2, HIGH);
        digitalWrite(4, LOW);
        updateDeviceStatus("ON", "OFF");
      }
      else if (targetedTemp == currentTemp)
      {
        Serial.print("FAN: OFF");
        Serial.println();
        Serial.print("RADIATOR: OFF");
        Serial.println();
        digitalWrite(2, LOW);
        digitalWrite(4, LOW);
        updateDeviceStatus("OFF", "OFF");
      }
    }
    delay(1000);
  }
  else
  {
    blinkNoWifi();
  }
}