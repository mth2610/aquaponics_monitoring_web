from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
# from django.core.context_processors import csrf
# Create your views here.
def index(request):
    template = loader.get_template('mainpage.html')
    context = {}
    return HttpResponse(template.render(context, request))
