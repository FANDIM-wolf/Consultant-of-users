#   Telegram bot algorithm for collecting data about damaged goods
#   Author: Mikhail Shishov  
#   Email:fandimfromitaly@yandex.ru
#   last time edited : 26.02.2022
import telebot;
from telebot import types
import psycopg2
from psycopg2 import Error, connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sqlite3 
import datetime
import random

files = []

#init token 
bot = telebot.TeleBot('your_token')
brand = " "
token = '5235250024:AAFn1MHDZy31aF9izO7U74trm1roqB_5NLg'
brands = ["get_teneleven" , "get_joe_lo", "get_jasson_lo","get_topface" ,"get_miss_tais" , "get_fabio" , "get_belucci" , "get_elitario"]
reasons = ["delay_and_damaged_box" , "not_base_function" , "base_function" ,"color_or_description"]
#get random ideficator 
def get_uniqe_id():
    id = 0
    id = random.randint(10,92323453)
    return id   


name = " "
user_id  = 0
photo = " "
marketplace = " "
category = " "
brand = " "
photo = " "
permission_to_send_photo = False 

#base 
def write_data_about_user_to_db(name,user_id,marketplace , category , brand , photo , date):
    
    

    #firstly set connection to database 
    try:
    # Connection to current database
        connection = psycopg2.connect(user="postgres",
                                  password="elkin",
                                  host="127.0.0.1",
                                  port="5432")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # cursor is tool for working with Data Base
        cursor = connection.cursor()
        
        insert_query = """INSERT INTO damaged_goods (id,user_id,user_name ,market_place , category , brand , photo , date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) """
        pk = get_uniqe_id() # get random indeficator for row in data base 
        item_object = (pk,int(user_id),str(name),str(marketplace), str(category), str(brand) , str(photo) , str(date))
        cursor.execute(insert_query,item_object)
        connection.commit()
        
        
        #cursor.execute("SELECT * FROM recipes_of_cakes")
        #for row in cursor:
            #cake = Cake()
            #cake.name = row[1]
            #cake.recipe = row[2]
            #cake.key_words = row[3]
            #cake.power_for_process = 0
            #cake.photo_name = row[5]
            #list_of_cakes.append(cake)
            #list_of_key_words.append(cake.key_words)
        #print(list_of_cakes)
        #print(list_of_key_words)
        
        #walk through all array key words and get any key_word
        #for el in list_of_cakes:
        #    for subject in el.key_words:
        #        print(subject)

        connection.commit()
        
        print("Connection to DataBase : Successfully")
        
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

#get all data from db
#get_data_from_data_base()



@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    # user get permissin in certain conditions : if current hour more than 9 pm and less than  6am , and yet he passed three stages
        global date , name , user_id  
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'files/' + file_info.file_path
        print(file_info.file_path)
        files.append(file_info.file_path)
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        bot.reply_to(message, "Пожалуй, я сохраню это")
        photo = file_info.file_path #get name of photo
        date = datetime.datetime.now()
        print("name:", message.from_user.username,"user_id:" , message.from_user.id,"market_place:",marketplace ,"category:",category ,"brand:",brand ,"photo:",photo ,"date:" , date)
        write_data_about_user_to_db(str(message.from_user.username),int(message.from_user.id), str(marketplace) , str(category) , str(brand) , str(photo) , str(date))
        
#start function to start conversation with bot
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == "/start":
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
    if message.text == "/send_photos":
        for i in range(len(files)):
            photo=open('files/'+files[i] , 'rb')
            bot.send_photo(message.from_user.id , photo)

def get_category(call):
    keyboard = types.InlineKeyboardMarkup() 
    key_indigrient_one = types.InlineKeyboardButton(text='Одежда ' , callback_data='get_clothes')
    keyboard.add(key_indigrient_one)
    key_indigrient_two = types.InlineKeyboardButton(text='Косметика' , callback_data='get_cosmetics')
    keyboard.add(key_indigrient_two)
    key_indigrient_three = types.InlineKeyboardButton(text='Музыкальные инструменты' , callback_data='get_musican')
    keyboard.add(key_indigrient_three)
    bot.send_message(call.from_user.id , text="Выберите категорию, к которой относится ваш товар:" , reply_markup=keyboard)
def get_brand(call ,brand ):
    if brand == "get_clothes":
        keyboard = types.InlineKeyboardMarkup() 
        key_indigrient_one = types.InlineKeyboardButton(text='Teneleven ' , callback_data='get_teneleven')
        keyboard.add(key_indigrient_one)
        key_indigrient_two = types.InlineKeyboardButton(text='Joe lo' , callback_data='get_joe_lo')
        keyboard.add(key_indigrient_two)
        key_indigrient_three = types.InlineKeyboardButton(text='Jasson lo' , callback_data='get_jasson_lo')
        keyboard.add(key_indigrient_three)
        bot.send_message(call.from_user.id , text="Выберите категорию, к которой относится ваш товар:" , reply_markup=keyboard)
    if brand == "get_cosmetics":
        keyboard = types.InlineKeyboardMarkup() 
        key_indigrient_one = types.InlineKeyboardButton(text='Topface ' , callback_data='get_topface')
        keyboard.add(key_indigrient_one)
        key_indigrient_two = types.InlineKeyboardButton(text='Miss Tais' , callback_data='get_misstais')
        keyboard.add(key_indigrient_two)
        bot.send_message(call.from_user.id , text="Выберите категорию, к которой относится ваш товар:" , reply_markup=keyboard)
    if brand == "get_musican":
        keyboard = types.InlineKeyboardMarkup() 
        key_indigrient_one = types.InlineKeyboardButton(text='Fabio' , callback_data='get_fabio')
        keyboard.add(key_indigrient_one)
        key_indigrient_two = types.InlineKeyboardButton(text='Belucci' , callback_data='get_belucci')
        keyboard.add(key_indigrient_two)
        key_indigrient_three = types.InlineKeyboardButton(text='Elitaro' , callback_data='get_elitaro')
        keyboard.add(key_indigrient_three)
        bot.send_message(call.from_user.id , text="Выберите категорию, к которой относится ваш товар:" , reply_markup=keyboard)
#display menu where user can choose reason his dissatisfaction
def choose_reason(call):
    keyboard = types.InlineKeyboardMarkup() 
    key_indigrient_one = types.InlineKeyboardButton(text='- Задержка доставки - Поврежденная упаковка' , callback_data='delay_and_damaged_box')
    keyboard.add(key_indigrient_one)
    key_indigrient_two = types.InlineKeyboardButton(text='Дефект не влияющй на основную функцию продукта ' , callback_data='not_base_function')
    keyboard.add(key_indigrient_two)
    key_indigrient_three = types.InlineKeyboardButton(text='Дефект делающий использование продукта невозможным' , callback_data='base_function')
    keyboard.add(key_indigrient_three)
    key_indigrient_fourth = types.InlineKeyboardButton(text='Несоответствие цвета/описания' , callback_data='color_or_description')
    keyboard.add(key_indigrient_fourth)
    key_indigrient_fith = types.InlineKeyboardButton(text='Что-то другое...' , callback_data='something_other')
    keyboard.add(key_indigrient_fith)
    bot.send_message(call.from_user.id , text="Выберите из перечня причину инцидента:" , reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call:True)
def callback_handler(call):
    global brand , photo , category , marketplace
    if call.data == "get_wildberries":
        get_category(call)
        marketplace = "wilberries"
    if call.data == "get_ozon":
        marketplcae = "ozon"
        get_category(call)
    if call.data == "get_kazanexpress":
        marketplace = "kazanexpress"
        get_category(call)
    if call.data == "get_clothes":
        category = "одежда"
        brand = call.data 
        get_brand(call , brand)
    if call.data == "get_cosmetics":
        category = "косметика"
        brand = call.data
        get_brand(call , brand)
    if call.data == "get_musican":
        category = "музыка"
        brand = call.data
        get_brand(call , brand) 
    if call.data in brands:
        brand = call.data
        print(call.data)
        choose_reason(call)
    if call.data in reasons:
        permission_to_send_photo = True
        bot.send_message(call.message.chat.id , "Пожалуйста, приложите фотографии, где будет виден дефект и опишите его. Так же, не забудьте указать номер вашего заказа.В ближайшее время с вами свяжется наш сотрудник и поможет в решении сложившейся ситуации. ")
           
#start bot 
bot.polling(none_stop=True , interval=0)        
