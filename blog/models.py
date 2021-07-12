from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone as timezone

# Create your models here.
class Topic(models.Model):
    """用户工作的主题"""
    text=models.CharField(max_length=200)
    date_add=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    is_publish=models.BooleanField(blank=False)
    def __str__(self):
        return self.text
class Entry(models.Model):
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE)
    text=models.TextField()
    date=models.DateTimeField(default=timezone.now)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    is_publish=models.BooleanField(blank=False)
    class Meta:
        verbose_name_plural='entries'
    def __str__(self):
        return self.text[:50]

class Entryimage(models.Model):
    entry_image=models.ForeignKey(Entry,on_delete=models.CASCADE)
    image=models.ImageField(verbose_name='entryimage',null=True,upload_to='entryimg/',blank=True)
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
           return self.image.url
class Entryfiile(models.Model):
    entry_file=models.ForeignKey(Entry,on_delete=models.CASCADE)
    file=models.FileField(verbose_name='entryfile',null=True,upload_to='entryfile/',blank=True)
    def file_url(self):
        if self.file and hasattr(self.file,'url'):
            return self.file.url

