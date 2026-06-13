import telebot
import requests

TOKEN = '8659798284:AAF6fIglX3stMsMTNoq_S1I0AKXnZnlc1hQ'
bot = telebot.TeleBot(TOKEN)

def запит_до_шi(текст_запиту):
    try:
        url = "https://pollinations.ai"
        системна_роль = "Ти розумний ШІ-помічник для навчання українською мовою. Допомагай вирішувати завдання, писати реферати та твори."
        
        payload = {
            "messages": [
                {"role": "system", "content": системна_роль},
                {"role": "user", "content": текст_запиту}
            ],
            "model": "openai"
        }
        
        response = requests.post(url, json=payload, timeout=20)
        if response.status_code == 200:
            return response.text
        return "ШІ тимчасово перевантажений. Спробуй ще раз!"
    except Exception as e:
        return "Сталася помилка з'єднання з ШІ. Спробуй ще раз."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привіт! Я твій ШІ-помічник для навчання. Напиши мені будь-яке завдання, і я вирішу його!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    статус = bot.reply_to(message, "Обробляю твій запит через ШІ...")
    вiдповiдь_шi = запит_до_шi(message.text)
    try:
        bot.delete_message(message.chat.id, status.message_id)
    except:
        pass
    bot.reply_to(message, вiдповiдь_шi)

if __name__ == "__main__":
    print("Бот запущений на сервері!")
    bot.infinity_polling()
