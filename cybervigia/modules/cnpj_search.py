import requests
from rich.console import Console
from rich.table import Table
from .. import config, utils
from .report_generator import export_to_html

console = Console()

def run(cnpj):
    try:
        cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
        console.print(f"\n[*] Consultando CNPJ [green]{cnpj_limpo}[/green] na BrasilAPI...")
        
        resp = requests.get(f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}", timeout=15)
        
        if resp.status_code != 200:
            utils.warn(f"CNPJ não encontrado ou erro na API (Status {resp.status_code}). Verifique se digitou corretamente.")
        else:
            data = resp.json()
            
            table = Table(title=f"Empresa - CNPJ {cnpj_limpo}")
            table.add_column("Campo", style="bold cyan")
            table.add_column("Valor")
            
            # Lógica nova para montar o endereço sem sobrar vírgulas
            partes_endereco = []
            if data.get("logradouro"): partes_endereco.append(data.get("logradouro"))
            if data.get("numero"): partes_endereco.append(data.get("numero"))
            if data.get("bairro"): partes_endereco.append(data.get("bairro"))
            endereco_final = ", ".join(partes_endereco) if partes_endereco else "N/A"

            campos = {
                "Razão social": data.get("razao_social", "N/A"),
                "Situação cadastral": data.get("descricao_situacao_cadastral", "N/A"),
                "Data de abertura": data.get("data_inicio_atividade", "N/A"),
                "Atividade principal (CNAE)": data.get("cnae_fiscal_descricao", "N/A"),
                "Endereço": endereco_final,
                "CEP": data.get("cep", "N/A"),
                "Capital social": str(data.get("capital_social", "N/A"))
            }
            
            for k, v in campos.items():
                table.add_row(k, str(v))
                
            console.print(table)
            
            escolha = input("\nDeseja exportar o resultado em HTML? (s/n): ").strip().lower()
            if escolha == 's':
                filename = f"cnpj_{cnpj_limpo}"
                path = export_to_html(f"Empresa - CNPJ {cnpj_limpo}", campos, filename)
                console.print(f"[green]✅ Relatório salvo com sucesso em:[/green] [bold]{path}[/bold]")
                
    except Exception as e:
        utils.warn(f"Erro ao consultar o CNPJ: {e}")

    input("\nPressione ENTER para voltar ao menu...")
