from django.shortcuts import render

def home_page(request):
    return render(request, 'homepage.html')

def all_courses(request):
    req = urllib.request.Request('http://exp-api:8000/course/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return render(request, 'course.html', resp)

def course_detail(request, sisid):
    req = urllib.request.Request('http://exp-api:8000/course/' + sisid + '/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return render(request, 'course_detail.html', resp)

def about(request):
    return render(request, 'about.html')
