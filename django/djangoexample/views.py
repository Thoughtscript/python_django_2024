from django.shortcuts import render
from .models import Example, SubExample
from django.http import JsonResponse
import json 
from django.core import serializers

def index(request):
    return render(request, 'index.html', {})

# https://stackoverflow.com/questions/2428092/creating-a-json-response-using-django-and-python
def all_examples(request):
    scan = Example.objects.all()
    response_data = {}
    response_data['data'] = serializers.serialize('json', scan)
    response_data['status'] = 200
    return JsonResponse(response_data)

# https://stackoverflow.com/questions/2428092/creating-a-json-response-using-django-and-python
def all_sub_examples(request):
    scan = SubExample.objects.all()
    response_data = {}
    response_data['data'] = serializers.serialize('json', scan)
    response_data['status'] = 200
    return JsonResponse(response_data)

def post_example(request):
    if request.method == "POST":
        print(request.body)