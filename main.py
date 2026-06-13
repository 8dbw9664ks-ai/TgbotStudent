import telebot
import google.generativeai as genai

# Токен вашого бота
TOKEN = '8659798284:AAF6fIglX3stMsMTNoqGGB-1XONkZnlc1hQ'
bot = telebot.TeleBot(TOKEN)

# ⚠️ 
GOOGLE_API_KEY = 'AQ.Ab8RN6JQP5Rw0-WJRfObbUP7skpAwzVBZXi8F0uLOdKHCOapiA'
genai.configure(api_key=GOOGLE_API_KEY)

def запит_до_шi(текст_запиту):
    try:
        # Підключаємо найсучаснішу швидку модель Gemini Flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        системна_роль = "Ти розумний ШІ-помічник для навчання українською мовою. Допомагай вирішувати завдання, писати реферати та твори чітко та структуровано."
        
        повний_запит = f"{системна_роль}\n\nКористувач запитує: {текст_запиту}"
        response = model.generate_content(повний_запит)
        return response.text
    except Exception as e:
        return "Тимчасова помилка ШІ. Будь ласка, спробуй ще раз за мить!"

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
    print("Бот на базі Google Gemini успішно працює!")
    bot.infinity_polling()
