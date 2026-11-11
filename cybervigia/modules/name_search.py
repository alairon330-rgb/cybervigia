import requests
from rich.console import Console
from rich.table import Table
from .. import config, utils

console = Console()

def search_ddg(query):
    url = 'https://html.duckduckgo.com/html/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        resp = requests.post(url, headers=headers, data={'q': query}, timeout=15)
        if resp.status_code == 200:
            # Se a busca funcionar, retorna o link
            return [{'title': f'Resultados para {query}', 'href': f'https://duckduckgo.com/?q={query.replace(" ", "+")}'}]
        else:
            console.print(f"[red]O DuckDuckGo bloqueou a requisição (Erro HTTP {resp.status_code})[/red]")
    except Exception as e:
        console.print(f"[red]Falha na conexão: {e}[/red]")
    return []

def run(name):
    console.print(f"\n[*] Buscando por nome: {name}...")
    resultados = search_ddg(name)

    if not resultados:
        utils.warn("Nenhum resultado encontrado ou erro na busca.")
    else:
        table = Table(title=f"Resultados para '{name}'")
        table.add_column("Título", style="cyan")
        table.add_column("Link", style="blue")

        for r in resultados:
            table.add_row(r['title'], r['href'])

        console.print(table)

    # A pausa mágica para você conseguir ler!
    input("\nPressione ENTER para voltar ao menu...")

def main(name):
    run(name)
