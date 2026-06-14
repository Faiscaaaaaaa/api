from django.db import models

class Licenciatura(models.Model):
    nome = models.CharField(max_length=100)
    apresentacao = models.TextField()
    logo = models.ImageField(upload_to='licenciaturas/', blank=True)

    class Meta:
        verbose_name_plural = "Licenciaturas"

    def __str__(self):
        return self.nome

class UnidadeCurricular(models.Model):
    nome = models.CharField(max_length=100)
    ano = models.IntegerField()
    semestre = models.IntegerField()
    ects = models.IntegerField()
    imagem = models.ImageField(upload_to='ucs/', blank=True, null=True) 
    docente_nome = models.CharField(max_length=100, blank=True, null=True)
    docente_link_lusofona = models.URLField(blank=True, null=True) 
    licenciatura = models.ForeignKey(Licenciatura, on_delete=models.CASCADE, related_name='ucs')

    class Meta:
        verbose_name_plural = "Unidades Curriculares"

    def __str__(self):
        return self.nome

class TipoTecnologia(models.Model):
    nome = models.CharField(max_length=50) # Ex: Frontend, Backend, Base de Dados, Storage, Outros

    def __str__(self):
        return self.nome

class Tecnologia(models.Model):
    nome = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='tecnologias/', blank=True)
    descricao = models.TextField(blank=True, help_text="O que faz, o que permite, o que gostou/não gostou.")
    link_oficial = models.URLField(blank=True, null=True) 
    nivel_interesse = models.IntegerField(default=1, help_text="Escala de 1 a 5") 
    tipo = models.ForeignKey(TipoTecnologia, on_delete=models.SET_NULL, null=True, related_name='tecnologias')
    
    class Meta:
        verbose_name_plural = "Tecnologias"

    def __str__(self):
        return self.nome

class Projeto(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    conceitos_aplicados = models.TextField(blank=True, null=True) 
    imagem = models.ImageField(upload_to='projetos/', blank=True)
    video_demo = models.URLField(blank=True, null=True) 
    github_link = models.URLField(blank=True, null=True) 
    uc = models.ForeignKey(UnidadeCurricular, on_delete=models.CASCADE)
    tecnologias = models.ManyToManyField(Tecnologia, blank=True, related_name="projetos")

    class Meta:
        verbose_name_plural = "Projetos"
        
    def __str__(self):
        return self.titulo

class TFC(models.Model):
    titulo = models.CharField(max_length=200)
    autores = models.CharField(max_length=200)
    orientadores = models.CharField(max_length=200)
    licenciatura = models.ForeignKey(Licenciatura, on_delete=models.CASCADE, related_name='tfcs', null=True, blank=True)
    ano = models.IntegerField()
    resumo = models.TextField()
    link_pdf = models.URLField(blank=True, null=True)
    link_imagem = models.URLField(blank=True, null=True)
    areas = models.CharField(max_length=200, blank=True)
    destaque = models.BooleanField(default=False, help_text="Marcar para destacar na página principal")

    class Meta:
        verbose_name_plural = "TFCs"

    def __str__(self):
        return self.titulo

class Competencia(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    projetos_associados = models.ManyToManyField(Projeto, blank=True) 
    tecnologias_associadas = models.ManyToManyField(Tecnologia, blank=True)
    
    class Meta:
        verbose_name_plural = "Competências"

    def __str__(self):
        return self.nome

class Formacao(models.Model):
    titulo = models.CharField(max_length=100)
    instituicao = models.CharField(max_length=100)
    ano = models.IntegerField()
    descricao = models.TextField(blank=True)

    class Meta:
        ordering = ['-ano']
        verbose_name_plural = "Formações"

    def __str__(self):
        return self.titulo

class MakingOf(models.Model):
    titulo = models.CharField(max_length=100)
    data = models.DateTimeField(auto_now_add=True)
    descricao_processo = models.TextField(help_text="Descrição de decisões e justificação de modelos (Pode usar Markdown)")
    erros_encontrados = models.TextField(blank=True, help_text="Erros encontrados e respetivas correções (Pode usar Markdown)")
    uso_ia = models.TextField(blank=True, help_text="Como a IA contribuiu (ou não) para o processo") 
    imagem_caderno = models.ImageField(upload_to='makingof/', blank=True, null=True, help_text="Registo em papel, DER, etc.")

    class Meta:
        verbose_name_plural = "Making Of"

    def __str__(self):
        return self.titulo
    
class InteressePessoal(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='interesses/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Interesses Pessoais"
        
    def __str__(self):
        return self.nome