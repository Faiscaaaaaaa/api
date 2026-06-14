"""
Comando de gestão Django para carregar dados da Liga Portugal 24/25.

Coloca este ficheiro em:
    <app>/management/commands/load_liga.py

Garante que existe um ficheiro __init__.py em:
    <app>/management/__init__.py
    <app>/management/commands/__init__.py

Uso:
    python manage.py load_liga
    python manage.py load_liga --json outro_ficheiro.json
    python manage.py load_liga --limpar   # apaga tudo antes de carregar
"""

import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

# Ajusta o import consoante o nome da tua app
from campeonato.models import Equipa, Jogador, Jogo  # noqa: E402


class Command(BaseCommand):
    help = "Carrega equipas, jogadores e jogos da Liga Portugal 24/25 a partir de um JSON."

    def add_arguments(self, parser):
        parser.add_argument(
            "--json",
            default="liga_portugal_2425.json",
            help="Caminho para o ficheiro JSON (default: liga_portugal_2425.json)",
        )
        parser.add_argument(
            "--limpar",
            action="store_true",
            help="Apaga todos os registos existentes antes de carregar.",
        )

    def handle(self, *args, **options):
        json_path = Path(options["json"])
        if not json_path.exists():
            raise CommandError(f"Ficheiro não encontrado: {json_path}")

        with open(json_path, encoding="utf-8") as f:
            dados = json.load(f)

        with transaction.atomic():
            if options["limpar"]:
                Jogo.objects.all().delete()
                Jogador.objects.all().delete()
                Equipa.objects.all().delete()
                self.stdout.write(self.style.WARNING("Registos existentes apagados."))

            # ── 1. Equipas ──────────────────────────────────────────────────
            equipas_map = {}
            criadas = 0
            for eq in dados.get("equipas", []):
                obj, created = Equipa.objects.get_or_create(
                    nome=eq["nome"],
                    defaults={
                        "cidade": eq["cidade"],
                        "AnoFundacao": eq["AnoFundacao"],
                    },
                )
                equipas_map[eq["nome"]] = obj
                if created:
                    criadas += 1

            self.stdout.write(
                self.style.SUCCESS(f"Equipas: {criadas} criadas, {len(equipas_map) - criadas} já existiam.")
            )

            # ── 2. Jogadores ─────────────────────────────────────────────────
            jogadores_criados = 0
            jogadores_skip = 0
            for jg in dados.get("jogadores", []):
                equipa = equipas_map.get(jg["equipa"])
                if not equipa:
                    self.stdout.write(
                        self.style.WARNING(f"  Equipa não encontrada para jogador '{jg['nome']}': {jg['equipa']}")
                    )
                    continue

                _, created = Jogador.objects.get_or_create(
                    nome=jg["nome"],
                    equipa=equipa,
                    defaults={
                        "idade": jg["idade"],
                        "posicao": jg["posicao"],
                        "nacionalidade": jg["nacionalidade"],
                        "lesionado": jg.get("lesionado", False),
                    },
                )
                if created:
                    jogadores_criados += 1
                else:
                    jogadores_skip += 1

            self.stdout.write(
                self.style.SUCCESS(f"Jogadores: {jogadores_criados} criados, {jogadores_skip} já existiam.")
            )

            # ── 3. Jogos ─────────────────────────────────────────────────────
            from django.utils.dateparse import parse_datetime

            jogos_criados = 0
            jogos_skip = 0
            for jogo in dados.get("jogos", []):
                casa = equipas_map.get(jogo["equipa_casa"])
                fora = equipas_map.get(jogo["equipa_fora"])

                if not casa or not fora:
                    self.stdout.write(
                        self.style.WARNING(
                            f"  Equipa não encontrada para jogo: {jogo['equipa_casa']} vs {jogo['equipa_fora']}"
                        )
                    )
                    continue

                data = parse_datetime(jogo["data"])

                _, created = Jogo.objects.get_or_create(
                    equipa_casa=casa,
                    equipa_fora=fora,
                    data=data,
                    defaults={
                        "golos_casa": jogo["golos_casa"],
                        "golos_fora": jogo["golos_fora"],
                    },
                )
                if created:
                    jogos_criados += 1
                else:
                    jogos_skip += 1

            self.stdout.write(
                self.style.SUCCESS(f"Jogos: {jogos_criados} criados, {jogos_skip} já existiam.")
            )

        self.stdout.write(self.style.SUCCESS("\n✓ Dados carregados com sucesso!"))
