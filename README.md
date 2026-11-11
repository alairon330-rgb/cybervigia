![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python&logoColor=white)
![OSINT](https://img.shields.io/badge/OSINT-Toolkit-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Ativo-success?style=for-the-badge)

# 🦉 CYBERVIGIA - OSINT Toolkit

CYBERVIGIA é uma ferramenta de linha de comando (CLI) para investigação em fontes abertas (OSINT), escrita em Python. 

### ⚠️ Uso Ético
Esta ferramenta foi criada para fins educacionais e de pesquisa em segurança da informação. Utilize apenas para consultar dados públicos. Respeite a LGPD.

## 🚀 Funcionalidades

| # | Busca | O que faz | Fonte de dados |
|---|-------|-----------|----------------|
| 1 | Username | Verifica username em +100 sites. | HTTP Direto |
| 2 | E-mail | Valida formato, MX, Gravatar e reputação. | DNS + APIs |
| 3 | CEP | Consulta endereço completo. | ViaCEP |
| 4 | Telefone | Valida número, operadora e localização. | libphonenumber |
| 5 | Nome completo | Busca na web via DuckDuckGo. | DuckDuckGo |
| 6 | IP | Geolocalização e dados do provedor. | ipinfo.io |
| 7 | WHOIS | Consulta registro RDAP de domínio. | rdap.org |
| 8 | Subdomínios | Busca passiva em Certificate Transparency. | crt.sh |
| 9 | CNPJ | Consulta dados públicos na Receita Federal. | BrasilAPI |
| 10 | Link suspeito | Análise de reputação de URL. | VirusTotal |
| 11 | Hash | Identifica o algoritmo (MD5, SHA, etc) - Offline. | Lógica local |
| 12 | Imagem (EXIF) | Gera links de busca reversa e extrai EXIF. | Motores de busca |
| 13 | CPF (validador) | Valida matematicamente o CPF - Offline. | Lógica local |
| 14 | Dono (Telefone) | Checa WhatsApp e busca rastros na web. | wa.me + DDG |

## 📄 Relatórios em HTML
Todas as buscas contam com a opção de exportar os resultados em um Relatório HTML formatado com tema escuro (Dark Mode). O arquivo é salvo na pasta `responsa_resultados/`.

## 📖 Manual Completo
Consulte o arquivo **MANUAL.md** para saber como rodar cada comando.

## 🛠️ Instalação Rápida
```bash
git clone https://github.com/alairon330-rgb/responsa.git
cd responsa
pip install -r requirements.txt
python -m responsa