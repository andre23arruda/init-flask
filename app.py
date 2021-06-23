from flask import Flask
from models import Jogo, Usuario
import os, sqlite3
from database import dao


# config
app = Flask(__name__)
app.secret_key = 'mestra'
debug = True

# sqlite
db = sqlite3.connect('database/database.db', check_same_thread=False)

# database tables
jogo_dao = dao.JogoDao(db)
usuario_dao = dao.UsuarioDao(db)

# uploads
app.config['UPLOAD_PATH'] = f'{ os.path.dirname(os.path.abspath(__file__)) }/uploads'

from views import *

# run
if __name__ == '__main__':
    app.run(debug=debug)