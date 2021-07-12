from django import forms
from .models import Topic,Entry,Entryimage,Entryfiile
from bootstrap3_datetime.widgets import DateTimePicker
class TopicForm(forms.ModelForm):
    class Meta:
        model=Topic
        fields=['text','is_publish']
        labels={'text':'','is_publish':'是否共享工作主题'}
        widgets={
           'is_publish':forms.RadioSelect(choices=[(True,'是'),(False,'否')])
        }
class EntryForm(forms.ModelForm):
    class Meta:
       model=Entry
       fields=['date','text','is_publish']
       labels={'date':'日期','text':'','is_publish':'是否共享工作条目'}
       widgets={'text':forms.Textarea(attrs={'col':400,'row':400}),
                'is_publish':forms.RadioSelect(choices=[(True,'是'),(False,'否')],),
                'date':DateTimePicker(options={"format": "YYYY-MM-DD HH:mm",
                                       "pickSeconds": False,
                                       "language":"zh-CN"
                                               })

       }

class EntryimageForm(forms.ModelForm):
    class Meta:
       model=Entryimage
       fields=['image']
       labels={'image':'图片'}

class EntryfileForm(forms.ModelForm):
    class Meta:
       model=Entryfiile
       fields=['file']
       labels={'file':'文件'}