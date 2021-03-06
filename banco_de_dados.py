import sqlite3
conn = sqlite3.connect('dados.db')

def create_table_if_not():
  cursor = conn.cursor()

  try:
    cursor.execute("""
    CREATE TABLE membros (
                nome TEXT NOT NULL,
                tia INTEGER,
                email TEXT,
                nomeservidor TEXT,
                mensagens INTEGER NOT NULL,
                datelogin DATE
        );""")
  except:
    pass



def criar_usuario(author, conn):
  cursor = conn.cursor()
  cursor.execute(f"""SELECT nome, mensagens FROM membros WHERE nome = '{author}' """)
  res = cursor.fetchall()

  cursor = conn.cursor()
  if res == []: 
    cursor.execute(f"""INSERT INTO membros (nome, mensagens) VALUES ('{author}', 1)""")
    conn.commit()
  else: 
    cursor.execute(f"""UPDATE membros SET mensagens = {int(res[0][1]) + 1} WHERE nome = '{author}'""") 
    conn.commit()