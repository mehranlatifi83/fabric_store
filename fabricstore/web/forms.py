from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import MyUser, Fabric, Address, City, State

class UserLoginForm(forms.Form):
    phone = forms.CharField()

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='پسورد', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تایید پسورد', widget=forms.PasswordInput)
    is_admin = forms.BooleanField(label='وضعیت ادمین بودن', required=False)
    class Meta:
        model = MyUser
        fields = ('phone', 'first_name', 'last_name', 'is_admin', 'email')
        labels = {
            "first_name": "نام",
            "last_name": "نام خانوادگی",
            "phone": "شماره تلفن",
            "email": "ایمیل",
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
        fields = ['name', 'price', 'description', 'image', 'category']
        labels = {
            "name": "نام پارچه",
            "price": "قیمت هر متر پارچه",
            "description": "توضیحات راجع به محصول",
            "image": "عکس پارچه",
            "category": "دسته بندی محصول",
        }

class AddressForm(forms.ModelForm):
    state = forms.ModelChoiceField(queryset=State.objects.all(), empty_label="انتخاب استان", label="استان")
    city = forms.ModelChoiceField(queryset=City.objects.none(), empty_label="انتخاب شهرستان", label="شهر")

    class Meta:
        model = Address
        fields = ['state', 'city', 'zipcode', 'address']
        labels = {
            "zipcode": "کد پستی",
            "address": "آدرس کامل",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['city'].queryset = City.objects.filter(state=self.instance.state).order_by('name')
        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset

class EmailChangeForm(forms.Form):
    email = forms.EmailField(label='ایمیل جدید')