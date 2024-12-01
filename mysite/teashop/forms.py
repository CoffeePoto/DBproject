from django import forms
from .models import MemberInfo

###로그인 무결성 확인
class SignupForm(forms.Form):
    ID = forms.CharField(max_length=10, required=True, label='ID')
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='password')
    
    def clean_name(self):
        ID = self.cleaned_data['ID']
        if MemberInfo.objects.filter(memID=ID).exists():
            raise forms.ValidationError("이미 사용 중인 ID입니다.")
        return ID