import telebot
import requests

TOKEN = '8659798284:AAF6fIglX3stMsMTNoq_S1I0AKXnZnlc1hQ'
bot = telebot.TeleBot(TOKEN)

def запит_до_шi(текст_запиту):
    try:
        url = "https://pollinations.ai"
        системна_роль = "Ти розумний ШІ-помічник для навчання українською мовою. Допомагай вирішувати завдання, писати реферати та твори чітко та структуровано."
        
        payload = {
            "messages": [
                {"role": "system", "content": системна_роль},
                {"role": "user", "content": текст_запиту}
            ],
            "model": "llama"
        }
        
        response = requests.post(url, json=payload, timeout=25)
        if response.status_code == 200:
            return response.text
        return "ШІ тимчасово перевантажений. Спробуй надіслати запит ще раз!"
    except Exception as e:
        return "Тимчасовий збій мережі ШІ. Будь ласка, спробуй ще раз!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    інструкція = (
        "🎓 Я вмію допомагати з:\n"
        "• Рефератами, планами та есе.\n"
        "• Контрольними роботами та тестами.\n"
        "• Заданнями з математики, програмування та інших предметів.\n\n"
        "📝 Просто напиши мені своє завдання, і я вирішу його!"
    )
    bot.reply_to(message, інструкція)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    статус = bot.reply_to(message, "Думаю над твоїм завданням... Зачекай кілька секунд...")
    вiдповiдь_шi = запит_до_шi(message.text)
    
    try:
        bot.delete_message(message.chat.id, статус.message_id)
    except:
        pass
        
    bot.reply_to(message, вiдповiдь_шi)

if __name__ == "__main__":
    print("Бот успішно працює на сервері!")
    bot.infinity_polling()
