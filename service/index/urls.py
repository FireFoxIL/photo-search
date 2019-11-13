from django.urls import path
from index.views import images_page, search_page

urlpatterns = [
    path('images', images_page, name='images'),
    path('search', search_page, name='search')
]
