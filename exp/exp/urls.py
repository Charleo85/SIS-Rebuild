"""exp URL Configuration

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

misc = [
    url(r'^$', views.index),
    url(r'^admin/', include(admin.site.urls)),
]

course = [
    url(r'^course/$', views.course_all),
    url(r'^course/(?P<sisid>[a-zA-Z0-9]+)/$', views.course_detail),
]

ins = [
    url(r'^instructor/$', views.instructor_all),
    url(r'^instructor/(?P<compid>[a-zA-Z0-9]+)/$', views.instructor_detail),
]

stud = [
    url(r'^student/$', views.student_all),
    url(r'^student/(?P<compid>[a-zA-Z0-9]+)/$', views.student_detail),
]

enr = [
    url(r'^enrollment/$', views.enrollment_all),
    url(r'^instructor/(?P<enrid>[0-9]+)/$', views.enrollment_detail),
]

urlpatterns = misc + course + ins + stud + enr
