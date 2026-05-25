from django.db import models
from django.urls import reverse
from slugify import slugify


class Publication(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, "Черновик"
        PUBLISHED = 1, "Опубликовано"

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(blank=True, verbose_name="Содержание")
    slug = models.SlugField(max_length=200, unique=True, db_index=True, verbose_name="Слаг")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    is_published = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
        default=Status.DRAFT,
        verbose_name="Статус публикации",
    )
    picture = models.ImageField(upload_to="publications/%Y/%m", blank=True, verbose_name="Картинка")
    category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
        related_name="publications",
        verbose_name="Категория",
    )
    factors = models.ManyToManyField(
        "InvestmentFactor",
        blank=True,
        related_name="publications",
        verbose_name="Факторы",
    )
    passport = models.OneToOneField(
        "ProjectPassport",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="publication",
        verbose_name="Паспорт проекта",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug": self.slug})

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"



class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, db_index=True, verbose_name="Слаг")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", kwargs={"category_slug": self.slug})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["id"]


class InvestmentFactor(models.Model):
    factor = models.CharField(max_length=100, db_index=True, verbose_name="Фактор")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Слаг")

    def __str__(self):
        return self.factor

    def get_absolute_url(self):
        return reverse("factor", kwargs={"factor_slug": self.slug})

    class Meta:
        verbose_name = "Инвестиционный фактор"
        verbose_name_plural = "Инвестиционные факторы"
        ordering = ["id"]


class ProjectPassport(models.Model):
    project_code = models.CharField(max_length=100, unique=True, db_index=True, verbose_name="Код проекта")
    initiator = models.CharField(max_length=100, verbose_name="Инициатор")
    budget_mln_rub = models.IntegerField(null=True, blank=True, verbose_name="Бюджет (млн руб.)")
    horizon_years = models.IntegerField(null=True, blank=True, verbose_name="Горизонт (лет)")

    def __str__(self):
        return self.project_code

    class Meta:
        verbose_name = "Паспорт проекта"
        verbose_name_plural = "Паспорта проектов"
        ordering = ["id"]
