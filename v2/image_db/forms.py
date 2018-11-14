from django import forms
from django.contrib import auth
from .models import Images
from django.utils.safestring import mark_safe

User = auth.get_user_model()


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label="",
                               widget=forms.TextInput(attrs={"class": "form-control",
                                                             "placeholder": "Email"}))
    password = forms.CharField(label="",
                               widget=forms.PasswordInput(attrs={"class": "form-control",
                                                                 "placeholder": "Введите пароль"}))
    password2 = forms.CharField(label="",
                                widget=forms.PasswordInput(attrs={"class": "form-control",
                                                                  "placeholder": "Подтвердите пароль"}))

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            'password2',
        ]

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        username_qs = User.objects.filter(username=username)
        if username_qs.exists():
            raise forms.ValidationError("Этот email уже зарегистрирован!")

        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Пароли должны совпадать!")
        return super(UserRegisterForm, self).clean(*args, **kwargs)


class AddImage(forms.ModelForm):

    description = forms.CharField(label="Описание\n",
                                  widget=forms.TextInput(
                                      attrs={"class": "form-control",
                                             "onchange": "readURL(this)"}))
    image = forms.ImageField(label='Изображение\n',
                             widget=forms.FileInput(
                                 attrs={"onchange": "readURL(this)",
                                        "placeholder": "123"}))

    class Meta:
        model = Images
        fields = [
            'description',
            'image',
        ]

    def __init__(self, *args, **kwargs):
        super(AddImage, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False
