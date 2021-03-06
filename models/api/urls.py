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

from . import views_model
from . import views_auth

indexpage = [
    url(r'^$', views_model.index),
]

course = [
    url(r'^course/detail/(?P<sisid>[a-zA-Z0-9]+)/$', views_model.course_detail, name='course_detail'),
    url(r'^course/create/$', views_model.course_create, name='course_create'),
    url(r'^course/delete/$', views_model.course_delete, name='course_delete'),
    url(r'^course/all/$', views_model.course_all, name='course_all'),
]

instructor = [
    url(r'^instructor/all/$', views_model.instructor_all, name = 'instructor_all'),
    url(r'^instructor/detail/(?P<compid>[a-zA-Z0-9]+)/$', views_model.instructor_detail, name='instructor_detail'),
    url(r'^instructor/create/$', views_model.instructor_create, name='instructor_create'),
    url(r'^instructor/delete/$', views_model.instructor_delete, name='instructor_delete'),
]

student = [
    url(r'^student/all/$', views_model.student_all, name='student_all'),
    url(r'^student/detail/(?P<compid>[a-zA-Z0-9]+)/$', views_model.student_detail, name='student_detail'),
    url(r'^student/create/$', views_model.student_create, name='student_create'),
    url(r'^student/delete/$', views_model.student_delete, name='student_delete'),
]

enrollment = [
    url(r'^enrollment/detail/(?P<enrid>[0-9]+)/$', views_model.enrollment_detail, name='enrollment_detail'),
    url(r'^enrollment/create/$', views_model.enrollment_create, name='enrollment_create'),
    url(r'^enrollment/delete/$', views_model.enrollment_delete, name='enrollment_delete'),
    url(r'^enrollment/all/$', views_model.enrollment_all, name='enrollment_all'),
]

auth = [
    url(r'^auth/login/$', views_auth.login),
    url(r'^auth/validate/$', views_auth.validate),
    url(r'^auth/logout/$', views_auth.logout),
    url(r'^auth/record_co-view/$', views_auth.record_coview),
]

urlpatterns = indexpage + course + instructor + student + enrollment + auth
