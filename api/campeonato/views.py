from django.shortcuts import redirect, render
from django.urls import reverse
import requests
from urllib3.exceptions import InsecureRequestWarning

# A API do colega usa um certificado que não é verificado pelo ambiente local.
# Aqui desativamos o warning apenas para estas chamadas externas.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Configurar aqui o endereço da API do colega e a chave (substituam quando for usar)
URL_API_COLEGA = "https://pedro-prata-21807403.pw.deisi.ulusofona.pt/api/eventos"
CHAVE_COLEGA = "KrZpAo0JLMmlxFGGUepr44JxZiL0atPTgbie5TnFZtE"
API_DOCS_COLEGA = "https://pedro-prata-21807403.pw.deisi.ulusofona.pt/api/docs"
API_PODE_EDITAR = True


def api_redirect_to_docs(request):
    return redirect('/api/docs/')


def pagina_colega(request):
    ordering = request.GET.get("ordering")
    search = request.GET.get("search")
    params = {}
    if search:
        params["titulo"] = search

    def _filtrar_dados(dados, search_text, ordering_value):
        if dados is None:
            return None

        if isinstance(dados, dict) and "results" in dados and isinstance(dados["results"], list):
            lista = dados["results"]
        elif isinstance(dados, list):
            lista = dados
        else:
            return dados

        if search_text:
            termo = search_text.strip().lower()

            def item_match(item):
                for campo in ("titulo", "title", "name", "description", "nome"):
                    valor = item.get(campo)
                    if isinstance(valor, str) and termo in valor.lower():
                        return True
                return False

            lista = [item for item in lista if item_match(item)]

        if ordering_value:
            reverse_order = ordering_value.startswith("-")
            campo = ordering_value.lstrip("-")
            if campo == "id":
                lista = sorted(lista, key=lambda item: item.get("id", 0), reverse=reverse_order)

        if isinstance(dados, dict) and "results" in dados and isinstance(dados["results"], list):
            dados["results"] = lista
            return dados
        return lista

    if "[IP_DO_COLEGA]" in URL_API_COLEGA or "COLOQUEM_A_CHAVE_AQUI" in CHAVE_COLEGA:
        dados = None
        erro = (
            "É necessário substituir o placeholder da API do colega. "
            "Abra `campeonato/views.py` e defina `URL_API_COLEGA` com o URL real da API "
            "do colega e `CHAVE_COLEGA` com a chave fornecida."
        )
    else:
        headers = {"X-API-Key": CHAVE_COLEGA}
        try:
            resposta = requests.get(URL_API_COLEGA, headers=headers, params=params, timeout=5, verify=False)
            if resposta.status_code == 200:
                dados = resposta.json()
                dados = _filtrar_dados(dados, search, ordering)
                erro = None
            else:
                dados = None
                erro = f"Erro na API: {resposta.status_code} - {resposta.text}"
        except requests.exceptions.RequestException as e:
            dados = None
            erro = f"Não foi possível conectar à API do colega. Detalhe: {e}"

    def _dados_para_lista(dados):
        if isinstance(dados, dict) and "results" in dados and isinstance(dados["results"], list):
            return dados["results"]
        if isinstance(dados, list):
            return dados
        return []

    contexto = {
        "dados_colega": dados,
        "dados_lista": _dados_para_lista(dados),
        "erro": erro,
        "ordering": ordering or "",
        "search": search or "",
        "api_base": URL_API_COLEGA,
        "api_docs": API_DOCS_COLEGA,
    }
    return render(request, "portfolio/pagina_colega.html", contexto)


def projetos_list(request):
    ordering = request.GET.get("ordering")
    search = request.GET.get("search")
    params = {}
    if search:
        params["titulo"] = search

    headers = {"X-API-Key": CHAVE_COLEGA}
    try:
        r = requests.get(URL_API_COLEGA, headers=headers, params=params, timeout=5, verify=False)
        r.raise_for_status()
        itens = r.json()
        if isinstance(itens, list):
            if search:
                termo = search.strip().lower()
                itens = [item for item in itens if any(
                    isinstance(item.get(campo), str) and termo in item.get(campo).lower()
                    for campo in ("titulo", "title", "name", "sinopse", "description", "nome")
                )]
            if ordering and ordering.lstrip("-") == "id":
                reverse_order = ordering.startswith("-")
                itens = sorted(itens, key=lambda item: item.get("id", 0), reverse=reverse_order)
        erro = None
    except requests.exceptions.RequestException as e:
        itens = []
        erro = str(e)

    return render(request, "portfolio/projetos_list.html", {
        "itens": itens,
        "erro": erro,
        "ordering": ordering or "",
        "search": search or "",
        "api_docs": API_DOCS_COLEGA,
    })


def projetos_detail(request, item_id):
    headers = {"X-API-Key": CHAVE_COLEGA}
    url = f"{URL_API_COLEGA}/{item_id}"

    if request.method == "POST":
        payload = request.POST.dict()
        try:
            r = requests.put(url, headers=headers, json=payload, timeout=5, verify=False)
            r.raise_for_status()
            return redirect(reverse('projetos_list'))
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 401:
                erro = "Não autorizado: a API do colega recusou a atualização com esta chave."
            else:
                erro = str(e)
            item = None
            return render(request, "portfolio/projeto_detail.html", {"item": item, "erro": erro})
        except requests.exceptions.RequestException as e:
            erro = f"Não foi possível conectar à API do colega. Detalhe: {e}"
            item = None
            return render(request, "portfolio/projeto_detail.html", {"item": item, "erro": erro, "edit_allowed": API_PODE_EDITAR})

    try:
        r = requests.get(url, headers=headers, timeout=5, verify=False)
        r.raise_for_status()
        item = r.json()
        erro = None
    except requests.exceptions.RequestException as e:
        item = None
        erro = str(e)

    return render(request, "portfolio/projeto_detail.html", {"item": item, "erro": erro, "edit_allowed": API_PODE_EDITAR})


def projetos_create(request):
    headers = {"X-API-Key": CHAVE_COLEGA}
    form_data = {}
    erro = None

    if request.method == "POST":
        form_data = request.POST.dict()
        try:
            r = requests.post(URL_API_COLEGA, headers=headers, json=form_data, timeout=5, verify=False)
            r.raise_for_status()
            return redirect(reverse('projetos_list'))
        except requests.exceptions.HTTPError as e:
            if e.response is not None:
                try:
                    erro_data = e.response.json()
                    erro = json.dumps(erro_data, indent=2, ensure_ascii=False)
                except ValueError:
                    erro = e.response.text or str(e)
            else:
                erro = str(e)
        except requests.exceptions.RequestException as e:
            erro = f"Não foi possível conectar à API do colega. Detalhe: {e}"

    return render(request, "portfolio/projeto_create.html", {"erro": erro, "form_data": form_data})


def projetos_delete(request, item_id):
    headers = {"X-API-Key": CHAVE_COLEGA}
    url = f"{URL_API_COLEGA}/{item_id}"
    try:
        r = requests.delete(url, headers=headers, timeout=5, verify=False)
        r.raise_for_status()
    except requests.exceptions.RequestException:
        pass
    return redirect(reverse('projetos_list'))
