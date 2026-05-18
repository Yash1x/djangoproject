from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

posts_db = [
    {
        'id': 1,
        'title': 'Автоматизация расчета NPV в учебных кейсах',
        'content': 'Сравниваем ручной расчет в таблицах и автоматизированный подход в веб-приложении.',
        'is_published': True,
    },
    {
        'id': 2,
        'title': 'Построение сценариев: базовый, оптимистичный и стрессовый',
        'content': 'Показываем, как изменение входных параметров влияет на итоговую эффективность проекта.',
        'is_published': True,
    },
    {
        'id': 3,
        'title': 'Интерфейс итогового отчета для защиты проекта',
        'content': 'Формат вывода метрик и визуализаций для демонстрации научному руководителю.',
        'is_published': True,
    },
]

menu = [
    {'title': 'О проекте', 'url_name': 'about'},
    {'title': 'Добавить расчет', 'url_name': 'add_page'},
    {'title': 'Контакты', 'url_name': 'contact'},
    {'title': 'Вход', 'url_name': 'login'},
]


def index(request):
    data = {
        'title': 'InvestDev — главная',
        'menu': menu,
        'posts': posts_db,
    }
    return render(request, 'investdev_app/index.html', context=data)


def about(request):
    return render(
        request,
        'investdev_app/about.html',
        {
            'title': 'О проекте',
            'menu': menu,
        },
    )


def post(request, post_id):
    return HttpResponse(f'Статья с id = {post_id}')


def addpage(request):
    return HttpResponse('Добавление расчета проекта')


def contact(request):
    return HttpResponse('Контакты проекта')


def login(request):
    return HttpResponse('Авторизация')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>404: Страница не найдена</h1>')
