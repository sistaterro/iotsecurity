from flask import Flask, request, jsonify, send_file, send_from_directory, safe_join, abort


from datetime import datetime
import sqlite3
import json
import traceback
import logging

app = Flask(__name__)
#globales y clases
ERROR_NOT_MATCH = "error_not_match_woker"
ERROR_EXISTING_WORKER = "error_existing_worker"
ERROR_PASSWORD = "error_password"
SUCCESS = "success"
NOT_SUCCESS = "not_success"
WORKER_MAX = 1000
GROUPS_MAX = 1000
class Worker:
    name = ""
    lastname = ""
    id = ""
    latitude = ""
    longitude = ""
    status = 0
    cod = ""
    mensajete = ""
    password = ""

class Job:
    cod = ""
    name = ""
    description = ""
    workercreator = ""
    workerslave = ""
    begin = ""
    end = ""
    estimated = int

class Group:
    cod = 0
    name = ""
    administradores = []
    integrantes = []

class WorkerGroup:
    codWorker = 0
    codGroup = 0
    administrator = False

class Log:
    cod = ""
    id = ""
    codworker = ""
    statusbefore = ""
    statusafter = ""
    latitude = ""
    longitude = ""
    time = datetime
    vitacora = ""


class Maine:
    worker = []
    job = []
    log = []
    group = []
 
    
    def insertarTrabajador(self, trabajador):

        nuevoTrabajador = self.chequearTrabajador(trabajador)

        if (nuevoTrabajador is not None): #si el trabajador está en la memoria ram, cancelo
            return False

        self.agregarWorkerDB(trabajador)

        return True
    
    def actualizarTrabajadorStatus(self, trabajador):
        viejoTrabajador = self.chequearTrabajador(trabajador)


        if viejoTrabajador is not None:
            if (viejoTrabajador.status != trabajador.status):
                conn=sqlite3.connect('data.db')
                c = conn.cursor()
              
                try:
                    if (trabajador.mensajete == ""):
                        c.execute('INSERT into log (codworker, statusbefore, statusafter, time, latitude, longitude) VALUES (?, ?, ?, dateTime(\'now\',\'localtime\'), ?, ?);', (viejoTrabajador.cod , viejoTrabajador.status, trabajador.status, trabajador.latitude, trabajador.longitude, ))
                    else:
                        c.execute('INSERT into log (codworker, statusbefore, statusafter, time, latitude, longitude, vitacora) VALUES (?, ?, ?, dateTime(\'now\',\'localtime\'), ?, ?, ?);', (viejoTrabajador.cod , viejoTrabajador.status, trabajador.status, trabajador.latitude, trabajador.longitude, trabajador.mensajete, ))
                except:
                    logging.error(traceback.format_exc())
                    conn.close()
                    return None
                conn.commit()
                conn.close()
                viejoTrabajador.status = trabajador.status

            viejoTrabajador.latitude = trabajador.latitude
            viejoTrabajador.longitude = trabajador.longitude
            

            i = 0

        else:
            return None

        return viejoTrabajador

    def eliminarTrabajador():
        return ""
    
    def usuariopassword(id, password):
        return False

    #estechequeartrabajador va a ser sustituido con usuario y contraseña
    def chequearTrabajador(self, trabajador):
        
        nuevoTrabajador = self.chequearWorkerRAM(trabajador)
        if (nuevoTrabajador is not None):
            return nuevoTrabajador

        conn=sqlite3.connect('data.db')
        c = conn.cursor()

        pala = ""
        pala = pala + "SELECT worker.id, worker.name, worker.lastname, worker.cod, log.statusafter, log.latitude, log.longitude, worker.password FROM worker "
        pala = pala + "INNER JOIN log ON worker.cod = log.codworker "
        pala = pala + "WHERE worker.id = ? AND log.time = (SELECT MAX(time) FROM log WHERE id = ?);"

        try:
            c.execute(pala,(trabajador.id,trabajador.id,))
            resultado = c.fetchone()
            conn.commit()
        except Exception as e:
            logging.error(traceback.format_exc())
            conn.close()
            return None

        if (resultado is None):#puede ser que no haya resgistros del trabajador, porque no hay nada en el log o el tipo no existe
            try:
                c.execute('SELECT * FROM worker WHERE id = ?;', (trabajador.id,))
                resultado = c.fetchone()
                
                if (resultado is None):
                    conn.commit()
                    conn.close()
                    return None
                nuevoTrabajador = Worker()
                nuevoTrabajador.id = resultado[0]
                nuevoTrabajador.name = resultado[1]
                nuevoTrabajador.lastname = resultado[2]
                nuevoTrabajador.cod = resultado[3]
                nuevoTrabajador.password = resultado[4]
                nuevoTrabajador.status = 0
                nuevoTrabajador.latitude = 0
                nuevoTrabajador.longitude = 0
                nuevoTrabajador.status = 0

                conn.commit()
                conn.close()
                
                
                self.agregaWorkerRAm(nuevoTrabajador)
                return nuevoTrabajador

            except Exception as e:
                logging.error(traceback.format_exc())
                return None
        else:
            nuevoTrabajador = Worker()
            nuevoTrabajador.id = resultado[0]
            nuevoTrabajador.name = resultado[1]
            nuevoTrabajador.lastname = resultado[2]
            nuevoTrabajador.cod = resultado[3]
            nuevoTrabajador.status = resultado[4]
            nuevoTrabajador.latitude = resultado[5]
            nuevoTrabajador.longitude = resultado[6]
            nuevoTrabajador.password = resultado[7]
            conn.close()
            self.agregaWorkerRAm(nuevoTrabajador)
            
            return nuevoTrabajador
            
        return None

    def chequearWorkerRAM(self, trabajador):
        i = len(self.worker) - 1
        while (i >= 0):
            #if (trabajador.id == self.worker[i].id and trabajador.name == self.worker[i].name and trabajador.lastname == self.worker[i].lastname):
            if (trabajador.id == self.worker[i].id):
                return self.worker[i]
            i = i -1
        return None

    def conseguirTrabajador(self, id):
        nuevoTrabajador = Worker()
        nuevoTrabajador.id = id

        return self.chequearTrabajador(nuevoTrabajador)
    
    def insertarTarea(self, tarea = Job()):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        creadorID = ""
        slaveID = ""


        pala = ""
        pala = pala + "SELECT id, cod FROM worker "
        pala = pala + "WHERE id = ? OR id = ? ;"

        try:
            c.execute(pala, (tarea.workercreator, tarea.workerslave))
            resultado = c.fetchall()
        except:
            conn.close()
            logging.error(traceback.format_exc())
            return None
        
        for row in resultado:
            if (row[0] == tarea.workercreator):
                creadorID = str(row[1])
            else:
                slaveID = str(row[1])

        pala = ""
        pala = pala + "INSERT INTO job"
        if (tarea.end == "null"):
            pala = pala + "(name, description, creator, workera, estimated, begin)"
            pala = pala + "VALUES (?, ?, ?, ?, ?, ?);"
        else:
            pala = pala + "(name, description, creator, workera, estimated, begin, ende)"
            pala = pala + "VALUES (?, ?, ?, ?, ?, ?, ?);"

        try:            
            if (tarea.end != "null"):
                c.execute(pala, (tarea.name, tarea.description, creadorID, slaveID,str(tarea.estimated), tarea.begin,tarea.end, ))
            else:
                c.execute(pala, (tarea.name, tarea.description, creadorID, slaveID,str(tarea.estimated), tarea.begin, ))
        except:
            conn.close()
            logging.error(traceback.format_exc())
            return None
        conn.commit()
        conn.close()
        
        return True
    
    def actualizarTarea():
        return ""

    def eliminarTarea():
        return ""
    
    def recibirTareas(self, trabajador = Worker()):
        tarea = Job()
        codWorker = ""
        conn=sqlite3.connect("data.db")
        c = conn.cursor()

        pala = "SELECT cod FROM worker WHERE id = ?;"

        try:
            c.execute(pala, (trabajador.id,))
            resultado = c.fetchone()
        except:
            conn.close()
            logging.error(traceback.format_exc())
            return False
        conn.commit()

        if (resultado is None):
            return False
    
        codWorker = str(resultado[0])

        pala = ""
        pala = pala + "SELECT * FROM job "
        pala = pala + "WHERE creator = ? "
        pala = pala + "OR workera = ?;"

        try:
            c.execute(pala, (codWorker,codWorker,))
            resultado = c.fetchall()
        except:
            conn.close()
            logging.error(traceback.format_exc())
            return False
        conn.commit()

        self.job.clear()

        for row in resultado:
            nuevaTarea = Job()
            nuevaTarea.cod = row[0]
            nuevaTarea.name = row[1]
            nuevaTarea.description = row[2]
            nuevaTarea.workercreator = row[3]
            nuevaTarea.workerslave = row[4]
            nuevaTarea.begin = row[5]
            nuevaTarea.end = row[6]
            nuevaTarea.estimated = row[7]
            self.job.append(nuevaTarea)
        conn.close()        

        return True
    
    def comparaTrabajadores(self, trabajador, nuevoTrabajador):
        if (str(trabajador.id) == str(nuevoTrabajador.id) and str(trabajador.name) == str(nuevoTrabajador.name) and str(trabajador.lastname) == str(nuevoTrabajador.lastname)):
            return True 
        return False
    
    
    def conseguirLog(self, timein, timeout, id):
        conn=sqlite3.connect('data.db')
        c = conn.cursor()
        
        pala = ""
        pala = pala + "select codworker,statusbefore, statusafter, time, latitude, longitude, vitacora from log "
        pala = pala + "where log.codworker in "
        pala = pala + "(select worker.cod from worker "
        pala = pala + "where cod in "
        pala = pala + "(select workergroup.codworker from workergroup "
        pala = pala + "where workergroup.codgroup in (select groupe.cod as grupos from groupe "
        pala = pala + "inner join workergroup on groupe.cod = workergroup.codgroup "
        pala = pala + "inner join worker on worker.cod = workergroup.codworker "
        pala = pala + "where worker.id = ? and administrator = 'True') "
        pala = pala + "group by workergroup.codworker)) "
        pala = pala + "and time between ? and ? "
        pala = pala + "order by time "
        
        try:
            c.execute(pala, (id, timein, timeout,))
            resultado = c.fetchall()
            conn.commit()
        except:
            logging.error(traceback.format_exc())
            conn.close()
            return None
        
        conn.close()

        self.log.clear()

        for row in resultado:
            nuevolog = Log()
            nuevolog.codworker = row[0]
            nuevolog.statusbefore = row[1]
            nuevolog.statusafter = row[2]
            nuevolog.time = row[3]
            nuevolog.latitude = row[4]
            nuevolog.longitude = row[5]
            nuevolog.vitacora= row[6]
            self.log.append(nuevolog)
        return True
    
    def conseguirUltimoLog(self, id):
        logue = Log()
        conn=sqlite3.connect('data.db')
        c = conn.cursor()

        pala = ""
        pala = pala + "SELECT cod FROM worker WHERE id = ?;"


        try:
            c.execute(pala, (id,))
            resultado = c.fetchone()
            conn.commit()
        except:
            logging.error(traceback.format_exc())
            conn.close()
            return None
        
        try:
            c.execute('SELECT * FROM log WHERE time = (SELECT MAX(time) FROM log WHERE codworker = ?);', (resultado[0],))
        except:
            logging.error(traceback.format_exc())
            conn.close()
            return None

        resultado = c.fetchone()

        conn.commit()
        conn.close()

        if (resultado is None):
            return None
        else:
            logue.cod = resultado[0]
            logue.id = resultado[1]
            logue.statusbefore = resultado[2]
            logue.statusafter = resultado[3]
            logue.time = resultado[4]
            logue.latitude = resultado[5]
            logue.longitude = resultado[6]
        return logue

    def agregarWorkerDB (self, trabajador):
        conn=sqlite3.connect('data.db')
        c = conn.cursor()

        try:
            c.execute('INSERT into worker (name, lastname, id) VALUES (?,?,?);', (trabajador.name , trabajador.lastname, trabajador.id))
        except:
            conn.commit()
            conn.close()
            return False

        conn.commit()
        conn.close()

        self.agregaWorkerRAm(trabajador)

        return True

    def agregaWorkerRAm(self, trabajador):
        if (len(self.worker) >= WORKER_MAX):
            del self.worker[0]
            self.worker.append(trabajador)
            
        if (len(self.worker) < WORKER_MAX):
            self.worker.append(trabajador)
        return

    def agregaGrupoRAM(self, grupo = Group()):
        if (len(self.group)>=GROUPS_MAX):
            del self.group[0]
            self.group.append(grupo)
        
        if (len(self.group)<GROUPS_MAX):
            self.group.append(grupo)
        return

    def agregarGrupo(self, trabajador = Worker(), grupo = Group()):
        nuevoTrabajador = self.chequearTrabajador(trabajador)
        if (nuevoTrabajador is None):
            return None

        if (grupo.name == ""):
            return None
        
        nuevoGrupo = self.agregaGrupoDB(nuevoTrabajador, grupo)

        if (nuevoGrupo is not None):
            #self.agregaGrupoRAM(nuevoGrupo)
            return True
        else:
            return False 

    def agregaGrupoDB(self, trabajador = Worker(), grupo = Group()):
        conn=sqlite3.connect('data.db')
        c = conn.cursor()

        try:
            c.execute('INSERT INTO groupe (name) VALUES (?);', (grupo.name,))
            c.execute('SELECT cod FROM groupe WHERE creation = (SELECT MAX(creation) FROM groupe);')
            resultado = c.fetchone()
            grupo.cod = resultado[0]
            c.execute('INSERT INTO workergroup (codworker, codgroup, administrator) VALUES (?, ?, ?);', (trabajador.cod, grupo.cod, 'True'))
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(traceback.format_exc())
            conn.close()
            return None
        return grupo
    
    def conseguirGrupos(self, trabajador=Worker()):
        return ""

    def conseguirGruposDB(self,trabajador = Worker()):
        aprobado = statuse(0)
        res = ""
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        primera = True
        primeraGrupos = True

        pala = ''
        pala = pala + 'SELECT groupe.cod, groupe.name FROM workergroup '
        pala = pala + 'INNER JOIN groupe ON groupe.cod = workergroup.codgroup '
        pala = pala + 'INNER JOIN worker ON workergroup.codworker = worker.cod where id = ?;'

        palados = ''
        palados = palados + 'SELECT worker.cod, worker.name, worker.lastname, workergroup.administrator, worker.id FROM groupe '
        palados = palados + 'INNER JOIN workergroup ON workergroup.codgroup = groupe.cod '
        palados = palados + 'INNER JOIN worker ON worker.cod = workergroup.codworker '
        palados = palados + 'WHERE  groupe.cod = ?;'

        try:
            c.execute(pala, (trabajador.id,))
            resultado = c.fetchall()
            conn.commit()

            grupocod = "\"" + "grupocod" + "\":["

            grupetes = "\"" + "grupete" + "\":["
            prima = True
            
            for row in resultado:
                nuevoGrup = Group()
                nuevoGrup.name = row[1]
                nuevoGrup.cod = row[0]

                if (prima == True):
                    prima = False
                else:
                    grupetes = grupetes + ", "
                    grupocod = grupocod + ", "
                
                grupetes = grupetes  + "\"" + nuevoGrup.name + "\""
                grupocod = grupocod  + str(nuevoGrup.cod) 
            
            grupetes = grupetes + "],"
            grupocod = grupocod + "],"

            
            for row in resultado:
                nuevoGrupo = Group()
                nuevoGrupo.cod = row[0]
                nuevoGrupo.name = row[1]
                
                if (primeraGrupos == True):
                    primeraGrupos = False
                else:
                    res = res + ","

                res = res  + "\"" + nuevoGrupo.name + "\":["

                try:
                    c.execute(palados, (nuevoGrupo.cod,))
                    resultadodos = c.fetchall()
                    conn.commit()

                    for row in resultadodos:

                        if (primera == True):
                            primera = False
                        else: 
                            res = res + ","
                        nuevoTraba = self.conseguirTrabajador(row[4])
                        if (nuevoTraba is None):
                            return None
                        # if row[4] == trabajador.id:
                        #     aprobado = "\"status\":" + "\"" + statuse(nuevoTraba.status) + "\""
                        #     res = res + "{\"cod\":-1, \"name\": " + "\"" + row[1] + "\", " + "\"lastname\": " + "\"" + row[2] + "\", " + "\"administrator\":" + "\"" +  row[3] + "\"" +", " + "\"" + "status\":" + str(nuevoTraba.status) + "}"
                        # else:
                        #     res = res + "{\"cod\":" + str(row[0]) + ", \"name\": " + "\"" + row[1] + "\", " + "\"lastname\": " + "\"" + row[2] + "\", " + "\"administrator\":" + "\"" +  row[3] + "\"" +", " + "\"" + "status\":" + str(nuevoTraba.status) + "}"
                        if row[4] == trabajador.id:
                            aprobado = "\"status\":" + "\"" + statuse(nuevoTraba.status) + "\""
                            res = res + "{\"cod\":-1, \"name\": " + "\"" + row[1] + "\", " + "\"lastname\": " + "\"" + row[2] + "\", " + "\"administrator\":" + "\"" +  row[3] + "\"" +", " + "\"" + "status\":" + str(nuevoTraba.status) + ", \"id\":\"" + str(row[4])+ "\"}"
                        else:
                            res = res + "{\"cod\":" + str(row[0]) + ", \"name\": " + "\"" + row[1] + "\", " + "\"lastname\": " + "\"" + row[2] + "\", " + "\"administrator\":" + "\"" +  row[3] + "\"" +", " + "\"" + "status\":" + str(nuevoTraba.status) + ", \"id\":\"" + str(row[4])+ "\"}"

                    res = res + "]"
                    primera = True

                except Exception as e:
                    logging.error(traceback.format_exc())
                    conn.close()
        except Exception as e:
            logging.error(traceback.format_exc())
            conn.close()

            conn.close()
        res = "{" +aprobado + "," +grupocod + grupetes + res + "}"
        return res


principal = Maine()
#globales y clases


@app.route("/", methods = ['GET'])
def inicio():


   

    return "Universidad de palermo " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')

@app.route("/worker/login/<id>/<password>", methods=['GET'])
def login (id, password):
    worker = Worker()
    worker = principal.conseguirTrabajador(id)

    if (worker is None): #si no existe el trabajador
        return jsonify(status=ERROR_EXISTING_WORKER)

    if (worker.password != password):
        return jsonify(status=ERROR_PASSWORD)

    return json.dumps(worker.__dict__)


@app.route("/worker/checkin", methods = ['POST'])
def index():
    aprobado = "checkedout"
    logue = Log()
    data = request.json
    if (data is None):
        return None
    trabajador = Worker()#este es el trabajador que viene por el json
    nuevoTrabajador = Worker()#este es el que saco de la base de datos

    trabajador.id = data['id'].lower()
    trabajador.name = data['name'].lower()
    trabajador.lastname = data['lastname'].lower()
    trabajador.latitude = str(data['latitude'])
    trabajador.longitude= str(data['longitude'])
    trabajador.status = data['status']
    trabajador.mensajete = data['mensajete']


    nuevoTrabajador = principal.actualizarTrabajadorStatus(trabajador)
 
    if nuevoTrabajador is None:
        aprobado = ERROR_NOT_MATCH
        return jsonify (status=aprobado)
    
    if (principal.comparaTrabajadores(trabajador, nuevoTrabajador) is False):
        aprobado = ERROR_NOT_MATCH
        return jsonify(status=aprobado)
    
    logue = principal.conseguirUltimoLog(trabajador.id)
    if logue is None:
        aprobado = statuse(0)

    elif (logue.statusafter == 1 and trabajador.status == "1"):
        aprobado = statuse(1)

    print("Name: " + nuevoTrabajador.name)
    print("Lastname: " + nuevoTrabajador.lastname)
    print("id: " + nuevoTrabajador.id)
    print("Latitude: " + nuevoTrabajador.latitude)
    print("Longitude: " + nuevoTrabajador.longitude)
    aprobado = statuse(nuevoTrabajador.status)
    print("Status: " + aprobado)
    
    return jsonify(status=aprobado)

@app.route("/worker/status/<name>/<lastname>/<latitude>/<longitude>/<ide>/<status>", methods = ['GET'])
def satusConexion (name, lastname, latitude,longitude, ide, status):
    trabajador = Worker()

    trabajador.id = ide.lower()
    trabajador.name = name.lower()
    trabajador.lastname =lastname.lower()
    trabajador.latitude = str(latitude)
    trabajador.latitude = str(longitude)
    trabajador.status = None

    nuevoTrabajador = principal.chequearTrabajador(trabajador)

    if (nuevoTrabajador is not None):
        logue = Log()
        logue = principal.conseguirUltimoLog(nuevoTrabajador.id)

        if (logue is None):
            return jsonify(status=statuse(0))
        
        x = datetime.now()
        y = datetime.strptime(logue.time, '%Y-%m-%d %H:%M:%S')



        return  jsonify(status = statuse(logue.statusafter), time = diferenciaFechas(x,y))
    else: 
        aprobado = ERROR_NOT_MATCH
        return jsonify(status=aprobado)   
    return ""

@app.route('/worker/task/insert', methods = ['POST'])
def insertTask ():
    
    data = request.json
    workernuevo = Worker()



    workernuevo.id = data["id"].lower()
    workernuevo.name = data["name"].lower()
    workernuevo.lastname = data["lastname"].lower()
    workernuevo.password = data["password"].lower()





    #acá tengo el worker si está correcto
    workerDB = principal.chequearTrabajador(workernuevo)

    if (workerDB is None):
        return jsonify(status=ERROR_EXISTING_WORKER)

    if (workerDB.password != workernuevo.password):
        return jsonify(status=ERROR_PASSWORD)
    



    nuevaTarea = Job()

    nuevaTarea.name = data["namework"].lower()
    nuevaTarea.description = data["description"].lower()
    nuevaTarea.workercreator = workernuevo.id
    nuevaTarea.workerslave = data["workerslavecod"].lower()
    nuevaTarea.begin = data["begin"]
    nuevaTarea.end = data["ende"]
    nuevaTarea.estimated = int(data["estimated"])

    resultado = principal.insertarTarea(nuevaTarea) 

    if (resultado is None):
        return jsonify(status=ERROR_EXISTING_WORKER)
    elif (resultado == True):
        return jsonify(status=SUCCESS)
    else:
        return jsonify(status=ERROR_EXISTING_WORKER)       

@app.route('/worker/task/status/<string:id>/<string:name>/<string:lastname>', methods = ['GET'])
def getTask (id, name, lastname):
    trabajador = Worker()

    trabajador.id = id
    trabajador.name = name
    trabajador.lastname = lastname 

    nuevoTrabajador = principal.chequearTrabajador(trabajador)

    if (nuevoTrabajador is None):
        return jsonify(status=ERROR_EXISTING_WORKER)

    if (nuevoTrabajador.id != trabajador.id or nuevoTrabajador.name != trabajador.name or nuevoTrabajador.lastname != trabajador.lastname):
        return jsonify(status=ERROR_NOT_MATCH)
    
    if (principal.recibirTareas(nuevoTrabajador)):
        return creaJSONtareas(principal.job, nuevoTrabajador)
    

@app.route('/worker/insert', methods = ['POST'])
def insertarUsuario():
    data = request.json
    workerNuevo = Worker()

    workerNuevo.id = data["id"].lower()
    workerNuevo.name = data["name"].lower()
    workerNuevo.lastname = data["lastname"].lower()
    #workerNuevo.password = data["password"]

    if (principal.insertarTrabajador(workerNuevo) is False):
        return jsonify(status=ERROR_EXISTING_WORKER)
    else:
        return jsonify(status=SUCCESS)

@app.route('/group/edit', methods = ['POST'])
def crearGrupo():
    data = request.json
    trabajador = Worker()
    grupo = Group()

    # trabajador.name = data["name"].lower()
    # trabajador.lastname = data["lastname"].lower()
    trabajador.id = data["id"].lower()
    trabajador.password = data["password"]
    grupo.name = data["namegroup"].lower()
    action = data["action"]

    #0 agregar grupo
    #1 editar grupo
    #2 eliminar grupo
    if (action == 0): 
        if (principal.agregarGrupo(trabajador, grupo)):
            return jsonify(status=SUCCESS)
        else:
            return jsonify(status=NOT_SUCCESS)
    
    return None
    
@app.route('/group/status/<name>/<lastname>/<latitude>/<longitude>/<ide>/<status>', methods = ['GET'])
def recibirGrupos(name, lastname, latitude,longitude, ide, status):

    trabajador = Worker()#este es el trabajador que viene por el json

    trabajador.id = ide.lower()
    trabajador.name = name.lower()
    trabajador.lastname =lastname.lower()
    trabajador.latitude = str(latitude)
    trabajador.latitude = str(longitude)
    trabajador.status = status


    workerDB = principal.chequearTrabajador(trabajador)

    if (workerDB is None):
        return jsonify(status=ERROR_NOT_MATCH)

    if (workerDB.id != trabajador.id or workerDB.name != trabajador.name or workerDB.lastname != trabajador.lastname):
        return jsonify(status=ERROR_NOT_MATCH)
        

    jsone = principal.conseguirGruposDB(trabajador)

    if (jsone is None):
        return jsonify(status=ERROR_NOT_MATCH)
    else :
        return jsone

@app.route('/log/<id>/<name>/<lastname>/<password>/<begin>/<ende>', methods = ['GET'])
def recibirLogs (id,name,lastname,password,begin, ende):
    
    workernuevo = Worker()
    


    workernuevo.id = id.lower()
    workernuevo.name = name.lower()
    workernuevo.lastname = lastname.lower()
    workernuevo.password = password.lower()


    #acá tengo el worker si está correcto
    workerDB = principal.chequearTrabajador(workernuevo)

    #acá tengo el worker si está correcto
    workerDB = principal.chequearTrabajador(workernuevo)

    if (workerDB is None):
        return jsonify(status=ERROR_EXISTING_WORKER)

    if (workerDB.password != workernuevo.password):
        return jsonify(status=ERROR_PASSWORD)

    

    if principal.conseguirLog(begin,ende,workerDB.id):
        pala = creaJSONLogs()
        return pala
    


@app.route('/returnpaper', methods = ['GET'])
def return_files_tut():
    try:
        return send_file('paper.pdf', attachment_filename='paper.pdf')
    except Exception as e:
        return str(e)


    return "success"
        













def statuse (num):
    
    nume = int(num)
    if (nume == 0):
        return "checkedout"
    if (nume == 1):
        return "checkedin"
    if (nume == 2):
        return "Idle"

def existe (dataid, dataname, datalastname):
    conn=sqlite3.connect('data.db')
    c = conn.cursor()

    try:
        c.execute('SELECT * FROM worker WHERE id = ? and name = ? and lastname = ? ;' , (dataid, dataname, datalastname))
    except:
        conn.close
        return None

    resultado = c.fetchone()

    conn.commit()
    conn.close

    if resultado is None:
        return False
    else:
        return True

def diferenciaFechas(now, then):
    diferencia = now - then
    return diferencia.days * 86400 + diferencia.seconds

def creaJSONtareas(listaTarea, trabajador = Worker()):
    pala = "\"" + "status" + "\": "
    pala = pala +  "\"" + statuse(trabajador.status) + "\", \"grupete\": ["


    primero = True
    for row in listaTarea:
    

        if (primero == False):
            pala = pala + "," + json.dumps(row.__dict__)
        else:
            primero = False
            pala = pala + json.dumps(row.__dict__)

    pala = pala + "]"
        

    return "{" + pala + "}"
    #return "get"

def creaJSONLogs():
    pala = ""
    first = True
    # if len(principal.log)==0:
    #     return None

    pala = "\"status\":\"success\","
    pala = pala + "\"log\":["

    for row in principal.log:

        if first:
            first = False
        else:
            pala = pala + ","


        pala = pala + "{\"codworker\": " + str(row.codworker) + ","
        pala = pala + "\"statusbefore\": " + str(row.statusbefore) + ","
        pala = pala + "\"statusafter\": " + str(row.statusafter) + ","
        pala = pala + "\"time\": \"" + str(row.time) + "\","
        pala = pala + "\"latitude\": " + str(row.latitude) + ","
        pala = pala + "\"longitude\": " + str(row.longitude) + ","
        pala = pala + "\"vitacora\": \"" + str(row.vitacora) + "\"}"

        #print(pala)
    pala = pala + "]"

    pala = "{" + pala + "}"

    return pala


 
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False,  threaded=True)
    #app.run(debug=True)
    