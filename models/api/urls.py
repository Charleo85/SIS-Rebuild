"""models URL Configuration

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

indexpage = [
    url(r'^$', views.index),
]

course = [
    url(r'^course/(?P<sisid>[0-9]{5})/$', views.course_detail),
    url(r'^course/create/$', views.course_create),
    url(r'^course/all/$', views.course_all),
]

instructor = [
    url(r'^instructor/all/$', views.instructor_all),
    url(r'^instructor/(?P<compid>[a-zA-Z0-9]+)/$', views.instructor_detail),
    url(r'^instructor/create/$', views.instructor_create),
]

student = [
    url(r'^instructor/all/$', views.instructor_all),
    url(r'^student/(?P<compid>[a-zA-Z0-9]+)/$', views.student_detail),
    url(r'^student/create/$', views.student_create),
]

enrollment = [
    url(r'^enrollment/(?P<enrid>[0-9]+)/$', views.enrollment_detail),
    url(r'^enrollment/create/$', views.enrollment_create),
    url(r'^enrollment/all/$', views.enrollment_all),
]

urlpatterns = indexpage + course + instructor + student + enrollment
