import requests
from rich.console import Console
from rich.table import Table
from .. import config, utils
from .report_generator import export_to_html

console = Console()

def run(domain):
    try:
        console.print(f"\n[*] Consultando registro RDAP de [green]{domain}[/green]...")
        # API pública de WHOIS via RDAP
        resp = requests.get(f"https://rdap.org/domain/{domain}", timeout=15)
        
        if resp.status_code != 200:
            utils.warn(f"Domínio não encontrado ou erro na API (Status {resp.status_code}).")
        else:
            data = resp.json()
            
            # Extraindo dados
            status = ", ".join(data.get("status", []))
            
            nameservers = []
            for ns in data.get("nameservers", []):
                nameservers.append(ns.get("ldhName", ""))
            ns_str = "\n".join(nameservers) if nameservers else "N/A"
            
            events = data.get("events", [])
            reg_date = "N/A"
            exp_date = "N/A"
            for ev in events:
                if ev.get("eventAction") == "registration":
                    reg_date = ev.get("eventDate", "N/A")[:10]
                elif ev.get("eventAction") == "expiration":
                    exp_date = ev.get("eventDate", "N/A")[:10]
                    
            entities = data.get("entities", [])
            registrar = "N/A"
            for ent in entities:
                if "registrar" in ent.get("roles", []):
                    vcard = ent.get("vcardArray", [])
                    if vcard and len(vcard) > 1:
                        for item in vcard[1]:
                            if item[0] == "fn":
                                registrar = item[3]
                                break
            
            table = Table(title=f"Registro de domínio — {domain}")
            table.add_column("Campo", style="bold cyan")
            table.add_column("Valor")
            
            campos = {
                "Status": status if status else "N/A",
                "Servidores DNS": ns_str,
                "Data de registro": reg_date,
                "Data de expiração": exp_date,
                "Entidade (registrar)": registrar
            }
            
            for k, v in campos.items():
                table.add_row(k, str(v))
                
            console.print(table)
            utils.warn("A maioria dos registros modernos oculta dados pessoais do titular (LGPD/GDPR).")
            
            escolha = input("\nDeseja exportar o resultado em HTML? (s/n): ").strip().lower()
            if escolha == 's':
                filename = f"whois_{domain.replace('.', '_')}"
                path = export_to_html(f"Registro de domínio - {domain}", campos, filename)
                console.print(f"[green]✅ Relatório salvo em:[/green] [bold]{path}[/bold]")
                
    except Exception as e:
        utils.warn(f"Erro ao consultar domínio: {e}")
    finally:
        input("\nPressione ENTER para voltar ao menu...")
