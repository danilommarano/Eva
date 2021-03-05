import discord
import os
import time
import sqlite3
#from neuralnet.neruralnet import *

import uteis
import translate

#os.system('pip3 install tf-nightly')
os.system('pip3 install requests')
os.system('pip3 install google_trans_new')


# Estabelece conexão com o banco de dados dados.db
conn = sqlite3.connect('dados.db')
cursor = conn.cursor()

# Se não existir, cria a tabela membros no banco de dados 
try:
  cursor.execute("""
  CREATE TABLE membros (
          nome TEXT NOT NULL,
          tia INTEGER,
          email TEXT,
          nomeservidor TEXT,
          mensagens INTEGER NOT NULL,
          datelogin DATE NOT NULL,
  );
  """)
except:
  pass

# Gera uma instância da Eva
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

# Essa função pode ser armazenada num outro arquivo, um destinado para funções do banco de dados?
def criar_usuario(author):
  cursor = conn.cursor()
  cursor.execute(f"""SELECT nome, mensagens FROM clientes WHERE nome = '{author}' """)
  res = cursor.fetchall()

  cursor = conn.cursor()
  if res == []: 
    cursor.execute(f"""INSERT INTO clientes (nome, mensagens) VALUES ('{author}', 1)""")
    conn.commit()
  else: 
    cursor.execute(f"""UPDATE clientes SET mensagens = {int(res[0][1]) + 1} WHERE nome = '{author}'""") 
    conn.commit()


# cursor = conn.cursor()
# cursor.execute(f"""UPDATE clientes SET email = 'gustavo.b.schwarz@gmail.com', tia = '32141157' WHERE nome = '{message.author}'""") 
# conn.commit()


# ————————————————————————————————— Evento: Eva online ————————————————————————————————— #
@client.event
async def on_ready():
  print(client.user)
# —————————————————————————————————————————————————————————————————————————————————————— #


# ———————————————————————————————— Evento: Novo Usuário ———————————————————————————————— #
@client.event
async def on_member_join(member):
  """
  Deseja boas vindas aos novos membros da liga mo
  """
  boas_vindas = client.get_channel(816451719205617695)
  await boas_vindas.send(f"{uteis.saudacoes()} {member.name}!\n Seja muito bem vindo ao servidor do discord da Liga Academica Estudantil de Inteligencia Artificial & Ciência de Dados da Universidade Presbiteriana Mackenzie")
  print(client.user)
  await boas_vindas.send(file=discord.File('imgs/Rect_Icon_Txt.png'))
  time.sleep(3)
  await boas_vindas.send("Agora vou precisar registrar seus dados em nosso banco")
  time.sleep(1)
  await boas_vindas.send("Digite o seu **primeiro e último nome** em letras maiúsculas, como: EVA DOMINGUES")
# —————————————————————————————————————————————————————————————————————————————————————— #



# ——————————————————————————————— Evento: Mensagem nova ———————————————————————————————— #
@client.event
async def on_message(message):

  #txt = open('neuralnet/mensagens.txt', 'a')
  #txt.write(message.content)
  #txt.close()
  #criar_usuario(message.author)


# ---------------------- Se for mensagem da Eva, não responda nada.--------------------- #
  if message.author == client.user:
    return
# -------------------------------------------------------------------------------------- #

# ----------------------- Nova mensagem no canal 🖖boas-vindas  ------------------------ #
  if message.channel.id == 816451719205617695 and message.author != client.user:
    boas_vindas = client.get_channel(816451719205617695)
    if message.content == message.content.title():
      cursor.execute(f"""UPDATE clientes SET nomeservidor = {message.content} WHERE nome = '{message.author}'""") 
      await boas_vindas.send()

    await message.channel.send(message.content)
    pass
# -------------------------------------------------------------------------------------- #
 
# ---------------------------------- Comando: !count ----------------------------------- #
  if message.content.startswith('!count'):
    cursor = conn.cursor()
    cursor.execute(f"""SELECT nome, mensagens FROM clientes WHERE nome = '{message.author}' """)
    res = cursor.fetchall()
    await message.channel.send(f"{message.author} sent {res[0][1]} messages!")
# -------------------------------------------------------------------------------------- #

# -------------------------------- Comando: !comandos ---------------------------------- #
  if message.content.startswith('!comandos'):
    await message.channel.send(uteis.show_commands())
# -------------------------------------------------------------------------------------- #

# -------------------------------- Comando: !linguas ----------------------------------- #
  if message.content.startswith('!linguas'):
    await message.channel.send(translate.show_langs())
# -------------------------------------------------------------------------------------- #

# -------------------------------- Comando: !traduzir ----------------------------------- #
  if message.content.startswith('!traduzir'):
    await message.channel.send(translate.translate_it(message.content))
# -------------------------------------------------------------------------------------- #

# -------------------------------- Comando: !py ----------------------------------- #
  """
  if message.content.startswith('!py'):
    await message.channel.send(display_output_file())
  """
# -------------------------------------------------------------------------------------- #
# —————————————————————————————————————————————————————————————————————————————————————— #


client.run(os.getenv('TOKEN'))
