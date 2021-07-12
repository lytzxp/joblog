from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import UserinfoForm
from .models import Userinfo
from django.db.models.signals import post_init,post_save
from django.dispatch.dispatcher import receiver #删除文件
import os

@receiver(post_init,sender = Userinfo)
def backup_image_path(sender,instance,**kwargs):
    if instance.ryimage:
        instance._current_ryimage_file = instance.ryimage

@receiver(post_save,sender = Userinfo)
def delete_old_image(sender,instance,**kwargs):
    if hasattr(instance,'_current_ryimage_file'):
         instance._current_ryimage_file.delete(save = False)

# Create your views here.
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('blog:index'))

def register(request):
    if request.method!='POST':
        form=UserCreationForm()
    else:
        form=UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user=form.save()
            authenticated_user=authenticate(username=new_user.username,password=request.POST['password1'])
            login(request,authenticated_user)
            return HttpResponseRedirect(reverse('blog:index'))

    context={'form':form}
    return render(request,'users/register.html',context)

def edituserinfo(request,user_id):
  try:
     new_userinfo=Userinfo.objects.get(owner=user_id)
  except Userinfo.DoesNotExist:
      form=UserinfoForm()
      new_userinfo = form.save(commit=False)
      new_userinfo.owner = request.user
      new_userinfo.save()
      return HttpResponseRedirect(reverse('blog:topics'))
  if request.method!='POST':
        form=UserinfoForm(instance=new_userinfo)
  else:

        #ryimage_delete(new_userinfo)
        form=UserinfoForm(instance=new_userinfo, data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blog:topics'))
  context={'form':form}
  return render(request,'users/userinfo.html',context)




