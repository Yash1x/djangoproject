from django import template
import investdev_app.views as views

register = template.Library()

@register.simple_tag()
def get_caregory():
    return views.category_db