#include <SoftwareSerial.h>
SoftwareSerial servidor(6, 7); //RX, TX;
SoftwareSerial gps(2, 3); // RX, TX //recibo posición el 2
SoftwareSerial bt(10, 11); //RX, TX // viene del bluetooth el 10

//el ingreso de la data del bt viene por el serial tradicional

String pos = "";
String nombre = "";


void setup() {
  servidor.begin(9600); //servidor
  bt.begin(9600); //al esp8266
  Serial.begin(9600);
  gps.begin(9600); // posicion
  
  
  Serial.println("arrancamos");
}

void loop() {

  if (gps.available()) //consigo la posicion
  {
    pos = gps.readString();
    pos = posicion(pos);
    Serial.println("gps listo");
    bt.listen();
  }

  if (bt.available()) //consigo el nombre
  {
    nombre = bt.readString();
    nombre = nombresa(nombre);
    Serial.println("BT listo");
    gps.listen();
  }

  if (pos != "" && nombre != "") //si tengo el nombre y la posicion la mando
  {
    String mensa = pos + "/" + nombre;
    servidor.println(mensa);
    nombre = "";
    pos = "";
  }
  
  
}

String posicion(String palabra)
{
  String linea = "";
  int comienzo = -1, finale = -1;

  comienzo = palabra.indexOf("$GPGLL");
  finale = palabra.indexOf("A,A*");

  if (comienzo != -1 and finale != -1)
  {
    linea = palabra.substring(comienzo, finale);
    return linea;
  }
  else
  {
    return "";
  }
}

String nombresa (String mensa)
{
  int begine = mensa.indexOf("000");
  int finale = mensa.indexOf("111");

  if (begine == 0 and finale == mensa.length() - 3)
  {
    return mensa.substring(3, finale);
  }

  return "";
}
