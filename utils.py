import os
from app import app, jogo_dao, usuario_dao
from flask import session

DEFAUL_COVER_IMAGE = 'capa_padrao.jpg'

def is_user_signed_in(session):
    '''Verifica se o usuário está logado'''
    if not 'usuario_logado' in session or not session['usuario_logado']:
        return False
    return True


def verify_user(usuario, senha):
    '''Verifica se o usuário está cadastrado e se a senha está correta'''
    if usuario in usuarios:
        return senha == usuarios[usuario].senha
    return False


def verify_user_dao(usuario, senha):
    '''Verifica se o usuário está cadastrado e se a senha está correta'''
    user_is_registered = usuario_dao.buscar_por_id(usuario)
    if user_is_registered:
        return user_is_registered.senha == senha
    return False


def file_exists(file_name):
    '''Verifica se o arquivo existe na pasta de uploads'''
    return os.path.exists(os.path.join(app.config['UPLOAD_PATH'], file_name))


def get_imagem(jogo_id):
    '''Retorna nome do arquivo completo de acordo com id'''
    for file_name in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa_{jogo_id}' in file_name:
            return file_name
    return DEFAUL_COVER_IMAGE


def delete_imagem(jogo_id):
    '''Apaga imagem do jogo de acordo com id'''
    file_name = f'{ app.config["UPLOAD_PATH"] }/{ get_imagem(jogo_id) }'
    if file_name and not DEFAUL_COVER_IMAGE in file_name :
        os.unlink(file_name)