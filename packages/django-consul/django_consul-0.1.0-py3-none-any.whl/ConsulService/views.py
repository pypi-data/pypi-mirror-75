from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


# Create your views here.
def healthy_check_view(request: HttpRequest):
    return HttpResponse(status=200)

