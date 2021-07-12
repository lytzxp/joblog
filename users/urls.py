from django.conf.urls import url
from django.contrib.auth.views import LoginView
from django.views import static
from django.conf import settings

#from djangolessong2 import settings
from . import views

urlpatterns=[
    url(r'^login/$',LoginView.as_view(template_name='users/login.html'),name='login'),
    url(r'^logout/$',views.logout_view,name='logout'),
    url(r'^register/$',views.register,name='register'),
    url(r'^userinfo/(?P<user_id>\d+)/$',views.edituserinfo,name='userinfo'),
    url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='media'),
]