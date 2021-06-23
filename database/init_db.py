import sqlite3
print('Conectando...')

conn = sqlite3.connect('database/database.db')

conn.execute('CREATE TABLE jogo (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, categoria TEXT, console TEXT)')
conn.execute('CREATE TABLE usuario (id TEXT PRIMARY KEY, nome TEXT, senha TEXT)')

# inserindo usuarios
cursor = conn.cursor()
cursor.executemany(
	'INSERT INTO usuario (id, nome, senha) VALUES (?, ?, ?)',
	[
		('root', 'Admin', 'senha1234'),
	]
)

cursor.execute('select * from usuario')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
cursor.executemany(
      'INSERT INTO jogo (nome, categoria, console) VALUES (?, ?, ?)',
      [
            ('God of War 4', 'Acao', 'PS4'),
            ('NBA 2k18', 'Esporte', 'Xbox One'),
            ('Rayman Legends', 'Indie', 'PS4'),
            ('Super Mario RPG', 'RPG', 'SNES'),
            ('Super Mario Kart', 'Corrida', 'SNES'),
            ('Fire Emblem Echoes', 'Estrategia', '3DS'),
      ])

cursor.execute('select * from jogo')
print(' -------------  Jogos:  -------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# commitando senão nada tem efeito
conn.commit()
cursor.close()