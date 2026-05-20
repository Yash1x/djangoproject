from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render

from investdev_app.models import Category, InvestmentFactor, Publication

menu = [
    {'title': 'О проекте', 'url_name': 'about'},
    {'title': 'Добавить расчет', 'url_name': 'add_page'},
    {'title': 'Контакты', 'url_name': 'contact'},
    {'title': 'Вход', 'url_name': 'login'},
]


def index(request):
    posts = (
        Publication.objects
        .filter(is_published=Publication.Status.PUBLISHED)
        .select_related('category')
        .prefetch_related('factors')
    )
    categories = Category.objects.all()
    factors = InvestmentFactor.objects.all()
    data = {
        'title': 'InvestDev — главная',
        'menu': menu,
        'posts': posts,
        'cats': categories,
        'factors': factors,
        'category_selected': 0,
        'factor_selected': 0,
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


def post(request, post_slug):
    current_post = get_object_or_404(
        Publication.objects.select_related('category').prefetch_related('factors'),
        slug=post_slug,
    )
    data = {
        'title': current_post.title,
        'content': current_post.content,
        'picture': current_post.picture,
        'menu': menu,
        'post': current_post,
    }
    return render(request, 'investdev_app/post.html', data)


def addpage(request):
    return HttpResponse('Добавление расчета проекта')


def contact(request):
    return HttpResponse('Контакты проекта')


def login(request):
    return HttpResponse('Авторизация')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>404: Страница не найдена</h1>')


def category(request, category_slug):
    current_category = get_object_or_404(Category, slug=category_slug)
    posts = (
        Publication.objects
        .filter(
            is_published=Publication.Status.PUBLISHED,
            category_id=current_category.pk,
        )
        .select_related('category')
        .prefetch_related('factors')
    )
    categories = Category.objects.all()
    factors = InvestmentFactor.objects.all()
    data = {
        'title': f'Работы: {current_category.name}',
        'menu': menu,
        'posts': posts,
        'cats': categories,
        'factors': factors,
        'category_selected': current_category.pk,
        'factor_selected': 0,
    }
    return render(request, 'investdev_app/index.html', context=data)


def factor(request, factor_slug):
    current_factor = get_object_or_404(InvestmentFactor, slug=factor_slug)
    posts = (
        Publication.objects
        .filter(
            is_published=Publication.Status.PUBLISHED,
            factors__slug=current_factor.slug,
        )
        .select_related('category')
        .prefetch_related('factors')
        .distinct()
    )
    categories = Category.objects.all()
    factors = InvestmentFactor.objects.all()
    data = {
        'title': f'Фактор: {current_factor.factor}',
        'menu': menu,
        'posts': posts,
        'cats': categories,
        'factors': factors,
        'category_selected': 0,
        'factor_selected': current_factor.pk,
    }
    return render(request, 'investdev_app/index.html', context=data)
