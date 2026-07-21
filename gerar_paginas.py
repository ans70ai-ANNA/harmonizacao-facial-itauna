#!/usr/bin/env python3
"""
Gera uma landing page por servico, a partir do mesmo template visual da pagina atual.

Cada pagina: mesmo visual, mesmo rastreamento de conversao, mesmo rodape (CRO — exigencia
do CFO), mas com H1/subtitulo/corpo e TEXTO PRE-PREENCHIDO DO WHATSAPP proprios do servico.

Regras de conformidade aplicadas a todas:
  - nenhuma promessa de resultado (CFO)
  - nenhum preco
  - nenhuma mencao a "botox"/"toxina botulinica" (politica Google Ads)
  - marcador "vi o anuncio no Google" preservado em todas (medicao da ANNA, regra R2 doc 09)

Uso: python3 gerar_paginas.py
"""
import os
import urllib.parse

WHATS = "5537999220550"
CONV_TAG = "AW-18305804748/opogCLXGxM0cEMzT8ZhE"
GTAG_ID = "AW-18305804748"
MAPS = "https://share.google/Lxpgk0PGhm8d8SXDa"

PAGINAS = {
    "clareamento": {
        "title": "Clareamento Dental em Itaúna-MG | Dra. Tatiane Mizael",
        "meta": "Clareamento dental a laser na Ampla Odontologia, com a Dra. Tatiane Mizael — Itaúna-MG.",
        "h1": "Clareamento Dental em Itaúna-MG",
        "subtitle": "Clareamento a laser com equipamento importado, na Ampla Odontologia — Dra. Tatiane Mizael",
        "body": "Avaliação individualizada para definir a técnica adequada ao seu caso. "
                "Tire suas dúvidas diretamente pelo WhatsApp.",
        "wa": "Olá, vi o anúncio no Google e quero saber sobre clareamento dental",
    },
    "dentista": {
        "title": "Dentista em Itaúna-MG | Ampla Odontologia",
        "meta": "Clínica odontológica no centro de Itaúna-MG, com a Dra. Tatiane Mizael.",
        "h1": "Dentista em Itaúna-MG",
        "subtitle": "Clínica Ampla Odontologia, no centro de Itaúna — Dra. Tatiane Mizael",
        "body": "Atendimento humanizado no centro de Itaúna, perto do comércio e do ponto de ônibus. "
                "Agende sua consulta pelo WhatsApp.",
        "wa": "Olá, vi o anúncio no Google e quero saber sobre consulta odontológica",
    },
    "limpeza": {
        "title": "Limpeza Dental em Itaúna-MG | Dra. Tatiane Mizael",
        "meta": "Limpeza dental, profilaxia e remoção de tártaro em Itaúna-MG, na Ampla Odontologia.",
        "h1": "Limpeza Dental em Itaúna-MG",
        "subtitle": "Profilaxia e remoção de tártaro — Dra. Tatiane Mizael, Ampla Odontologia",
        "body": "Limpeza profissional com avaliação individualizada, no centro de Itaúna. "
                "Agende pelo WhatsApp.",
        "wa": "Olá, vi o anúncio no Google e quero saber sobre limpeza dental",
    },
    "facetas": {
        "title": "Facetas e Lentes de Contato Dental em Itaúna-MG | Dra. Tatiane Mizael",
        "meta": "Facetas de porcelana e lentes de contato dental em Itaúna-MG, na Ampla Odontologia.",
        "h1": "Facetas e Lentes de Contato Dental",
        "subtitle": "Facetas de porcelana e resina em Itaúna-MG — Dra. Tatiane Mizael, Ampla Odontologia",
        "body": "Avaliação individualizada para definir o que se adequa ao seu caso. "
                "Fale com a gente pelo WhatsApp.",
        "wa": "Olá, vi o anúncio no Google e quero saber sobre facetas e lentes de contato dental",
    },
    "bruxismo": {
        "title": "Placa de Bruxismo e ATM em Itaúna-MG | Dra. Tatiane Mizael",
        "meta": "Placa para bruxismo e avaliação de ATM em Itaúna-MG, na Ampla Odontologia.",
        "h1": "Placa de Bruxismo e ATM",
        "subtitle": "Placa sob medida e avaliação de disfunção de ATM em Itaúna-MG — Dra. Tatiane Mizael",
        "body": "Avaliação individualizada para bruxismo e dores na articulação da mandíbula. "
                "Agende pelo WhatsApp.",
        "wa": "Olá, vi o anúncio no Google e quero saber sobre placa de bruxismo",
    },
}

TEMPLATE = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{meta}">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={gtag_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{gtag_id}');
</script>
<style>
  :root {{
    --bg: #faf8f6; --card: #ffffff; --text: #2b2622; --muted: #6b6058;
    --accent: #b98b5e; --whatsapp: #25D366; --whatsapp-dark: #1da851;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: var(--bg); color: var(--text); line-height: 1.5;
  }}
  .wrap {{ max-width: 480px; margin: 0 auto; padding: 0 0 40px; }}
  .hero {{ position: relative; width: 100%; aspect-ratio: 1.91 / 1; overflow: hidden; }}
  .hero img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
  header.content {{ text-align: center; padding: 28px 24px 8px; }}
  h1 {{ font-size: 1.5rem; margin: 0 0 8px; color: var(--text); }}
  .subtitle {{ font-size: 1rem; color: var(--muted); margin: 0 0 20px; }}
  .cta-wrap {{ padding: 0 24px; text-align: center; }}
  .cta-btn {{
    display: inline-flex; align-items: center; justify-content: center; gap: 10px;
    width: 100%; background: var(--whatsapp); color: #fff; font-size: 1.1rem;
    font-weight: 600; text-decoration: none; padding: 16px 20px; border-radius: 14px;
    box-shadow: 0 6px 16px rgba(37, 211, 102, 0.35); transition: background 0.15s ease;
  }}
  .cta-btn:active {{ background: var(--whatsapp-dark); }}
  .cta-btn svg {{ width: 24px; height: 24px; flex-shrink: 0; }}
  .body-text {{ padding: 24px 24px 8px; text-align: center; color: var(--text); font-size: 0.98rem; }}
  .portrait-card {{
    margin: 24px 24px 0; background: var(--card); border-radius: 16px;
    overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.06);
  }}
  .portrait-card img {{ width: 100%; display: block; }}
  .portrait-caption {{ padding: 14px 18px 18px; text-align: center; font-size: 0.92rem; color: var(--muted); }}
  .secondary {{ text-align: center; margin: 20px 24px 0; }}
  .secondary a {{
    color: var(--accent); text-decoration: none; font-size: 0.95rem;
    border-bottom: 1px solid var(--accent); padding-bottom: 2px;
  }}
  footer {{
    margin-top: 32px; padding: 18px 24px 0; border-top: 1px solid #e8e2db;
    text-align: center; color: var(--muted); font-size: 0.78rem; line-height: 1.6;
  }}
</style>
</head>
<body>
  <div class="wrap">
    <div class="hero">
      <img src="../img/fachada.jpg" alt="Fachada da Ampla Odontologia em Itaúna-MG">
    </div>

    <header class="content">
      <h1>{h1}</h1>
      <p class="subtitle">{subtitle}</p>
    </header>

    <div class="cta-wrap">
      <a class="cta-btn" href="https://wa.me/{whats}?text={wa_encoded}" target="_blank" rel="noopener" id="whatsapp-cta" onclick="gtag('event', 'conversion', {{'send_to': '{conv_tag}'}});">
        <svg viewBox="0 0 32 32" fill="currentColor" aria-hidden="true"><path d="M16.001 3C9.373 3 4 8.373 4 15c0 2.362.687 4.564 1.874 6.417L4 29l7.762-1.84A11.94 11.94 0 0 0 16 27c6.627 0 12-5.373 12-12S22.628 3 16.001 3zm0 21.75c-1.99 0-3.85-.55-5.44-1.51l-.39-.23-4.61 1.09 1.13-4.49-.25-.4A9.7 9.7 0 0 1 5.25 15c0-5.93 4.82-10.75 10.75-10.75S26.75 9.07 26.75 15 21.93 24.75 16 24.75zm5.86-8.06c-.32-.16-1.9-.94-2.19-1.05-.29-.11-.51-.16-.72.16-.21.32-.83 1.05-1.02 1.26-.19.21-.37.24-.69.08-.32-.16-1.35-.5-2.57-1.59-.95-.85-1.59-1.9-1.78-2.22-.19-.32-.02-.49.14-.65.14-.14.32-.37.48-.55.16-.19.21-.32.32-.53.11-.21.05-.4-.03-.56-.08-.16-.72-1.74-.99-2.38-.26-.63-.53-.54-.72-.55-.19-.01-.4-.01-.61-.01-.21 0-.56.08-.85.4-.29.32-1.11 1.09-1.11 2.65 0 1.56 1.14 3.07 1.3 3.28.16.21 2.24 3.42 5.42 4.8.76.33 1.35.52 1.81.67.76.24 1.45.21 2 .13.61-.09 1.9-.78 2.17-1.53.27-.75.27-1.4.19-1.53-.08-.13-.29-.21-.61-.37z"/></svg>
        Falar no WhatsApp
      </a>
    </div>

    <p class="body-text">{body}</p>

    <div class="portrait-card">
      <img src="../img/dra-tatiane.jpg" alt="Dra. Tatiane Mizael">
      <p class="portrait-caption">Dra. Tatiane Mizael — Ampla Odontologia</p>
    </div>

    <div class="cta-wrap" style="margin-top:24px">
      <a class="cta-btn" href="https://wa.me/{whats}?text={wa_encoded}" target="_blank" rel="noopener" onclick="gtag('event', 'conversion', {{'send_to': '{conv_tag}'}});">
        <svg viewBox="0 0 32 32" fill="currentColor" aria-hidden="true"><path d="M16.001 3C9.373 3 4 8.373 4 15c0 2.362.687 4.564 1.874 6.417L4 29l7.762-1.84A11.94 11.94 0 0 0 16 27c6.627 0 12-5.373 12-12S22.628 3 16.001 3zm0 21.75c-1.99 0-3.85-.55-5.44-1.51l-.39-.23-4.61 1.09 1.13-4.49-.25-.4A9.7 9.7 0 0 1 5.25 15c0-5.93 4.82-10.75 10.75-10.75S26.75 9.07 26.75 15 21.93 24.75 16 24.75zm5.86-8.06c-.32-.16-1.9-.94-2.19-1.05-.29-.11-.51-.16-.72.16-.21.32-.83 1.05-1.02 1.26-.19.21-.37.24-.69.08-.32-.16-1.35-.5-2.57-1.59-.95-.85-1.59-1.9-1.78-2.22-.19-.32-.02-.49.14-.65.14-.14.32-.37.48-.55.16-.19.21-.32.32-.53.11-.21.05-.4-.03-.56-.08-.16-.72-1.74-.99-2.38-.26-.63-.53-.54-.72-.55-.19-.01-.4-.01-.61-.01-.21 0-.56.08-.85.4-.29.32-1.11 1.09-1.11 2.65 0 1.56 1.14 3.07 1.3 3.28.16.21 2.24 3.42 5.42 4.8.76.33 1.35.52 1.81.67.76.24 1.45.21 2 .13.61-.09 1.9-.78 2.17-1.53.27-.75.27-1.4.19-1.53-.08-.13-.29-.21-.61-.37z"/></svg>
        Falar no WhatsApp
      </a>
    </div>

    <div class="secondary">
      <a href="{maps}" target="_blank" rel="noopener">📍 Ver no Google Maps</a>
    </div>

    <footer>
      Dra. Tatiane Mizael — CRO MG35169<br>
      R. Cel. Francisco Manoel Franco, 54 - Setor Centro, Itaúna - MG, 35680-053
    </footer>
  </div>
</body>
</html>
"""

BLOQUEADOS = ["botox", "toxina botul", "garantido", "perfeito", "definitivo",
              "melhor resultado", "R$", "preço", "promoção"]

base = os.path.dirname(os.path.abspath(__file__))
problemas = []

for slug, p in PAGINAS.items():
    html = TEMPLATE.format(
        title=p["title"], meta=p["meta"], h1=p["h1"], subtitle=p["subtitle"],
        body=p["body"], wa_encoded=urllib.parse.quote(p["wa"]),
        whats=WHATS, conv_tag=CONV_TAG, gtag_id=GTAG_ID, maps=MAPS,
    )
    # checagem de conformidade antes de gravar
    low = html.lower()
    for termo in BLOQUEADOS:
        if termo.lower() in low:
            problemas.append(f"{slug}: contem termo proibido {termo!r}")

    pasta = os.path.join(base, slug)
    os.makedirs(pasta, exist_ok=True)
    with open(os.path.join(pasta, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] /{slug}/index.html  — H1: {p['h1']}")

print()
if problemas:
    print("PROBLEMAS DE CONFORMIDADE:")
    for x in problemas:
        print("  [X]", x)
else:
    print("[OK] Nenhuma promessa de resultado, preco ou termo bloqueado encontrado.")
print(f"[OK] {len(PAGINAS)} paginas geradas. NADA foi publicado ainda.")
