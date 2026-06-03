from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, UpdateView

from investdev_app.forms import AddPageForm
from investdev_app.models import Category, InvestmentFactor, ProjectPassport, Publication
from investdev_app.utils import DataMixin



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
        "posts": posts,
        "cats": categories,
        "factors": factors,
        "category_selected": 0,
        "factor_selected": 0,
    }
    return render(request, "investdev_app/index.html", context=data)


def about(request):
    from django.conf import settings
    return render(
        request,
        "investdev_app/about.html",
        {
            "title": "О проекте",
            "yandex_maps_api_key": settings.YANDEX_MAPS_API_KEY,
        },
    )


def ask_gpt(request):

    import json
    import urllib.request
    import urllib.error
    from django.conf import settings
    from django.http import JsonResponse

    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    try:
        body = json.loads(request.body.decode("utf-8"))
        question = (body.get("question") or "").strip()
    except Exception:
        return JsonResponse({"error": "bad JSON"}, status=400)
    if not question:
        return JsonResponse({"error": "пустой вопрос"}, status=400)

    payload = {
        "model": settings.OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "Ты — помощник на сайте InvestDev. Отвечай кратко и по делу."},
            {"role": "user", "content": question},
        ],
    }
    import time
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://127.0.0.1:8000",
        "X-Title": "InvestDev",
    }
    last_err = None
    for attempt in range(3):
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            answer = data["choices"][0]["message"]["content"]
            return JsonResponse({"answer": answer})
        except urllib.error.HTTPError as e:
            text = e.read().decode("utf-8", "ignore")
            last_err = f"OpenRouter HTTP {e.code}: {text}"
            if e.code == 429:
                time.sleep(1.5)
                continue
            return JsonResponse({"error": last_err}, status=502)
        except Exception as e:
            return JsonResponse({"error": f"{type(e).__name__}: {e}"}, status=502)
    return JsonResponse({"error": last_err or "rate limited"}, status=502)


def post(request, post_slug):
    current_post = get_object_or_404(
        Publication.objects.select_related("category").prefetch_related("factors"),
        slug=post_slug,
    )
    data = {
        "title": current_post.title,
        "content": current_post.content,
        "picture": current_post.picture,
        "post": current_post,
    }
    return render(request, "investdev_app/post.html", data)

class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPageForm
    template_name = "investdev_app/add_page.html"
    success_url = reverse_lazy("home")
    title_page = "Добавление проекта"
    permission_required = "investdev_app.add_publication"

    def form_valid(self, form):
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

            self.object = publication
            return HttpResponseRedirect(self.get_success_url())
        except Exception:
            form.add_error(None, "Ошибка добавления проекта")
            return self.form_invalid(form)


class UpdatePage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, UpdateView):
    model = Publication
    fields = ["title", "content", "picture", "is_published", "category", "factors"]
    template_name = "investdev_app/add_page.html"
    success_url = reverse_lazy("home")
    title_page = "Редактирование проекта"
    slug_url_kwarg = "slug"
    slug_field = "slug"
    permission_required = "investdev_app.change_publication"


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

        "posts": posts,
        "cats": categories,
        "factors": factors,
        "category_selected": 0,
        "factor_selected": current_factor.pk,
    }
    return render(request, "investdev_app/index.html", context=data)
