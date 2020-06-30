from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User

class LoginForm(forms.Form):
    phone = forms.IntegerField(label= 'Your Phone Number')
    password = forms.CharField(widget=forms.PasswordInput)

class VerifyForm(forms.Form):
    key = forms.IntegerField(label='Please Enter OTP here')


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone',)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        qs = User.object.filter(phone=phone)
        if qs.exists():
            raise forms.ValidationError('phone is taken')
        return phone

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don't match")
        return password2

class TempRegisterForm(forms.Form):
    phone = forms.IntegerField()
    otp = forms.IntegerField()

class SetPasswordForm(forms.Form):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password Confirmation', widget=forms.PasswordInput)


class UserAdminCreationForm(forms.ModelForm):
    '''A form for creating new users.
    Includes all the required fields,
    plus a repeated password'''

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmayion', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone',)

    def clean_password2(self):
        #check that two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        #save the password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data('password1'))
        #user.active = false
        if commit:
            user.save()
            return user


class UserAdminChangeForm(forms.ModelForm):
    '''A form for updating users.
    Includes all the fields on the user,
    but replaces the password field with admin`s
    password hash display field.
    '''

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('phone', 'password', 'active', 'admin')

    def clean_password(self):
        return self.initial('password')
