import mediator as db
from clases import Usuario

#id = db.insertUser("juan", "/$GPGLL,3435.46496,S,05825.13509,W,105601.00,")

us = Usuario()

us.insert("hhhh", "/$GPGLL,3435.46496,S,05825.13509,W,105601.00,")

db.insertUser(us)