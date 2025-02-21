import telebot
from config import bot_config
from handlers import start, test, survey
from utils.logger import get_logger
from utils.referral import ref_system
import random

# Инициализация логгера
logger = get_logger(__name__)

def register_admin_handlers(bot):
    """Регистрация обработчиков админ-команд"""
    
    @bot.message_handler(commands=['create_link'])
    def handle_create_link(message):
        """Создание реферальной ссылки"""
        if str(message.from_user.id) != bot_config.ADMIN_ID:
            return
            
        try:
            args = message.text.split()[1:]  # Получаем аргументы после команды
            if len(args) != 2:
                raise ValueError("Неверное количество аргументов")
                
            platform, theme = args
            
            # Создаём новый ID для партнера
            partner_id = random.randint(1000, 9999)
            
            # Создаём ссылку
            link = ref_system.create_referral_link(
                partner_id=partner_id,
                platform=platform,
                theme=theme
            )
            
            # Отправляем красивое сообщение с информацией
            response = f"✨ Новая реферальная ссылка создана!\n\n"
            response += f"🔗 Ссылка: {link}\n"
            response += f"📱 Платформа: {platform}\n"
            response += f"🎯 Тема: {theme}\n"
            response += f"🆔 ID партнера: {partner_id}\n\n"
            response += "Сохраните ID партнера для просмотра статистики!"
            
            bot.reply_to(message, response)
            
        except (ValueError, IndexError) as e:
            bot.reply_to(message, "❌ Использование: /create_link platform theme\n"
                                 "Например: /create_link tiktok crypto")
            logger.error(f"Ошибка создания ссылки: {e}")
    
    @bot.message_handler(commands=['stats'])
    def handle_stats(message):
        """Просмотр статистики"""
        if str(message.from_user.id) != bot_config.ADMIN_ID:
            return
            
        try:
            args = message.text.split()[1:]  # Получаем аргументы после команды
            
            if args:
                # Статистика конкретного партнера
                partner_id = int(args[0])
                stats = ref_system.get_partner_stats(partner_id)
                
                response = f"📊 Статистика партнера #{partner_id}\n\n"
                response += f"👆 Всего кликов: {stats['total_clicks']}\n"
                response += f"🎯 Начали опрос: {stats['total_starts']}\n"
                response += f"✅ Завершили: {stats['total_completes']}\n\n"
                
                for platform, data in stats['by_platform'].items():
                    response += f"📱 {platform.upper()}:\n"
                    response += f"   Клики: {data.get('clicks', 0)}\n"
                    response += f"   Старты: {data.get('starts', 0)}\n"
                    response += f"   Завершения: {data.get('completes', 0)}\n"
            else:
                # Общая статистика
                stats = ref_system.get_total_stats()
                response = "📈 Общая статистика:\n\n"
                response += f"🔗 Активных ссылок: {stats['total_links']}\n"
                response += f"👥 Партнеров: {stats['total_partners']}\n"
                response += f"👆 Всего конверсий: {stats['total_conversions']}\n"
            
            bot.reply_to(message, response)
            
        except (ValueError, IndexError) as e:
            bot.reply_to(message, "❌ Использование:\n"
                                 "/stats - общая статистика\n"
                                 "/stats partner_id - статистика партнера")
            logger.error(f"Ошибка получения статистики: {e}")

def main():
    """Основная функция запуска бота"""
    # Проверка наличия токена
    if not bot_config.TOKEN:
        logger.error("Ошибка! Токен не установлен в файле .env")
        return
    
    # Создание экземпляра бота
    bot = telebot.TeleBot(bot_config.TOKEN)
    
    # Регистрация обработчиков
    register_admin_handlers(bot)
    start.register_handlers(bot)
    test.register_handlers(bot)
    survey.register_handlers(bot)
    
    # Запуск бота
    logger.info("🤖 Бот запущен!")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)

if __name__ == "__main__":
    main()
