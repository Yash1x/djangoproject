from django import template

from investdev_app.models import Category, InvestmentFactor

register = template.Library()

menu = [
    {"title": "О проекте", "url_name": "about"},
    {"title": "Добавить расчет", "url_name": "add_page"},
    {"title": "Контакты", "url_name": "contact"},
]


@register.simple_tag
def get_menu():
    return menu


@register.inclusion_tag("investdev_app/category.html")
def category(category_selected=0):
    categories = Category.objects.all()
    return {"category": categories, "category_selected": category_selected}


@register.inclusion_tag("investdev_app/list_factors.html")
def show_all_factors(factor_selected=0):
    factors = InvestmentFactor.objects.all()
    return {"factors": factors, "factor_selected": factor_selected}
