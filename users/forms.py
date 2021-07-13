from django import forms
from .models import Userinfo



class UserinfoForm(forms.ModelForm):
    class Meta:
        model=Userinfo
        fields=['nametext','birdate','zwtext','zwdate','djtext','djdate','zctext','zcdate','dwtext','ryimage']
        labels={'nametext':'姓名','birdate':'出生日期',
                'zwtext':'职务','zwdate':'职务时间',
                'djtext':'待遇等级','djdate':'待遇等级时间',
                'zctext':'职称','zcdate':'职称时间','dwtext':'部门','ryimage':'照片'}

        widgets={
            'birdate':forms.DateInput(format=('%Y-%m-%d'),attrs={'type':'date'}),
            'zwdate':forms.DateInput(format=('%Y-%m-%d'),attrs={'type':'date'}),
            'djdate':forms.DateInput(format=('%Y-%m-%d'),attrs={'type':'date'}),
            'zcdate':forms.DateInput(format=('%Y-%m-%d'),attrs={'type':'date'}),
    }
        ryimage=forms.ImageField(allow_empty_file=True)