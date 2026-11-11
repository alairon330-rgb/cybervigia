import requests
import re
from rich.console import Console
from rich.table import Table
from .. import config, utils
from .report_generator import export_to_html

console = Console()

def check_whatsapp(phone):
    numero_limpo = re.sub(r'\D', '', phone)
    url = f"https://wa.me/{numero_limpo}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if "O número de telefone compartilhado por url é inválido" in resp.text or "Invalid phone number" in resp.text:
            return "Não (Número inválido ou sem conta)"
        return "Sim (Número válido com WhatsApp)"
    except:
        return "Indefinido (Erro na conexão)"

def run(phone):
    try:
        console.print(f"\n[*] Analisando telefone e buscando rastros na web: [green]{phone}[/green]...")
        
        wa_status = check_whatsapp(phone)
        
        query = f'"{phone}" OR "{phone.replace(" ", "")}"'
        url = 'https://html.duckduckgo.com/html/'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        
        resultados_web = []
        try:
            resp = requests.post(url, headers=headers, data={'q': query}, timeout=15)
            if resp.status_code == 200:
                links = re.findall(r'class="result__url" href="(.*?)"', resp.text)
                for link in links[:5]:
                    if "uddg=" in link:
                        link_limpo = requests.utils.unquote(link.split("uddg=")[1].split("&")[0])
                        resultados_web.append(link_limpo)
        except:
            pass

        table = Table(title=f"Investigacão de Telefone - {phone}")
        table.add_column("Campo", style="bold cyan")
        table.add_column("Resultado")
        
        campos = {
            "Telefone analisado": phone,
            "Possui WhatsApp?": wa_status,
        }
        
        for k, v in campos.items():
            table.add_row(k, v)
            
        if resultados_web:
            links_str = "\n".join(resultados_web)
            table.add_row("Rastros na Web", links_str)
        else:
            table.add_row("Rastros na Web", "Nenhum resultado público encontrado.")
            
        console.print(table)
        
        escolha = input("\nDeseja exportar o resultado em HTML? (s/n): ").strip().lower()
        if escolha == 's':
            html_data = {
                "Telefone analisado": phone,
                "Possui WhatsApp?": wa_status
            }
            
            if resultados_web:
                links_html = "<br>".join([f"<a href='{l}' target='_blank' style='color:#00ffff;'>{l}</a>" for l in resultados_web])
                html_data["Rastros na Web"] = links_html
            else:
                html_data["Rastros na Web"] = "Nenhum resultado público encontrado."

            filename = f"telefone_{phone.replace('+', '').replace(' ', '')}"
            path = export_to_html(f"Investigação de Telefone - {phone}", html_data, filename)
            console.print(f"[green]✅ Relatório salvo em:[/green] [bold]{path}[/bold]")

    except Exception as e:
        utils.warn(f"Erro ao investigar telefone: {e}")
    finally:
        input("\nPressione ENTER para voltar ao menu...")
