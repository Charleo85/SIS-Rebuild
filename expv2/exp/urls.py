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

from . import views_model
from . import views_auth

misc = [
    url(r'^$', views_model.index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^homepage/$', views_model.home_page),
    # url(r'^search/$', views_model.search),
    url(r'^auth/record_co-view/$', views_auth.record_coview),
    ]

course = [
    url(r'^department/(?P<specific_department>)[a-z]{1,10}/$', views_model.department_courses),
    url(r'^course/(?P<mnemonic>[a-zA-Z]{1,4})(?P<number>[0-9]{4})/$', views_model.course_detail),
    url(r'^course/(?P<mnemonic>[a-zA-Z]{1,4})/$', views_model.mnemonic_courses),
    #url(r'^course/(?<sis_id>[0-9]{5})/(?<semester>[0-9]{4})', views_model.section_detail()),
]

urlpatterns = misc + course

# course = [
#     url(r'^course/$', views_model.course_all),
#     url(r'^course/detail/(?P<sisid>[a-zA-Z0-9]+)/$', views_model.course_detail),
#     url(r'^course/create/$', views_model.course_create),
# ]


#
# ins = [
#     url(r'^instructor/$', views_model.instructor_all),
#     url(r'^instructor/detail/(?P<compid>[a-zA-Z0-9]+)/$', views_model.instructor_detail),
#     url(r'^instructor/auth/login/$', views_auth.login, {'user_type' : 0}),
#     url(r'^instructor/auth/validate/$', views_auth.validate, {'user_type' : 0}),
#     url(r'^instructor/auth/logout/$', views_auth.logout),
#     url(r'^instructor/signup/$', views_auth.signup, {'user_type' : 0}),
# ]
#
# stud = [
#     url(r'^student/$', views_model.student_all),
#     url(r'^student/detail/(?P<compid>[a-zA-Z0-9]+)/$', views_model.student_detail),
#     url(r'^student/auth/login/$', views_auth.login, {'user_type' : 1}),
#     url(r'^student/auth/validate/$', views_auth.validate, {'user_type' : 1}),
#     url(r'^student/auth/logout/$', views_auth.logout),
#     url(r'^student/signup/$', views_auth.signup, {'user_type' : 1}),
# ]
#
# enr = [
#     url(r'^enrollment/$', views_model.enrollment_all),
#     url(r'^enrollment/detail/(?P<enrid>[0-9]+)/$', views_model.enrollment_detail),
# ]

# urlpatterns = misc + course + ins + stud + enr
