# first function in algorithm , start conversation to bot.
def start(message):
#get  id and nickname of user
    name = message.from_user.username
    user_id = message.from_user.id
    print(message.from_user )
    print("nickname:" , name)
    print("id" , user_id)
    bot.send_message(message.from_user.id , text="Здравствуйте, благодарим за обращение.Мы намерены как можно скорее разобраться в вашем вопросе.Для этого, пожалуйста, предоставьте несколько уточнений:")
    keyboard = types.InlineKeyboardMarkup() 
    key_indigrient_one = types.InlineKeyboardButton(text='Wildberries' , callback_data='get_wildberries')
    keyboard.add(key_indigrient_one)
    key_indigrient_two = types.InlineKeyboardButton(text='Ozon' , callback_data='get_ozon')
    keyboard.add(key_indigrient_two)
    key_indigrient_three = types.InlineKeyboardButton(text='KazanExpress' , callback_data='get_kazanexpress')
    keyboard.add(key_indigrient_three)
    bot.send_message(message.from_user.id , text="Где вы оформляли заказ?" , reply_markup=keyboard)