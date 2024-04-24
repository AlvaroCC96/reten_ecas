from django import forms

class CustomLoginForm(forms.Form):
    email = forms.EmailField(label='Usuario', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'email'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password'}))
