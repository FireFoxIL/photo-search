from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from index.handlers import upload_files, search_for_face
from index.forms import UploadImageForm, SearchImageForm
from index.models import ImageIndex

__all__ = ['images_page']


@csrf_exempt
def images_page(request):
    if request.method == 'POST':
        upload_files(request)

    form = UploadImageForm()
    images = ImageIndex.objects.all()

    out = {
        'form': form,
        'images': images
    }

    return render(request, 'images.html', out)

@csrf_exempt
def search_page(request):
    if request.method == "POST":
        urls = search_for_face(request)
    else:
        urls = []

    form = SearchImageForm()
    out = {
        'form': form,
        'images': urls
    }

    return render(request, 'search.html', out)
