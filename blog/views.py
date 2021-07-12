import json

from django.shortcuts import render, redirect
from .models import Topic, Entry, Entryimage, Entryfiile
from users.models import Userinfo
from django.urls import reverse
from .forms import TopicForm, EntryForm, EntryimageForm, EntryfileForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from flask import url_for, Flask
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver  # 删除文件
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
app = Flask(__name__)


@app.route('/')
def check_topic_owner(owner, user, is_publish):
    if owner != user and is_publish == False:
        raise Http404


def check_entry_owner(request, owner):
    if owner == request.user:
        return True


def check_topicdel_owner(request, owner):
    if owner == request.user:
        return True


def index(request):
    return render(request, 'blog/index.html')


@login_required
def topics(request):
    topics = Topic.objects.filter(Q(is_publish=True)).order_by('date_add')
    grtopics = Topic.objects.filter(Q(is_publish=False) & Q(owner=request.user)).order_by(('date_add'))
    context = {'topics': topics, "topicscount": len(topics), 'grtopics': grtopics, 'grtopicscount': len(grtopics)}
    return render(request, 'blog/topics.html', context)


@login_required
@app.route("/topics/<topic_id>/")
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic.owner, request.user, topic.is_publish)
    entries = topic.entry_set.order_by('-date').filter(Q(is_publish=True) | Q(owner=request.user))
    page = Paginator(entries, 5)
    page_id = request.GET.get('page_id')
    enty_id = request.GET.get("entry_id")
    if enty_id:
        for pa in page:
            for p in pa:
                if p.id == int(enty_id):
                    page_id = pa.number
    if page_id:
        try:
            entries = page.page(page_id)
        except PageNotAnInteger:
            entries = page.page(1)
        except EmptyPage:
            entries = page.page(1)
    else:
        entries = page.page(1)
    entries_images = []
    entries_files = []
    for entry in entries:
        entry_image = Entryimage.objects.filter(entry_image=entry)
        entry_file = Entryfiile.objects.filter(entry_file=entry)
        x = {entry.id: entry_image}
        y = {entry.id: entry_file}
        entries_images.append(x)
        entries_files.append(y)
    context = {'topic': topic, 'entries': entries, 'paginator': page, 'entries_images': entries_images,
               'entries_files': entries_files}
    return render(request, 'blog/topic.html', context)


@login_required
def gxentry(request):
    entries = Entry.objects.filter(Q(topic__is_publish=False) & Q(is_publish=True)).order_by('-date')
    page = Paginator(entries, 5)
    page_id = request.GET.get('page_id')
    enty_id = request.GET.get("entry_id")
    if enty_id:
        for pa in page:
            for p in pa:
                if p.id == int(enty_id):
                    page_id = pa.number
    if page_id:
        try:
            entries = page.page(page_id)
        except PageNotAnInteger:
            entries = page.page(1)
        except EmptyPage:
            entries = page.page(1)
    else:
        entries = page.page(1)
    entries_images = []
    entries_files = []
    for entry in entries:
        entry_image = Entryimage.objects.filter(entry_image=entry)
        entry_file = Entryfiile.objects.filter(entry_file=entry)
        x = {entry.id: entry_image}
        y = {entry.id: entry_file}
        entries_images.append(x)
        entries_files.append(y)
    context = {'topic': topic, 'entries': entries, 'paginator': page, 'entries_images': entries_images,
               'entries_files': entries_files}
    return render(request, 'blog/gxentry.html', context)


@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('blog:topics'))
    context = {'form': form}
    return render(request, 'blog/new_topic.html', context)


@login_required
def entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.owner = request.user
            new_entry.save()
            return HttpResponseRedirect(reverse('blog:topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'blog/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topicit = entry.topic
    check_topic_owner(topicit.owner, request.user, topicit.is_publish)
    if check_entry_owner(request, entry.owner) != True:
        return render(request, 'blog/error_entry.html')
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            with app.test_request_context():
                return redirect(url_for('topic', topic_id=topicit.id, entry_id=entry_id))
    context = {'entry': entry, 'topic': topicit, 'form': form}
    return render(request, 'blog/edit_entry.html', context)


@login_required
def del_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if check_entry_owner(request, entry.owner) == True:
        entry.delete()
        return HttpResponseRedirect(reverse('blog:topic', args=[topic.id]))
    else:
        return render(request, 'blog/error_entry.html')


@login_required
def del_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if check_topicdel_owner(request, topic.owner) == True:
        topic.delete()
        return HttpResponseRedirect(reverse('blog:topics'))
    else:
        return render(request, 'blog/error_entry.html')


@receiver(pre_delete, sender=Entryimage)
def delete_image(sender, instance, **kwargs):
    instance.image.delete(save=False)


@login_required
def edit_entry_image(request, topic_id, entry_id):
    entry = Entry.objects.get(id=entry_id)
    if check_entry_owner(request, entry.owner) != True:
        return render(request, 'blog/error_entry.html')
    if request.method != 'POST':
        imform = EntryimageForm()
    else:
        imform = EntryimageForm(data=request.POST, files=request.FILES)
        if imform.is_valid():
            new_entyimage = imform.save(commit=False)
            new_entyimage.entry_image_id = entry.id
            new_entyimage.save()
            with app.test_request_context():
                return redirect(url_for('topic', topic_id=topic_id, entry_id=entry_id))
    context = {'topic_id': topic_id, 'entry': entry, 'imform': imform}
    return render(request, 'blog/entry_image.html', context)


@login_required
def del_entry_image(request, topic_id, entry_id, entry_image_id):
    enty_image = Entryimage.objects.get(id=entry_image_id)
    entry = Entry.objects.get(id=entry_id)
    if check_entry_owner(request, entry.owner) != True:
        return render(request, 'blog/error_entry.html')
    enty_image.delete()
    with app.test_request_context():
        return redirect(url_for('topic', topic_id=topic_id, entry_id=entry_id))


@login_required
def edit_entry_file(request, topic_id, entry_id):
    entry = Entry.objects.get(id=entry_id)
    if check_entry_owner(request, entry.owner) != True:
        return render(request, 'blog/error_entry.html')
    if request.method != 'POST':
        ifform = EntryfileForm()
    else:
        ifform = EntryfileForm(data=request.POST, files=request.FILES)
        if ifform.is_valid():
            new_entryfile = ifform.save(commit=False)
            new_entryfile.entry_file_id = entry.id
            new_entryfile.save()
            with app.test_request_context():
                return redirect(url_for('topic', topic_id=topic_id, entry_id=entry_id))
    context = {'topic_id': topic_id, 'entry': entry, 'ifform': ifform}
    return render(request, 'blog/edit_file.html', context)


@receiver(pre_delete, sender=Entryfiile)
def delete_image(sender, instance, **kwargs):
    instance.file.delete(save=False)


@login_required
def del_entry_file(request, topic_id, entry_id, entry_file_id):
    entry_file = Entryfiile.objects.get(id=entry_file_id)
    entry = Entry.objects.get(id=entry_id)
    if check_entry_owner(request, entry.owner) != True:
        return render(request, 'blog/error_entry.html')
    entry_file.delete()
    with app.test_request_context():
        return redirect(url_for('topic', topic_id=topic_id, entry_id=entry_id))


@login_required
def hzzj(requset):
    return render(requset, 'blog/hzzj.html')


@csrf_exempt
def ajax_bthz_handle(request):
    response = HttpResponse()
    response['Content-Type'] = "text/json"
    stardate = request.POST.get("star_date")
    enddate = request.POST.get("end_date")
    entries = Entry.objects.filter(Q(is_publish=True), date__range=(stardate, enddate)).order_by('topic_id', '-date')
    x=[]
    for entry in entries:
        entryimages=Entryimage.objects.filter(entry_image_id=entry.id)
        entryfiles=Entryfiile.objects.filter(entry_file_id=entry.id)
        img_url=[]
        file_url=[]
        if entryimages:
            for entryimage in entryimages:
                img_url.append(entryimage.image.url)

        if entryfiles:
            for entryfile in entryfiles:
                file_url.append(entryfile.file.url)
        if not entry.topic.is_publish:
            str="未公开主题"
        else:
            str=entry.topic.text
        y={
            'topic':str,
            'entry':entry.text,
            'date':entry.date.strftime("%Y-%m-%d %H:%M:%S"),
            'owner':entry.owner.userinfo.nametext,
            'image_url':img_url,
            'file_url':file_url,
        }
        x.append(y)
    d={"total":entries.count(),
        "rows":x
           }
    if d:
        data=json.dumps(d)
        return HttpResponse(data)
    else:
        return ""
@csrf_exempt
def ajax_grhz_handle(request):
    response = HttpResponse()
    response['Content-Type'] = "text/json"
    stardate = request.POST.get("star_date")
    enddate = request.POST.get("end_date")
    entries = Entry.objects.filter(Q(owner=request.user), date__range=(stardate, enddate)).order_by('-date')
    x=[]
    for entry in entries:
        entryimages=Entryimage.objects.filter(entry_image_id=entry.id)
        entryfiles=Entryfiile.objects.filter(entry_file_id=entry.id)
        img_url=[]
        file_url=[]
        if entryimages:
            for entryimage in entryimages:
                img_url.append(entryimage.image.url)

        if entryfiles:
            for entryfile in entryfiles:
                file_url.append(entryfile.file.url)
        if not entry.is_publish:
             str="公开"
        else:
             str="私有"
        y={
            'topic':entry.topic.text,
            'entry':entry.text,
            'date':entry.date.strftime("%Y-%m-%d %H:%M:%S"),
            'owner':entry.owner.userinfo.nametext,
            'is_publish': str,
            'image_url':img_url,
            'file_url':file_url,

        }
        x.append(y)
    d={"total":entries.count(),
        "rows":x
           }
    if d:
        data=json.dumps(d)
        return HttpResponse(data)
    else:
        return ""
@csrf_exempt
def tc_user(request,topic_id):
    response = HttpResponse()
    response['Content-Type'] = "text/json"
    user_id = request.POST.get("user_id")
    userinfo=Userinfo.objects.get(owner=int(user_id))
    y={}
    if userinfo:
        if userinfo.ryimage:
            image_url=userinfo.ryimage.url
        else:
            image_url=""
        y={
            'name':userinfo.nametext,
            'dw':userinfo.dwtext,
            'imag_url':image_url
        }
    if y:

       data = json.dumps(y)
       return HttpResponse(data)

    else:
        return ""


if __name__ == '__main__':
    app.run(debug=True)
