elif prato_entrada_use == prato_qua_n_1:
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
  elif prato_entrada_use == prato_qua_n_2:
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



#########################################################################33
elif prato_entrada_use == prato_qua_n_1:
    valor_celu = int(val_cell('C4').value)
    val1 = (valor_celu - 1)
    if dia_semana == 2:
      if valor_celu == 0:
        update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nEsse prato não está mais disponível.")
      else:
        worksheet.update_acell("A{}".format(next_row), update.message.from_user['first_name'])
        worksheet.update_acell("B{}".format(next_row), update.message.from_user['last_name'])
        worksheet.update_acell("C{}".format(next_row), prato_entrada_use)

        sh.worksheet("Almoco").update('C4', val1)
        update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nSeu pedido está sendo preparado.")
    elif dia_semana != 2:
              update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\n Esse prato não está disponivel nesse cardápio.""\n Recomedamos que revise o cardapio diario no /almoco")

  elif prato_entrada_use == prato_qua_n_2:
    valor_celu = int(val_cell('E4').value)
    val1 = (valor_celu - 1)
    if dia_semana == 2:
      if valor_celu == 0:
        update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nEsse prato não está mais disponível.")
      else:
        worksheet.update_acell("A{}".format(next_row), update.message.from_user['first_name'])
        worksheet.update_acell("B{}".format(next_row), update.message.from_user['last_name'])
        worksheet.update_acell("C{}".format(next_row), prato_entrada_use)
        sh.worksheet("Almoco").update('E4', val1)
        update.message.reply_text(f"Olá {update.message.from_user['first_name']}.""\nSeu pedido está sendo preparado.")
