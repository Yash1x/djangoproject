from django import template
from investdev_app.models import Category, InvestmentFactor

register = template.Library()


@register.inclusion_tag('investdev_app/category.html')
def category(category_selected=0):
    category = Category.objects.all()
    return {'category': category, 'category_selected': category_selected}


@register.inclusion_tag('investdev_app/list_factors.html')
def show_all_factors(factor_selected=0):
    factors = InvestmentFactor.objects.all()
    return {'factors': factors, 'factor_selected': factor_selected}
