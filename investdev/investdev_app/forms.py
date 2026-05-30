from django import forms

from .models import Publication


class AddPageForm(forms.ModelForm):
    is_published = forms.BooleanField(required=False, initial=True, label="Опубликовать")

    class Meta:
        model = Publication
        fields = ["title", "content", "picture", "is_published", "category"]
        labels = {
            "title": "Заголовок",
            "content": "Содержание",
            "picture": "Картинка",
            "category": "Категория",
        }
