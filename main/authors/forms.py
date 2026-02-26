from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


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
        required=False,  # 🔥 agora é opcional (importante para edição)
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

        # Remove atributo required automático do HTML
        for field in self.fields:
            self.fields[field].widget.attrs.pop("required", None)

    # 🔥 Corrigido para não acusar duplicado na edição
    def clean_username(self):
        username = self.cleaned_data.get("username")

        qs = User.objects.filter(username=username)

        # Se estiver editando, ignora o próprio usuário
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError("Esse usuário já existe.")

        return username

    # 🔥 Corrigido para não acusar duplicado na edição
    def clean_email(self):
        email = self.cleaned_data.get("email")

        qs = User.objects.filter(email=email)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError("Esse e-mail já está cadastrado.")

        return email

    # 🔥 Senha opcional na edição
    def clean_password(self):
        password = self.cleaned_data.get("password")

        # Se estiver editando e não digitou senha → mantém a atual
        if not password:
            return password

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
