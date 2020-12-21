from django.http import HttpResponse
from django.shortcuts import render

from main.tasks import check_videos_and_create


def home(request):
    return render(request, 'main/home.html')


