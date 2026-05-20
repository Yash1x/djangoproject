# Быстрый старт на новом компьютере

## 1. Требования
- `Git`
- `Python 3.11+`

Проверка:

```powershell
git --version
python --version
```

## 2. Клонирование

```powershell
git clone git@github.com:Yash1x/djangoproject.git
cd djangoproject
```

Если используешь HTTPS:

```powershell
git clone https://github.com/Yash1x/djangoproject.git
cd djangoproject
```

## 3. Виртуальное окружение

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install django==5.2.14
```

## 4. Первый запуск проекта с готовыми данными

```powershell
cd investdev
.\bootstrap_local.ps1
python manage.py runserver
```

Открыть в браузере:
- `http://127.0.0.1:8000/`

## 5. Что делает `bootstrap_local.ps1`
- применяет миграции (`migrate`)
- загружает данные публикаций/категорий/факторов/паспортов из fixture
- выполняет `python manage.py check`

## 6. Важно про медиа
- Медиа-файлы публикаций уже лежат в репозитории в `investdev/media/publications/...`
- Поэтому после `git pull` картинки на карточках и в постах должны появиться без ручного копирования

## 7. Полезные команды

Проверка проекта:

```powershell
python manage.py check
```

Создание администратора:

```powershell
python manage.py createsuperuser
```

Админка:
- `http://127.0.0.1:8000/admin/`
