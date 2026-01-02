import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import json
from datetime import datetime
import random
import string

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен вашего бота
TOKEN = "8228472308:AAFarC-gKzt3ZTaaafo5-wQLv03zXz6ZKMg"

# Хранение данных
class Storage:
    def __init__(self):
        self.data = {}
        self.load()
    
    def load(self):
        try:
            with open('data.json', 'r') as f:
                self.data = json.load(f)
        except:
            self.data = {'codes': {}, 'users': {}}
    
    def save(self):
        with open('data.json', 'w') as f:
            json.dump(self.data, f)

storage = Storage()

# Генерация кодов
def generate_code(prefix="BOT"):
    """Генерирует случайный код"""
    chars = string.ascii_uppercase + string.digits
    code = f"{prefix}-{''.join(random.choice(chars) for _ in range(6))}"
    return code

# Команды бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    user = update.effective_user
    
    keyboard = [
        [InlineKeyboardButton("🎫 Код проверки", callback_data="get_verify")],
        [InlineKeyboardButton("📱 Код регистрации", callback_data="get_register")],
        [InlineKeyboardButton("📋 Мои коды", callback_data="my_codes")],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data="help_info")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = f"""
    🚀 *Добро пожаловать в Menta Code Bot!*
    
    *Создатель:* Г. Марк
    *Команда:* NexusMind2026
    *Telegram:* t.me/nexusmind20_26
    
    *Выберите действие:*
    """
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатий кнопок"""
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    user_name = query.from_user.first_name
    
    if query.data == "get_verify":
        # Генерация кода проверки
        code = generate_code("BOT")
        
        # Сохраняем
        if user_id not in storage.data['users']:
            storage.data['users'][user_id] = []
        
        code_info = {
            'code': code,
            'type': 'verification',
            'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'used': False
        }
        
        storage.data['users'][user_id].append(code_info)
        storage.data['codes'][code] = code_info
        storage.save()
        
        response = f"""
        ✅ *Код проверки сгенерирован!*
        
        📝 *Код:* `{code}`
        👤 *Для:* {user_name}
        ⏰ *Срок:* 24 часа
        🎯 *Назначение:* Проверка работы ботов
        
        *Инструкция:*
        1. Используйте код в течение 24 часов
        2. Один код = одна проверка
        3. Не передавайте код другим
        """
        
        await query.edit_message_text(response, parse_mode='Markdown')
    
    elif query.data == "get_register":
        # Генерация кода регистрации
        code = generate_code("REG")
        
        # Сохраняем
        if user_id not in storage.data['users']:
            storage.data['users'][user_id] = []
        
        code_info = {
            'code': code,
            'type': 'registration',
            'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'used': False
        }
        
        storage.data['users'][user_id].append(code_info)
        storage.data['codes'][code] = code_info
        storage.save()
        
        response = f"""
        ✅ *Код регистрации сгенерирован!*
        
        📝 *Код:* `{code}`
        👤 *Для:* {user_name}
        ⏰ *Срок:* 7 дней
        🎯 *Назначение:* Регистрация в Menta
        
        *Инструкция:*
        1. Откройте приложение Menta
        2. Перейдите к регистрации
        3. Введите этот код
        4. Завершите настройку аккаунта
        """
        
        await query.edit_message_text(response, parse_mode='Markdown')
    
    elif query.data == "my_codes":
        # Показать коды пользователя
        if user_id not in storage.data['users'] or not storage.data['users'][user_id]:
            await query.edit_message_text("📭 У вас еще нет кодов.")
            return
        
        codes = storage.data['users'][user_id][-10:]  # Последние 10 кодов
        text = "📋 *Ваши последние коды:*\n\n"
        
        for i, code_info in enumerate(codes, 1):
            status = "🟢 Активен" if not code_info['used'] else "🔴 Использован"
            text += f"{i}. `{code_info['code']}`\n"
            text += f"   Тип: {'Проверка' if code_info['type'] == 'verification' else 'Регистрация'}\n"
            text += f"   Дата: {code_info['created']}\n"
            text += f"   Статус: {status}\n\n"
        
        await query.edit_message_text(text, parse_mode='Markdown')
    
    elif query.data == "help_info":
        help_text = """
        ℹ️ *Помощь по боту*
        
        *Команды:*
        • /start - Запустить бота
        • /help - Эта справка
        • /stats - Статистика
        
        *Типы кодов:*
        🎫 *Код проверки* - Для тестирования ботов
        📱 *Код регистрации* - Для регистрации в Menta
        
        *Ограничения:*
        • Каждый код одноразовый
        • Проверка: 24 часа
        • Регистрация: 7 дней
        
        *Поддержка:*
        👨‍💻 Создатель: Г. Марк
        🏢 Команда: NexusMind2026
        📢 Канал: t.me/nexusmind20_26
        """
        
        await query.edit_message_text(help_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /help"""
    await update.message.reply_text("Используйте /start для начала работы")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /stats"""
    total_codes = len(storage.data['codes'])
    total_users = len(storage.data['users'])
    
    stats_text = f"""
    📊 *Статистика бота*
    
    • Всего кодов: {total_codes}
    • Всего пользователей: {total_users}
    • Работает с: 15.12.2023
    
    🏢 *NexusMind2026*
    👨‍💻 *Создатель:* Г. Марк
    """
    
    await update.message.reply_text(stats_text, parse_mode='Markdown')

def main():
    """Запуск бота"""
    # Создаем приложение
    app = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CallbackQueryHandler(handle_button))
    
    # Запускаем
    logger.info("🤖 Бот запущен на Koyeb!")
    print("=" * 50)
    print("🚀 Menta Code Bot запущен!")
    print(f"👨‍💻 Создатель: Г. Марк")
    print(f"🏢 Команда: NexusMind2026")
    print(f"📢 Канал: t.me/nexusmind20_26")
    print("=" * 50)
    
    app.run_polling()

if __name__ == "__main__":
    main()
