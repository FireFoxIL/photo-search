from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from index.handlers import upload_files, search_for_face
from index.forms import SearchImageForm
from index.models import ImageIndex

import os
__all__ = ['images_page', 'search_page', 'main_page']


@csrf_exempt
def images_page(request):
    if request.method == 'POST':
        upload_files(request, 'images')

    images = ImageIndex.objects.all()
    paginator = Paginator(images, 18)

    page = int(request.GET.get('page', 1))
    imgs = paginator.get_page(page)

    out = {
        'has_next_page': imgs.has_next(),
        'has_previous_page': imgs.has_previous(),
        'next_page': imgs.next_page_number() if imgs.has_next() else None,
        'prev_page': imgs.previous_page_number() if imgs.has_previous() else None,
        'cur_page': page,
        'images': imgs,
        'allow_input': bool(os.environ.get('ALLOW_INPUT', False))
    }

    return render(request, 'images.html', out)


@csrf_exempt
def main_page(request):
    return render(request, 'main.html')


@csrf_exempt
def search_page(request):
    if request.method == "POST":
        urls = search_for_face(request)
        is_empty = len(urls) == 0
    else:
        urls = []
        is_empty = False

    form = SearchImageForm()
    out = {
        'form': form,
        'images': urls,
        'is_empty': is_empty
    }

    return render(request, 'search.html', out)
