/*
   D0 = GPIO16;
  D1 = GPIO5;
  D2 = GPIO4;
  D3 = GPIO0;
  D4 = GPIO2;
  D5 = GPIO14;
  D6 = GPIO12;
  D7 = GPIO13;
  D8 = GPIO15;
  D9 = GPIO3;
  D10 = GPIO1;
  LED_BUILTIN = GPIO16 (auxiliary constant for the board LED, not a board pin);*/


#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>



SoftwareSerial ss(2, 3); // RX 4, TX
const char *ssid = "red wifi";
const char *password = "password";


//String url = "http://jkuuijyjuig.sa.ngrok.io";
String url = "http://192.168.1.16:5000/";

HTTPClient http;
WiFiClient client;



void setup ()
{
  Serial.begin(9600);
  ss.begin(9600);
  WiFi.mode(WIFI_OFF);
  delay(1000);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println();
  Serial.println();
  Serial.println();
  Serial.print("Conectando");

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println("Conectado con éxito con mi IP: ");
  Serial.println(WiFi.localIP());




}
void loop()
{

  if (ss.available())
  {
    //Serial.println("hola");
    String mensa = ss.readString();
    Serial.println(mensa);
    envio(mensa);
  }




}
void envio (String mensaje)
{

  if (http.begin(client, url + mensaje)) //Iniciar conexión
  {
    //Serial.print("[HTTP] GET...\n");
    int httpCode = http.GET();  // Realizar petición

    if (httpCode > 0) {

      if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
        String payload = http.getString();   // Obtener respuesta
        Serial.println(payload);   // Mostrar respuesta por serial
      }

    }
    else {
      Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }

    http.end();
  }
  else {
    Serial.printf("[HTTP} Unable to connect\n");
  }

  delay(3000);



}
