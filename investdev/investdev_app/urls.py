from django.urls import path, register_converter
from . import views
from . import convertors

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('post/<slug:post_slug>/', views.post, name='post'),
    path('addpage/', views.addpage, name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('category/<slug:category_slug>/', views.category, name='category'),
    path('factor/<slug:factor_slug>/', views.factor, name='factor'),
]
