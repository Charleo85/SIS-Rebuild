from django.shortcuts import render
import urllib.request
import json

def home_page(request):
    return render(request, 'homepage.html')

def about(request):
    return render(request, 'about.html')

def list_item(request, modelname):
    req = urllib.request.Request('http://exp-api:8000/' + modelname + '/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return render(request, modelname + '.html', resp)

def item_detail(request, itemid, modelname):
    req = urllib.request.Request('http://exp-api:8000/' + modelname + '/' + itemid + '/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return render(request, modelname + '_detail.html', resp)
