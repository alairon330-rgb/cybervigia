import requests
from rich.console import Console
from rich.table import Table
from .. import config, utils
from .report_generator import export_to_html

console = Console()

def run(ip):
    try:
        console.print(f"\n[*] Consultando informações públicas do IP [green]{ip}[/green] (ipinfo.io, HTTPS)...")
        
        resp = requests.get(f"https://ipinfo.io/{ip}/json", timeout=10)
        data = resp.json()
        
        if "bogon" in data or "error" in data:
            utils.warn("Este é um IP privado, reservado ou inválido. Não há dados públicos de geolocalização.")
        else:
            table = Table(title=f"Informações públicas do IP {ip}")
            table.add_column("Campo", style="bold cyan")
            table.add_column("Valor")

            campos = {
                "País": data.get("country", "N/A"),
                "Região": data.get("region", "N/A"),
                "Cidade": data.get("city", "N/A"),
                "CEP/ZIP aprox.": data.get("postal", "N/A"),
                "Localização": data.get("loc", "N/A"),
                "Organização/ISP": data.get("org", "N/A"),
                "Hostname (rDNS)": data.get("hostname", "N/A")
            }

            for k, v in campos.items():
                table.add_row(k, str(v))

            console.print(table)
            utils.warn("A geolocalização por IP é aproximada (geralmente reflete o provedor, não o endereço exato da pessoa).")

            # Pergunta se quer exportar
            escolha = input("\nDeseja exportar o resultado em HTML? (s/n): ").strip().lower()
            if escolha == 's':
                filename = f"ip_{ip.replace('.', '_')}"
                path = export_to_html(f"Análise de IP - {ip}", campos, filename)
                console.print(f"[green]✅ Relatório salvo com sucesso em:[/green] [bold]{path}[/bold]")

    except Exception as e:
        utils.warn(f"Erro ao consultar o IP: {e}")

    finally:
        # A PAUSA MÁGICA: O terminal não vai mais voltar sozinho!
        input("\nPressione ENTER para voltar ao menu...")
