import discord
import os
import time
import sqlite3
#from neuralnet.neruralnet import *
import banco_de_dados
import matplotlib.pyplot as plt
import uteis
import translate
import seaborn

import base64
import io 


# os.system('pip3 install requests')
# os.system('pip3 install google_trans_new')

conn = sqlite3.connect('dados.db')
banco_de_dados.create_table_if_not()

# Gera uma instância da Eva
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

# cursor = conn.cursor()
# cursor.execute(f"""UPDATE clientes SET email = 'gustavo.b.schwarz@gmail.com', tia = '32141157' WHERE nome = '{message.author}'""") 
# conn.commit()


# ————————————————————————————————— Evento: Eva online ————————————————————————————————— #
@client.event
async def on_ready():
  boas_vindas = client.get_channel(816451719205617695)
  await boas_vindas.send("Olá Mackenzista!\n Seja muito bem vindo ao servidor do discord da **Liga Academica Estudantil de Inteligencia Artificial & Ciência de Dados da Universidade Presbiteriana Mackenzie**.")
  await boas_vindas.send(f"""```
╭─╮    ╭─────╮╭─────╮    ╭─────╮╭─────╮    ╭─────╮┌─────╮    ╭─┐ ┌─╮╭─────╮╭────╮╭────╮
│ │    │ ╭─╮ ││ ╭───╯    ╰─┐ ┌─╯│ ╭─╮ │    │ ┌───┘│ ┌─╮ │    │ │ │ ││ ╭─╮ ││ ╭╮ ││ ╭╮ │
│ │    │ ╰─╯ ││ └───╮      │ │  │ ╰─╯ │    │ │    │ │ │ │    │ │ │ ││ └─╯ ││ ││ ╰╯ ││ │
│ │    │ ┌─┐ ││ ╭───╯      │ │  │ ┌─┐ │    │ │    │ │ │ │    │ │ │ ││ ┌───╯│ │╰────╯│ │
│ └───╮│ │ │ ││ └───╮    ╭─┘ └─╮│ │ │ │    │ └───┐│ └─╯ │    │ └─┘ ││ │    │ │      │ │
└─────╯╰─╯ ╰─╯╰─────╯    ╰─────╯╰─╯ ╰─╯    ╰─────╯└─────╯    ╰─────╯└─╯    ╰─╯      ╰─╯ 
```""")
  await boas_vindas.send("Para você ter acesso ao nosso servidor vou precisar fazer três perguntinhas sobre seus dados mackenzistas. Se estiver pronto para responde-las clique no simbolo ✅ logo aqui embaixo.")
# —————————————————————————————————————————————————————————————————————————————————————— #


# ———————————————————————————————— Evento: Novo Usuário ———————————————————————————————— #
@client.event
async def on_member_join(member):
  """
  Deseja boas vindas aos novos membros da liga mo
  """
  novatoa_role = discord.utils.get(member.guild.roles, name="Novato(a)")
  await member.add_roles(novatoa_role)
# —————————————————————————————————————————————————————————————————————————————————————— #



# ——————————————————————————————— Evento: Mensagem nova ———————————————————————————————— #
@client.event
async def on_message(message):

  #txt = open('neuralnet/mensagens.txt', 'a')
  #txt.write(message.content)
  #txt.close()
  banco_de_dados.criar_usuario(message.author, conn)

# ---------------------- Se for mensagem da Eva, não responda nada.--------------------- #
  if message.author == client.user:
    if '✅' in message.content:
      await message.add_reaction('✅')
    return
# -------------------------------------------------------------------------------------- #

# ---------------------------------- Cadastro dados ------------------------------------ #
  if message.content.startswith('!nome'):
    all_channels = [channel for channel in client.get_all_channels()]
    if message.channel.id not in all_channels:
      name = message.content.split()[1:]
      name = ' '.join(name).lower()
      # TODO: query salva no banco de dados
      await message.channel.send("Agora vou precisar do seu TIA. Só que dessa vez você tem que colocar o comando `!tia` na frente.")
      await message.channel.send("https://i.imgur.com/031qOEI.gif")

  if message.content.startswith('!tia'):
    all_channels = [channel for channel in client.get_all_channels()]
    if message.channel.id not in all_channels:
      tia = message.content.split()[1]
      # TODO: query salva no banco de dados
      nome = "danilo matrangolo marano".title()
      tia  = 41915704
      # TODO: query pegas nome e tia no banco de dados
      await message.channel.send("Quase pronto. Agora eu preciso que você confirme se seus dados estão corretos. Leia atentamente para que não precise alterar no futuro.")
      await message.channel.send(f"```\nNome: {nome}\nTIA: {tia}```")
      await message.channel.send("Clique em ✅ se seus dados estão ok.")
# -------------------------------------------------------------------------------------- #

# ---------------------------------- Comando: !count ----------------------------------- #
  if message.content.startswith('!count'):
    cursor = conn.cursor()
    cursor.execute(f"""SELECT nome, mensagens FROM membros WHERE nome = '{message.author}' """)
    res = cursor.fetchall()
    cursor.execute("""SELECT nome, mensagens FROM membros""")
    res_plot = cursor.fetchall()

    pessoas = []
    mensagens = []

    for value in res_plot:
      pessoas.append(value[0])
      mensagens.append(value[1])

    plt.bar(pessoas, mensagens, width=0.25)
    plt.title("Number of messages")
    
    IObytes = io.BytesIO()
    plt.savefig(IObytes,  format='png')
    IObytes.seek(0)

    await message.channel.send(file=discord.File(IObytes, 'plot.png'))

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

@client.event
async def on_reaction_add(reaction, user):
  boas_vindas = client.get_channel(816451719205617695)
  if (str(reaction) == '✅') and (user != client.user) and (reaction.message.channel == boas_vindas):
    await user.send('Oie!') 
    await user.send('Vou precisar do seu nome completo. Digite primeiro o comando `!nome` e depois o seu nome.  Se você fosse o Paulo Coelho preencheria da seguinte forma:')
    await user.send('https://i.imgur.com/pLY0YcT.gif')
    
client.run(os.getenv('TOKEN'))
