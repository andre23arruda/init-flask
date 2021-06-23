from flask import (
    render_template, request,
    redirect, session,
    flash, url_for,
    send_from_directory
)
from database import dao
from models import Jogo, Usuario
import os, time
from app import app, jogo_dao, usuario_dao
from utils import *


@app.route('/')
def lista():
    '''Lista todos os jogos'''
    context = {
        'nome_pagina': 'Jogoteca',
        'titulo': 'Jogoteca',
        'jogos': jogo_dao.listar()
    }
    return render_template('lista.html', **context)


@app.route('/novo')
def novo():
    '''Página para criar jogo novo'''
    if is_user_signed_in(session):
        context = {
            'nome_pagina': 'Novo Jogo',
            'titulo': 'Novo Jogo',
        }
        return render_template('novo.html', **context)
    flash(f'Faça login', 'warning')
    return redirect(url_for('login', next_page='novo'))


@app.route('/criar', methods=['POST',])
def criar():
    '''Cria jogo novo'''
    jogo = Jogo(
        request.form['nome'],
        request.form['categoria'],
        request.form['console'],
    )
    jogo_dao.salvar(jogo)
    flash(f'Jogo criado com sucesso', 'success')

    # arquivo
    arquivo = request.files['arquivo']
    if arquivo:
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        arquivo.save(f'{ upload_path }/capa_{ jogo.id }-{ timestamp }.jpg')

    return redirect(url_for('lista'))


@app.route('/editar/<int:jogo_id>')
def editar(jogo_id):
    '''Página para editar jogo'''
    capa_jogo = get_imagem(jogo_id)
    if is_user_signed_in(session):
        context = {
            'nome_pagina': 'Editar Jogo',
            'titulo': 'Editar Jogo',
            'jogo': jogo_dao.busca_por_id(jogo_id),
            'capa_jogo': capa_jogo,
        }
        return render_template('editar.html', **context)
    flash(f'Faça login', 'warning')
    return redirect(url_for('login', next_page='novo'))


@app.route('/atualizar/<int:jogo_id>', methods=['POST',])
def atualizar(jogo_id):
    '''Atualiza jogo'''
    jogo = Jogo(
        request.form['nome'],
        request.form['categoria'],
        request.form['console'],
        jogo_id
    )
    jogo_dao.salvar(jogo)
    flash(f'Jogo editado com sucesso', 'success')

    # arquivo
    arquivo = request.files['arquivo']
    if arquivo:
        delete_imagem(jogo.id)
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        arquivo.save(f'{ upload_path }/capa_{ jogo.id }-{ timestamp }.jpg')

    return redirect(url_for('lista'))


@app.route('/deletar/<int:jogo_id>')
def deletar(jogo_id):
    '''Apaga novo'''
    jogo_dao.deletar(jogo_id)
    flash(f'Jogo removido com sucesso', 'warning')
    return redirect(url_for('lista'))


@app.route('/ver/<int:jogo_id>')
def ver(jogo_id):
    '''Página ver detalhes do jogo'''
    capa_jogo = get_imagem(jogo_id)
    if is_user_signed_in(session):
        jogo = jogo_dao.busca_por_id(jogo_id)
        context = {
            'nome_pagina': 'Detalhes',
            'titulo': jogo.nome,
            'jogo': jogo,
            'capa_jogo': capa_jogo,
        }
        return render_template('detalhes.html', **context)
    flash(f'Faça login', 'warning')
    return redirect(url_for('login', next_page='novo'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    '''Retorna imagem do jogo salva no servidor'''
    upload_path = app.config['UPLOAD_PATH']
    return send_from_directory(upload_path, nome_arquivo)


@app.route('/login')
def login():
    '''Página de login do usuário'''
    if is_user_signed_in(session):
        usuario = session['usuario_logado']
        flash(f'{ usuario } já está logado', 'success')
        return redirect(url_for('lista'))

    context = {
        'nome_pagina': 'Login',
        'titulo': 'Login',
        'next_page': request.args.get('next_page')
    }
    return render_template('login.html', **context)


@app.route('/autenticar', methods=['POST',])
def autenticar():
    '''Autenticação do usuário'''
    usuario = request.form['usuario']
    senha = request.form['senha']

    if verify_user_dao(usuario, senha):
        flash(f'{ usuario } logou com sucesso!', 'success')
        session['usuario_logado'] = usuario
        next_page = request.form['next_page']
        return redirect(url_for(next_page))

    flash(f'Tente novamente.', 'danger')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    '''Logout do usuário'''
    session['usuario_logado'] = None
    flash(f'Nenhum usuário logado.', 'warning')
    return redirect(url_for('login'))