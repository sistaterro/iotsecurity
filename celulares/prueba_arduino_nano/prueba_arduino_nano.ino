#include <SoftwareSerial.h>
SoftwareSerial ss(2,3);// RX, TX 3
String mensaje = "#######";



void setup() {
  ss.begin(9600);
}

void loop() {
  mensaje = "$GPRMC,105601.00,A,3435.46496,S,05825.13509,W,0.127,,111219,,,A*7F";
  ss.println(mensaje);
  mensaje = "$GPVTG,,T,,M,0.127,N,0.235,K,A*23";
  ss.println(mensaje);
  mensaje = "$GPGGA,105601.00,3435.46496,S,05825.13509,W,1,05,2.87,-2.1,M,13.6,M,,*7E";
  ss.println(mensaje);
  mensaje = "$GPGSA,A,2,19,17,13,15,28,,,,,,,,3.03,2.87,1.00*0D";
  ss.println(mensaje);
  mensaje = "$GPGSV,3,1,11,01,01,139,,06,06,041,,12,24,286,,13,63,349,35*73";
  ss.println(mensaje);
  mensaje = "$GPGSV,3,2,11,15,55,270,34,17,58,099,32,19,61,057,27,20,00,240,*78";
  ss.println(mensaje);
  mensaje = "$GPGSV,3,3,11,24,28,231,,28,31,132,23,30,18,075,*44";
  ss.println(mensaje);
  mensaje = "$GPGLL,3435.46496,S,05825.13509,W,105601.00,A,A*69";
  ss.println(mensaje);
  delay(1000);

}                                                           
