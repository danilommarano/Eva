from datetime import datetime

def show_commands():
  """
  Retorna uma string com todos os comandos que a Eva aceita
  """
  commands = {
    '!comandos': 'Imprime lista com todos os comandos',
    '!linguas' : 'Imprime lista com todas as linguas',
    '!traduzir': 'Traduz um texto de uma lingua para outra.',
    '!dados': 'Imprime gráficos sobre os dados do servidor',
  }

  texto = f"```\n{'Comando':<15}{'Descrição'}\n" + '—' * 30 + '\n'
  for keys, values in commands.items():
    texto += f"{keys:<15}{values}\n"
  texto += "```"
  return texto

def saudacoes():
  """
  Retorna uma string com a saudação correta de acordo com o horário do dia 
  ('Bom dia', 'Boa tarde', 'Boa noite').
  """
  hour = datetime.now().hour

  if hour >= 4 and hour < 12:
    return 'Bom dia'
  elif hour >= 12 and hour < 18:
    return 'Boa tarde'
  else:
    return 'Boa noite'