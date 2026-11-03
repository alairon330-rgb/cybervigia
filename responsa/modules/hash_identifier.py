import re
from rich.console import Console
from rich.table import Table
from .. import config, utils
from .report_generator import export_to_html

console = Console()

def run(hash_str):
    try:
        hash_str = hash_str.strip()
        console.print(f"\n[*] Analisando hash...")
        
        if not re.match(r'^[a-fA-F0-9]+$', hash_str):
            utils.warn("O hash contém caracteres inválidos (apenas 0-9 e a-f são permitidos).")
        else:
            tipos = []
            length = len(hash_str)
            
            if length == 32:
                tipos = ["MD5", "NTLM", "MD4"]
            elif length == 40:
                tipos = ["SHA-1"]
            elif length == 56:
                tipos = ["SHA-224"]
            elif length == 64:
                tipos = ["SHA-256"]
            elif length == 96:
                tipos = ["SHA-384"]
            elif length == 128:
                tipos = ["SHA-512"]
            else:
                tipos = ["Desconhecido (tamanho não padrão)"]
            
            table = Table(title="Identificação de hash")
            table.add_column("Campo", style="bold cyan")
            table.add_column("Valor")
            
            campos = {
                "Hash informado": hash_str,
                "Comprimento": str(length),
                "Algoritmo(s) provável(is)": ", ".join(tipos)
            }
            
            for k, v in campos.items():
                table.add_row(k, v)
                
            console.print(table)
            utils.warn("Hashes de mesmo comprimento são indistinguíveis só pelo formato — o contexto resolve a ambiguidade.")
            
            escolha = input("\nDeseja exportar o resultado em HTML? (s/n): ").strip().lower()
            if escolha == 's':
                filename = f"hash_{hash_str[:8]}"
                path = export_to_html(f"Identificação de Hash", campos, filename)
                console.print(f"[green]✅ Relatório salvo em:[/green] [bold]{path}[/bold]")

    except Exception as e:
        utils.warn(f"Erro ao analisar hash: {e}")
    finally:
        input("\nPressione ENTER para voltar ao menu...")
