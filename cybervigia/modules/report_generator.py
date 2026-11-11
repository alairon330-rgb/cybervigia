import os
from datetime import datetime

def export_to_html(title, data, filename):
    # Cria a pasta de resultados se não existir
    os.makedirs('responsa_resultados', exist_ok=True)
    filepath = f"responsa_resultados/{filename}.html"
    
    # Gera as linhas da tabela
    rows = ""
    for key, value in data.items():
        rows += f"<tr><td class='key'>{key}</td><td class='value'>{value}</td></tr>\n"

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Responsa OSINT - {title}</title>
    <style>
        body {{
            background-color: #1e1e1e;
            color: #d4d4d4;
            font-family: 'Courier New', Courier, monospace;
            margin: 0;
            padding: 20px;
        }}
        .header {{
            text-align: center;
            color: #00ffff;
            border-bottom: 2px solid #00ffff;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        h1 {{ margin: 0; font-size: 2em; text-transform: uppercase; }}
        h2 {{ color: #ff00ff; font-size: 1.2em; margin-top: 5px; }}
        .date {{ color: #888; font-size: 0.9em; text-align: right; margin-bottom: 20px; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background-color: #252526;
        }}
        th, td {{
            border: 1px solid #3e3e42;
            padding: 12px;
            text-align: left;
        }}
        th {{ background-color: #333333; color: #00ff00; }}
        .key {{ color: #00ffff; font-weight: bold; width: 40%; }}
        .value {{ color: #ffffff; word-break: break-all; }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            font-size: 0.8em;
            color: #666;
            border-top: 1px solid #333;
            padding-top: 10px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>RESPONSA</h1>
        <h2>OSINT Toolkit</h2>
    </div>
    
    <h3>Relatório: {title}</h3>
    <div class="date">Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</div>
    
    <table>
        <thead>
            <tr>
                <th>Campo</th>
                <th>Resultado</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>

    <div class="footer">
        Gerado automaticamente pela ferramenta RESPONSA.<br>
        Uso ético e responsável apenas. Consulte a LGPD.
    </div>
</body>
</html>"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return filepath
