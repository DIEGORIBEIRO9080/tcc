from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    
    ROLE_CHOICES = (
        ('Leitor', 'Leitor'),
        ('Criador', 'Criador'),
        ('Editor', 'Editor'),
        ('Admin', 'Administrador'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Tipo de usuário")

    class Meta:
        model= User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
