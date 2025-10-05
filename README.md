# 🎮 Telegram Крестики-Нолики Бот

Современный телеграм-бот для игры в крестики-нолики с непобедимым AI на основе алгоритма minimax.

## 🚀 Технологический стек

- **Python 3.11+**
- **aiogram 3.x** - современный асинхронный фреймворк для Telegram Bot API
- **UV** - быстрый пакетный менеджер для Python
- **Pydantic Settings** - управление конфигурацией
- **aiohttp** - для webhook режима

## ✨ Особенности

- ✅ Игра против непобедимого AI (алгоритм minimax)
- ✅ Интерактивные inline-клавиатуры
- ✅ Поддержка двух режимов: polling (локально) и webhook (продакшн)
- ✅ Современная архитектура с разделением на модули
- ✅ Type hints и Pydantic для валидации
- ✅ Готовность к масштабированию (будущий онлайн режим)

## 📦 Установка

### 1. Установите UV

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Через pip:**
```bash
pip install uv
```

### 2. Клонируйте репозиторий

```bash
git clone <your-repo-url>
cd Tic-tac-toe_tg
```

### 3. Установите зависимости

```bash
uv sync
```

UV автоматически создаст виртуальное окружение и установит все зависимости из `pyproject.toml`.

### 4. Настройте конфигурацию

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Отредактируйте `.env` и добавьте токен вашего бота:

```env
BOT_TOKEN=your_bot_token_here
BOT_MODE=polling
```

**Получение токена бота:**
1. Напишите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям
4. Скопируйте полученный токен в `.env`

## 🎯 Запуск

### Локальный запуск (polling)

```bash
uv run python main.py
```

### Продакшн запуск (webhook)

1. Настройте `.env` для webhook режима:

```env
BOT_TOKEN=your_bot_token_here
BOT_MODE=webhook
WEBHOOK_URL=https://your-domain.com
WEBHOOK_PATH=/webhook
WEBAPP_HOST=0.0.0.0
WEBAPP_PORT=8080
```

2. Запустите:

```bash
uv run python main.py
```

## 🏗️ Структура проекта

```
Tic-tac-toe_tg/
├── app/
│   ├── __init__.py
│   ├── config.py           # Конфигурация (Pydantic Settings)
│   ├── game/
│   │   ├── __init__.py
│   │   └── logic.py        # Игровая логика и AI
│   ├── handlers/
│   │   ├── __init__.py
│   │   └── game_handlers.py # Обработчики команд и callback'ов
│   └── keyboards/
│       ├── __init__.py
│       └── game_keyboards.py # Inline-клавиатуры
├── main.py                 # Точка входа
├── pyproject.toml          # Зависимости и настройки проекта
├── .env.example            # Пример конфигурации
└── README.md
```

## 🎮 Использование

1. Найдите вашего бота в Telegram
2. Отправьте `/start`
3. Нажмите "🎮 Играть с ботом"
4. Играйте, нажимая на клетки поля

**Команды:**
- `/start` - Начать работу с ботом
- `/newgame` - Начать новую игру

## 🧠 О AI

Бот использует алгоритм **minimax** для выбора оптимальных ходов. Это делает его практически непобедимым! Лучшее, на что можно рассчитывать — ничья.

## 🔮 Планы на будущее

- [ ] Онлайн режим с подбором игроков
- [ ] Рейтинговая система
- [ ] Статистика игр
- [ ] Режимы сложности AI
- [ ] Поддержка нескольких языков

## 🛠️ Разработка

### Добавление зависимостей

```bash
uv add package-name
```

### Обновление зависимостей

```bash
uv sync --upgrade
```

### Форматирование кода

```bash
uv run ruff check app/ main.py
```

## 📝 Переменные окружения

| Переменная | Описание | По умолчанию |
|-----------|----------|--------------|
| `BOT_TOKEN` | Токен Telegram бота | - (обязательно) |
| `BOT_MODE` | Режим работы (polling/webhook) | `polling` |
| `WEBHOOK_URL` | URL для webhook | - |
| `WEBHOOK_PATH` | Путь для webhook | `/webhook` |
| `WEBAPP_HOST` | Хост веб-приложения | `0.0.0.0` |
| `WEBAPP_PORT` | Порт веб-приложения | `8080` |
| `LOG_LEVEL` | Уровень логирования | `INFO` |

## 📄 Лицензия

MIT

## 🤝 Вклад в проект

Pull requests приветствуются! Для серьёзных изменений, пожалуйста, сначала откройте issue для обсуждения.

---

Сделано с ❤️ используя современные технологии Python
