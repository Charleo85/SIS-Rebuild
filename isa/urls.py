"""isa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views

from django.conf.urls.static import static
from django.conf import settings

statics = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

misc = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
]

course = [
    url(r'^course/(?P<sisid>[0-9]{5})/$', views.course_detail),
    url(r'^course/$', views.course_form),
    url(r'^course/create/$', views.course_create),
]

instructor = [
    url(r'instructor/(?P<compid>[a-z]{2,3}[0-9]{1}[a-z]{1,2})/$', views.instructor_detail),
    url(r'instructor/create/$', views.instructor_create),
]

student = [
    url(r'student/(?P<compid>[a-z]{2,3}[0-9]{1}[a-z]{1,2})/$', views.student_detail),
    url(r'student/create/$', views.student_create),
]

urlpatterns = statics + misc + course + instructor + student
