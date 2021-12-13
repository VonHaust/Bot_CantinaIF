from telegram.ext import *
import gspread
import os
#import random
#from gspread.models import Cell
#import string as string
import pandas as pd
#import schedule || Schedule não funciona porque o while() necessário bloqueia qualquer outra coisa que estiver rodando. No caso as outras funções/métodos. 
import time
import functools
import matplotlib.pyplot as plt

from datetime import datetime, timedelta
from threading import Timer

x=datetime.today()
#print(x.day, (x.hour - 3), x.minute, x.second)

t = time.localtime()
#print((t.tm_hour - 3), t.tm_min, t.tm_sec)
##Contagem de dias da semana(tm_wday), cmç em 0.
token = '1962960347:AAHxxhnb26z0Xy6hUVx47pVfEJlkhDCF8nw'
credentials = {
  "type": "service_account",
  "project_id": "botplanilhatest",
  "private_key_id": "1fc9cdf3836780ae3ffcb32caa769ccf758221c2",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCegs2M9PNMxlTX\nskwKiD8JwFb2gRJTQlDva1+QfxUnKxo6i7c96QejoV6GIM8wwK2y+KSMqFoj610D\n6KTap3n6mHRcDcC5dXaFDs9BW1nggpvJpdysJ2P1tJxCz6fXwl0KqMwf4SVz9SIw\ndgqPIpBYdyl41+y1SoBRAJ+J6u3Utvd0ijvxbw826EQJRY3WSF3nC4pu41t8IPBy\nNBsGMjoyHauysd6OtqQQRKRGkZin+HrZyw/UogYQWBC0JxqLW1Ad9J1L13F7hO0T\nf7aqx04ka8scE90+y/HOsQFLCue/YmUZ1Xi0W6R383iXcPlN/NhIRGKPgpjKofvz\n1OPCNGAbAgMBAAECggEALuCFFIIeb96Zmb6PcW/woJwiu7zZJAlRMTUCapPCuDYt\niBHoq6T+Ttx6vVT3oTXiSLLyyuxA2C2TcQP8uPNdhghPJSgmDlLYLap/DZeMAXLu\nyphEJh9yFuiGa9XIj+zZojzgPS9S6bOdnFJUdhclNBxtheDpjoXNY+c4x0tUcZsB\nc507A7YKqQTpjJ+b7DYLvy/2doaX7UXq1KZVaQCbB6WPblpUpgj6Wa9+zqaU4WUU\noTACT6UAOUEJY9yT6NDs1Xplwgcr16nZzBP0F52XS1TifAOcqET33n5sV5/mXIeq\nmQV3IOtFwVEXawg4bXI16K237qRBEU9rP3otGS/oOQKBgQDMUCTd9B17+/l9+Bdw\npXJ2OHNnCtCKXYVpo5Tk+08Q7W2VKHwgJIRLWLaCbmbngEt4LoiZBQByLGQFg4VH\nNtjSVi1zBg3gdfT+y4S1lQD+E2cF0hWNTdzvWYR8JqtBZsvpkyFLkDBabkLte+b2\nCuLeyFhBpIvzrduMQjZcb3CyKQKBgQDGnGR8sYIE1eFdvwIVPdwKeFTENff1RCyq\noKrflrE00ohNmAyIigwW+D03mnpiidkqgI+4cSI1y+kSec0G3vg/3fBR0duIHxQV\nAmUbC58cd/aN3hyoDnJA9fB/EMhC1Zepuhjef+PZUMlHngRleLTLA5HNDW9jMCVC\nWApXfZlwowKBgF6IWnaDw7yhGpAJYTcSpgJDHko3+8N5gAgf0v2btbqcUI6qG7x3\niOqf0lpJIL3OY5zo0vUSFmG9Xk4ay2jm3K19iCvnSjZn/YKCwhWOKtZkPc+4o5Ys\nx6PLJHyZG7X4DTM2izo+LdE5oSfmozeGU/BGfGdq7gJCmAmufR6JxXf5AoGAbbRl\nLRs/njwlyAqBtAn/SSk+aUMGO8v0gCtPN0GdkHfaIkIiaikWlHl6FwSVJWjPM9Lf\nkBmts9l2XGY7AdiXd2+4Fvm8MWw5Q4GXJ2E7+hWpcqOFYK7aHVe8B/PVKlWg+Hd6\n1Sv/R0KAa7a05vfNpXXLS2Bobnlhm0vWKo2N+9ECgYA0CDZRVwhjEi+rxp2GxYMp\ncTQ0aqOdbGzyGL3qo4Vs/iCcZe83bNRc7ndqv8m/lAUs/IY+IDvTAJF6KjF+29pU\nGDoDFXiEGTDliaj7tRjx3UZ8xNbOfjjR0GkG/wqPHAxqRPZqbcrrPNFWCw1z79l0\naMuuK9ryORSmpC1vnPmX2w==\n-----END PRIVATE KEY-----\n",
  "client_email": "botcantinaif@botplanilhatest.iam.gserviceaccount.com",
  "client_id": "110394672237536992027",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/botcantinaif%40botplanilhatest.iam.gserviceaccount.com"
}

gc = gspread.service_account_from_dict(credentials)
sh = gc.open("CantinaTest")

'''
#Comando do botão 'Start' da tela inicial.
def start_command(update,context):
  update.message.reply_text(f"Seja bem vindo(a) {update.message.from_user['first_name']}.""\n Esses são os principais comandos que possa vir a desejar:""\n/comandos; \n/menu; \n/almoco; \n/ajuda")
  

#Comando de help do bot, lista os comandos.
def comandos_command(update, context):
  update.message.reply_text(f"Olá, {update.message.from_user['first_name']}.""\n Essa é alista de comandos que eu reconheço:""\n /start - Poderá rever as boas vidas;""\n /comandos - Lista todos os comandos que reconheço;""\n /menu - Ainda em fase de implementação;""\n /almoco - Disponibiliza os comandos para os almoços diários;\n /sobre - Trago informações sobre meus criadores;""\n /campus - Site oficial do Campus - Jacobina;\n /ajuda - Disponibiliza um link para um vídeo que ensina o passo-a-passo sobre como utilizar o bot.")

#Comando do botão 'Sobre' da tela inicial.
def sobre_command(update,context):
  update.message.reply_text(f"Este bot e suas propriedades foram desenvolvidos pelo grupo Quack Studios sob orientação da mestra em Ciência da Computação, Rebeca Barros.""\n Os membros deste grupo são Matheus Oliveira e Marcella Portela, estudantes do Curso Técnico em Informática na instituição do IFBA, Campus Jacobina.")

  #Comando do botão 'Campus' da tela inicial.
def campus_command(update,context):
  update.message.reply_text(f"Este é o link para o site oficial do Campus Jacobina: ""\n https://portal.ifba.edu.br/jacobina")

  #Comando do botão 'ajuda' da tela inicial.
def ajuda_command(update,context):
  update.message.reply_text(f"Este é o link do vídeo que demonstra o passo-a-passo de como utilizar o bot, indicado para iniciantes: ""\n (link)")

#Quando o bot não reconhece algum comando.
def unknown(update, context):
    response_message = "Desculpa, não conheço esse comando.""\n Qualquer dúvida consulte o /ajuda"
    context.bot.send_message(
        chat_id = update.effective_chat.id, text = response_message
    )

#Comando do botão 'Menu' da tela inicial.
def menu_command(update,context):
  update.message.reply_text("Bem vindo ao cardápio da cantina! Digite a categoria do alimento que gostaria de consultar:\n/A - Bebidas\n/B - Salgados\n/C - Doces")

FLOAT_COLUMNS = ('Floats',)
BOOLEAN_COLUMNS = ('Booleans',)

def left_justified(melao1):
    formatters = {}

    # Pass a custom pattern to format(), based on
    # type of data
    for li in list(melao1.columns):
        if li in FLOAT_COLUMNS:
           form = "{{!s:<5}}".format()
        elif li in BOOLEAN_COLUMNS:
            form = "{{!s:<8}}".format()
        else:
            max = melao1[li].str.len().max()
            form = "{{:<{}s}}".format(max)
        formatters[li] = functools.partial(str.format, form)
    return melao1.to_string(formatters=formatters, index=False)
  
def A_command(update,context):
  melao = pd.DataFrame(sh.sheet1.get_all_records())
  melao1 = melao.query('Categoria=="Bebidas"')
  update.message.reply_text("As bebidas são: \n{}".format(left_justified(melao1)))

def B_command(update,context):
  melao = pd.DataFrame(sh.sheet1.get_all_records())
  melao1 = melao.query('Categoria=="Salgados"')
  update.message.reply_text("Os salgados são: \n{}".format(left_justified(melao1)))

def C_command(update,context):
  melao = pd.DataFrame(sh.sheet1.get_all_records())
  #melao.style.set_properties(**{'text-align': 'right'})
  melao1 = melao.query('Categoria=="Doces"')
  update.message.reply_text("Os doces são: \n{}".format(left_justified(melao1)))

def almoco_command(update,context):
  #goiaba = pd.DataFrame(sh.worksheet("Almoco").get_all_records())
  #update.message.reply_text("Gostaria de realizar a reserva de uma ficha do almoço do dia? Confira os pratos de cada dia digitando: \n'/D' para Segunda\n'/E' para Terça\n'/F' para Quarta\n'/G' para Quinta\n'/H' para Sexta")
  goiaba = pd.DataFrame(sh.worksheet("Almoco").get_all_records())
  dia_semana = t.tm_wday
  if dia_semana == 0:
    f = goiaba.query('Dia=="Segunda"')
  elif dia_semana == 1:
    f = goiaba.query('Dia=="Terça"')
  elif dia_semana == 2:
    f = goiaba.query('Dia=="Quarta"')
  elif dia_semana == 3:
    f = goiaba.query('Dia=="Quinta"')
  elif dia_semana == 4:
    f = goiaba.query('Dia=="Sexta"')
  else:
    pass
  update.message.reply_text("Os pratos do dia são: \n{}".format(f))

def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)

def pedidos_command(update, context):
  pedidos_list = pd.DataFrame(sh.worksheet("Pedidos").get_all_records())

  update.message.reply_text("Os pratos retirados ate o momento são: \n""\n""{}".format(pedidos_list))
  print(type(pedidos_list))
  print(pedidos_list)
  #print(pedidos_list['Fichas'] == 'Segunda')
  #print(pedidos_list[0]['Nome'])

def pedido_command(update, context):
  hora_pedido = (t.tm_hour - 3) 
  dia_semana = t.tm_wday
  if (hora_pedido >= 7 and hora_pedido <= 15): #Se a hora for maior/igual à 7AM E menor/igual à 15PM (também aceita pedidos até 15:59)
    val_cell = sh.worksheet("Almoco").acell
    #Pedidos feitos através de número (id) e não por nomes
    #Apenas 3 colunas na worksheet almoço (Dia, Pedidos, Quantidade de fichas por dia)
    #Adicionar "quantidade de fichas total" à worksheeet "Pedido"
    #Horário por datetime+BRT
    #Pesquisar a worksheet "Almoco" (linha 142) por dataframe e não células.
    prato_entrada_use = update.message.text.split(" ")[1]
    prato_s_n_1 = val_cell('B2').value
    prato_s_n_2 = val_cell('D2').value
    prato_t_n_1 = val_cell('B3').value
    prato_t_n_2 = val_cell('D3').value
    prato_qua_n_1 = val_cell('B4').value
    prato_qua_n_2 = val_cell('D4').value
    prato_qui_n_1 = val_cell('B5').value
    prato_qui_n_2 = val_cell('D5').value
    prato_sex_n_1 = val_cell('B6').value
    prato_sex_n_2 = val_cell('D6').value

    worksheet = sh.worksheet("YTD")
    next_row = next_available_row(worksheet)


    if prato_entrada_use == prato_s_n_1:
      if dia_semana == 0:
        valor_celu = int(val_cell('C2').value)
        val1 = (valor_celu - 1)
        if valor_celu == 0:
          update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nEsse prato não está mais disponível.")
        else:
          worksheet.update_acell("A{}".format(next_row), update.message.from_user['first_name'])
          worksheet.update_acell("B{}".format(next_row), update.message.from_user['last_name'])
          worksheet.update_acell("C{}".format(next_row), prato_entrada_use)
    #sh.worksheet("Pedidos").update('A3',update.message.from_user['first_name'])
    #sh.worksheet("Pedidos").update('B3',update.message.from_user['last_name'])
    #sh.worksheet("Pedidos").update('C3',prato_entrada_use)
          sh.worksheet("Almoco").update('C2', val1)
          update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nSeu pedido está sendo preparado.")
      elif dia_semana != 0:
              update.message.reply_text(f"  Olá {update.message.from_user['first_name']}.""\n \n Esse prato não faz parte do cardápio atual.\n \n Consulte o cardápio atualizado em /almoco.")

    elif prato_entrada_use == prato_s_n_2:
      valor_celu = int(val_cell('E2').value)
      val1 = (valor_celu - 1)
      if dia_semana == 0:
        if valor_celu == 0:
          update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nEsse prato não está mais disponível.")
        else:
          worksheet.update_acell("A{}".format(next_row), update.message.from_user['first_name'])
          worksheet.update_acell("B{}".format(next_row), update.message.from_user['last_name'])
          worksheet.update_acell("C{}".format(next_row), prato_entrada_use)
          sh.worksheet("Almoco").update('E2', val1)
          update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nSeu pedido está sendo preparado.")
      elif dia_semana != 0:
              update.message.reply_text(f"  Olá {update.message.from_user['first_name']}.""\n \n Esse prato não faz parte do cardápio atual.\n \n Consulte o cardápio atualizado em /almoco.")


    elif prato_entrada_use == prato_t_n_1:
      if dia_semana == 1:
        valor_celu = int(val_cell('C3').value)
        val1 = (valor_celu - 1)
        if valor_celu == 0:
          update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nEsse prato não está mais disponível.")
        else:
          worksheet.update_acell("A{}".format(next_row), update.message.from_user['first_name'])
          worksheet.update_acell("B{}".format(next_row), update.message.from_user['last_name'])
          worksheet.update_acell("C{}".format(next_row), prato_entrada_use)
          sh.worksheet("Almoco").update('C3', val1)
          update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nSeu pedido está sendo preparado.")
      elif dia_semana != 1:
              update.message.reply_text(f"  Olá {update.message.from_user['first_name']}.""\n \n Esse prato não faz parte do cardápio atual.\n \n Consulte o cardápio atualizado em /almoco.")
    elif prato_entrada_use == prato_t_n_2:
      if dia_semana == 1:
        valor_celu = int(val_cell('E3').value)
        val1 = (valor_celu - 1)
        if valor_celu == 0:
          update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nEsse prato não está mais disponível.")
        else:
          worksheet.update_acell("A{}".format(next_row), update.message.from_user['first_name'])
          worksheet.update_acell("B{}".format(next_row), update.message.from_user['last_name'])
          worksheet.update_acell("C{}".format(next_row), prato_entrada_use)
          sh.worksheet("Almoco").update('E3', val1)
          update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nSeu pedido está sendo preparado.")
      elif dia_semana != 1:
              update.message.reply_text(f"  Olá {update.message.from_user['first_name']}.""\n \n Esse prato não faz parte do cardápio atual.\n \n Consulte o cardápio atualizado em /almoco.")

    elif prato_entrada_use == prato_qua_n_1:
      if dia_semana == 2:
        valor_celu = int(val_cell('C4').value)
        val1 = (valor_celu - 1)
        if valor_celu == 0:
          update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nEsse prato não está mais disponível.")
        else:
          worksheet.update_acell("A{}".format(next_row), update.message.from_user['first_name'])
          worksheet.update_acell("B{}".format(next_row), update.message.from_user['last_name'])
          worksheet.update_acell("C{}".format(next_row), prato_entrada_use)

          sh.worksheet("Almoco").update('C4', val1)
          update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nSeu pedido está sendo preparado.")
      elif dia_semana != 2:
              update.message.reply_text(f"  Olá {update.message.from_user['first_name']}.""\n \n Esse prato não faz parte do cardápio atual.\n \n Consulte o cardápio atualizado em /almoco.")
    elif prato_entrada_use == prato_qua_n_2:
      if dia_semana == 2:
    
        valor_celu = int(val_cell('E4').value)
        val1 = (valor_celu - 1)
        if valor_celu == 0:
          update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nEsse prato não está mais disponível.")
        else:
          worksheet.update_acell("A{}".format(next_row), update.message.from_user['first_name'])
          worksheet.update_acell("B{}".format(next_row), update.message.from_user['last_name'])
          worksheet.update_acell("C{}".format(next_row), prato_entrada_use)

          sh.worksheet("Almoco").update('E4', val1)
          update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nSeu pedido está sendo preparado.")
      elif dia_semana != 2:
              update.message.reply_text(f"  Olá {update.message.from_user['first_name']}.""\n \n Esse prato não faz parte do cardápio atual.\n \n Consulte o cardápio atualizado em /almoco.")
    elif prato_entrada_use == prato_qui_n_1:
      if dia_semana == 3:

        valor_celu = int(val_cell('C5').value)
        val1 = (valor_celu - 1)
        if valor_celu == 0:
          update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nEsse prato não está mais disponível.")
        else:
          worksheet.update_acell("A{}".format(next_row), update.message.from_user['first_name'])
          worksheet.update_acell("B{}".format(next_row), update.message.from_user['last_name'])
          worksheet.update_acell("C{}".format(next_row), prato_entrada_use)

          sh.worksheet("Almoco").update('C5', val1)
          update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nSeu pedido está sendo preparado.")
      elif dia_semana != 3:
              update.message.reply_text(f"  Olá {update.message.from_user['first_name']}.""\n \n Esse prato não faz parte do cardápio atual.\n \n Consulte o cardápio atualizado em /almoco.")
    elif prato_entrada_use == prato_qui_n_2:
      if dia_semana == 3:
        valor_celu = int(val_cell('E5').value)
        val1 = (valor_celu - 1)
        if valor_celu == 0:
          update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nEsse prato não está mais disponível.")
        else:
          worksheet.update_acell("A{}".format(next_row), update.message.from_user['first_name'])
          worksheet.update_acell("B{}".format(next_row), update.message.from_user['last_name'])
          worksheet.update_acell("C{}".format(next_row), prato_entrada_use)

          sh.worksheet("Almoco").update('E5', val1)
          update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nSeu pedido está sendo preparado.")
      elif dia_semana != 3:
              update.message.reply_text(f"  Olá {update.message.from_user['first_name']}.""\n \n Esse prato não faz parte do cardápio atual.\n \n Consulte o cardápio atualizado em /almoco.")

    elif prato_entrada_use == prato_sex_n_1:
      if dia_semana == 4:

        valor_celu = int(val_cell('C6').value)
        val1 = (valor_celu - 1)
        if valor_celu == 0:
          update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nEsse prato não está mais disponível.")
        else:
          worksheet.update_acell("A{}".format(next_row), update.message.from_user['first_name'])
          worksheet.update_acell("B{}".format(next_row), update.message.from_user['last_name'])
          worksheet.update_acell("C{}".format(next_row), prato_entrada_use)

          sh.worksheet("Almoco").update('C6', val1)
          update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nSeu pedido está sendo preparado.")
      elif dia_semana != 4:
              update.message.reply_text(f"  Olá {update.message.from_user['first_name']}.""\n \n Esse prato não faz parte do cardápio atual.\n \n Consulte o cardápio atualizado em /almoco.")
    elif prato_entrada_use == prato_sex_n_2:
      if dia_semana == 4:

        valor_celu = int(val_cell('E6').value)
        val1 = (valor_celu - 1)
        if valor_celu == 0:
          update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nEsse prato não está mais disponível.")
        else:
          worksheet.update_acell("A{}".format(next_row), update.message.from_user['first_name'])
          worksheet.update_acell("B{}".format(next_row), update.message.from_user['last_name'])
          worksheet.update_acell("C{}".format(next_row), prato_entrada_use)

          sh.worksheet("Almoco").update('E6', val1)
          update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nSeu pedido está sendo preparado.")
      elif dia_semana != 4:
              update.message.reply_text(f"  Olá {update.message.from_user['first_name']}.""\n \n Esse prato não faz parte do cardápio atual.\n \n Consulte o cardápio atualizado em /almoco.")

    else:
       update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\n Não conhecemos esse prato.")
  # bot.copy_message(chat_id=chat_id, from_chat_id=update.effective_message.chat_id, message_id=update.effective_message.message_id,*args,**kwargs)
  else: #Se a hora for menor que 7AM ou maior que 15:59PM.
              update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nA cantina ainda não disponibilizou a retirada de fichas.")
              #Fazer um if de horário fora de funções
              sh.values_clear("'YTD'!A1:C1")

              sh.worksheet("Almoco").update('C2', 10) 
              sh.worksheet("Almoco").update('C3', 10)
              sh.worksheet("Almoco").update('C4', 10)
              sh.worksheet("Almoco").update('C5', 10)
              sh.worksheet("Almoco").update('C6', 10)
              sh.worksheet("Almoco").update('E2', 10)
              sh.worksheet("Almoco").update('E3', 10)
              sh.worksheet("Almoco").update('E4', 10)
              sh.worksheet("Almoco").update('E5', 10)
              sh.worksheet("Almoco").update('E6', 10)


def error(update, context):
    print(f"Update: {update} caused error: {context.error}")
'''
#Função Teste para manipulação da planilha
def teste():
  df = pd.DataFrame(sh.worksheet("Almoco").get_all_records())
  df.set_index("Dia", inplace = True) # transforma dia em index do dataframe
  data = df.loc[["Segunda"]] # apenas as linhas que possuem segunda na coluna Dia
  print("Funcão teste")
  print(data)
  for index, linha in data.iterrows():
    print(linha['Almoço_1'])

'''
#Chamada de todos os comandos.
def main():
  updater = Updater(token, use_context=True)
  dp = updater.dispatcher
  
  dp.add_handler(CommandHandler("start", start_command))
  dp.add_handler(CommandHandler("comandos", comandos_command))
  dp.add_handler(CommandHandler("pedido" , pedido_command))
  dp.add_handler(CommandHandler("sobre", sobre_command))
  dp.add_handler(CommandHandler("campus", campus_command))
  dp.add_handler(CommandHandler("menu", menu_command))
  dp.add_handler(CommandHandler("ajuda", ajuda_command))
  dp.add_handler(CommandHandler("A", A_command))
  dp.add_handler(CommandHandler("B", B_command))
  dp.add_handler(CommandHandler("C", C_command))
  #dp.add_handler(CommandHandler("echo", echo))
  dp.add_handler(CommandHandler("pedidos", pedidos_command))
  dp.add_handler(CommandHandler("almoco", almoco_command))
  #dp.add_handler(MessageHandler(Filters.text, handle_message))
  dp.add_handler(MessageHandler(Filters.command, unknown))
  updater.start_polling()
  updater.idle()

#main()
'''
teste()