from django.db import models
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Artigo(models.Model):
    titulo = models.CharField(max_length=200)
    texto = models.TextField()
    fotografia = models.ImageField(upload_to='artigos/', blank=True, null=True)
    link_externo = models.URLField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artigos')

    class Meta:
        ordering = ['-data_criacao']
        verbose_name_plural = "Artigos"

    def __str__(self):
        return self.titulo

    def total_likes(self):
        return self.likes.count()

    def total_comentarios(self):
        return self.comentarios.count()

    def rating_count(self):
        return self.ratings.count()

    def average_rating(self):
        average = self.ratings.aggregate(Avg('valor'))['valor__avg']
        return round(average, 1) if average is not None else None


class Like(models.Model):
    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name='likes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('artigo', 'usuario')
        verbose_name_plural = "Likes"

    def __str__(self):
        return f"{self.usuario.username} gostou de {self.artigo.titulo}"


class Comentario(models.Model):
    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    autor_nome = models.CharField(max_length=100, blank=True)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data_criacao']
        verbose_name_plural = "Comentários"

    def __str__(self):
        autor = self.autor.username if self.autor else self.autor_nome or 'Visitante'
        return f"Comentário de {autor} em {self.artigo.titulo}"


class Rating(models.Model):
    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name='ratings')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    valor = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_criacao']
        verbose_name_plural = "Avaliações"

    def __str__(self):
        usuario = self.usuario.username if self.usuario else 'Visitante'
        return f"{self.valor} estrelas para {self.artigo.titulo} por {usuario}"
