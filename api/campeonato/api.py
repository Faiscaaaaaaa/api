from typing import List
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from ninja.security import APIKeyHeader

from .models import Equipa, Jogador, Jogo, APIKey
from .schemas import (
    EquipaSchema, EquipaInSchema,
    JogadorSchema, JogadorInSchema,
    JogoSchema, JogoInSchema
)

api = NinjaAPI(
    title="Campeonato",
    description="API para ver um campeonato",
    version="1.0.0",
    docs_url="/docs/",
    openapi_url="/openapi.json",
)


class AuthAPIKey(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key: str):
        try:
            api_key = APIKey.objects.get(key=key)
            if api_key.is_valid():
                return api_key.name
        except APIKey.DoesNotExist:
            pass
        return None


@api.get("/equipas", response=List[EquipaSchema], tags=["Equipas"])
def listar_equipas(request):
    return Equipa.objects.all()


@api.get("/equipas/{equipa_id}", response=EquipaSchema, tags=["Equipas"])
def obter_equipa(request, equipa_id: int):
    return get_object_or_404(Equipa, id=equipa_id)


@api.post("/equipas", response=EquipaSchema, tags=["Equipas"], auth=AuthAPIKey())
def criar_equipa(request, payload: EquipaInSchema):
    equipa = Equipa.objects.create(**payload.dict())
    return equipa


@api.put("/equipas/{equipa_id}", response=EquipaSchema, tags=["Equipas"], auth=AuthAPIKey())
def atualizar_equipa(request, equipa_id: int, payload: EquipaInSchema):
    equipa = get_object_or_404(Equipa, id=equipa_id)
    for attr, value in payload.dict().items():
        setattr(equipa, attr, value)
    equipa.save()
    return equipa


@api.delete("/equipas/{equipa_id}", tags=["Equipas"], auth=AuthAPIKey())
def eliminar_equipa(request, equipa_id: int):
    equipa = get_object_or_404(Equipa, id=equipa_id)
    equipa.delete()
    return {"sucesso": True, "mensagem": "Equipa eliminada com sucesso."}


@api.get("/jogadores", response=List[JogadorSchema], tags=["Jogadores"])
def listar_jogadores(request):
    return Jogador.objects.all()


@api.post("/jogadores", response=JogadorSchema, tags=["Jogadores"], auth=AuthAPIKey())
def criar_jogador(request, payload: JogadorInSchema):
    jogador = Jogador.objects.create(**payload.dict())
    return jogador


@api.put("/jogadores/{jogador_id}", response=JogadorSchema, tags=["Jogadores"], auth=AuthAPIKey())
def atualizar_jogador(request, jogador_id: int, payload: JogadorInSchema):
    jogador = get_object_or_404(Jogador, id=jogador_id)
    for attr, value in payload.dict().items():
        setattr(jogador, attr, value)
    jogador.save()
    return jogador


@api.delete("/jogadores/{jogador_id}", tags=["Jogadores"], auth=AuthAPIKey())
def eliminar_jogador(request, jogador_id: int):
    jogador = get_object_or_404(Jogador, id=jogador_id)
    jogador.delete()
    return {"sucesso": True, "mensagem": "Jogador eliminado com sucesso."}


@api.get("/jogos", response=List[JogoSchema], tags=["Jogos"])
def listar_jogos(request):
    return Jogo.objects.all()


@api.post("/jogos", response=JogoSchema, tags=["Jogos"], auth=AuthAPIKey())
def criar_jogo(request, payload: JogoInSchema):
    jogo = Jogo.objects.create(**payload.dict())
    return jogo


@api.put("/jogos/{jogo_id}", response=JogoSchema, tags=["Jogos"], auth=AuthAPIKey())
def atualizar_jogo(request, jogo_id: int, payload: JogoInSchema):
    jogo = get_object_or_404(Jogo, id=jogo_id)
    for attr, value in payload.dict().items():
        setattr(jogo, attr, value)
    jogo.save()
    return jogo


@api.delete("/jogos/{jogo_id}", tags=["Jogos"], auth=AuthAPIKey())
def eliminar_jogo(request, jogo_id: int):
    jogo = get_object_or_404(Jogo, id=jogo_id)
    jogo.delete()
    return {"sucesso": True, "mensagem": "Jogo eliminado com sucesso."}
