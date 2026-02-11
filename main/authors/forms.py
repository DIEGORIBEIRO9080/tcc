from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms

class RegisterForm(forms.ModelForm):

    ROLE_CHOICES = (
        ('Leitor', 'Leitor'),
        ('Criador', 'Criador'),
        ('Editor', 'Editor'),
        ('Admin', 'Administrador'),
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        label="Tipo de usuário",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        label="Senha",
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # REMOVE required automático do HTML
        for field in self.fields:
            self.fields[field].widget.attrs.pop("required", None)

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if User.objects.filter(username=username).exists():
            raise ValidationError("Esse usuário já existe.")

        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise ValidationError("Esse e-mail já está cadastrado.")

        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if len(password) < 8:
            raise ValidationError("A senha deve ter pelo menos 8 caracteres.")

        if password.isdigit():
            raise ValidationError("A senha não pode conter apenas números.")

        return password

# authors/forms.py



class LoginForm(forms.Form):
    username = forms.CharField(
        label="Usuário",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu usuário'})
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite sua senha'})
    )
