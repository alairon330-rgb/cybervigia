import requests
from rich.console import Console
from rich.table import Table
from .. import config, utils
from .report_generator import export_to_html

console = Console()

def run(cep):
    try:
        cep_limpo = ''.join(filter(str.isdigit, cep))
        console.print(f"\n[*] Consultando CEP [green]{cep_limpo}[/green] na base ViaCEP...")
        
        resp = requests.get(f"https://viacep.com.br/ws/{cep_limpo}/json/", timeout=10)
        data = resp.json()
        
        if "erro" in data:
            utils.warn("CEP não encontrado ou inválido.")
        else:
            table = Table(title=f"Endereço referente ao CEP {cep_limpo}")
            table.add_column("Campo", style="bold cyan")
            table.add_column("Valor")
            
            campos = {
                "Logradouro": data.get("logradouro", "N/A"),
                "Bairro": data.get("bairro", "N/A"),
                "Cidade": data.get("localidade", "N/A"),
                "UF": data.get("uf", "N/A"),
                "Código IBGE": data.get("ibge", "N/A"),
                "DDD": data.get("ddd", "N/A")
            }
            
            for k, v in campos.items():
                table.add_row(k, str(v))
                
            console.print(table)
            
            escolha = input("\nDeseja exportar o resultado em HTML? (s/n): ").strip().lower()
            if escolha == 's':
                filename = f"cep_{cep_limpo}"
                path = export_to_html(f"Endereço - CEP {cep_limpo}", campos, filename)
                console.print(f"[green]✅ Relatório salvo em:[/green] [bold]{path}[/bold]")
                
    except Exception as e:
        utils.warn(f"Erro ao consultar o CEP: {e}")
    finally:
        input("\nPressione ENTER para voltar ao menu...")
