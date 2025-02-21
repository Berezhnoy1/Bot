import json
from typing import List, Dict, Any
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import bot_config
from utils.logger import get_logger

logger = get_logger(__name__)

class GoogleSheetsManager:
    """Менеджер для работы с Google Sheets"""
    
    def __init__(self):
        self.scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
        self.client = None
        self.sheet = None
        self._connect()
    
    def _connect(self) -> None:
        """Подключение к Google Sheets"""
        try:
            with open(bot_config.GOOGLE_SHEETS_CREDS_FILE, "r") as file:
                creds_dict = json.load(file)
            
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, self.scope)
            self.client = gspread.authorize(creds)
            self.sheet = self.client.open(bot_config.SPREADSHEET_NAME).sheet1
            
            logger.info("✅ Подключение к Google Sheets успешно установлено")
        except Exception as e:
            logger.error(f"❌ Ошибка подключения к Google Sheets: {e}")
            raise
    
    def _ensure_headers(self) -> None:
        """Проверка и создание заголовков таблицы"""
        headers = [
            "Дата та час",
            "Ім'я",
            "Telegram",
            "Результат тесту",
            "Відсоток",
            "Рівень",
            "Мета",
            "Час на навчання",
            "Бюджет",
            "Формат",
            "Спосіб оплати",
            "Телефон"
        ]
        
        try:
            existing_headers = self.sheet.row_values(1)
            if not existing_headers:
                self.sheet.append_row(headers)
                self._format_headers()
        except Exception as e:
            logger.error(f"❌ Ошибка при проверке заголовков: {e}")
            raise
    
    def _format_headers(self) -> None:
        """Форматирование заголовков таблицы"""
        try:
            # Форматирование заголовков
            header_format = {
                "backgroundColor": {"red": 0.2, "green": 0.2, "blue": 0.2},
                "textFormat": {"foregroundColor": {"red": 1, "green": 1, "blue": 1}, "bold": True},
                "horizontalAlignment": "CENTER"
            }
            
            self.sheet.format("A1:L1", header_format)
            
            # Установка ширины столбцов
            column_widths = {
                "A": 150,  # Дата та час
                "B": 100,  # Ім'я
                "C": 120,  # Telegram
                "D": 100,  # Результат тесту
                "E": 80,   # Відсоток
                "F": 150,  # Рівень
                "G": 200,  # Мета
                "H": 120,  # Час на навчання
                "I": 100,  # Бюджет
                "J": 150,  # Формат
                "K": 120,  # Спосіб оплати
                "L": 120   # Телефон
            }
            
            for col, width in column_widths.items():
                self.sheet.set_column_width(col, width)
                
        except Exception as e:
            logger.error(f"❌ Ошибка форматирования заголовков: {e}")
            raise
    
    def save_user_data(self, user_data: Dict[str, Any], test_results: Dict[str, Any]) -> None:
        """Сохранение данных пользователя в таблицу"""
        try:
            self._ensure_headers()
            
            # Подготовка данных
            row_data = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                user_data.get('name', ''),
                f"@{user_data.get('username', '')}" if user_data.get('username') else "Не вказано",
                f"{test_results['correct']}/{test_results['total']}",
                f"{test_results['percentage']:.1f}%",
                test_results['level'],
                user_data.get('goal', 'Не вказано'),
                user_data.get('time', 'Не вказано'),
                user_data.get('budget', 'Не вказано'),
                user_data.get('format', 'Не вказано'),
                user_data.get('payment', 'Не вказано'),
                user_data.get('phone', 'Не вказано')
            ]
            
            # Добавление данных
            self.sheet.append_row(row_data)
            
            # Форматирование новой строки
            last_row = len(self.sheet.get_all_values())
            row_format = {
                "backgroundColor": {"red": 0.95, "green": 0.95, "blue": 0.95},
                "horizontalAlignment": "CENTER",
                "textFormat": {"foregroundColor": {"red": 0, "green": 0, "blue": 0}}
            }
            
            self.sheet.format(f"A{last_row}:L{last_row}", row_format)
            
            logger.info(f"✅ Данные успешно сохранены для пользователя {user_data.get('name', 'Unknown')}")
        except Exception as e:
            logger.error(f"❌ Ошибка сохранения данных: {e}")
            # Пробуем переподключиться и повторить
            self._connect()
            try:
                self.sheet.append_row(row_data)
                logger.info("✅ Данные успешно сохранены после переподключения")
            except Exception as e:
                logger.error(f"❌ Повторная ошибка сохранения данных: {e}")
                raise

    def create_tables(self):
        """Создание необходимых таблиц в базе данных"""
        create_tables_queries = [
            # Существующие таблицы
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                username TEXT,
                first_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            
            # Новые таблицы для реферальной системы
            """
            CREATE TABLE IF NOT EXISTS referral_codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                partner_id INTEGER NOT NULL,
                code TEXT UNIQUE NOT NULL,
                platform TEXT NOT NULL,
                theme TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            
            """
            CREATE TABLE IF NOT EXISTS conversions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                partner_id INTEGER NOT NULL,
                code TEXT NOT NULL,
                platform TEXT NOT NULL,
                event_type TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (code) REFERENCES referral_codes(code)
            )
            """
        ]
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for query in create_tables_queries:
            try:
                cursor.execute(query)
            except Exception as e:
                logger.error(f"Ошибка при создании таблицы: {e}")
        
        conn.commit()
        conn.close()

# Создаем глобальный экземпляр менеджера
db = GoogleSheetsManager()
