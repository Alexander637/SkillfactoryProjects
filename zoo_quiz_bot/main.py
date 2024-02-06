import telebot
import config

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start_handler(message: telebot.types.Message):
    user = message.from_user

    text = config.start_text.replace('user_first_name', f'{user.first_name}')

    bot.reply_to(message, text, reply_markup=keyboard_add())


@bot.message_handler(commands=['help'])
def help_handler(message: telebot.types.Message):
    text = config.help_text

    bot.reply_to(message, text, reply_markup=keyboard_add())


@bot.message_handler(commands=['quiz'])
def quiz_handler(message):
    user_id = message.from_user.id
    config.user_answers[user_id] = {"answers": {}, "current_question": 0}
    bot.reply_to(message, f'Викторина началась!')
    send_question(message)


@bot.message_handler(commands=['feedback'])
def handle_feedback_command(message):
    chat_id = message.chat.id
    config.user_feedback[chat_id] = []
    bot.send_message(chat_id, "Введите ваш отзыв:")

    bot.register_next_step_handler(message, handle_feedback_input)


@bot.message_handler(commands=["hide_keyboard"])
def hide_keyboard_handler(message):
    remove_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Клавиатура скрыта.", reply_markup=remove_markup)


def keyboard_add():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    help_button = telebot.types.KeyboardButton("/help")
    quiz_button = telebot.types.KeyboardButton("/quiz")
    feedback_button = telebot.types.KeyboardButton("/feedback")
    remove_button = telebot.types.KeyboardButton("/hide_keyboard")

    markup.add(help_button, quiz_button, feedback_button, remove_button)

    return markup


def handle_feedback_input(message):
    chat_id = message.chat.id
    feedback_text = message.text

    config.user_feedback[chat_id].append(feedback_text)

    bot.send_message(chat_id, "Спасибо за ваш отзыв! Он был успешно записан.")


def send_question(message):
    user_id = message.from_user.id
    current_question_index = config.user_answers[user_id]["current_question"]

    if current_question_index < len(config.questions):
        current_question_key = list(config.questions.keys())[current_question_index]
        question_text = config.questions[current_question_key]
        options = config.answers[current_question_key].values()

        question_message = f"{question_text}\n\nВыберите один из вариантов:\n"
        question_message += "\n".join([f"- {option}" for option in options])

        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

        for option in options:
            markup.add(telebot.types.KeyboardButton(option))

        bot.send_message(user_id, question_message, reply_markup=markup)
    else:
        send_final_answers(user_id, message)


@bot.message_handler(func=lambda message: True)
def handle_answer(message):
    user_id = message.from_user.id
    if user_id in config.user_answers:
        try:
            current_question_index = config.user_answers[user_id]["current_question"]
            current_question_key = list(config.questions.keys())[current_question_index]
            selected_answer = message.text.lower().strip()

            if selected_answer in config.answers[current_question_key].values():
                config.user_answers[user_id]["answers"][current_question_key] = selected_answer
                config.user_answers[user_id]["current_question"] += 1
                send_question(message)

            else:
                bot.send_message(user_id, "Пожалуйста, выберите один из предоставленных вариантов.")

        except IndexError:
            error_index_logic(message, user_id)
    else:
        user_nodata_answers(message, user_id)


def error_index_logic(message, user_id):
    if message.text == "обратится":
        send_final_answers(user_id, message)
        bot.send_message(user_id, f"Обращение отправлено.")
        del config.user_answers[user_id]
    elif message.text == "пройти еще раз":
        del config.user_answers[user_id]
        quiz_handler(message)
    elif message.text == "основные команды":
        del config.user_answers[user_id]
        bot.reply_to(message, 'Предоставляю основные команды.', reply_markup=keyboard_add())
    else:
        del config.user_answers[user_id]
        bot.send_message(user_id, f"Для дополнительной информации используйте команду /help")


def user_nodata_answers(message, user_id):
    if message.text == "пройти еще раз":
        quiz_handler(message)
    elif message.text == "основные команды":
        bot.reply_to(message, 'Предоставляю основные команды.', reply_markup=keyboard_add())
    else:
        bot.send_message(user_id, f"Для дополнительной информации используйте команду /help")


def send_final_answers(user_id, message):
    user_tag = message.from_user.username
    user_answers = config.user_answers[user_id]["answers"].values()
    selected_animal = config.animals.get(tuple(user_answers), "Животное не определено")

    final_message = (f"Подходящее животное: {selected_animal}\n\n{config.animal_description[selected_animal]}\n\n"
                     f"{config.guardianship_program}")
    if selected_animal in config.animal_images:
        image_path = config.animal_images[selected_animal]
        with open(image_path, 'rb') as photo:
            send_message_with_bot_tag(user_id, final_message, photo)
    else:
        send_message_with_bot_tag(user_id, final_message)

    send_result_button = telebot.types.KeyboardButton("обратится")
    restart_quiz_button = telebot.types.KeyboardButton("пройти еще раз")
    main_keyboard = telebot.types.KeyboardButton('основные команды')
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add(send_result_button, restart_quiz_button,
                                                                         main_keyboard)

    if message.text == "обратится":
        bot.send_message(config.WORKER_ID, f'Пользователь @{user_tag} нуждается в консультации!',
                         reply_markup=markup)
    else:
        bot.send_message(user_id, f"Если есть вопросы по итогам викторины, обратитесь к нашим сотрудникам."
                                  f" Они свяжутся с вами в ближайшее время!",
                         reply_markup=markup)


def send_message_with_bot_tag(user_id, message, photo=None):
    message += f'\n\n{config.BOT_TAG}'

    markup = telebot.types.ReplyKeyboardRemove(selective=False)

    if photo:
        bot.send_photo(user_id, photo, caption=message, parse_mode='HTML', reply_markup=markup)
    else:
        bot.send_message(user_id, message, parse_mode='HTML', reply_markup=markup)


bot.polling(none_stop=True)
