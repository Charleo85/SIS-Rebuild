from django.shortcuts import render

def home_page(request):
    return render(request, 'homepage.html')

def all_courses(request):
    return render(request, 'Course.html')

def course_detail(request, sisid):
    return render(request, 'course_detail.html')

def about(request):
    return render(request, 'about.html')
