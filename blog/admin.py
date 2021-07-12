from django.contrib import admin
from blog.models import Topic,Entry
from users.models import Userinfo
admin.site.register(Topic)
admin.site.register(Entry)
admin.site.register(Userinfo)

# Register your models here.
