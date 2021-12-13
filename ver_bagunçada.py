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
#import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from threading import Timer
from pytz import timezone


data_e_hor_serv = datetime.now()
fuso_horario = timezone('America/Sao_Paulo')
data_e_hor_fuso = data_e_hor_serv.astimezone(fuso_horario)
print(data_e_hor_fuso.strftime('%H:%M:%S'))

t = time.localtime()
#Alvorada = t.tm_wday

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

#Comando do botão 'Start' da tela inicial.
def start_command(update,context):
  update.message.reply_text(f"Seja bem vindo(a) {update.message.from_user['first_name']}.""\n Esses são os principais comandos que possa vir a desejar:""\n/comandos; \n/menu; \n/almoco; \n/ajuda")
  

#Comando de help do bot, lista os comandos.
def comandos_command(update, context):
  update.message.reply_text(f"Olá, {update.message.from_user['first_name']}.""\n Essa é alista de comandos que eu reconheço:""\n /start - Poderá rever as boas vindas;""\n /comandos - Lista todos os comandos que reconheço;""\n /menu - Ainda em fase de implementação;""\n /almoco - Disponibiliza os comandos para os almoços diários;\n /sobre - Trago informações sobre meus criadores;""\n /campus - Site oficial do Campus - Jacobina;\n /ajuda - Disponibiliza um link para um vídeo que ensina o passo-a-passo sobre como utilizar o bot.")

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
  #Filtrar o nome das colunas ('doce', 'salgados', etc)
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


dia_semana = t.tm_wday


def almoco_command(update,context):
  goiaba = pd.DataFrame(sh.worksheet("Almoco").get_all_records())
  goiaba.set_index("id", inplace = True)

  if dia_semana == 0:
    f = goiaba.loc[goiaba['Dia'] == 'Segunda']
    a = f.iloc[:, 0:2] 
  elif dia_semana == 1:
    f = goiaba.loc[goiaba['Dia'] == 'Terça']
    a = f.iloc[:, 0:2] 
  elif dia_semana == 2:
    f = goiaba.loc[goiaba['Dia'] == 'Quarta']
    a = f.iloc[:, 0:2] 
  elif dia_semana == 3:
    f = goiaba.loc[goiaba['Dia'] == 'Quinta']
    a = f.iloc[:, 0:2] 
  elif dia_semana == 4:
    f = goiaba.loc[goiaba['Dia'] == 'Sexta']
    a = f.iloc[:, 0:2] 
  else:
    #pass
    update.message.reply_text(f"  Olá {update.message.from_user['first_name']}.""\n \n A cantina não disponibiliza seus serviços durante os fins de semana. \n \n Por favor aguarde o próximo dia útil.")
  update.message.reply_text("Os pratos do dia são: \n{}".format(a))

def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)

def pedidos_command(update, context):
  df = pd.DataFrame(sh.worksheet("Pedidos").get_all_records())
  df.set_index("id", inplace = True)

  pedidos_list = df.iloc[:, 0:3] 
  quant_fichas = df.loc[1, 'Total']

  print(quant_fichas)
  print(type(quant_fichas))

  #s1 = pedidos_list                           #initializing cell from the excel file mentioned through the cell position
  #print("No. of rows:", s1.nrows)               #Counting & Printing thenumber of rows & columns respectively
  #print("No. of columns:", s1.ncols)

  update.message.reply_text("Os pratos retirados ate o momento são: \n""\n""{}".format(pedidos_list))
  update.message.reply_text("O total de pedidos realizados são: {}".format(quant_fichas))
  #print(pedidos_list['Fichas'] == 'Segunda')
  #print(pedidos_list[0]['Nome'])


def pedido_command(update, context):
  hora_pedido = (data_e_hor_fuso.hour) 
  #print(type(hora_pedido))
  #print(hora_pedido)
  if (hora_pedido >= 7 and hora_pedido <= 15): #Se a hora for maior/igual à 7AM E menor/igual à 15PM (também aceita pedidos até 15:59)
    sh.worksheet("Almoco").acell
    #Pedidos feitos através de número (id) e não por nomes
    #Apenas 3 colunas na worksheet almoço (Dia, Pedidos, Quantidade de fichas por dia)
    #Adicionar "quantidade de fichas total" à worksheeet "Pedido"
    #Horário por datetime+BRT 
    #Pesquisar a worksheet "Almoco" (linha 152) por dataframe e não células.

    df = pd.DataFrame(sh.worksheet("Almoco").get_all_records())
    # transforma id em index do dataframe
    df.set_index("id", inplace = True)

    # pega o id do almoço que o usuário quer
    #update.message.reply_text("Informe o almoço que deseja: ")
    k = update.message.text.split(" ")[1]
    # transforma o k (string) em integer
    J = int(k)

    prato_entrada_use = df.loc[J, 'Almoco']
    #print(type(prato_entrada_use))
    va_ce = df.loc[J, 'Fichas']
    valor_celu = int(va_ce)
    #print(type(valor_celu))
    #print(valor_celu)

    worksheet = sh.worksheet("Pedidos")
    next_row = next_available_row(worksheet)
    
   #print(dia_semana)
    
    if dia_semana == 0:
      # pega apenas as linhas onde o valor em Dia é Segunda
      df.loc[df['Dia'] == 'Segunda']
      if valor_celu == 0:
        update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nEsse prato não está mais disponível.")
      else:
        worksheet.update_acell("B{}".format(next_row), update.message.from_user['first_name'])
        worksheet.update_acell("C{}".format(next_row), update.message.from_user['last_name'])
        worksheet.update_acell("D{}".format(next_row), prato_entrada_use)

        #diminui 1 na ficha do index informado
        df.loc[J, 'Fichas'] -= 1
        update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nSeu pedido está sendo preparado.")

      #reseta o index para a coluna id voltar a ser coluna da planilha
      df.reset_index(inplace=True)
      #atualiza a planilha inteira com o df atualizado
      sh.worksheet("Almoco").update([df.columns.values.tolist()] + df.values.tolist())

    elif dia_semana == 1:
      df.loc[df['Dia'] == 'Terça']
      if valor_celu == 0:
        update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nEsse prato não está mais disponível.")
      else:
        worksheet.update_acell("B{}".format(next_row), update.message.from_user['first_name'])
        worksheet.update_acell("C{}".format(next_row), update.message.from_user['last_name'])
        worksheet.update_acell("D{}".format(next_row), prato_entrada_use)

        df.loc[J, 'Fichas'] -= 1

        update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nSeu pedido está sendo preparado.")

      df.reset_index(inplace=True)
      sh.worksheet("Almoco").update([df.columns.values.tolist()] + df.values.tolist())

    elif dia_semana == 2:
      df.loc[df['Dia'] == 'Quarta']
      if valor_celu == 0:
        update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nEsse prato não está mais disponível.")
      else:
        worksheet.update_acell("B{}".format(next_row), update.message.from_user['first_name'])
        worksheet.update_acell("C{}".format(next_row), update.message.from_user['last_name'])
        worksheet.update_acell("D{}".format(next_row), prato_entrada_use)

        df.loc[J, 'Fichas'] -= 1

        update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nSeu pedido está sendo preparado.")

      df.reset_index(inplace=True)
      sh.worksheet("Almoco").update([df.columns.values.tolist()] + df.values.tolist())
      
    elif dia_semana == 3:
      df.loc[df['Dia'] == 'Quinta']
      if valor_celu == 0:
        update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nEsse prato não está mais disponível.")
      else:
        worksheet.update_acell("B{}".format(next_row), update.message.from_user['first_name'])
        worksheet.update_acell("C{}".format(next_row), update.message.from_user['last_name'])
        worksheet.update_acell("D{}".format(next_row), prato_entrada_use)

        df.loc[J, 'Fichas'] -= 1

        update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nSeu pedido está sendo preparado.")

      df.reset_index(inplace=True)
      sh.worksheet("Almoco").update([df.columns.values.tolist()] + df.values.tolist())

    elif dia_semana == 4:
      df.loc[df['Dia'] == 'Sexta']
      if valor_celu == 0:
        update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nEsse prato não está mais disponível.")
      else:
        worksheet.update_acell("B{}".format(next_row), update.message.from_user['first_name'])
        worksheet.update_acell("C{}".format(next_row), update.message.from_user['last_name'])
        worksheet.update_acell("D{}".format(next_row), prato_entrada_use)

        df.loc[J, 'Fichas'] -= 1

        update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nSeu pedido está sendo preparado.")

      df.reset_index(inplace=True)
      sh.worksheet("Almoco").update([df.columns.values.tolist()] + df.values.tolist())
    
    else:
       update.message.reply_text(f"  Olá {update.message.from_user['first_name']}.""\n \n A cantina não disponibiliza seus serviços durante os fins de semana. \n \n Por favor aguarde o próximo dia útil.")
       
       #update.message.reply_text(f"  Olá {update.message.from_user['first_name']}.""\n \n Esse prato não faz parte do cardápio atual.\n \n Consulte o cardápio atualizado em /almoco.")
       #update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\n Não conhecemos esse prato.")
  # bot.copy_message(chat_id=chat_id, from_chat_id=update.effective_message.chat_id, message_id=update.effective_message.message_id,*args,**kwargs)
  else: #Se a hora for menor que 7AM ou maior que 15:59PM.
    update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nA cantina ainda não disponibilizou a retirada de fichas.")
              #Fazer um if de horário fora de funções
    sh.values_clear("'YTD'!A2:C2")

   #df.loc[dia = tal]... Df.loc['fichas' ] == 10 
    sh.worksheet("Almoco").update('D2', 10) 
    sh.worksheet("Almoco").update('D3', 10)


def fegws(update, context):
  update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nA cantina ainda não disponibilizou a retirada de fichas.")
              #Fazer um if de horário fora de funções
  sh.values_clear("'YTD'!A2:C2")

  
  sh.worksheet("Almoco").update('D2', 10) 
  sh.worksheet("Almoco").update('D3', 10)

def error(update, context):
    print(f"Update: {update} caused error: {context.error}")

#Função Teste para manipulação da planilha
def teste(update, context):
  df = pd.DataFrame(sh.worksheet("Almoco").get_all_records())
  # transforma id em index do dataframe
  df.set_index("id", inplace = True) 
  # pega apenas as linhas onde o valor em Dia é Segunda
  data = df.loc[df['Dia'] == 'Segunda'] 
  # itera por cada linha de data, permitindo pegar os valores correspondente a cada coluna
  for index, linha in data.iterrows():
     update.message.reply_text(f"{index} - {linha['Almoco']} - {linha['Fichas']} fichas")
  # pega o id do almoço que o usuário quer
  #i = int(input("Informe o almoço que deseja: "))
  update.message.reply_text("Informe o almoço que deseja: ")
  k = update.message.text.split(" ")[1]
  print(type(k))
  print(k)

  #strings= [int(string) for string in k]
 # a_string = "". join(strings)
  #an_integer = int(a_string)
  #oi = float(an_integer)
  #print(an_integer)
                    
  #s = [int(i) for i in k] # Converting integers into strings

  #result = int(.join(s)) # Join the string values into one string

  #k = int(map(int, k))    
  #print(type(an_integer))
  
  J = int(k) 
  print(type(J))

# if i = 1/2 não é necessário nesse caso
  
  #diminui 1 na ficha do index informado
  df.loc[J, 'Fichas'] -= 1 
  #reseta o index para a coluna id voltar a ser coluna da planilha
  df.reset_index(inplace=True)
  #atualiza a planilha inteira com o df atualizado
  sh.worksheet("Almoco").update([df.columns.values.tolist()] + df.values.tolist())

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
  dp.add_handler(CommandHandler("teste", teste))

  #dp.add_handler(CommandHandler("echo", echo))
  dp.add_handler(CommandHandler("pedidos", pedidos_command))
  dp.add_handler(CommandHandler("almoco", almoco_command))
  #dp.add_handler(MessageHandler(Filters.text, handle_message))
  dp.add_handler(MessageHandler(Filters.command, unknown))
  updater.start_polling()
  updater.idle()

main()

