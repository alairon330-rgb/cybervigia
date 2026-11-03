import json
import requests
import concurrent.futures
import os
from rich.console import Console
from rich.table import Table
from .. import config, utils
from .report_generator import export_to_html

console = Console()

def check_site(site, username):
    # Inicializa as variáveis AQUI, antes do try, para o except não dar erro!
    name = "Desconhecido"
    category = "geral"
    profile_url = ""
    try:
        name = site.get("name") or site.get("site") or site.get("nome") or "Desconhecido"
        category = site.get("category") or site.get("categoria") or "geral"
        
        url_base = site.get("url") or site.get("url_main") or site.get("main_url") or ""
        check_url_base = site.get("check_url") or url_base
        
        if not check_url_base:
            return (name, category, "Erro no JSON", "")

        check_url = check_url_base.replace("{username}", username)
        profile_url = url_base.replace("{username}", username)
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        
        resp = requests.get(check_url, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            texto = resp.text.lower()
            if "not found" in texto or "não encontrado" in texto or "página não existe" in texto:
                return (name, category, "Não Encontrado", profile_url)
            return (name, category, "Encontrado", profile_url)
        elif resp.status_code == 404:
            return (name, category, "Não Encontrado", profile_url)
        else:
            return (name, category, "Indefinido", profile_url)
    except Exception:
        return (name, category, "Erro/Timeout", profile_url)

def run(username):
    try:
        caminho_sites = os.path.join(os.path.dirname(__file__), '..', 'data', 'sites.json')
        
        with open(caminho_sites, 'r', encoding='utf-8') as f:
            sites = json.load(f)
            
        console.print(f"\n[*] Base carregada! Buscando por [green]{username}[/green] em {len(sites)} sites...")
        
        resultados = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(check_site, site, username): site for site in sites}
            for future in concurrent.futures.as_completed(futures):
                resultados.append(future.result())

        encontrados = [r for r in resultados if r[2] == "Encontrado"]
        indefinidos = [r for r in resultados if r[2] == "Indefinido"]
        erros = [r for r in resultados if r[2] == "Erro/Timeout"]
        
        table = Table(title=f"Resultados para '{username}'")
        table.add_column("Site", style="cyan")
        table.add_column("Categoria", style="magenta")
        table.add_column("URL", style="blue")

        for r in encontrados:
            table.add_row(r[0], r[1], r[3])
        
        if encontrados:
            console.print(table)
        else:
            utils.warn("Nenhum perfil encontrado.")
        
        console.print(f"\n[+] {len(encontrados)} encontrado(s) | [*] {len(indefinidos)} indefinido(s) | [!] {len(erros)} erro(s)")
        
        escolha = input("\nDeseja exportar o resultado em HTML? (s/n): ").strip().lower()
        if escolha == 's':
            html_data = {}
            for r in encontrados:
                html_data[f"{r[0]} ({r[1]})"] = f"<a href='{r[3]}' target='_blank' style='color:#00ffff;'>{r[3]}</a>"
            
            if indefinidos:
                html_data["--- INDEFINIDOS ---"] = ""
                for r in indefinidos:
                    html_data[f"{r[0]} ({r[1]})"] = f"<a href='{r[3]}' target='_blank' style='color:#ffaa00;'>{r[3]}</a>"
            
            filename = f"username_{username}"
            path = export_to_html(f"Busca de Username - {username}", html_data, filename)
            console.print(f"[green]✅ Relatório salvo em:[/green] [bold]{path}[/bold]")

    except Exception as e:
        console.print(f"\n[red]ERRO INTERNO: {e}[/red]")
    finally:
        input("\nPressione ENTER para voltar ao menu...")
