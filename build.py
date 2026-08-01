#!/usr/bin/env python3
"""Gera as páginas do site a partir de templates em src/.

Como usar:
    python3 build.py

O que faz:
    1. Lê a configuração abaixo (menu, páginas, contato, formulário, site).
    2. Renderiza header/footer compartilhados a partir de src/partials/.
    3. Injeta o conteúdo de cada página (src/paginas/) no esqueleto (src/base.html).
    4. Escreve os *.html na raiz + robots.txt e sitemap.xml.

Regra de ouro: se você mudar o menu, o rodapé ou um horário, mude na fonte
(este arquivo ou src/partials) e rode `python3 build.py` de novo.
"""

import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
SRC = RAIZ / "src"
PARTIALS = SRC / "partials"
PAGINAS_DIR = SRC / "paginas"
SAIDA = RAIZ

# ---------------------------------------------------------------------------
# CONFIGURAÇÃO — a fonte única da verdade
# ---------------------------------------------------------------------------

# URL pública (sem barra final). Usada no sitemap, robots e compartilhamento.
SITE_URL = "https://www.evangelhopleno.com.br"

# Menu principal. 'rotulo' é o texto visível; 'href' é a página de destino.
NAV = [
    {"href": "index.html", "rotulo": "Início"},
    {"href": "primeira-visita.html", "rotulo": "Primeira visita"},
    {"href": "quem-somos.html", "rotulo": "Quem somos"},
    {"href": "ministerios.html", "rotulo": "Ministérios"},
    {"href": "agenda.html", "rotulo": "Agenda"},
    {"href": "contato.html", "rotulo": "Contato"},
]
CTA = {"href": "contribua.html", "rotulo": "Contribua"}

# Cada página: nome do arquivo gerado, <title> e <meta description>.
# O conteúdo vem de src/paginas/<arquivo>.
PAGINAS = [
    {
        "arquivo": "index.html",
        "titulo": "Igreja Evangelho Pleno — Nossa paixão é por vidas",
        "descricao": (
            "Três congregações no Espírito Santo: Santa Teresa, São Roque do "
            "Canaã e Várzea Alegre. Veja os horários dos cultos e venha nos visitar."
        ),
    },
    {
        "arquivo": "primeira-visita.html",
        "titulo": "Primeira visita — Igreja Evangelho Pleno",
        "descricao": (
            "Tudo o que você quer saber antes de visitar a Igreja Evangelho "
            "Pleno pela primeira vez."
        ),
    },
    {
        "arquivo": "quem-somos.html",
        "titulo": "Quem somos — Igreja Evangelho Pleno",
        "descricao": (
            "A história, a liderança e o que a Igreja Evangelho Pleno acredita. "
            "Três congregações no Espírito Santo, uma igreja só."
        ),
    },
    {
        "arquivo": "ministerios.html",
        "titulo": "Ministérios — Igreja Evangelho Pleno",
        "descricao": (
            "Os grupos e equipes da Igreja Evangelho Pleno: louvor, espaço "
            "infantil, recepção, intercessão e mais."
        ),
    },
    {
        "arquivo": "agenda.html",
        "titulo": "Agenda — Igreja Evangelho Pleno",
        "descricao": (
            "Horários de culto das três congregações e a programação semanal da "
            "Igreja Evangelho Pleno."
        ),
    },
    {
        "arquivo": "contato.html",
        "titulo": "Contato — Igreja Evangelho Pleno",
        "descricao": (
            "Fale com a Igreja Evangelho Pleno. Pedido de oração, primeira "
            "visita, dúvidas — a gente responde."
        ),
    },
    {
        "arquivo": "contribua.html",
        "titulo": "Contribua — Igreja Evangelho Pleno",
        "descricao": (
            "Saiba como contribuir com a Igreja Evangelho Pleno por PIX ou "
            "transferência — e o que a sua doação sustenta."
        ),
    },
    {
        "arquivo": "unidade.html",
        "titulo": "Ano da Unidade 2K26 — Igreja Evangelho Pleno",
        "descricao": (
            "O Ano da Unidade: três congregações no Espírito Santo decididas a "
            "andar juntas como uma igreja só."
        ),
    },
    {
        "arquivo": "404.html",
        "titulo": "Página não encontrada — Igreja Evangelho Pleno",
        "descricao": (
            "A página que você procura não existe ou mudou de endereço. Volte "
            "para a página inicial da Igreja Evangelho Pleno."
        ),
    },
]

# Contatos exibidos no rodapé e na página de contato.
# Coloque `None` enquanto o dado ainda não existir — vira texto [A DEFINIR].
CONTATO = {
    "whatsapp": "5527999123456",          # DDD + número, sem símbolos
    "instagram": None,                    # ex.: "https://instagram.com/evangelhopleno"
    "email_pix": "contribuicao@evangelhopleno.com.br",
}

# Formulário de contato (Web3Forms — grátis no volume de uma igreja).
# Crie uma chave em https://web3forms.com e cole aqui.
FORMS = {
    "chave_web3forms": "SEU-ACCESS-KEY-DA-WEB3FORMS",
}

# ---------------------------------------------------------------------------
# Renderização
# ---------------------------------------------------------------------------


def render(texto: str, contexto: dict) -> str:
    """Substitui os marcadores {{chave}} pelo valor correspondente."""
    for chave, valor in contexto.items():
        texto = texto.replace("{{" + chave + "}}", str(valor))
    return texto


def render_arquivo(caminho: Path, contexto: dict) -> str:
    return render(caminho.read_text(encoding="utf-8"), contexto)


def render_nav(ativo: str) -> str:
    linhas = []
    for item in NAV:
        atual = ' aria-current="page"' if item["href"] == ativo else ""
        linhas.append(f'    <a href="{item["href"]}"{atual}>{item["rotulo"]}</a>')
    atual = ' aria-current="page"' if CTA["href"] == ativo else ""
    linhas.append(
        f'    <a class="btn btn--brasa nav__cta" href="{CTA["href"]}"{atual}>{CTA["rotulo"]}</a>'
    )
    return "\n".join(linhas)


def montar_pagina(pagina: dict) -> str:
    whatsapp = CONTATO["whatsapp"]
    instagram = CONTATO["instagram"]
    contexto = {
        "titulo": pagina["titulo"],
        "descricao": pagina["descricao"],
        "og_url": f"{SITE_URL}/assets/img/fotos/congregacao-cheia.jpg",
        "nav": render_nav(pagina["arquivo"]),
        "whatsapp": whatsapp or "",
        "instagram": instagram or "",
        "whatsapp_li": (
            f'<li><a href="https://wa.me/{whatsapp}" target="_blank" rel="noopener">WhatsApp</a></li>'
            if whatsapp
            else "<li>[WHATSAPP A DEFINIR]</li>"
        ),
        "instagram_li": (
            f'<li><a href="{instagram}" target="_blank" rel="noopener">Instagram</a></li>'
            if instagram
            else "<li>[INSTAGRAM A DEFINIR]</li>"
        ),
        "email_pix": CONTATO["email_pix"],
        "form_chave": FORMS["chave_web3forms"],
        "ano": datetime.date.today().year,
    }

    cabecalho = render_arquivo(PARTIALS / "cabecalho.html", contexto)
    rodape = render_arquivo(PARTIALS / "rodape.html", contexto)
    conteudo = render_arquivo(PAGINAS_DIR / pagina["arquivo"], contexto)

    contexto.update({"cabecalho": cabecalho, "rodape": rodape, "conteudo": conteudo})
    return render_arquivo(SRC / "base.html", contexto)


def montar_sitemap() -> str:
    urls = "\n".join(
        f'  <url><loc>{SITE_URL}/{p["arquivo"]}</loc></url>'
        for p in PAGINAS
        if p["arquivo"] != "404.html"
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n"
        "</urlset>\n"
    )


def montar_robots() -> str:
    return (
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        f"Sitemap: {SITE_URL}/sitemap.xml\n"
    )


def validar() -> None:
    """Confere que todo link interno aponta para um arquivo existente."""
    erros = []
    for pagina in PAGINAS:
        html = (SAIDA / pagina["arquivo"]).read_text(encoding="utf-8")
        for trecho in html.split('href="')[1:]:
            href = trecho.split('"', 1)[0]
            if href.startswith(("http", "mailto:", "#", "tel:")):
                continue
            if href and not (SAIDA / href).exists():
                erros.append(f'{pagina["arquivo"]} -> {href}')
    if erros:
        raise SystemExit("Links quebrados:\n  " + "\n  ".join(erros))


def main() -> None:
    for pagina in PAGINAS:
        html = montar_pagina(pagina)
        (SAIDA / pagina["arquivo"]).write_text(html, encoding="utf-8")

    (SAIDA / "sitemap.xml").write_text(montar_sitemap(), encoding="utf-8")
    (SAIDA / "robots.txt").write_text(montar_robots(), encoding="utf-8")

    validar()
    print(f"Build ok: {len(PAGINAS)} páginas + sitemap.xml + robots.txt")


if __name__ == "__main__":
    main()
