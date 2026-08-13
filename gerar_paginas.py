#!/usr/bin/env python3
"""
Gera uma landing page por servico a partir do template visual criado na Lovable
(_template_lovable.html), aplicando o mesmo design a todas as paginas.

O template ja veio limpo: HTML+CSS puros, sem framework, sem CDN externo, sem o
badge/analytics que a hospedagem da Lovable injeta (removidos em 13/08/2026).

Cada pagina: mesmo visual, mesmo rastreamento de conversao, mesmo rodape (CRO —
exigencia do CFO), mas com titulo/subtitulo/paragrafo e TEXTO PRE-PREENCHIDO DO
WHATSAPP proprios do servico.

Regras de conformidade verificadas automaticamente antes de gravar:
  - nenhuma promessa de resultado (CFO Art. 44, I)
  - nenhum preco, desconto ou modalidade de pagamento (CFO Art. 44, I)
  - nenhuma mencao a cartao de desconto/beneficio (CFO Art. 44, XIV)
  - nenhum "antes e depois" (CFO Art. 44, XII)
  - nenhum depoimento/nome de paciente (CFO Art. 44, VI)
  - nenhuma mencao a "botox"/"toxina botulinica" (politica Google Ads)
  - marcador "vi o anuncio no Google" preservado em todas (medicao da ANNA, doc 09 R2)

Uso: python3 gerar_paginas.py
"""
import os
import re
import sys
import urllib.parse

WHATS = "5537999220550"
CONV_TAG = "AW-18305804748/opogCLXGxM0cEMzT8ZhE"
GTAG_ID = "AW-18305804748"
MAPS = "https://share.google/Lxpgk0PGhm8d8SXDa"
# Mesmo link do perfil no Google — leva ao perfil onde as avaliacoes aparecem.
AVALIACOES = "https://share.google/Lxpgk0PGhm8d8SXDa"

# TELEFONE: deliberadamente NAO publicado. A ANNA nao atende ligacao, e o numero
# (37) 99918-4874 nao existe na configuracao dela. Caso real de 06/08/2026: emergencia
# com duas escalacoes de encaixe expiradas sem resposta humana. Publicar telefone criaria
# promessa de atendimento sem lastro. Confirmado com a instancia da ANNA em 13/08/2026.

# Horario CONFIRMADO pelo Anderson via instancia da ANNA em 13/08/2026.
HORARIO = "Segunda a sexta, 8h às 18h"

PAGINAS = {
    "": {  # raiz — harmonizacao facial (destino do grupo G5)
        "title": "Harmonização Facial em Itaúna-MG | Dra. Tatiane Mizael",
        "meta": "Harmonização facial com a Dra. Tatiane Mizael — Ampla Odontologia, Itaúna-MG.",
        "h1": "Harmonização Facial em Itaúna-MG",
        "subtitle": "Dra. Tatiane Mizael — rinomodelação, preenchimento e harmonização facial em Itaúna",
        "body": "Atendimento humanizado e avaliação individualizada para cada paciente.",
        "wa": "Olá, vi o anúncio no Google e quero saber mais sobre harmonização facial",
    },
    "clareamento": {
        "title": "Clareamento Dental em Itaúna-MG | Dra. Tatiane Mizael",
        "meta": "Clareamento dental a laser na Ampla Odontologia, com a Dra. Tatiane Mizael — Itaúna-MG.",
        "h1": "Clareamento Dental em Itaúna-MG",
        "subtitle": "Dra. Tatiane Mizael — clareamento a laser com equipamento importado, em Itaúna",
        "body": "Avaliação individualizada para definir a técnica adequada ao seu caso.",
        "wa": "Olá, vi o anúncio no Google e quero saber sobre clareamento dental",
    },
    "dentista": {
        "title": "Dentista em Itaúna-MG | Ampla Odontologia",
        "meta": "Clínica odontológica no centro de Itaúna-MG, com a Dra. Tatiane Mizael.",
        "h1": "Dentista em Itaúna-MG",
        "subtitle": "Dra. Tatiane Mizael — Ampla Odontologia, no centro de Itaúna",
        "body": "Atendimento humanizado no centro de Itaúna, perto do comércio e do ponto de ônibus.",
        "wa": "Olá, vi o anúncio no Google e quero saber sobre consulta odontológica",
    },
    "limpeza": {
        "title": "Limpeza Dental em Itaúna-MG | Dra. Tatiane Mizael",
        "meta": "Limpeza dental, profilaxia e remoção de tártaro em Itaúna-MG, na Ampla Odontologia.",
        "h1": "Limpeza Dental em Itaúna-MG",
        "subtitle": "Dra. Tatiane Mizael — profilaxia e remoção de tártaro em Itaúna",
        "body": "Limpeza profissional com avaliação individualizada, no centro de Itaúna.",
        "wa": "Olá, vi o anúncio no Google e quero saber sobre limpeza dental",
    },
    "facetas": {
        "title": "Facetas e Lentes de Contato Dental em Itaúna-MG | Dra. Tatiane Mizael",
        "meta": "Facetas de porcelana e lentes de contato dental em Itaúna-MG, na Ampla Odontologia.",
        "h1": "Facetas e Lentes de Contato Dental",
        "subtitle": "Dra. Tatiane Mizael — facetas de porcelana e resina em Itaúna",
        "body": "Avaliação individualizada para definir o que se adequa ao seu caso.",
        "wa": "Olá, vi o anúncio no Google e quero saber sobre facetas e lentes de contato dental",
    },
    "bruxismo": {
        "title": "Placa de Bruxismo e ATM em Itaúna-MG | Dra. Tatiane Mizael",
        "meta": "Placa para bruxismo e avaliação de ATM em Itaúna-MG, na Ampla Odontologia.",
        "h1": "Placa de Bruxismo e ATM",
        "subtitle": "Dra. Tatiane Mizael — placa sob medida e avaliação de ATM em Itaúna",
        "body": "Avaliação individualizada para bruxismo e dores na articulação da mandíbula.",
        "wa": "Olá, vi o anúncio no Google e quero saber sobre placa de bruxismo",
    },
    "canal": {
        "title": "Tratamento de Canal em Itaúna-MG | Dra. Tatiane Mizael",
        "meta": "Tratamento de canal (endodontia) em Itaúna-MG, na Ampla Odontologia.",
        "h1": "Tratamento de Canal em Itaúna-MG",
        "subtitle": "Dra. Tatiane Mizael — endodontia com avaliação individualizada em Itaúna",
        "body": "Avaliação individualizada para tratamento de canal, no centro de Itaúna.",
        "wa": "Olá, vi o anúncio no Google e quero saber sobre tratamento de canal",
    },
    "proteses": {
        "title": "Próteses Dentárias em Itaúna-MG | Dra. Tatiane Mizael",
        "meta": "Próteses dentárias fixas, parciais e removíveis em Itaúna-MG, na Ampla Odontologia.",
        "h1": "Próteses Dentárias em Itaúna-MG",
        "subtitle": "Dra. Tatiane Mizael — prótese fixa, parcial ou removível em Itaúna",
        "body": "Avaliação individualizada para definir a prótese adequada ao seu caso.",
        "wa": "Olá, vi o anúncio no Google e quero saber sobre próteses dentárias",
    },
    "convenio": {
        "title": "Atendimento por Convênio Odontológico em Itaúna-MG | Dra. Tatiane Mizael",
        "meta": "Atendimento odontológico por convênio em Itaúna-MG, na Ampla Odontologia.",
        "h1": "Atendimento por Convênio Odontológico",
        "subtitle": "Dra. Tatiane Mizael — Ampla Odontologia, no centro de Itaúna",
        "body": "Confirme o seu convênio e agende sua avaliação diretamente pelo WhatsApp.",
        "wa": "Olá, vi o anúncio no Google e quero saber sobre atendimento por convênio odontológico",
    },
}

# Paginas que mencionam convenio. Revisado em 13/08/2026 com a instancia da ANNA:
#  - FORA: clareamento, facetas, raiz/harmonizacao (esteticos, particular com a Dra. Tatiane)
#  - FORA: proteses — no cadastro da ANNA, protese esta com a Dra. Tatiane (particular).
#    ⏳ PENDENTE confirmar com a Dra. Tatiane; ate la nao afirmamos.
#  - FORA: bruxismo — placa e terapeutica e PODE ser coberta, mas nao ha dado sobre o que
#    ESTES planos cobrem nesta clinica. ⏳ PENDENTE confirmar; ate la nao afirmamos.
MENCIONA_CONVENIO = {"dentista", "limpeza", "canal", "convenio"}

# ⚠️ Linha de texto sobre cartao de beneficio segue FORA das paginas. CFO Art. 44, XIV veda
# oferecer servicos odontologicos "atraves de cartao de descontos". O Anderson informou em
# 13/08/2026 que ha contrato com os parceiros e autorizou o VIDEO de parceiros; a decisao e
# dele, ciente da ressalva.

# Videos institucionais (a Dra. Tatiane falando a camera — nao mostram procedimento, portanto
# fora da vedacao da Resolucao CFO 196/2019 sobre video de procedimento).
# Convertidos com avconvert (nativo do macOS) em 720x1280. Ficaram grandes (10-15MB) porque
# os presets do avconvert nao permitem controlar bitrate; por isso vao com preload="none":
# so baixam se a pessoa tocar em play, sem afetar o carregamento da pagina.
VIDEOS = {
    # Decisao do Anderson em 13/08/2026: o video de PARCEIROS vai para /dentista/, que
    # concentra 99% dos cliques — a ideia e oferecer um diferencial concreto a quem ja
    # esta procurando dentista. O de CONVENIO fica na /convenio/, como teste isolado.
    "dentista": [
        ("parceiros", "Tem cartão de benefício ou é associado a sindicato? Veja como funciona"),
    ],
    "convenio": [
        ("convenio", "A Dra. Tatiane explica como funciona o atendimento por convênio"),
    ],
}

# Linha sobre parceiros — so na /dentista/, junto do video. Sem percentual e sem valor:
# a ANNA informa as condicoes na conversa, mesmo padrao usado para convenio.
BLOCO_PARCEIROS = (
    '      <div class="fact">\n'
    '        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 8h18v11H3z"/>'
    '<path d="M3 8l3-4h12l3 4"/><path d="M12 8v11"/></svg>\n'
    '        <span>Tem JADAPAX, cartão de benefício ou é associado a sindicato? '
    'Consulte as condições pelo WhatsApp</span>\n'
    '      </div>\n')
MENCIONA_PARCEIROS = {"dentista"}


def bloco_videos(slug, prefixo):
    itens = VIDEOS.get(slug)
    if not itens:
        return ""
    partes = ['    <section class="videos" aria-label="Vídeos">',
              '      <span class="videos-label">Entenda em vídeo</span>']
    for nome, legenda in itens:
        partes.append(
            f'      <figure class="video-card">\n'
            f'        <video controls playsinline preload="none"\n'
            f'               poster="{prefixo}video/{nome}-poster.jpg"\n'
            f'               src="{prefixo}video/{nome}.mp4"></video>\n'
            f'        <figcaption>{legenda}</figcaption>\n'
            f'      </figure>')
    partes.append('    </section>\n')
    return "\n".join(partes)

GTAG_HEAD = f"""  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GTAG_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{GTAG_ID}');
  </script>
"""

GTAG_BODY = f"""  <script>
    // Conversao "Clique no WhatsApp" — anexada a todos os botoes .cta-btn
    document.querySelectorAll('.cta-btn').forEach(function (el) {{
      el.addEventListener('click', function () {{
        gtag('event', 'conversion', {{'send_to': '{CONV_TAG}'}});
      }});
    }});
  </script>
"""

BLOCO_CONVENIO = (
    '      <div class="fact">\n'
    '        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16v12H4z"/>'
    '<path d="M9 7V5h6v2"/><path d="M4 12h16"/></svg>\n'
    '        <span>Atendemos diversos convênios odontológicos — confirme o seu pelo WhatsApp</span>\n'
    '      </div>\n')

# Termos que invalidam a pagina. Cada um mapeado para a regra que o proibe.
BLOQUEADOS = {
    "botox": "Google Ads — medicamento restrito",
    "toxina botul": "Google Ads — medicamento restrito",
    "garantido": "CFO Art. 44, I — promessa de resultado",
    "definitivo": "CFO Art. 44, I — promessa de resultado",
    "resultado garantido": "CFO Art. 44, I",
    "antes e depois": "CFO Art. 44, XII",
    "r$": "CFO Art. 44, I — preço",
    "promoção": "CFO Art. 44, I",
    "gratuito": "CFO Art. 44, I — serviço gratuito",
    "parcelamento": "CFO Art. 44, I — modalidade de pagamento",
    "desconto de": "CFO Art. 44, I — desconto explicito",
}
# NOTA: "cartão de benefício" saiu desta lista por decisao do Anderson em 13/08/2026,
# que informou existir contrato com os parceiros. A ressalva do CFO Art. 44, XIV foi
# apresentada a ele por escrito; a decisao e dele. O percentual (15%/10%) segue
# BLOQUEADO — a pagina so convida a consultar, e a ANNA informa as condicoes na conversa.


def render(template, slug, p):
    html = template
    # Subpaginas ficam um nivel abaixo da raiz: img/ e fonts/ sobem um nivel.
    prefixo = "" if slug == "" else "../"

    # --- textos variaveis ---
    html = re.sub(r"<title>.*?</title>", f"<title>{p['title']}</title>", html, count=1, flags=re.S)
    html = re.sub(r'(<meta name="description" content=")[^"]*(">)',
                  lambda m: m.group(1) + p["meta"] + m.group(2), html, count=1)
    # Hifen nao-separavel (U+2011) em "Itauna-MG" para o titulo nao quebrar feio
    # entre "Itauna-" e "MG" no celular.
    h1 = p["h1"].replace("-MG", "‑MG")
    html = re.sub(r'(<h1 class="title">).*?(</h1>)',
                  lambda m: m.group(1) + h1 + m.group(2), html, count=1, flags=re.S)
    html = re.sub(r'(<p class="subtitle">).*?(</p>)',
                  lambda m: m.group(1) + p["subtitle"] + m.group(2), html, count=1, flags=re.S)
    html = re.sub(r'(<p class="description">).*?(</p>)',
                  lambda m: m.group(1) + p["body"] + m.group(2), html, count=1, flags=re.S)

    # --- horario ---
    html = re.sub(r"(<strong>Atendimento:</strong>)[^<]*", rf"\1 {HORARIO}", html, count=1)

    # --- blocos condicionais ---
    html = html.replace("{BLOCO_CONVENIO}",
                        BLOCO_CONVENIO if slug in MENCIONA_CONVENIO else "")
    html = html.replace("{BLOCO_PARCEIROS}",
                        BLOCO_PARCEIROS if slug in MENCIONA_PARCEIROS else "")
    html = html.replace("{BLOCO_VIDEOS}", bloco_videos(slug, prefixo))

    # --- links e caminhos ---
    wa_url = f"https://wa.me/{WHATS}?text={urllib.parse.quote(p['wa'])}"
    html = html.replace("{LINK_WHATSAPP}", wa_url)
    html = html.replace("{LINK_MAPS}", MAPS)
    html = html.replace("{LINK_AVALIACOES}", AVALIACOES)
    html = html.replace("{PREFIXO}", prefixo)

    # --- rastreamento de conversao ---
    html = html.replace("</head>", GTAG_HEAD + "</head>", 1)
    html = html.replace("</body>", GTAG_BODY + "</body>", 1)
    return html


def texto_visivel(html):
    """So o texto que o paciente le: sem <style>, <script>, atributos nem URLs.
    Evita falso positivo (ex.: '%' em 'width:100%' ou em '%C3%BA' de URL)."""
    t = re.sub(r"<style.*?</style>", " ", html, flags=re.S | re.I)
    t = re.sub(r"<script.*?</script>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)          # remove tags e seus atributos
    return re.sub(r"\s+", " ", t).lower()


def conferir(slug, html):
    problemas = []
    low = html.lower()
    visivel = texto_visivel(html)
    for termo, regra in BLOQUEADOS.items():
        if termo in visivel:
            problemas.append(f"/{slug or '(raiz)'}: termo proibido {termo!r} — {regra}")
    # Percentual de desconto no texto visivel (ex.: "15%", "10 %")
    for m in re.findall(r"\d+\s*%", visivel):
        problemas.append(f"/{slug or '(raiz)'}: percentual no texto {m!r} — CFO Art. 44, I")
    # O marcador de origem precisa existir para a ANNA medir (doc 09, R2).
    # Comparar em minusculas dos dois lados: urllib.quote gera hex maiusculo (%C3%BA).
    if "vi%20o%20an%c3%bancio%20no%20google" not in low:
        problemas.append(f"/{slug or '(raiz)'}: perdeu o marcador 'vi o anúncio no Google'")
    # nada de dependencia externa
    for padrao in ("gpteng", "lovable", "googlefonts", "fonts.googleapis"):
        if padrao in low:
            problemas.append(f"/{slug or '(raiz)'}: dependência externa {padrao!r}")
    # placeholders nao resolvidos
    for ph in re.findall(r"\{LINK_[A-Z]+\}", html):
        problemas.append(f"/{slug or '(raiz)'}: placeholder não substituído {ph}")
    return problemas


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    tpl_path = os.path.join(base, "_template.html")
    if not os.path.exists(tpl_path):
        print(f"ERRO: template não encontrado em {tpl_path}", file=sys.stderr)
        return 1
    template = open(tpl_path, encoding="utf-8").read()

    todos_problemas = []
    gerados = []
    for slug, p in PAGINAS.items():
        html = render(template, slug, p)
        todos_problemas += conferir(slug, html)

        if slug:
            pasta = os.path.join(base, slug)
            os.makedirs(pasta, exist_ok=True)
            destino = os.path.join(pasta, "index.html")
        else:
            destino = os.path.join(base, "index.html")
        with open(destino, "w", encoding="utf-8") as f:
            f.write(html)
        conv = "convênio" if slug in MENCIONA_CONVENIO else "—"
        gerados.append((slug or "(raiz)", p["h1"], conv, len(html)))

    for slug, h1, conv, tam in gerados:
        print(f"[OK] /{slug:<12} {tam/1024:5.1f}KB  {conv:<8}  {h1}")

    print()
    if todos_problemas:
        print("PROBLEMAS DE CONFORMIDADE — nada deve ser publicado:")
        for x in todos_problemas:
            print("  [X]", x)
        return 2
    print("[OK] Conformidade: sem termo proibido, sem dependência externa,")
    print("     marcador de origem presente, placeholders resolvidos.")
    print(f"[OK] {len(gerados)} páginas geradas. NADA foi publicado ainda.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
