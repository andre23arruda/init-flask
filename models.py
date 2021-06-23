class Jogo:
    '''Model Jogo'''
    def __init__(self, nome, categoria, console, id=None):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.console = console


class Usuario:
    '''Model Usuário'''
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha