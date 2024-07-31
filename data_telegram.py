import telebot
from telebot import types

# Reemplaza con tu token de bot
bot = telebot.TeleBot('BOT_TOKEN')

# Estado de la conversación
user_data = {}

# Falta implementar VERIFICACIÓN y ERRORES

@bot.message_handler(content_types=["text"])
def start_conversation(message):
    markup = types.ForceReply() # Citar los mensajes
    bot.reply_to(message, "¡Hola! ¿Cómo te llamas?", reply_markup=markup)
    user_data[message.from_user.id] = {'stage': 'name'} # message.from_user.id: Este ID es un número entero que identifica de manera única al usuario en la plataforma de Telegram.
    bot.register_next_step_handler(message, handle_name)

def handle_name(message):
    user_data[message.from_user.id]['name'] = message.text
    markup = types.ForceReply() # Citar los mensajes
    bot.reply_to(message, f"Encantado de conocerte, {message.text}! ¿Cuántos años tienes?", reply_markup=markup)
    user_data[message.from_user.id]['stage'] = 'age'
    bot.register_next_step_handler(message, handle_age)

def handle_age(message):
    user_data[message.from_user.id]['age'] = message.text
    name = user_data[message.from_user.id].get('name')
    age = message.text
    markup = types.ForceReply()
    bot.reply_to(message, f"Gracias, {name}. Tienes {age} años. Otra pregunta más, ¿eres hombre o mujer?", reply_markup=markup)
    
    # Crear teclado personalizado con botones
    btn = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, 
        input_field_placeholder="Selecciona tu género",
        resize_keyboard=True # Ajustar el tamaño de los botones
        )
    btn.add(types.KeyboardButton("Hombre"), types.KeyboardButton("Mujer"))
    user_data[message.from_user.id]['stage'] = 'sex'
    bot.send_message(message.chat.id, "Selecciona tu género:", reply_markup=btn)
    bot.register_next_step_handler(message, handle_sex)
    
def handle_sex(message):
    user_data[message.from_user.id]['sex'] = message.text
    name = user_data[message.from_user.id].get('name')
    age = user_data[message.from_user.id].get('age')
    sex = message.text
    markup = types.ReplyKeyboardRemove() # Eliminar botonera Hombre/Mujer
    bot.reply_to(message, f"Gracias, {name}. Tienes {age} años. Y eres {sex}.", reply_markup=markup)
    user_data[message.from_user.id]['stage'] = 'completed'
    bot.register_next_step_handler(message, end_conversation)

def end_conversation(message):
    bot.reply_to(message, "Gracias por hablar conmigo. Si quieres volver a hablar conmigo escribe algo.")
    print(user_data)
    # Falta guardar los datos en un archivo csv o base de datos.
    del user_data[message.from_user.id] # Limpiar la memoria

if __name__ == '__main__':
    bot.polling(none_stop=True)
