import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv(dotenv_path=".env")

@dataclass
class BotConfig:
    """Конфигурация бота"""
    TOKEN: str = os.getenv("TOKEN", "")
    ADMIN_ID: str = os.getenv("ADMIN_ID", "")
    GOOGLE_SHEETS_CREDS_FILE: str = "google_sheets.json"
    SPREADSHEET_NAME: str = "Stats"

@dataclass
class TestConfig:
    """Конфигурация теста"""
    MIN_QUESTIONS: int = 10
    PASS_PERCENTAGE: float = 50.0
    LEVELS: dict = None

    def __post_init__(self):
        self.LEVELS = {
            90: {"name": "C2 (Вільне володіння) 🎭", "description": "Ви володієте англійською на найвищому рівні!"},
            80: {"name": "C1 (Просунутий) 🎯", "description": "Ви маєте глибоке розуміння мови!"},
            70: {"name": "B2+ (Вище середнього) 🌸", "description": "Ви впевнено володієте мовою!"},
            60: {"name": "B1 (Середній) 🌺", "description": "У вас хороший базовий рівень!"},
            50: {"name": "A2 (Елементарний) 🌿", "description": "Ви знаєте основи мови!"},
            0: {"name": "A1 (Початковий) 🌱", "description": "Ви починаєте вивчати мову!"}
        }

@dataclass
class UIConfig:
    """Конфигурация интерфейса"""
    MAIN_COLOR: str = "#2B2D42"  # Темно-синий
    ACCENT_COLOR: str = "#EF233C"  # Красный
    SUCCESS_COLOR: str = "#2EC4B6"  # Бирюзовый
    WARNING_COLOR: str = "#FF9F1C"  # Оранжевый
    ERROR_COLOR: str = "#E71D36"  # Красный
    
    # Эмодзи для разных случаев
    EMOJIS = {
        "correct": "✨",
        "wrong": "❌",
        "back": "🔙",
        "next": "➡️",
        "test": "📝",
        "money": "💰",
        "time": "⏳",
        "goal": "🎯",
        "phone": "📞",
        "calendar": "📅",
        "level": "📚"
    }

# Создаем экземпляры конфигураций
bot_config = BotConfig()
test_config = TestConfig()
ui_config = UIConfig()
