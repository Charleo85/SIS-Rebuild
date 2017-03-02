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

webv2 = [
    url(r'^$', views.home_page, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^department/(?P<specific_department>[a-zA-Z-]{0,30})/$', views.department_view),
    url(r'^course/(?P<mnemonic>[a-zA-Z]{1,4})(?P<number>[0-9]{4})/', views.course_detail),
    # Need section detail!
]


# ###############################
# misc = [
#     url(r'^admin/', include(admin.site.urls)),
#     # url(r'^$', views.home_page, name='home'),
#     # url(r'^about/$', views.about, name='about'),
#     url(r'^search/$', views.search_page, name='search_page'),
# ]
#
# course = [
#     url(
#         r'^course/$', views.list_item,
#         { 'modelname' : 'course' }, name='course_list',
#     ),
#     url(
#         r'^course/detail/(?P<itemid>[0-9]{5})/$',
#         views.item_detail, { 'modelname' : 'course' }, name='course_detail',
#     ),
#     url(
#         r'^course/create/$', views.create_course_listing,
#         { 'modelname' : 'course' }, name='course_create',
#     ),
# ]
#
# ins = [
#     url(
#         r'^instructor/$', views.list_item,
#         { 'modelname' : 'instructor' }, name='instructor_list'
#     ),
#     url(
#         r'^instructor/detail/(?P<itemid>[a-zA-Z0-9]+)/$',
#         views.item_detail, { 'modelname' : 'instructor' },
#         name='instructor_detail',
#     ),
#     url(
#         r'^instructor/login/$',
#         views.login, { 'modelname' : 'instructor' },
#         name='instructor_login',
#     ),
#     url(
#         r'^instructor/profile/$',
#         views.instructor_profile, name='instructor_profile',
#     ),
#     url(
#         r'^instructor/logout/$',
#         views.logout, { 'modelname' : 'instructor' },
#         name='instructor_logout',
#     ),
#     url(
#         r'^instructor/signup/$',
#         views.signup, { 'modelname' : 'instructor' },
#         name='instructor_signup',
#     ),
# ]
#
# stud = [
#     url(
#         r'^student/login/$',
#         views.login, { 'modelname' : 'student' },
#         name='student_login',
#     ),
#     url(
#         r'^student/profile/$',
#         views.student_profile, name='student_profile',
#     ),
#     url(
#         r'^student/logout/$',
#         views.logout, { 'modelname' : 'student' },
#         name='student_logout',
#     ),
#     url(
#         r'^student/signup/$',
#         views.signup, { 'modelname' : 'student' },
#         name='student_signup',
#     ),
# ]

urlpatterns = webv2 + statics  # + misc + course + ins + stud
