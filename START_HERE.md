# Быстрый старт на новом компьютере

## 1. Что должно быть установлено
- `Git`
- `Python 3.11+`

Проверка:

```powershell
git --version
python --version
```

## 2. Клонирование проекта

```powershell
git clone git@github.com:Yash1x/djangoproject.git
cd djangoproject
```

Если работаешь по HTTPS:

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

## 4. Запуск проекта Django

```powershell
cd investdev
python manage.py migrate
python manage.py runserver
```

Открыть в браузере:
- `http://127.0.0.1:8000/`

## 5. Полезные команды

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

## 6. Частые проблемы и фиксы

`error: src refspec main does not match any`
- Локальная ветка называется `master`, а пушишь `main`.
- Решение:

```powershell
git branch -M main
git push -u origin main
```

`You have unapplied migrations`
- Не применены миграции.
- Решение:

```powershell
python manage.py migrate
```

CSS/изображения не подгружаются в дев-режиме
- Проверь, что запускаешь из папки `investdev`.
- Проверь, что в `settings.py` стоит `DEBUG = True`.

## 7. Рабочий цикл

```powershell
git pull
.\.venv\Scripts\activate
cd investdev
python manage.py runserver
```

