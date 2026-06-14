import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto.settings')
django.setup()

from portfolio.models import TFC, Licenciatura

def importar_tfcs():
    caminho = 'data/jsonTFC.json'
    if not os.path.exists(caminho):
        print("Ficheiro não encontrado.")
        return

    with open(caminho, 'r', encoding='utf-8') as f:
        dados = json.load(f)
        for item in dados:
            try:
                ano_str = str(item.get('ano', '2025')).strip()
                ano = int(ano_str)
            except ValueError:
                ano = 2025

            autores_lista = item.get('autores') or []
            orientadores_lista = item.get('orientadores') or []
            areas_lista = item.get('areas') or item.get('palavras_chave') or []

            autores = ", ".join([str(x).strip() for x in autores_lista])
            orientadores = ", ".join([str(x).strip() for x in orientadores_lista])
            areas = ", ".join([str(x).strip() for x in areas_lista])

            nome_json = item.get('curso', 'Sem Curso Especificado')
            
            mapa_cursos = {
                "Licenciatura em Engenharia Informática": "Engenharia Informática (LEI)",
                "Licenciatura em Informática de Gestão": "Informática de Gestão (LIG)",
                "Licenciatura em Ciência de Dados": "Ciência de Dados",
                "Licenciatura em Computação e Matemática Aplicada": "Computação e Matemática Aplicada"
            }
            
            nome_oficial = mapa_cursos.get(nome_json, nome_json)
            
            licenciatura_obj, created = Licenciatura.objects.get_or_create(
                nome=nome_oficial,
                defaults={'apresentacao': f'Apresentação de {nome_oficial}.'}
            )

            TFC.objects.get_or_create(
                titulo=item.get('titulo', 'Sem Título'),
                autores=autores,
                orientadores=orientadores,
                licenciatura=licenciatura_obj,
                ano=ano,
                resumo=item.get('resumo', ''),
                link_pdf=item.get('pdf', ''),
                link_imagem=item.get('imagem', ''),
                areas=areas
            )
            
    print("TFCs importados com sucesso!")

if __name__ == '__main__':
    importar_tfcs()