import telebot  # Импортируем библиотеку для работы с Telegram API
from telebot import types  # Импортируем типы для создания кнопок и других элементов
import datetime  # Импортируем модуль для работы с датой и временем
import time # Этот модуль используется в основном для задержек. С помощью него можно, программу приостановить.
import threading # Этот модуль нужен для работы с потоками.

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
bot = telebot.TeleBot('7690161467:AAFtqGG-OheB7ax6Vd1Io01vZc5qorTM2s0')

# ID наставника (замените на реальный ID)
MENTOR_CHAT_ID = 1348557433

# Словарь для хранения данных пользователя
user_data = {}


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    # Приветственное сообщение
    bot.send_message(message.chat.id,"Привет! Я помогу тебе подготовиться к собеседованию на должность системного аналитика.")
    # Запрашиваем требования работодателя
    bot.send_message(message.chat.id, "Пожалуйста, введи требования работодателя к соискателю:")
    # Регистрируем следующий шаг — функцию get_requirements
    bot.register_next_step_handler(message, get_requirements)


# Функция для получения требований работодателя
def get_requirements(message):
    # Сохраняем требования в словарь user_data по ID пользователя
    user_data[message.chat.id] = {'requirements': message.text}
    # Запрашиваем дату и время собеседования
    bot.send_message(message.chat.id, "Теперь введи дату и время проведения собеседования в формате ДД.ММ.ГГГГ ЧЧ:ММ:")
    # Регистрируем следующий шаг — функцию get_interview_time
    bot.register_next_step_handler(message, get_interview_time)


# Функция для получения даты и времени собеседования
def get_interview_time(message):
    try:
        # Пытаемся преобразовать введенный текст в объект datetime
        interview_time = datetime.datetime.strptime(message.text, '%d.%m.%Y %H:%M')
        # Сохраняем время собеседования в словарь user_data
        user_data[message.chat.id]['interview_time'] = interview_time
        # Уведомляем пользователя, что данные приняты
        bot.send_message(message.chat.id, "Спасибо! Сейчас я отправлю уведомление наставнику.")
        # Вызываем функцию для уведомления наставника и пользователя
        notify_mentor_and_user(message.chat.id)
    except ValueError:
        # Если формат даты и времени неверный, сообщаем об ошибке
        bot.send_message(message.chat.id,
                         "Неверный формат даты и времени. Пожалуйста, введи дату и время в формате ДД.ММ.ГГГГ ЧЧ:ММ:")
        # Повторно запрашиваем дату и время
        bot.register_next_step_handler(message, get_interview_time)


# Функция для уведомления наставника и пользователя
def notify_mentor_and_user(user_chat_id):
    # Получаем требования из словаря user_data
    requirements = user_data[user_chat_id]['requirements']
    # Получаем время собеседования из словаря user_data
    interview_time = user_data[user_chat_id]['interview_time']

    # Определяем темы для повторения на основе требований
    topics_to_review = determine_topics_to_review(requirements)

    # Формируем сообщение для наставника
    message_to_mentor = f"У пользователя {user_chat_id} запланировано собеседование на {interview_time.strftime('%d.%m.%Y %H:%M')}.\n"
    message_to_mentor += f"Требования работодателя:\n{requirements}\n"
    message_to_mentor += f"Рекомендуемые темы для повторения:\n{topics_to_review}"

    # Отправляем сообщение наставнику
    bot.send_message(MENTOR_CHAT_ID, message_to_mentor)

    # Формируем сообщение для пользователя
    message_to_user = f"Ваше собеседование запланировано на {interview_time.strftime('%d.%m.%Y %H:%M')}.\n"
    message_to_user += f"Требования работодателя:\n{requirements}\n"
    message_to_user += f"Рекомендуемые темы для повторения:\n{topics_to_review}"

    # Отправляем сообщение пользователю
    bot.send_message(user_chat_id, message_to_user)


# Функция для определения тем для повторения
def determine_topics_to_review(requirements):
    # Пример логики для определения тем для повторения
    topics = []
    if "SQL" in requirements:
        topics.append("- Основы SQL, запросы, оптимизация")
    if "UML" in requirements:
        topics.append("- Диаграммы UML (Use Case, Sequence, Class)")
    if "требования" in requirements.lower():
        topics.append("- Сбор и анализ требований")
    if "анализ данных" in requirements.lower():
        topics.append("- Анализ данных, работа с большими данными")
    if "Agile" in requirements:
        topics.append("- Методологии Agile, Scrum, Kanban")

    # Если ни одна тема не подошла, добавляем общую тему
    if not topics:
        topics.append("- Общие темы по системному анализу")

    # Возвращаем темы в виде строки
    return "\n".join(topics)


# Запуск бота
bot.polling(none_stop=True)
