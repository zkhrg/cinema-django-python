from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'имя'}))
    second_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'фамилия'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'повторите пароль'}))

    # переопределяем метод сохранения, чтобы он сохранял юзернейм как емаил
    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.username = self.cleaned_data['email']

        if User.objects.filter(username=user.username).exists():
            raise forms.ValidationError("Пользователь с таким email уже зарегистрирован")
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['first_name', 'second_name', 'email', 'password1', 'password2']