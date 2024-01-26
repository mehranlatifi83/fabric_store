from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import MyUser, Fabric

class UserLoginForm(forms.Form):
    phone = forms.CharField()

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='پسورد', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تایید پسورد', widget=forms.PasswordInput)
    is_admin = forms.BooleanField(label='وضعیت ادمین بودن', required=False)
    class Meta:
        model = MyUser
        fields = ('phone', 'first_name', 'last_name', 'is_admin')
        labels = {
            "first_name": "نام",
            "last_name": "نام خانوادگی",
            "phone": "شماره تلفن",
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
class FabricForm(forms.ModelForm):
    class Meta:
        model = Fabric
        fields = ['name']
        labels = {
            "name": "نام پارچه",
        }