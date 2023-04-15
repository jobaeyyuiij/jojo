import sqlite3
import telebot

bot_token = '5961557186:AAFOKKlACzYLZ0PWxKCeu5KOqtIqDLMLhuw'
bot = telebot.TeleBot(bot_token)
5
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ادخل الاسم الاول")

@bot.message_handler(func=lambda message: True)
def search_person(message):
    search_first = message.text
    bot.reply_to(message, "ادخل اسم الاب")
    bot.register_next_step_handler(message, search_father, search_first)

def search_father(message, search_first):
    search_father = message.text
    bot.reply_to(message, "ادخل اسم الجد")
    bot.register_next_step_handler(message, search_grand, search_first, search_father)

def search_grand(message, search_first, search_father):
    search_grand = message.text

    conn = sqlite3.connect('meaan.sqlite')
    c = conn.cursor()

    c.execute(f"SELECT * FROM PERSON WHERE p_first LIKE '%{search_first}%' AND p_father LIKE '%{search_father}%' AND p_grand LIKE '%{search_grand}%'")

    matching_rows = c.fetchall()
    if matching_rows:
        fam_nos = [row[1] for row in matching_rows]
        
        c.execute(f"SELECT * FROM PERSON WHERE fam_no IN ({','.join(['?']*len(fam_nos))})", fam_nos)
        
        rows = c.fetchall()
        results = "Results found:\n\n"
        for row in rows:
            results += f"الاسم الاول: {row[3]}, الاب: {row[4]}, الجد: {row[5]}, مواليد {row[7]}\n"
        bot.reply_to(message, results)
    else:
        bot.reply_to(message, "No results found.")

    conn.close()

bot.polling()
