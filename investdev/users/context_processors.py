menu = [
    {"title": "О проекте", "url_name": "about"},
    {"title": "Добавить расчет", "url_name": "add_page"},
    {"title": "Контакты", "url_name": "contact"},
    {"title": "Вход", "url_name": "users:login"},
]
def get_menu_context(request):
    return {"mainmenu": menu}