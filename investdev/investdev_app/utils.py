class DataMixin:
    """Подмешивает title_page и другие общие данные в контекст CBV."""
    title_page = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context["title"] = self.title_page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.title_page:
            context["title"] = self.title_page
        return context
