from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from .models import ShortComment


def index(request):
    return HttpResponse("Hello there Django!")


def homework(request):
    short_comments = [{'id': 1, 'content': "something", 'stars': 3, 'ts': '2020-08-30'}]
    short_comments = ShortComment.objects.all()
    return render(request, 'index.html', locals())
