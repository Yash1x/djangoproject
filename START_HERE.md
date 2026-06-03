# Быстрый старт на новом компьютере

## 1. Требования

- Git
- Python 3.11+

Проверка:

```powershell
git --version
python --version
```

## 2. Клонирование репозитория

```powershell
git clone https://github.com/Yash1x/djangoproject.git
cd djangoproject
```

(если уже клонирован — `git pull`)

## 3. Виртуальное окружение и зависимости

```powershell
python -m venv djangovenv
.\djangovenv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Запуск проекта

База данных (`investdev/db.sqlite3`) уже лежит в репозитории со всеми пользователями, публикациями и применёнными миграциями. Ничего применять/загружать не нужно.

```powershell
cd investdev
python manage.py runserver
```

Открыть: `http://127.0.0.1:8000/`

## 5. Учётные данные

Пользователи из репозитория:

- `yashix` — основной аккаунт
- `yashix2`, `prrivat` — тестовые

Если забыл пароль — сбросить можно командой:

```powershell
python manage.py changepassword yashix
```

Или создать нового суперюзера:

```powershell
python manage.py createsuperuser
```

## 6. Файл `.env` (секреты)

В корне `investdev/` должен лежать файл `.env` (он НЕ в репозитории, скачивается отдельно из Google Drive). Формат:

```
EMAIL_HOST_PASSWORD=...
YANDEX_MAPS_API_KEY=...
OPENROUTER_API_KEY=...
OPENROUTER_MODEL=openrouter/auto
```

Если файла нет — карта и AI-помощник работать не будут, всё остальное — будет.

- **Яндекс Карты** — `YANDEX_MAPS_API_KEY`, получить на https://developer.tech.yandex.ru/ (сервис «JavaScript API»)
- **Нейросеть (OpenRouter)** — `OPENROUTER_API_KEY`, получить на https://openrouter.ai/settings/keys. У ключа в настройках **Credit limit поставить unlimited**, иначе бесплатные модели не работают.
- **SMTP (сброс пароля)** — настройки `EMAIL_*`. Работает только без VPN/прокси на порте 587.

## 7. Полезные команды

```powershell
# Проверка проекта
python manage.py check

# Применить новые миграции (если будут)
python manage.py migrate

# Шелл Django
python manage.py shell

# Админка
# http://127.0.0.1:8000/admin/
```

## 8. Что в проекте

- `investdev/` — Django-проект
  - `investdev_app/` — основное приложение (публикации, категории, факторы, паспорта проектов)
  - `users/` — кастомная модель пользователя, авторизация, регистрация, сброс пароля
  - `media/` — загруженные картинки публикаций и аватарки (в репозитории)
  - `db.sqlite3` — БД с готовыми данными (в репозитории)
- `requirements.txt` — Python-зависимости
- `START_HERE.md` — этот файл

## 9. Структура страниц

- `/` — главная со списком публикаций
- `/about/` — карта Яндекс + AI-помощник (OpenRouter)
- `/post/<slug>/` — карточка публикации (есть кнопка «Редактировать» для юзеров с правами)
- `/addpage/` — добавление публикации (требует право `investdev_app.add_publication`)
- `/edit/<slug>/` — редактирование (требует право `investdev_app.change_publication`)
- `/users/login/`, `/users/register/`, `/users/profile/` — аккаунт
- `/users/password-reset/` — сброс пароля по e-mail
- `/admin/` — админка Django
