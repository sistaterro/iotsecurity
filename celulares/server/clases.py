
class Usuario():
    name = ""
    latitude = ""
    longitude = ""

    def transformacion(self, pos, norte,):
        copia = pos

        res = ""
        numero_grado = copia[0:copia.find(".")-2]
        numero_minuto = ""
        numero_minuto = copia[len(str(numero_grado)):]

        res =  str(numero_grado) + str("° ") + numero_minuto + "\" " + norte

        return res
        


    def insert(self, name, position, ):
        self.name = name
        posstring= position
        
        
        
        if position.find("/$GPGLL"):
            latitud = "" #estas son las postas
            longitud = "" #estas son las postas
            comienzo = len("/$GPGLL")
            latitudetext = ""
            longitudetext = ""
            posstring = posstring[comienzo:]

            numero = posstring.find(",")
            latitud = posstring[0:numero]
            posstring = posstring[posstring.find(",")+1:]
            letra_latitud = posstring[0:1]

            posstring = posstring[2:]
            numero = posstring.find(",")
            longitud = posstring[0:numero]
            posstring = posstring[posstring.find(",")+1:]
            letra_longitud = posstring[0:1]

            latitudetext = self.transformacion(latitud, letra_latitud)
            longitudetext = self.transformacion(longitud, letra_longitud)

            latitudetext = self.quitaCeros(latitudetext)
            longitudetext = self.quitaCeros(longitudetext)
            
            self.latitude = latitudetext
            self.longitude = longitudetext

    
    def quitaCeros(self, texto):
        
        while(texto[0]=="0"):
            texto = texto[1:]

        return texto