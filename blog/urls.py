from django.conf.urls import url
#from django.conf.urls.static import static
#from djangolessong2 import settings
from django.views import static
from django.conf import settings
from. import views
urlpatterns=[
    #主页
    url(r'^$',views.index,name='index'),
    url(r'^topics/$',views.topics,name='topics'),
    url(r'^topics/(?P<topic_id>\d+)/tc_user$',views.tc_user,name='tc_user'),
    url(r'^hzzj/ajax_bthz_handle', views.ajax_bthz_handle,name='ajax_bahz'),
    url(r'^hzzj/ajax_grhz_handle', views.ajax_grhz_handle,name='ajax_grhz'),
    url(r'^hzzj/$',views.hzzj,name='hzzj'),
    url(r'^topics/(?P<topic_id>\d+)/$',views.topic,name='topic'),
    url(r'^new_topic/$',views.new_topic,name='new_topic'),
    url(r'^new_entry/(?P<topic_id>\d+)/$',views.entry,name='new_entry'),
    url(r'^edit_entry/(?P<entry_id>\d+)/$',views.edit_entry,name='edit_entry'),
    url(r'^del_entry/(?P<entry_id>\d+)/$',views.del_entry,name='del_entry'),
    url(r'^del_topic/(?P<topic_id>\d+)/$',views.del_topic,name='del_topic'),
    url(r'^topics/gxentry.html$',views.gxentry,name='gxentry'),
    url(r'^topics/(?P<topic_id>\d+)/(?P<entry_id>\d+)/$',views.edit_entry_image,name='edit_entry_image'),
    url(r'^topics/(?P<topic_id>\d+)/(?P<entry_id>\d+)/f/$',views.edit_entry_file,name='edit_entry_file'),
    url(r'^topics/(?P<topic_id>\d+)/(?P<entry_id>\d+)/(?P<entry_image_id>\d+)/$',views.del_entry_image,name='del_entry_image'),
    url(r'^topics/(?P<topic_id>\d+)/(?P<entry_id>\d+)/(?P<entry_file_id>\d+)/f/$',views.del_entry_file,name='del_entry_file'),
    url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='media')
    ]