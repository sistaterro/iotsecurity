import sqlite3
import traceback
import logging
from clases import  Usuario


def insertUser(user = Usuario()):
    conn = sqlite3.connect('data.db')

    c = conn.cursor()

    resultado = ""

    pala = ""
    pala = pala + "INSERT INTO user (name) VALUES "
    pala = pala + "(?);"

    try:
        c.execute(pala, (user.name,))
        conn.commit()
    except:
        logging.error(traceback.format_exc())
        conn.close()
        return None        


    pala = ""
    pala = pala + "SELECT id FROM user "
    pala = pala + "WHERE name = ?;"

    try:
        c.execute(pala, (user.name,))
        conn.commit()
    except:
        logging.error(traceback.format_exc())
        conn.close()
        return None

    resultado = c.fetchone()

    user.id = resultado[0]

    pala = ""
    pala = pala + "INSERT INTO position (id_user, latitude, longitude) "
    pala = pala + "VALUES (?, ?, ?);"


    try:
        c.execute(pala, (user.id, user.latitude, user.longitude,))
        conn.commit()
    except:
        logging.error(traceback.format_exc())
        conn.close()
        return None        


    conn.close()

    return True



