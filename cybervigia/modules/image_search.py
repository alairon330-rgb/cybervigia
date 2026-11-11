from rich.console import Console
from rich.table import Table
from .. import config, utils
from .report_generator import export_to_html

console = Console()

def run(image_url):
    try:
        console.print(f"\n[*] Gerando links de busca reversa para: [green]{image_url}[/green]")
        
        # Gera os links dos motores de busca
        links = {
            "Google Lens": f"https://lens.google.com/uploadbyurl?url={image_url}",
            "Yandex Images": f"https://yandex.com/images/search?url={image_url}&rpt=imageview",
            "Bing Visual Search": f"https://www.bing.com/images/search?q=imgurl:{image_url}&view=detailv2&iss=sbi",
            "TinEye": f"https://tineye.com/search?url={image_url}"
        }
        
        # Tabela do terminal
        table = Table(title="Busca reversa de imagem — links diretos")
        table.add_column("Motor", style="bold cyan")
        table.add_column("Link", style="blue")
        
        for motor, link in links.items():
            table.add_row(motor, link)
            
        console.print(table)
        utils.warn("Cada motor tem um jeito diferente de indexar/comparar imagens — vale abrir mais de um para comparar os resultados.")
        
        # Exportação HTML
        escolha = input("\nDeseja exportar o resultado em HTML? (s/n): ").strip().lower()
        if escolha == 's':
            html_data = {}
            # Transforma os links em tags HTML clicáveis
            for motor, link in links.items():
                html_data[motor] = f"<a href='{link}' target='_blank' style='color:#00ffff; text-decoration:none;'>{link}</a>"
            
            # Pega os primeiros caracteres da URL para nomear o arquivo
            nome_arquivo = image_url.split('/')[-1][:10]
            filename = f"busca_imagem_{nome_arquivo}"
            
            path = export_to_html("Busca Reversa de Imagem", html_data, filename)
            console.print(f"[green]✅ Relatório salvo em:[/green] [bold]{path}[/bold]")
            
    except Exception as e:
        utils.warn(f"Erro ao processar imagem: {e}")
    finally:
        input("\nPressione ENTER para voltar ao menu...")
