import telebot
import re
import datetime
from telebot import types

TOKEN = '7765106437:AAFyZMleggq6HUcNJIy0Zjn7LEw6PS9Qurs'
bot = telebot.TeleBot(TOKEN)

SUBJECTS = [
    "математика", "русский язык", "литература", "физика", "химия",
    "биология", "история", "обществознание", "география", "информатика",
    "английский язык"
]

passing_scores = {
    "мгу": {
        "мехмат": 320,
        "философский": 280,
        "юрфак": 350,
        "экономический": 340,
        "журналистика": 330,
        "психология": 325,
        "географический": 290,
        "исторический": 310
    },
    "спбгу": {
        "прикладная математика": 310,
        "международные отношения": 290,
        "филология": 285,
        "востоковедение": 300,
        "социология": 270,
        "история": 295,
        "биология": 280,
        "химия": 305
    },
    "вшэ": {
        "программная инженерия": 340,
        "медиакоммуникации": 300,
        "экономика": 360,
        "право": 350,
        "дизайн": 320,
        "международные отношения": 330,
        "психология": 345,
        "социология": 310
    },
    "мгту им. баумана": {
        "информатика и вычислительная техника": 290,
        "машиностроение": 250,
        "робототехника и мехатроника": 280,
        "авиастроение": 260,
        "энергетическое машиностроение": 240,
        "приборостроение": 270,
        "радиотехника": 285,
        "лазерная техника": 295
    },
    "мфти": {
        "прикладные математика и физика": 330,
        "аэрокосмическая техника": 300,
        "системный анализ и управление": 310,
        "инноватика": 290,
        "нанотехнологии и микросистемная техника": 320,
        "биотехнические системы и технологии": 280,
        "физика": 340,
        "химия": 320
    },
    "мифи": {
        "ядерная физика и технологии": 300,
        "техническая физика": 280,
        "электроника и автоматика физических установок": 270,
        "лазерные технологии и оптоэлектроника": 290,
        "медицинская физика": 260,
        "информационная безопасность": 310,
        "материаловедение и технологии материалов": 250,
        "наноинженерия": 280
    }
}

materials = {
    "математика": [
        "https://math.ru/problems",
        "https://stepik.org/course/132",
        "Книга: 'Алгебра и начала анализа' И. И. Зубарева"
    ],
    "русский язык": [
        "https://ruslanguage.ru/grammar",
        "https://ege.sdamgia.ru",
        "Книга: 'Русский язык. Теория и практика' Ладыженская"
    ],
    "физика": [
        "https://phys-ege.sdamgia.ru/",
        "https://stepik.org/course/123",
        "Книга: 'Физика для школьников' Пёрышкин"
    ]
}

grades = {}

schedule = {}

olympiad_schedule = {
    "11.01.2025": [("Искусство (МХК)", "Региональный этап")],
    "13.01.2025": [("Испанский язык", "Региональный этап")],
    "14.01.2025": [("Испанский язык", "Региональный этап")],
    "15.01.2025": [("Астрономия", "Региональный этап")],
    "16.01.2025": [("Обществознание", "Региональный этап")],
    "17.01.2025": [("Обществознание", "Региональный этап")],
    "18.01.2025": [("Информатика", "Региональный этап")],
    "19.01.2025": [("Информатика", "Региональный этап")],
    "21.01.2025": [("Химия", "Региональный этап")],
    "22.01.2025": [("Химия", "Региональный этап")],
    "23.01.2025": [("Русский язык", "Региональный этап")],
    "24.01.2025": [("Немецкий язык", "Региональный этап")],
    "25.01.2025": [("Немецкий язык", "Региональный этап")],
    "27.01.2025": [("Физика", "Региональный этап")],
    "28.01.2025": [("Физика", "Региональный этап")],
    "29.01.2025": [("Итальянский язык", "Региональный этап"), ("Китайский язык", "Региональный этап")],
    "30.01.2025": [("Итальянский язык", "Региональный этап"), ("Китайский язык", "Региональный этап")],
    "31.01.2025": [("Математика", "Региональный этап")],
    "01.02.2025": [("Математика", "Региональный этап")],
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton("📚 Учебные материалы")
    item2 = types.KeyboardButton("💯 Оценки")
    item3 = types.KeyboardButton("🏆 Расписание олимпиад")
    item4 = types.KeyboardButton("💡 Советы")
    item5 = types.KeyboardButton("📅 Расписание занятий")
    item6 = types.KeyboardButton("🏛 Проходные баллы")
    item7 = types.KeyboardButton("❓ Помощь")
    markup.add(item1, item2, item3, item4, item5, item6, item7)

    bot.send_message(message.chat.id,
                     "Привет! 👋 Я твой помощник для подготовки к поступлению! 🎓\n"
                     "Выбери команду:", reply_markup=markup)

@bot.message_handler(commands=['олимпиады', 'расписание_олимпиад'])
def send_olympiad_schedule(message):
    response = "📅 Расписание регионального этапа олимпиад РСОШ 2024/25:\n"
    for date, events in sorted(olympiad_schedule.items()):
        response += f"\n{date}:\n"
        for subject, stage in events:
            response += f" - {subject} ({stage})\n"
    bot.send_message(message.chat.id, response, reply_markup=get_main_markup())

def get_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton("📚 Учебные материалы")
    item2 = types.KeyboardButton("💯 Оценки")
    item3 = types.KeyboardButton("🏆 Расписание олимпиад")
    item4 = types.KeyboardButton("💡 Советы")
    item5 = types.KeyboardButton("📅 Расписание занятий")
    item6 = types.KeyboardButton("🏛 Проходные баллы")
    item7 = types.KeyboardButton("❓ Помощь")
    markup.add(item1, item2, item3, item4, item5, item6, item7)
    return markup

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()
    user_id = message.from_user.id

    if text == "помощь" or text == "❓ помощь":
        help_text = (
            "Доступные команды:\n"
            "- 📚 учебные материалы - подбор учебных материалов\n"
            "- 💯 оценки - работа с оценками\n"
            "- 🏆 расписание олимпиад - расписание олимпиад РСОШ\n"
            "- 📅 расписание занятий - добавить/посмотреть расписание занятий\n"
            "- 🏛 проходные баллы - просмотр проходных баллов в вузы\n"
            "- 💡 советы - советы по подготовке\n"
            "- ❓ помощь - показать это сообщение"
        )
        bot.send_message(message.chat.id, help_text, reply_markup=get_main_markup())
        return

    if text == "учебные материалы" or text == "📚 учебные материалы":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for subject in SUBJECTS:
            item = types.KeyboardButton(subject.capitalize())
            markup.add(item)
        back = types.KeyboardButton("⬅️ Назад")
        markup.add(back)
        bot.send_message(message.chat.id, "Выберите предмет:", reply_markup=markup)
        bot.register_next_step_handler(message, process_subject_for_materials)
        return

    if text == "оценки" or text == "💯 оценки":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item1 = types.KeyboardButton("➕ Добавить оценку")
        item2 = types.KeyboardButton("🔍 Показать оценки по предмету")
        item3 = types.KeyboardButton("📝 Показать все оценки")
        item4 = types.KeyboardButton("📊 Средний балл")
        back = types.KeyboardButton("⬅️ Назад")
        markup.add(item1, item2, item3, item4, back)
        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)
        bot.register_next_step_handler(message, process_grades_action)
        return

    if text in ["олимпиады", "расписание олимпиад", "🏆 расписание олимпиад"]:
        send_olympiad_schedule(message)
        return

    if text == "советы" or text == "💡 советы":
        advice = (
            "Советы по подготовке к поступлению:\n"
            "- ⏰ Начинайте подготовку заранее.\n"
            "- ✍️ Решайте пробные тесты и экзаменационные задания.\n"
            "- 📅 Следите за расписанием и не забывайте отдыхать. 🧘\n"
            "- 🚪 Посещайте дни открытых дверей вузов и консультируйтесь с преподавателями. 🧑‍🏫"
        )
        bot.send_message(message.chat.id, advice, reply_markup=get_main_markup())
        return

    if text == "расписание занятий" or text == "📅 расписание занятий":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item1 = types.KeyboardButton("➕ Добавить занятие")
        item2 = types.KeyboardButton("🗓 Показать расписание")
        back = types.KeyboardButton("⬅️ Назад")
        markup.add(item1, item2, back)
        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)
        bot.register_next_step_handler(message, process_schedule_action)
        return

    if text == "проходные баллы" or text == "🏛 проходные баллы":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for university in passing_scores.keys():
            item = types.KeyboardButton(university.capitalize())
            markup.add(item)
        back = types.KeyboardButton("⬅️ Назад")
        markup.add(back)
        bot.send_message(message.chat.id, "Выберите ВУЗ:", reply_markup=markup)
        bot.register_next_step_handler(message, process_university)
        return

    if text == "назад" or text == "⬅️ назад":
        start(message)
        return

    bot.send_message(message.chat.id,
                     "Извините, я не понял запрос. 😕 Напишите 'помощь' для списка команд.", reply_markup=get_main_markup())

def process_subject_for_materials(message):
    try:
        subject = message.text.lower()
        if subject in materials:
            response = f"📚 Учебные материалы по {subject}:\n" + "\n".join(materials[subject])
        elif subject == "назад" or subject == "⬅️ назад":
            start(message)
            return
        else:
            response = f"Извините, материалов по предмету '{subject}' нет. 🙁"
        bot.send_message(message.chat.id, response, reply_markup=get_main_markup())
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так. ⚠️')
        start(message)

def process_grades_action(message):
    try:
        action = message.text.lower()
        if action == "добавить оценку" or action == "➕ добавить оценку":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            for subject in SUBJECTS:
                item = types.KeyboardButton(subject.capitalize())
                markup.add(item)
            back = types.KeyboardButton("⬅️ Назад")
            markup.add(back)
            bot.send_message(message.chat.id, "Выберите предмет:", reply_markup=markup)
            bot.register_next_step_handler(message, process_subject_for_add_grade)
        elif action == "показать оценки по предмету" or action == "🔍 показать оценки по предмету":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            for subject in SUBJECTS:
                item = types.KeyboardButton(subject.capitalize())
                markup.add(item)
            back = types.KeyboardButton("⬅️ Назад")
            markup.add(back)
            bot.send_message(message.chat.id, "Выберите предмет:", reply_markup=markup)
            bot.register_next_step_handler(message, process_subject_for_show_grades)
        elif action == "показать все оценки" or action == "📝 показать все оценки":
            user_id = message.from_user.id
            user_grades = grades.get(user_id, {})
            if not user_grades:
                bot.send_message(message.chat.id, "У вас пока нет оценок. 🙁", reply_markup=get_main_markup())
                return
            response = "Ваши оценки:\n"
            for subject, grade_list in user_grades.items():
                response += f"{subject}: {grade_list if grade_list else 'оценок нет'}\n"
            bot.send_message(message.chat.id, response, reply_markup=get_main_markup())
        elif action == "средний балл" or action == "📊 средний балл":
            user_id = message.from_user.id
            user_grades = grades.get(user_id, {})
            if not user_grades:
                bot.send_message(message.chat.id, "У вас пока нет оценок. 🙁", reply_markup=get_main_markup())
                return
            response = "Средний балл по предметам:\n"
            total_sum = 0
            total_count = 0
            for subject, grade_list in user_grades.items():
                if grade_list:
                    avg = sum(grade_list) / len(grade_list)
                    response += f"{subject}: {avg:.2f}\n"
                    total_sum += sum(grade_list)
                    total_count += len(grade_list)
                else:
                    response += f"{subject}: 0.00\n"
            if total_count == 0:
                bot.send_message(message.chat.id, "У вас пока нет оценок. 🙁", reply_markup=get_main_markup())
                return
            overall_avg = total_sum / total_count
            response += f"\nОбщий средний балл: {overall_avg:.2f}"
            bot.send_message(message.chat.id, response, reply_markup=get_main_markup())
        elif action == "назад" or action == "⬅️ назад":
            start(message)
            return
        else:
            bot.send_message(message.chat.id, "Неизвестное действие. ⚠️", reply_markup=get_main_markup())
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так. ⚠️')
        start(message)

def process_subject_for_add_grade(message):
    try:
        subject = message.text.lower()
        if subject not in materials and subject not in SUBJECTS and subject != "назад":
            bot.send_message(message.chat.id, f"Неизвестный предмет '{subject}'. 🤔", reply_markup=get_main_markup())
            return
        if subject == "назад" or subject == "⬅️ назад":
            start(message)
            return
        bot.send_message(message.chat.id, f"Введите оценку по предмету '{subject}':")
        bot.register_next_step_handler(message, process_grade, subject)
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так. ⚠️')
        start(message)

def process_grade(message, subject):
    try:
        grade = int(message.text)
        user_id = message.from_user.id
        if grade < 1 or grade > 5:
            bot.send_message(message.chat.id, "Оценка должна быть числом от 1 до 5. 🔢", reply_markup=get_main_markup())
            return
        grades.setdefault(user_id, {}).setdefault(subject, []).append(grade)
        bot.send_message(message.chat.id, f"Оценка {grade} по предмету '{subject}' добавлена. ✅", reply_markup=get_main_markup())
    except ValueError:
        bot.send_message(message.chat.id, "Оценка должна быть числом от 1 до 5. 🔢", reply_markup=get_main_markup())
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так. ⚠️')
        start(message)

def process_subject_for_show_grades(message):
    try:
        subject = message.text.lower()
        if subject not in materials and subject not in SUBJECTS and subject != "назад":
            bot.send_message(message.chat.id, f"Неизвестный предмет '{subject}'. 🤔", reply_markup=get_main_markup())
            return
        if subject == "назад" or subject == "⬅️ назад":
            start(message)
            return
        user_id = message.from_user.id
        user_grades = grades.get(user_id, {}).get(subject, [])
        if not user_grades:
            bot.send_message(message.chat.id, f"Оценок по предмету '{subject}' пока нет. 🙁", reply_markup=get_main_markup())
            return
        avg = sum(user_grades) / len(user_grades)
        bot.send_message(message.chat.id,
                         f"Оценки по предмету '{subject}': {user_grades}\nСредний балл: {avg:.2f}", reply_markup=get_main_markup())
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так. ⚠️')
        start(message)

def process_schedule_action(message):
    try:
        action = message.text.lower()
        if action == "добавить занятие" or action == "➕ добавить занятие":
            bot.send_message(message.chat.id,
                             "Введите дату и время занятия в формате ДД.ММ.ГГГГ ЧЧ:ММ (например, 20.04.2025 15:00):")
            bot.register_next_step_handler(message, process_date_time)
        elif action == "показать расписание" or action == "🗓 показать расписание":
            bot.send_message(message.chat.id, "Введите дату для просмотра расписания в формате ДД.ММ.ГГГГ:")
            bot.register_next_step_handler(message, show_schedule_for_date)
        elif action == "назад" or action == "⬅️ назад":
            start(message)
            return
        else:
            bot.send_message(message.chat.id, "Неизвестное действие. ⚠️", reply_markup=get_main_markup())
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так. ⚠️')
        start(message)

def process_date_time(message):
    try:
        date_time_str = message.text
        date_time_obj = datetime.datetime.strptime(date_time_str, "%d.%m.%Y %H:%M")

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for subject in SUBJECTS:
            item = types.KeyboardButton(subject.capitalize())
            markup.add(item)
        back = types.KeyboardButton("⬅️ Назад")
        markup.add(back)
        bot.send_message(message.chat.id, "Выберите предмет:", reply_markup=markup)
        bot.register_next_step_handler(message, process_subject_for_schedule, date_time_obj)
    except ValueError:
        bot.send_message(message.chat.id,
                         "Неверный формат даты и времени. Используйте формат ДД.ММ.ГГГГ ЧЧ:ММ (например, 20.04.2025 15:00).")
        start(message)
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так. ⚠️')
        start(message)

def process_subject_for_schedule(message, date_time_obj):
    try:
        subject = message.text.lower()
        if subject not in materials and subject not in SUBJECTS and subject != "назад":
            bot.send_message(message.chat.id, f"Неизвестный предмет '{subject}'. 🤔")
            start(message)
            return
        if subject == "назад" or subject == "⬅️ назад":
            start(message)
            return
        bot.send_message(message.chat.id, "Введите описание занятия:")
        bot.register_next_step_handler(message, process_description, date_time_obj, subject)
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так. ⚠️')
        start(message)

def process_description(message, date_time_obj, subject):
    try:
        description = message.text
        user_id = message.from_user.id
        date = date_time_obj.date()
        time = date_time_obj.time()

        schedule.setdefault(user_id, {}).setdefault(date, []).append((time, subject, description))
        bot.send_message(message.chat.id,
                         f"Занятие добавлено на {date_time_obj.strftime('%d.%m.%Y')} в {date_time_obj.strftime('%H:%M')} по предмету {subject} с описанием: {description}",
                         reply_markup=get_main_markup())
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так. ⚠️')
        start(message)

def show_schedule_for_date(message):
    try:
        date_str = message.text
        user_id = message.from_user.id
        date = datetime.datetime.strptime(date_str, "%d.%m.%Y").date()
        user_schedule = schedule.get(user_id, {}).get(date, [])

        if not user_schedule:
            bot.send_message(message.chat.id, f"На {date_str} занятий нет. 🙁", reply_markup=get_main_markup())
            return

        response = f"Расписание на {date_str}:\n"
        for time, subject, desc in sorted(user_schedule):
            response += f"- {time.strftime('%H:%M')} | {subject} | {desc}\n"
        bot.send_message(message.chat.id, response, reply_markup=get_main_markup())
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат даты. 📅", reply_markup=get_main_markup())
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так. ⚠️')
        start(message)

def process_university(message):
    try:
        university = message.text.lower()
        if university not in passing_scores:
            bot.send_message(message.chat.id, f"Нет информации о проходных баллах в '{message.text}'. 🙁", reply_markup=get_main_markup())
            return

        response = f"<b>Проходные баллы в {message.text}:</b>\n"
        response += "<pre>"  # Открываем тег для форматирования кода

        # Определяем максимальную длину названия направления для выравнивания
        max_len = max(len(faculty) for faculty in passing_scores[university].keys())

        # Формируем таблицу
        table_header = f"| {'Направление':<{max_len}} | Балл |\n"
        response += table_header
        response += f"| {'-' * max_len}-|------|\n"  # Разделитель

        for faculty, score in passing_scores[university].items():
            response += f"| {faculty:<{max_len}} | {score:4} |\n"

        response += "</pre>"  # Закрываем тег для форматирования кода

        bot.send_message(message.chat.id, response, parse_mode="HTML", reply_markup=get_main_markup())

    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так. ⚠️')
        start(message)

bot.polling(none_stop=True)
