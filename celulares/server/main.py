from flask import Flask, jsonify
import mediator as db
from clases import Usuario


app = Flask(__name__)




@app.route('/', methods = ['GET'])
def index():
    return "hola mundo"



@app.route('/<string:gps>/<string:name>', methods = ['GET'])
def posicion(gps, name):


    us = Usuario()

    us.insert(name,gps)

    if db.insertUser(us) is not None:
        return "success"
    else:
        return "failure"









if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')