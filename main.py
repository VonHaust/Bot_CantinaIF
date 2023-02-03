#Importação de pacotes
from telegram.ext import *
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
token = '#TOKEN_DO_BOT_TELEGRAM'
credentials = {
    #TOKEN_DO_GSPREAD_DA_PLANILHA
}

#Acessando a planilha do google
gc = gspread.service_account_from_dict(credentials)
sh = gc.open("#NOME_DA_PLANILHA")

#Acessando worksheets (páginas) específicas da planilha (variáveis globais):
#Pega todos os dados da worksheet 1 (Menu)
dados_menu = pd.DataFrame(sh.worksheet("#WORKSHEET_MENU").get_all_records())



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

#Comando '/start'.
def start_command(update, context):
    update.message.reply_text(
        f"Seja bem vindo(a) {update.message.from_user['first_name']}."
        "\n \nGostaria de checar o almoço do dia? Digite '/almoco'."
        " \n \nEstá na dúvida em quais são os produtos da cantina? Digite '/menu' para checar entre as categorias."
        " \n \nBusca solicitar uma ficha de almoço? Digite '/pedido' + o id do almoço do dia."
        " \n \nDemais comandos podem ser vistos em '/comandos'.")


#Comando de help do bot, lista todos os comandos.
def comandos_command(update, context):
    update.message.reply_text(
        f"Olá, {update.message.from_user['first_name']}."
        "\nEssa é alista de comandos que eu reconheço:"
        "\n /start - Poderá rever as boas vindas;"
        "\n /comandos - Lista todos os comandos que reconheço;"
        "\n /menu - Lista as categorias de alimentos da cantina;"
        "\n /almoco - Mostra os almoços do dia e seus respectivos id's;"
        "\n /a - Bebidas disponíveis na cantina;" 
        "\n /b - Salgados disponíveis na cantina;" 
        "\n /c - Doces disponíveis na cantina;"
        "\n /pedido - Realiza a solicitação de uma ficha de almoço. Deve ser escrito acompanhado do id do almoço que deseja reservar, ex: '/pedido 2';"
        "\n /pedidos - Retorna uma lista em tempo real de todos os pedidos feitos;"
        "\n /reset - Retorna as fichas aos valores padrões. Limpa a lista de pedidos;"
        "\n /sobre - Trago informações sobre meus criadores;"
        "\n /campus - Disponibiliza o link para o site oficial do IFBA - Campus Jacobina."
    )


    #Comando '/sobre'.
def sobre_command(update, context):
    update.message.reply_text(
        f"Este bot e suas propriedades foram desenvolvidos pelo grupo Quack Studios sob orientação da mestra em Ciência da Computação, Rebeca Barros."
        "\nOs membros desse grupo são Matheus Oliveira e Marcella Portela, estudantes do Curso Técnico em Informática na instituição do IFBA - Campus Jacobina."
    )


    #Comando '/campus'.
def campus_command(update, context):
    update.message.reply_text(
        f"Este é o link para o site oficial do Campus Jacobina: "
        "\n https://portal.ifba.edu.br/jacobina"
    )


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

    #Comando '/almoco'
def almoco_command(update, context):
    #Pega todos os dados da worksheet 2 (Almoço)
    dados_almoco = pd.DataFrame(sh.worksheet("#WORKSHEET_ALMOÇO").get_all_records())

    #Define a coluna "id" como index
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
            "\n \nA cantina não disponibiliza seus serviços durante os fins de semana. \n \nPor favor aguarde o próximo dia útil."
        )

    update.message.reply_text("Os pratos do dia são: \n{}".format(col))


#Comando '/pedidos'
def pedidos_command(update, context):
  dados_pedidos = pd.DataFrame(sh.worksheet("#WORKSHEET_PEDIDOS").get_all_records())

  #Pega apenas as 3 primeiras colunas (exclui 'Total')
  pedidos_lista = dados_pedidos.iloc[:, 0:3]
  #Pega apenas primeira linha da coluna 'Total'
  quant_fichas = dados_pedidos.loc[0, 'Total']

  update.message.reply_text("Os pratos retirados ate o momento são: \n \n{}".format(pedidos_lista))
  update.message.reply_text("O total de pedidos realizados são: {}".format(quant_fichas))


#Função que altera as páginas da planilha (worksheets) Almoço e Pedidos
def realizar_pedido(dia, id_pedido, nome_usuario, sobrenome_usuario):
    df = get_as_dataframe(sh.worksheet("#WORKSHEET_ALMOÇO"))
    pedidos = get_as_dataframe(sh.worksheet("#WORKSHEET_PEDIDOS"))
    pratos_dia = df.loc[df['Dia'] == dia, 'id'].values
    if id_pedido in pratos_dia: #checa se o id_pedido informado é válido para o dia da semana
      qtde_fichas = df.loc[(df['id'] == id_pedido), 'Fichas'].item()
      prato = df.loc[(df['id'] == id_pedido), '#WORKSHEET_ALMOÇO'].item()
      if qtde_fichas == 0:
        return False
      else:
          df.loc[(df['id'] == id_pedido),'Fichas'] -= 1
          pedidos = pedidos.append({'Nome': nome_usuario, 'Sobrenome': sobrenome_usuario, 'Nome do Prato': prato}, ignore_index=True)
          set_with_dataframe(sh.worksheet("#WORKSHEET_ALMOÇO"), df) #atualiza a planilha Almoco com o dataframe atualizado
          set_with_dataframe(sh.worksheet("#WORKSHEET_PEDIDOS"), pedidos)
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
          if dia_semana == 0 or dia_semana == 6:
              update.message.reply_text(f"Olá {nome_usuario}.""\n \n A cantina não disponibiliza seus serviços durante os fins de semana. \n \n Por favor aguarde o próximo dia útil.")
          else:
              #Se a hora for maior/igual à 7AM E menor/igual à 15PM (também aceita pedidos até 15:59)
            if (hora_pedido >= 1 and hora_pedido <= 15): 
              pedido_realizado = realizar_pedido(dias[dia_semana], id_pedido, nome_usuario, sobrenome_usuario)
              if pedido_realizado: #retorna True se o pedido foi realizado
                update.message.reply_text(f"Olá {nome_usuario}.""\nSeu pedido está sendo preparado. Após 30 minutos se dirija à cantina para a retirada.")    
              else:
                update.message.reply_text(f"Olá {nome_usuario}.""\nEsse prato não está mais disponível.")
            else: #Se a hora for menor que 7AM ou maior que 15:59PM
              update.message.reply_text(f"Olá {nome_usuario}.""\nA cantina ainda não disponibilizou a retirada de fichas.")
              
            
        
    except (IndexError, ValueError):
        #Lida com as exceções, ex: se o usuário informar uma letra ou emoji.
        update.message.reply_text(f"Olá {nome_usuario}.""\n \nVocê não iformou um caractere válido. Os ID's são caracteres numéricos.\n \nPor favor consulte os ID's disponíveis no comando '/almoco'.")
        update.message.reply_text('Forma de uso: /pedido <id>')
        return


def reset_fichas(update, context): 
  #Se o horário for antes de 7AM ou depois de 15PM, pega a worksheet almoço (onde ficam o número das fichas) e diminui -1 no total que está lá.
  if (hora_pedido < 12 or hora_pedido > 15):
    tabela_almoco = get_as_dataframe(sh.worksheet("#WORKSHEET_ALMOÇO"))
    #Trava na coluna "Fichas" que é onde estão os números
    tabela_almoco.loc[tabela_almoco['Fichas'] != 10, 'Fichas'] = 10
    #Devolve a worksheet com os valores atualizados
    set_with_dataframe(sh.worksheet("#WORKSHEET_ALMOÇO"), tabela_almoco)

    #Abre a worksheet "Pedidos" e restrutura o tamanho dela para apenas 2 linhas, excluindo todas as outras.
    tabela_pedidos = sh.worksheet("#WORKSHEET_PEDIDOS")
    tabela_pedidos.resize(rows=2)

    update.message.reply_text(f"Os valores das fichas foram resetados e a lista de pedidos zerada.")
  else:
    update.message.reply_text(f"Olá, a cantina está em funcionamento portanto a reiniciação das fichas e a limpeza dos pedidos não está liberada. Aguarde o horário pós-funcionamento.")



#Chamada de todos os comandos.
def main():
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("comandos", comandos_command))
    dp.add_handler(CommandHandler("pedido", pedido_command))
    dp.add_handler(CommandHandler("sobre", sobre_command))
    dp.add_handler(CommandHandler("campus", campus_command))
    dp.add_handler(CommandHandler("menu", menu_command))
    dp.add_handler(CommandHandler("A", A_command))
    dp.add_handler(CommandHandler("B", B_command))
    dp.add_handler(CommandHandler("C", C_command))
    dp.add_handler(CommandHandler("reset", reset_fichas))
    dp.add_handler(CommandHandler("pedidos", pedidos_command))
    dp.add_handler(CommandHandler("almoco", almoco_command))
    
    dp.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    updater.idle()


main()
