from ninja import Schema
from datetime import datetime
from typing import Optional  # Importamos o Optional para os campos que podem ser nulos


class EquipaSchema(Schema):
    id: int
    nome: str
    cidade: str
    AnoFundacao: int
    emblema: Optional[str] = None  # CORREÇÃO: Agora aceita explicitamente None (nulo)

class EquipaInSchema(Schema):
    nome: str
    cidade: str
    AnoFundacao: int



class JogadorSchema(Schema):
    id: int
    nome: str
    idade: int
    posicao: str
    nacionalidade: str
    lesinado: bool
    imagem: Optional[str] = None  # CORREÇÃO: O jogador também pode não ter imagem
    equipa_id: int

class JogadorInSchema(Schema):
    nome: str
    idade: int
    posicao: str
    nacionalidade: str
    lesinado: bool
    equipa_id: int


class JogoSchema(Schema):
    id: int
    equipa_casa_id: int
    equipa_fora_id: int
    data: datetime
    golos_casa: int
    golos_fora: int

class JogoInSchema(Schema):
    equipa_casa_id: int
    equipa_fora_id: int
    data: datetime
    golos_casa: int
    golos_fora: int