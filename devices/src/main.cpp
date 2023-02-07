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

float getTemperatures()
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

void updateDeviceStatus(String fan, String radiator)
{
  String url = "/devices?fan=" + String(fan) + "&radiator=" + String(radiator);
  if (!client.connect(host, httpPort))
  {
    Serial.println("Connection failed");
    return;
  }
  client.print(String("POST ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n");
  client.stop();
  delay(1000);
}

void loop()
{

  float targetedTemp = getTemperatures();
  if (targetedTemp != 0)
  {
    if (targetedTemp > 25)
    {
      Serial.print("FAN: OFF");
      Serial.println();
      Serial.print("RADIATOR: ON");
      Serial.println();
      digitalWrite(2, LOW);
      digitalWrite(4, HIGH);
      updateDeviceStatus("OFF", "ON");
    }
    else if (targetedTemp < 25)
    {
      Serial.print("FAN: ON");
      Serial.println();
      Serial.print("RADIATOR: OFF");
      Serial.println();
      digitalWrite(2, HIGH);
      digitalWrite(4, LOW);
      updateDeviceStatus("ON", "OFF");
    }
    else if (targetedTemp == 25)
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
}