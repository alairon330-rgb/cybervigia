import requests
from rich.console import Console
from rich.table import Table
from .. import config, utils
from .report_generator import export_to_html

console = Console()

def run(domain):
    try:
        console.print(f"\n[*] Consultando logs de Certificate Transparency (crt.sh) para [green]*.{domain}[/green]...")
        
        resp = requests.get(f"https://crt.sh/?q=%.{domain}&output=json", timeout=45)
        
        if resp.status_code != 200:
            utils.warn(f"Falha ao consultar crt.sh: Erro {resp.status_code}")
        else:
            data = resp.json()
            subdomains = set()
            
            for entry in data:
                name_value = entry.get("name_value", "")
                for sub in name_value.split("\n"):
                    sub = sub.strip().lower()
                    if sub.endswith(domain) and not sub.startswith("*"):
                        subdomains.add(sub)
            
            subdomains = sorted(list(subdomains))
            
            if not subdomains:
                utils.warn("Nenhum subdomínio encontrado.")
            else:
                table = Table(title=f"Subdomínios encontrados para {domain}")
                table.add_column("Subdomínio", style="cyan")
                
                # Mostra os 20 primeiros no terminal para não lotar
                for sub in subdomains[:20]:
                    table.add_row(sub)
                    
                if len(subdomains) > 20:
                    table.add_row(f"... e mais {len(subdomains) - 20} subdomínios.")
                    
                console.print(table)
                console.print(f"\n[+] Total de {len(subdomains)} subdomínios únicos encontrados.")
                
                escolha = input("\nDeseja exportar o resultado em HTML? (s/n): ").strip().lower()
                if escolha == 's':
                    html_data = {}
                    for sub in subdomains:
                        html_data[sub] = f"<a href='http://{sub}' target='_blank' style='color:#00ffff;'>http://{sub}</a>"
                    
                    filename = f"subdominios_{domain.replace('.', '_')}"
                    path = export_to_html(f"Subdomínios - {domain}", html_data, filename)
                    console.print(f"[green]✅ Relatório salvo em:[/green] [bold]{path}[/bold]")

    except Exception as e:
        utils.warn(f"Erro ao consultar subdomínios: {e}")
    finally:
        input("\nPressione ENTER para voltar ao menu...")
