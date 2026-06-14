from django.db import models
from django.utils import timezone
import secrets

class Equipa(models.Model):
    nome = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    ano_fundacao = models.PositiveIntegerField(name="AnoFundacao") 
    emblema = models.ImageField(upload_to='emblemas/', blank=True, null=True)

    def __str__(self):
        return self.nome


class Jogador(models.Model):
    equipa = models.ForeignKey(Equipa, on_delete=models.CASCADE, related_name='jogadores')
    nome = models.CharField(max_length=100)
    idade = models.PositiveIntegerField() # Idade é guardada mais eficientemente como número inteiro
    posicao = models.CharField(max_length=50)
    nacionalidade = models.CharField(max_length=50)
    imagem = models.ImageField(upload_to='jogadores/', blank=True, null=True)
    lesionado = models.BooleanField(default=False)

    def __str__(self):
        return self.nome


class Jogo(models.Model):
    equipa_casa = models.ForeignKey(Equipa, on_delete=models.CASCADE, related_name='jogos_casa')
    equipa_fora = models.ForeignKey(Equipa, on_delete=models.CASCADE, related_name='jogos_fora')
    data = models.DateTimeField()
    golos_casa = models.PositiveIntegerField()
    golos_fora = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.equipa_casa} {self.golos_casa}-{self.golos_fora} {self.equipa_fora}"


def generate_api_key():
    # Gera uma chave segura e aleatória
    return secrets.token_urlsafe(32)


# modelo para guardar e gerir chaves de acesso
class APIKey(models.Model):
    name = models.CharField(max_length=100, help_text="Nome de quem vai usar a chave")
    key = models.CharField(max_length=255, unique=True, default=generate_api_key)
    is_active = models.BooleanField(default=True)
    expiration_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {'Ativa' if self.is_active else 'Inativa'}"

    def is_valid(self):
        # Verifica se a chave está ativa e se ainda não expirou
        return self.is_active and self.expiration_date > timezone.now()