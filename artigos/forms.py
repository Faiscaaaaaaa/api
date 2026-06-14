from django import forms
from .models import Artigo, Comentario, Rating


class ArtigoForm(forms.ModelForm):
    class Meta:
        model = Artigo
        fields = ['titulo', 'texto', 'fotografia', 'link_externo']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título do artigo'
            }),
            'texto': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Conteúdo do artigo',
                'rows': 10
            }),
            'fotografia': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'link_externo': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://exemplo.com (opcional)'
            }),
        }


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['autor_nome', 'texto']
        widgets = {
            'autor_nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seu nome (opcional)'
            }),
            'texto': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escreva seu comentário...',
                'rows': 4
            }),
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['valor']
        widgets = {
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5,
                'step': 1,
                'placeholder': '1 a 5'
            }),
        }
        labels = {
            'valor': 'Pontuação (1-5)'
        }
