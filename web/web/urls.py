"""web URL Configuration

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
from django.conf.urls.static import static
from django.conf import settings

from . import views

statics = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

misc = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home_page, name='home'),
    url(r'^about/$', views.about, name='about'),
]

course = [
    url(
        r'^course/$', views.list_item,
        { 'modelname' : 'course' }, name='course_list',
    ),
    url(
        r'^course/(?P<itemid>[0-9]{5})/$',
        views.item_detail, { 'modelname' : 'course' }, name='course_detail',
    ),
]

ins = [
    url(
        r'^instructor/$', views.list_item,
        { 'modelname' : 'instructor' }, name='instructor_list'
    ),
    url(
        r'^instructor/(?P<itemid>[a-zA-Z0-9]+)/$',
        views.item_detail, { 'modelname' : 'instructor' },
        name='instructor_detail',
    ),
    url(
        r'^instructor/login/$',
        views.login, { 'modelname' : 'instructor' },
        name='instructor_login',
    ),
    url(
        r'^instructor/validate/$',
        views.instructor_validate, name='instructor_validate',
    ),
]

stud = [
    url(
        r'^student/(?P<itemid>[a-zA-Z0-9]+)/$',
        views.item_detail, { 'modelname' : 'student' },
        name='student_detail',
    ),
    url(
        r'^student/login/$',
        views.login, { 'modelname' : 'student' },
        name='student_login',
    ),
    url(
        r'^student/validate/$',
        views.student_validate, name='student_validate',
    ),
]

enr = [
    url(
        r'^enrollment/(?P<itemid>[0-9]+)/$',
        views.item_detail, { 'modelname' : 'enrollment' },
        name='enrollment_detail',
    ),
]

urlpatterns = statics + misc + course + ins + stud + enr
