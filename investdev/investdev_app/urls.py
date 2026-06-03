from django.urls import path, register_converter
from . import views
from . import convertors

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('ask-gpt/', views.ask_gpt, name='ask_gpt'),
    path('post/<slug:post_slug>/', views.post, name='post'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('category/<slug:category_slug>/', views.category, name='category'),
    path('factor/<slug:factor_slug>/', views.factor, name='factor'),
]
