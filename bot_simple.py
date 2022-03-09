#   Telegram bot algorithm for collecting data about damaged goods
#   Author: Mikhail Shishov  
#   Email:fandimfromitaly@yandex.ru
#   last time edited : 5.03.2022
import telebot;
from telebot import types
import psycopg2
from psycopg2 import Error, connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sqlite3 
import datetime
import random
import time
from start_component import *
files = []

#init token 
bot = telebot.TeleBot('5156581426:AAFZuke4ELUG41V0dPGrpngz8wOAVm763tc')
brand = " "

brands = ["get_teneleven" , "get_joe_lo", "get_jasson_lo","get_topface" ,"get_misstais" , "get_fabio" , "get_belucci" , "elitario"]
reasons = [ "not_base_function" , "base_function" ,"color_or_description"]
#get random ideficator 
def get_uniqe_id():
    id = 0
    id = random.randint(10,92323453)
    return id   

answer_about_marketplace_mistake = "Спасибо , что ответили на уточняющие вопросы, теперь мы сможем быстрее помочь вам в решении возникшей проблеме. Также хотим поблагодарить вас за проявленное терпение. Мы, как продавец, отгружаем товар в течение 12 часов после поступления заказа, всё дальнейшее ожидание зависит от скорости логистических процессов маркетплейса. аркетплейса. Встав на вашу сторону, мы прекрасно понимаем, что подобные инциденты неприемлемы поэтому, несмотря на то, что от нас эти процессы не зависят, мы всё же направим запросы в службу поддержки с целью решить ваш вопрос. Нам важно, чтобы у вас остался позитивный опыт, поэтому на следующую покупку дарим вам скидку в размере 10% на весь наш ассортимент."
answer_two = "нт. Я передам эту информацию ответственному сотруднику и он в ближайшее время отправит вам промокод. Будем признательны, если вы поддержите нас отзывом. Надеемся, нам удалось решить возникший инцидент. Если же у вас остались вопросы - нажмите 'МЕНЕДЖЕР'.Если возникли вопросы по другому товару - отправьте 'СТАРТ' Желаем хорошего дня и приятных покупок!"
answer = answer_about_marketplace_mistake + answer_two
answer_for_something_another = "В ближайшее время с вами свяжется наш сотрудник и поможет в решении сложившейся ситуации."

name = " "
user_id  = 0
photo = " "
marketplace = " "
category = " "
brand = " "
photo = " "
permission_to_send_photo = False 
path = " "
promocode = "nope"
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

def send_details_to_menager(name):
    bot.send_message( 1959493547, text="Nickname:@"+name)
    bot.send_message( 1959493547, text="Category:"+category )
    bot.send_message( 1959493547, text="Brand:"+brand )
    bot.send_message( 1959493547, text="Marketplace:"+marketplace )
    print(files)
    for i in range(len(files)):
        bot.send_photo(1959493547, photo=open("files/"+files[i], 'rb'))

    #delete last file in array    
    files.pop()

@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    # user get permissin in certain conditions : if current hour more than 9 pm and less than  6am , and yet he passed three stages
        global date , name , user_id  , path
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'files/' + file_info.file_path
        print(file_info.file_path)
        files.append(file_info.file_path)
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        bot.reply_to(message, "Отправлено менеджеру")
        photo = file_info.file_path #get name of photo
        path = src # current path of photo
        #send details to menager
        #save name of user 
        name = message.from_user.username 
        send_details_to_menager(name)
        #wait 2 seconds and clear array 
        time.sleep(2)
        #files.clear()
        print("Path of current photo: " , path)
        
        date = datetime.datetime.now()
        print("name:", message.from_user.username,"user_id:" , message.from_user.id,"market_place:",marketplace ,"category:",category ,"brand:",brand ,"photo:",photo ,"date:" , date)
        #write_data_about_user_to_db(str(message.from_user.username),int(message.from_user.id), str(marketplace) , str(category) , str(brand) , str(photo) , str(date))
        
#start function to start conversation with bot
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == "/start":
        if len(files) >= 1:
            files.clear()
        global name
        #get  id and nickname of user
        name = message.from_user.username
        user_id = message.from_user.id
        print(message.from_user )
        print("nickname:" , name)
        print("id" , user_id)
        bot.send_message(message.from_user.id , text="Здравствуйте, благодарим за обращение.Мы намерены как можно скорее разобраться в вашем вопросе.Для этого, пожалуйста, предоставьте несколько уточнений:")
        keyboard = types.InlineKeyboardMarkup() 
        key_indigrient_one = types.InlineKeyboardButton(text='Wildberries' , callback_data='wildberries')
        keyboard.add(key_indigrient_one)
        key_indigrient_two = types.InlineKeyboardButton(text='Ozon' , callback_data='ozon')
        keyboard.add(key_indigrient_two)
        key_indigrient_three = types.InlineKeyboardButton(text='KazanExpress' , callback_data='kazanexpress')
        keyboard.add(key_indigrient_three)
        bot.send_message(message.from_user.id , text="Где вы оформляли заказ?" , reply_markup=keyboard)
    if message.text == "/send_all_photos":
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
        bot.send_message(call.from_user.id , text="Выберите бренд, к которой относится ваш товар:" , reply_markup=keyboard)
    if brand == "get_cosmetics":
        keyboard = types.InlineKeyboardMarkup() 
        key_indigrient_one = types.InlineKeyboardButton(text='Topface ' , callback_data='get_topface')
        keyboard.add(key_indigrient_one)
        key_indigrient_two = types.InlineKeyboardButton(text='Miss Tais' , callback_data='get_misstais')
        keyboard.add(key_indigrient_two)
        bot.send_message(call.from_user.id , text="Выберите бренд, к которой относится ваш товар:" , reply_markup=keyboard)
    if brand == "get_musican":
        keyboard = types.InlineKeyboardMarkup() 
        key_indigrient_one = types.InlineKeyboardButton(text='Fabio' , callback_data='get_fabio')
        keyboard.add(key_indigrient_one)
        key_indigrient_two = types.InlineKeyboardButton(text='Belucci' , callback_data='get_belucci')
        keyboard.add(key_indigrient_two)
        key_indigrient_three = types.InlineKeyboardButton(text='Elitaro' , callback_data='elitario')
        keyboard.add(key_indigrient_three)
        bot.send_message(call.from_user.id , text="Выберите бренд, к которой относится ваш товар:" , reply_markup=keyboard)
#display menu where user can choose reason his dissatisfaction
def choose_reason(call):
    
    keyboard = types.InlineKeyboardMarkup()
     
    key_indigrient_one = types.InlineKeyboardButton(text='- Задержка доставки ' , callback_data='mistake_of_marketplace')
    keyboard.add(key_indigrient_one)
    key_indigrient_two = types.InlineKeyboardButton(text='- Поврежденная упаковка ' , callback_data='mistake_of_marketplace')
    keyboard.add(key_indigrient_two)
    key_indigrient_three = types.InlineKeyboardButton(text='Дефект делающий использование продукта невозможным' , callback_data='base_function')
    keyboard.add(key_indigrient_three)
    key_indigrient_fourth = types.InlineKeyboardButton(text='Дефект, не влияющий на основную функцию продукта' , callback_data='not_base_function')
    keyboard.add(key_indigrient_fourth)
    key_indigrient_fith = types.InlineKeyboardButton(text='-Несоответствие цвета/описания' , callback_data='color_or_description')
    keyboard.add(key_indigrient_fith)
    key_indigrient_six = types.InlineKeyboardButton(text='Что-то другое' , callback_data='something_other')
    keyboard.add(key_indigrient_six)
    bot.send_message(call.from_user.id , text="Выберите из перечня причину инцидента:" , reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call:True)
def callback_handler(call):
    global brand , photo , category , marketplace ,promocode
    if call.data == "wildberries":
        time.sleep(5)
        get_category(call)
        marketplace = call.data
    if call.data == "ozon":
   
        get_category(call)
        marketplace = call.data
    if call.data == "kazanexpress":
       
        get_category(call)
        marketplace = call.data
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
    if call.data == "mistake_of_marketplace":
        bot.send_message(call.message.chat.id , answer )
        keyboard = types.InlineKeyboardMarkup() 
        key_indigrient_one = types.InlineKeyboardButton(text='МЕНЕДЖЕР' , callback_data='MENAGER')
        keyboard.add(key_indigrient_one)
        key_indigrient_two = types.InlineKeyboardButton(text='СТАРТ' , callback_data='START')
        keyboard.add(key_indigrient_two)
        key_indigrient_two = types.InlineKeyboardButton(text='ПРОМОКОД' , callback_data='PROMOCODE')
        keyboard.add(key_indigrient_two)
        bot.send_message(call.from_user.id , text="Выберете действие" , reply_markup=keyboard)
    if call.data == "START":
        print("start")
        bot.send_message(call.from_user.id , text="Нажмите /start" )
    if call.data == "MENAGER":
        bot.send_message(1959493547 , text="Клиенту нужна помошь" )
        bot.send_message(1959493547 , text="PROMOCODE:"+promocode )
        bot.send_message(call.message.chat.id, text="Отправлено менеджеру" )
        print("menager")
    if call.data == "PROMOCODE":
        promocode = "yep"
        bot.send_message(1959493547 , text="Клиенту нужна помошь" )
        bot.send_message(1959493547, text="PROMOCODE:"+promocode )
        bot.send_message(call.message.chat.id ,text="Отправлено менеджеру" )
        print("menager")
    if call.data == "something_other":
        global answer_for_something_another 
        bot.send_message(1959493547 , text="Клиенту нужна помошь" )
        bot.send_message(1959493547 , text=name )
        #bot.send_message(call.message.chat.id , text=name )
        bot.send_message(call.message.chat.id ,text=answer_for_something_another)
        print("username:",name)
        
    if call.data == "delay_and_damaged_box":

        
        bot.send_message(call.message.chat.id , answer )
        keyboard = types.InlineKeyboardMarkup() 
        key_indigrient_one = types.InlineKeyboardButton(text='МЕНЕДЖЕР' , callback_data='MENAGER')
        keyboard.add(key_indigrient_one)
        key_indigrient_two = types.InlineKeyboardButton(text='СТАРТ' , callback_data='START')
        keyboard.add(key_indigrient_two)
        key_indigrient_two = types.InlineKeyboardButton(text='ПРОМОКОД' , callback_data='PROMOCODE')
        keyboard.add(key_indigrient_two)
        bot.send_message(call.from_user.id , text="Выберете действие" , reply_markup=keyboard)
        

#start bot 
bot.polling(none_stop=True , interval=0)        