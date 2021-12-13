#Importação de pacotes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import *
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import logging
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import os
import pandas as pd
import functools
from datetime import datetime
from pytz import timezone

#Definição do horário
data_e_hor_serv = datetime.now()
fuso_horario = timezone('America/Sao_Paulo')
data_e_hor_fuso = data_e_hor_serv.astimezone(fuso_horario)
hora_pedido = (data_e_hor_fuso.hour)

#Definição do dia da semana
#Retorna um valor decimal que representa o dia da semana. Começa em 0 e vai até 6, sendo 0: domingo e 6: sábado.
dia_semana = int(datetime.today().strftime('%w'))

#Informando os dados de acesso ao bot
token = '1962960347:AAHxxhnb26z0Xy6hUVx47pVfEJlkhDCF8nw'
credentials = {
    "type":
    "service_account",
    "project_id":
    "botplanilhatest",
    "private_key_id":
    "1fc9cdf3836780ae3ffcb32caa769ccf758221c2",
    "private_key":
    "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCegs2M9PNMxlTX\nskwKiD8JwFb2gRJTQlDva1+QfxUnKxo6i7c96QejoV6GIM8wwK2y+KSMqFoj610D\n6KTap3n6mHRcDcC5dXaFDs9BW1nggpvJpdysJ2P1tJxCz6fXwl0KqMwf4SVz9SIw\ndgqPIpBYdyl41+y1SoBRAJ+J6u3Utvd0ijvxbw826EQJRY3WSF3nC4pu41t8IPBy\nNBsGMjoyHauysd6OtqQQRKRGkZin+HrZyw/UogYQWBC0JxqLW1Ad9J1L13F7hO0T\nf7aqx04ka8scE90+y/HOsQFLCue/YmUZ1Xi0W6R383iXcPlN/NhIRGKPgpjKofvz\n1OPCNGAbAgMBAAECggEALuCFFIIeb96Zmb6PcW/woJwiu7zZJAlRMTUCapPCuDYt\niBHoq6T+Ttx6vVT3oTXiSLLyyuxA2C2TcQP8uPNdhghPJSgmDlLYLap/DZeMAXLu\nyphEJh9yFuiGa9XIj+zZojzgPS9S6bOdnFJUdhclNBxtheDpjoXNY+c4x0tUcZsB\nc507A7YKqQTpjJ+b7DYLvy/2doaX7UXq1KZVaQCbB6WPblpUpgj6Wa9+zqaU4WUU\noTACT6UAOUEJY9yT6NDs1Xplwgcr16nZzBP0F52XS1TifAOcqET33n5sV5/mXIeq\nmQV3IOtFwVEXawg4bXI16K237qRBEU9rP3otGS/oOQKBgQDMUCTd9B17+/l9+Bdw\npXJ2OHNnCtCKXYVpo5Tk+08Q7W2VKHwgJIRLWLaCbmbngEt4LoiZBQByLGQFg4VH\nNtjSVi1zBg3gdfT+y4S1lQD+E2cF0hWNTdzvWYR8JqtBZsvpkyFLkDBabkLte+b2\nCuLeyFhBpIvzrduMQjZcb3CyKQKBgQDGnGR8sYIE1eFdvwIVPdwKeFTENff1RCyq\noKrflrE00ohNmAyIigwW+D03mnpiidkqgI+4cSI1y+kSec0G3vg/3fBR0duIHxQV\nAmUbC58cd/aN3hyoDnJA9fB/EMhC1Zepuhjef+PZUMlHngRleLTLA5HNDW9jMCVC\nWApXfZlwowKBgF6IWnaDw7yhGpAJYTcSpgJDHko3+8N5gAgf0v2btbqcUI6qG7x3\niOqf0lpJIL3OY5zo0vUSFmG9Xk4ay2jm3K19iCvnSjZn/YKCwhWOKtZkPc+4o5Ys\nx6PLJHyZG7X4DTM2izo+LdE5oSfmozeGU/BGfGdq7gJCmAmufR6JxXf5AoGAbbRl\nLRs/njwlyAqBtAn/SSk+aUMGO8v0gCtPN0GdkHfaIkIiaikWlHl6FwSVJWjPM9Lf\nkBmts9l2XGY7AdiXd2+4Fvm8MWw5Q4GXJ2E7+hWpcqOFYK7aHVe8B/PVKlWg+Hd6\n1Sv/R0KAa7a05vfNpXXLS2Bobnlhm0vWKo2N+9ECgYA0CDZRVwhjEi+rxp2GxYMp\ncTQ0aqOdbGzyGL3qo4Vs/iCcZe83bNRc7ndqv8m/lAUs/IY+IDvTAJF6KjF+29pU\nGDoDFXiEGTDliaj7tRjx3UZ8xNbOfjjR0GkG/wqPHAxqRPZqbcrrPNFWCw1z79l0\naMuuK9ryORSmpC1vnPmX2w==\n-----END PRIVATE KEY-----\n",
    "client_email":
    "botcantinaif@botplanilhatest.iam.gserviceaccount.com",
    "client_id":
    "110394672237536992027",
    "auth_uri":
    "https://accounts.google.com/o/oauth2/auth",
    "token_uri":
    "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url":
    "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url":
    "https://www.googleapis.com/robot/v1/metadata/x509/botcantinaif%40botplanilhatest.iam.gserviceaccount.com"
}

updater = Updater(token)


#Acessando a planilha do google
gc = gspread.service_account_from_dict(credentials)
sh = gc.open("CantinaTest")

#Acessando worksheets específicas da planilha:
#Pega todos os dados da worksheet 1 (Menu)
dados_menu = pd.DataFrame(sh.worksheet("Menu").get_all_records())
#Pega todos os dados da worksheet 2 (Almoço)
dados_almoco = pd.DataFrame(sh.worksheet("Almoco").get_all_records())
#Pega todos os dados da worksheet 3 (Pedidos)
#dados_pedidos = pd.DataFrame(sh.worksheet("Pedidos").get_all_records())

#Código que formata a saída das informações (texto ajustado para a esquerda e justificado)
Colunas_float = ('Floats', )
Colunas_bool = ('Booleans', )


def left_justified(texto):
    formatters = {}

    for li in list(texto.columns):
        if li in Colunas_float:
            form = "{{!s:<5}}".format()
        elif li in Colunas_bool:
            form = "{{!s:<8}}".format()
        else:
            max = texto[li].str.len().max()
            form = "{{:<{}s}}".format(max)
        formatters[li] = functools.partial(str.format, form)
    return texto.to_string(formatters=formatters, index=False)


#Quando o bot não reconhece algum comando.
def unknown(update, context):
    response_message = "Desculpa, não conheço esse comando." "\n Qualquer dúvida consulte o /ajuda"
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=response_message)


#Para eventuais erros no código
def error(update, context):
    print(f"Update: {update} caused error: {context.error}")


#Para adicionar o novo pedido do usuário na próxima linha vazia da worksheet 'Pedidos'
def next_available_row(pedidos):
    #Originalmente o col_values(x) era 1, porém deu erro depois de um tempo funcionando e, segundo a solução que encontrei, deveria incrementar +1
    str_list = list(filter(None, pedidos.col_values(2)))
    return str(len(str_list) + 1)


#Comando '/start'.
def start_command(update, context):
    update.message.reply_text(
        f"Seja bem vindo(a) {update.message.from_user['first_name']}."
        "\nGostaria de checar o almoço do dia? Digite '/almoco'."
        " \nEstá na dúvida em quais são os produtos da cantina? Digite '/menu' para checar entre as categorias."
        " \nBusca solicitar uma ficha de almoço? Digite '/pedido' + o id do almoço do dia."
        " \nDemais comandos podem ser vistos em '/comandos'.")


#Comando de help do bot, lista todos os comandos.
def comandos_command(update, context):
    update.message.reply_text(
        f"Olá, {update.message.from_user['first_name']}."
        "\nEssa é alista de comandos que eu reconheço:"
        "\n /start - Poderá rever as boas vindas;"
        "\n /comandos - Lista todos os comandos que reconheço;"
        "\n /menu - Lista as categorias de alimentos da cantina;"
        "\n /almoco - Mostra os almoços do dia e seus respectivos id's;\n /pedido - Realiza a solicitação de uma ficha de almoço. Deve ser escrito acompanhado do id do almoço que deseja reservar, ex: '/pedido 2';\n /sobre - Trago informações sobre meus criadores;"
        "\n /campus - Disponibiliza o link para o site oficial do IFBA - Campus Jacobina;\n /ajuda - Disponibiliza um link para um vídeo que ensina o passo-a-passo sobre como utilizar o bot."
    )


    #Comando '/sobre'.
def sobre_command(update, context):
    update.message.reply_text(
        f"Este bot e suas propriedades foram desenvolvidos pelo grupo Quack Studios sob orientação da mestra em Ciência da Computação, Rebeca Barros."
        "\nOs membros deste grupo são Matheus Oliveira e Marcella Portela, estudantes do Curso Técnico em Informática na instituição do IFBA - Campus Jacobina."
    )


    #Comando '/campus'.
def campus_command(update, context):
    update.message.reply_text(
        f"Este é o link para o site oficial do Campus Jacobina: "
        "\n https://portal.ifba.edu.br/jacobina")


    #Comando '/ajuda'.
def ajuda_command(update, context):
    update.message.reply_text(
        f"Este é o link do vídeo que demonstra o passo-a-passo de como utilizar o bot, indicado para iniciantes: "
        "\n (link)")  #A inserir


    #Comando '/menu'
def menu_command(update, context):
    update.message.reply_text(
        "Bem vindo ao cardápio da cantina! Digite a categoria do alimento que gostaria de consultar:\n/A - Bebidas\n/B - Salgados\n/C - Doces"
    )


    #Comando '/A', refere à categoria de Bebidas.
def A_command(update, context):
    #Filtra apenas os dados que tem a categoria = bebidas
    categoria = dados_menu.query('Categoria=="Bebidas"')
    #Seleciona todas as colunas menos 'Categoria'
    texto = categoria.loc[:, categoria.columns != 'Categoria']
    update.message.reply_text("As bebidas são: \n{}".format(
        left_justified(texto)))


    #Comando '/B', refere à categoria de Salgados.
def B_command(update, context):
    #Filtra apenas os dados que tem a categoria = salgados
    categoria = dados_menu.query('Categoria=="Salgados"')
    #Seleciona todas as colunas menos 'Categoria'
    texto = categoria.loc[:, categoria.columns != 'Categoria']
    update.message.reply_text("Os salgados são: \n{}".format(
        left_justified(texto)))


    #Comando '/C', refere à categoria de Sobremesas.
def C_command(update, context):
    #Filtra apenas os dados que tem a categoria = doces
    categoria = dados_menu.query('Categoria=="Doces"')
    #Seleciona todas as colunas menos 'Categoria'
    texto = categoria.loc[:, categoria.columns != 'Categoria']
    update.message.reply_text("Os doces são: \n{}".format(
        left_justified(texto)))




def botao(update, context):
  query = update.callback_query
  query.answer()
  mamao = query.data
  query.edit_message_text(text=f"Opção escolhida: {mamao}")

  #print(type(query.data))
  #print(query.data)
  return mamao




def amora_command(update, context):
  teclado = [
    [
        InlineKeyboardButton("Segunda", callback_data='Segunda'),
        InlineKeyboardButton("Terça", callback_data='Terça'),
    ],
    [
      InlineKeyboardButton("Quarta", callback_data='Quarta'),
      InlineKeyboardButton("Quinta", callback_data='Quinta'),
      InlineKeyboardButton("Sexta", callback_data='Sexta')
      ],
  ]

  reply_markup = InlineKeyboardMarkup(teclado)
  update.message.reply_text("Por favor escolha o dia da semana:", reply_markup=reply_markup)
  botao(update, context)
  print(botao.mamao)

  #baor = (str(update.message.text()))
  #print(baor)

  #print(type(reply_markup))
  #print(reply_markup)

  #botao(update, context)
  #print(botao.mamao)
  #dia_escolhido = botao(update, context, mamao)
  #print(type(dia_escolhido))
  #print(dia_escolhido)
  #if dia_escolhido == "Segunda"






    #Comando '/almoco'
def almoco_command(update, context):
    dados_almoco.set_index("id", inplace=True)

    if dia_semana == 1:
        #Pega apenas os dados em que o dia = segunda
        almoco_dia = dados_almoco.loc[dados_almoco['Dia'] == 'Segunda']
        #Pega apenas as 3 primeiras colunas (exclui 'Fichas')
        col = almoco_dia.iloc[:, 0:2]
    elif dia_semana == 2:
        almoco_dia = dados_almoco.loc[dados_almoco['Dia'] == 'Terça']
        col = almoco_dia.iloc[:, 0:2]
    elif dia_semana == 3:
        almoco_dia = dados_almoco.loc[dados_almoco['Dia'] == 'Quarta']
        col = almoco_dia.iloc[:, 0:2]
    elif dia_semana == 4:
        almoco_dia = dados_almoco.loc[dados_almoco['Dia'] == 'Quinta']
        col = almoco_dia.iloc[:, 0:2]
    elif dia_semana == 5:
        almoco_dia = dados_almoco.loc[dados_almoco['Dia'] == 'Sexta']
        col = almoco_dia.iloc[:, 0:2]
    else:
        update.message.reply_text(
            f"  Olá {update.message.from_user['first_name']}."
            "\n \n A cantina não disponibiliza seus serviços durante os fins de semana. \n \n Por favor aguarde o próximo dia útil."
        )
    update.message.reply_text("Os pratos do dia são: \n{}".format(col))


#Comando '/pedidos'
def pedidos_command(update, context):
  dados_pedidos = pd.DataFrame(sh.worksheet("Pedidos").get_all_records())
  dados_pedidos.set_index("id", inplace=True)

  #Pega apenas as 4 primeiras colunas (exclui 'Total')
  pedidos_lista = dados_pedidos.iloc[:, 0:3]
  #Pega apenas primeira linha da coluna 'Total'
  quant_fichas = dados_pedidos.loc[1, 'Total']

  update.message.reply_text("Os pratos retirados ate o momento são: \n{}".format(pedidos_lista))
  update.message.reply_text("O total de pedidos realizados são: {}".format(quant_fichas))


#A implementar:
#    if int_ID is None:
#update.message.reply_text(f"  Olá {update.message.from_user['first_name']}.""\n \n Parece que você não informou um ID de um dos almoços disponíveis. \n \n Por favor consulte os ID's no comando '/almoco'.")

#Função que altera as planilhas Almoço e Pedidos
def realizar_pedido(dia, id_pedido, nome_usuario, sobrenome_usuario):
    df = get_as_dataframe(sh.worksheet("Almoco"))
    pedidos = get_as_dataframe(sh.worksheet("Pedidos"))
    pratos_dia = df.loc[df['Dia'] == dia, 'id'].values
    if id_pedido in pratos_dia: #checa se o id_pedido informado é válido para o dia da semana
      qtde_fichas = df.loc[(df['id'] == id_pedido), 'Fichas'].item()
      prato = df.loc[(df['id'] == id_pedido), 'Almoco'].item()
      if qtde_fichas == 0:
        return False
      else:
          df.loc[(df['id'] == id_pedido),'Fichas'] -= 1
          pedidos = pedidos.append({'Nome': nome_usuario, 'Sobrenome': sobrenome_usuario, 'Nome do Prato': prato}, ignore_index=True)
          set_with_dataframe(sh.worksheet("Almoco"), df) #atualiza a planilha Almoco com o dataframe atualizado
          set_with_dataframe(sh.worksheet("Pedidos"), pedidos)
          return True
    else:
      return False

#Comando '/pedido' (DEVE ser composto)
def pedido_command(update, context):
    dias = {0:'Domingo', 1: 'Segunda', 2: 'Terça', 3: 'Quarta', 4: 'Quinta', 5: 'Sexta', 6: 'Sábado'}
    nome_usuario = update.message.from_user['first_name']
    sobrenome_usuario = update.message.from_user['last_name']
    try:
        lista = update.message.text.split()
        if (len(lista) <= 1):
            update.message.reply_text(
                f"  Olá {nome_usuario}."
                "\n \nParece que você não informou um ID de um dos almoços disponíveis. \n \nPor favor consulte os ID's no comando '/almoco'.")   
        else:
          id_pedido = int(update.message.text.split()[1])
          print(id_pedido)
          print(type(id_pedido))
          if type(id_pedido) == str:
            update.message.reply_text(f"Olá {nome_usuario}.""\n \n Você não iformou um caractere válido. Os ID's são caracteres numéricos.\n \nPor favor consulte os ID's no comando '/almoco'.")


        
    except (IndexError, ValueError):
        #Lidar com esse except
        update.message.reply_text('Forma de uso: /pedido <id>')
        return



#def reset_fichas():
 # if hora_pedido == 23:
  #  tabela_almoco = get_as_dataframe(sh.worksheet("test_reset"))
   # tabela_almoco.loc[tabela_almoco['Fichas'] != 10, 'Fichas'] = 10
    #set_with_dataframe(sh.worksheet("test_reset"), tabela_almoco)


#Chamada de todos os comandos.
def main():
    #reset_fichas()
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("comandos", comandos_command))
    dp.add_handler(CommandHandler("pedido", pedido_command))
    dp.add_handler(CommandHandler("amora", amora_command))

    dp.add_handler(CallbackQueryHandler(botao))

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


main()
