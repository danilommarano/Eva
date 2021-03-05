from googletrans import LANGUAGES
from google_trans_new import google_translator

def show_langs():
  """
  Retorna um texto formatado mostrando todas as linguas disponíveis para tradução
  """
  texto = f"```\n{'Codigo':<8} {'Lingua'}\n" + '—' * 20 + '\n'
  for keys, values in LANGUAGES.items():
    texto += f"{keys:<8} {values}\n"
  texto += "```"
  return texto



def translate_it(command):
  """
  Traduz o texto dado o comando como parâmetro. 
  Sintaxe:

    !traduzir <código_origem>-<código_objetivo> <texto_a_traduzir>

  Exemplo:

    !traduzir pt-en Eu ainda estou apaixonada com você, garoto.

    # Output:
    # I'm still in love with you, boy.

  """
  translator = google_translator() 

  try:
    command = command.split()[1:]  # remove '!traduzir'
    params = command[0].split('-') # 
    text =  ' '.join(command[1:])
    src, tgt = params[0], params[1]
    result = translator.translate(text, lang_tgt=tgt, lang_src=src)
  except IndexError:
    result = """Não entendi nada do que você escreveu kk. Esta é a sintaxe do comando `!traduzir`: \n```!traduzir <código_origem>-<código_objetivo> <texto_a_traduzir>```Exemplo: \n```!traduzir pt-en Este texto será traduzido para o inglês.``` Para mais informações sobre os códigos de linguas disponíveis digite `!linguas`."""
  except:
    result = """Você inseriu um código de lingua não disponível. Para mais informações sobre os códigos disponíveis digite `!linguas`."""
  finally:
    return result