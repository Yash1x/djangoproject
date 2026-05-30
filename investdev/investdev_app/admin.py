from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Category, InvestmentFactor, ProjectPassport, Publication


class HasPassport(admin.SimpleListFilter):
    title = "Наличие паспорта"
    parameter_name = "passport"

    def lookups(self, request, model_admin):
        return [
            ("passport", "Есть паспорт"),
            ("nopassport", "Нет паспорта"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "passport":
            return queryset.filter(passport__isnull=False)
        if self.value() == "nopassport":
            return queryset.filter(passport__isnull=True)
        return queryset


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    readonly_fields = ("slug", "post_photo")
    list_display = (
        "id",
        "title",
        "slug",
        "post_photo",
        "time_create",
        "is_published",
        "category",
        "passport",
    )
    fields = (
        "title",
        "content",
        "category",
        "picture",
        "post_photo",
        "factors",
        "is_published",
        "passport",
        "slug",
    )
    list_display_links = ("id", "title")
    search_fields = ("title", "content", "category__name")
    ordering = ("id", "title")
    filter_horizontal = ("factors",)
    list_editable = ("is_published",)
    list_per_page = 5
    actions = ["set_published", "set_draft"]
    list_filter = ("category__name", "is_published", HasPassport)

    @admin.display(description="Фото")
    def post_photo(self, publication: Publication):
        if publication.picture:
            return mark_safe(f"<img src='{publication.picture.url}' width='50'>")
        return "—"

    @admin.action(description="Опубликовать")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f"Изменено {count} записей")

    @admin.action(description="Снять с публикации")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=False)
        self.message_user(request, f"Изменено {count} записей", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    list_display_links = ("id", "name")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("id", "name")
    list_per_page = 5


@admin.register(InvestmentFactor)
class InvestmentFactorAdmin(admin.ModelAdmin):
    list_display = ("id", "factor", "slug")
    list_display_links = ("id", "factor")
    prepopulated_fields = {"slug": ("factor",)}
    ordering = ("id", "factor")
    list_per_page = 5


@admin.register(ProjectPassport)
class ProjectPassportAdmin(admin.ModelAdmin):
    list_display = ("id", "project_code", "initiator", "budget_mln_rub", "horizon_years")
    list_display_links = ("id", "project_code")
    ordering = ("id", "project_code")
    list_per_page = 5
