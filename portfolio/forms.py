from django import forms
from .models import Projeto, Tecnologia, Competencia, Formacao, UnidadeCurricular, Licenciatura

class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = '__all__'

class TecnologiaForm(forms.ModelForm):
    class Meta:
        model = Tecnologia
        fields = '__all__'

class CompetenciaForm(forms.ModelForm):
    class Meta:
        model = Competencia
        fields = '__all__'

class FormacaoForm(forms.ModelForm):
    class Meta:
        model = Formacao
        fields = '__all__'

class UnidadeCurricularForm(forms.ModelForm):
    class Meta:
        model = UnidadeCurricular
        fields = '__all__'

class LicenciaturaForm(forms.ModelForm):
    class Meta:
        model = Licenciatura
        fields = '__all__'