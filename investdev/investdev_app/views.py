from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from investdev_app.forms import AddPageForm
from investdev_app.models import Category, InvestmentFactor, ProjectPassport, Publication

menu = [
    {"title": "О проекте", "url_name": "about"},
    {"title": "Добавить расчет", "url_name": "add_page"},
    {"title": "Контакты", "url_name": "contact"},
    {"title": "Вход", "url_name": "login"},
]


def index(request):
    posts = (
        Publication.objects.filter(is_published=True)
        .select_related("category")
        .prefetch_related("factors")
    )
    categories = Category.objects.all()
    factors = InvestmentFactor.objects.all()
    data = {
        "title": "InvestDev — главная",
        "menu": menu,
        "posts": posts,
        "cats": categories,
        "factors": factors,
        "category_selected": 0,
        "factor_selected": 0,
    }
    return render(request, "investdev_app/index.html", context=data)


def about(request):
    return render(
        request,
        "investdev_app/about.html",
        {
            "title": "О проекте",
            "menu": menu,
        },
    )


def post(request, post_slug):
    current_post = get_object_or_404(
        Publication.objects.select_related("category").prefetch_related("factors"),
        slug=post_slug,
    )
    data = {
        "title": current_post.title,
        "content": current_post.content,
        "picture": current_post.picture,
        "menu": menu,
        "post": current_post,
    }
    return render(request, "investdev_app/post.html", data)


def addpage(request):
    if request.method == "POST":
        form = AddPageForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                publication = form.save()

                date_suffix = timezone.now().strftime("%Y%m%d")
                base_code = f"{publication.slug.upper()}-{date_suffix}"
                project_code = base_code
                counter = 1
                while ProjectPassport.objects.filter(project_code=project_code).exists():
                    counter += 1
                    project_code = f"{base_code}-{counter}"

                passport = ProjectPassport.objects.create(
                    project_code=project_code,
                    initiator=publication.title,
                )
                publication.passport = passport
                publication.save(update_fields=["passport"])

                return redirect("home")
            except Exception:
                form.add_error(None, "Ошибка добавления проекта")
    else:
        form = AddPageForm()

    data = {
        "title": "Добавление проекта",
        "menu": menu,
        "form": form,
    }
    return render(request, "investdev_app/add_page.html", data)


def contact(request):
    return HttpResponse("Контакты проекта")


def login(request):
    return HttpResponse("Авторизация")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>404: Страница не найдена</h1>")


def category(request, category_slug):
    current_category = get_object_or_404(Category, slug=category_slug)
    posts = (
        Publication.objects.filter(is_published=True, category_id=current_category.pk)
        .select_related("category")
        .prefetch_related("factors")
    )
    categories = Category.objects.all()
    factors = InvestmentFactor.objects.all()
    data = {
        "title": f"Работы: {current_category.name}",
        "menu": menu,
        "posts": posts,
        "cats": categories,
        "factors": factors,
        "category_selected": current_category.pk,
        "factor_selected": 0,
    }
    return render(request, "investdev_app/index.html", context=data)


def factor(request, factor_slug):
    current_factor = get_object_or_404(InvestmentFactor, slug=factor_slug)
    posts = (
        Publication.objects.filter(is_published=True, factors__slug=current_factor.slug)
        .select_related("category")
        .prefetch_related("factors")
        .distinct()
    )
    categories = Category.objects.all()
    factors = InvestmentFactor.objects.all()
    data = {
        "title": f"Фактор: {current_factor.factor}",
        "menu": menu,
        "posts": posts,
        "cats": categories,
        "factors": factors,
        "category_selected": 0,
        "factor_selected": current_factor.pk,
    }
    return render(request, "investdev_app/index.html", context=data)
