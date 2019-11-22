from django.urls import path
from index.views import images_page, search_page, main_page

urlpatterns = [
    path('images', images_page, name='images'),
    path('search', search_page, name='search'),
    path('', main_page, name='main')
]
