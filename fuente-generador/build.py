# -*- coding: utf-8 -*-
"""Genera el sitio estático CHEM SAFE (index, fichas y etiquetas).

Uso:  python3 tools/build.py
Salida: carpeta ../site  (lista para publicar en GitHub Pages)
"""
import os, re, html
from data import *

import sys
ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")

SECTIONS = [
    ("s1", "Identificación"),
    ("s2", "Identificación de peligros"),
    ("s3", "Composición"),
    ("s4", "Primeros auxilios"),
    ("s5", "Manipulación y almacenamiento"),
    ("s6", "Equipos de protección personal"),
    ("s7", "Propiedades físicas y químicas"),
    ("s8", "Estabilidad, reactividad y compatibilidad"),
    ("s9", "Emergencias, derrames y eliminación"),
]

ICONS = {
    "i1": '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="11" r="2.2"/><path d="M14 10h4M14 14h4M6 16c.8-1.4 2-2 3-2s2.2.6 3 2"/>',
    "i2": '<path d="M12 3 2.5 20h19z"/><path d="M12 10v4.5M12 17.2v.1"/>',
    "i3": '<path d="M9 3h6M10 3v6l-5.5 9.2A2 2 0 0 0 6.2 21h11.6a2 2 0 0 0 1.7-2.8L14 9V3"/><path d="M7.5 15h9"/>',
    "i4": '<rect x="3" y="3" width="18" height="18" rx="4"/><path d="M12 7.5v9M7.5 12h9"/>',
    "i5": '<path d="M3 8l9-5 9 5v11a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1z"/><path d="M8 20v-7h8v7M8 16.5h8"/>',
    "i6": '<path d="M3 11a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v3a4 4 0 0 1-4 4h-1.5a3 3 0 0 1-2.5-1.5 2 2 0 0 0-3 0A3 3 0 0 1 8.5 18H7a4 4 0 0 1-4-4z"/><path d="M3 11l1.5-5.5M21 11l-1.5-5.5"/>',
    "i7": '<path d="M10 14.8V5a2 2 0 0 1 4 0v9.8a4 4 0 1 1-4 0z"/><path d="M12 9v7"/>',
    "i8": '<path d="M4 8h13l-3-3M20 16H7l3 3"/>',
    "i9": '<path d="M12 3s5 4.4 5 9.2A5 5 0 0 1 7 12.2C7 9 9 7.5 9 7.5s.5 2 2 2c0 0 1.5-2 1-6.5z"/>',
}

def icon(k):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[k]}</svg>'

def sprite():
    return ""  # los iconos se incrustan directamente (sin dependencias)

BRAND_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
             '<path d="M9 3h6M10 3v6l-5.5 9.2A2 2 0 0 0 6.2 21h11.6a2 2 0 0 0 1.7-2.8L14 9V3"/><path d="M12 12.5l2 1v2.5l-2 1-2-1v-2.5z"/></svg>')

def cites(refs):
    if not refs:
        return ""
    out = "".join(f'<a href="#ref{n.strip()}">[{n.strip()}]</a>' for n in refs.split(","))
    return f' <sup class="cite">{out}</sup>'

def fmt(t):
    """Convierte marcas [n] en citas enlazadas."""
    return re.sub(r"\[(\d+)\]", lambda m: f'<sup class="cite"><a href="#ref{m.group(1)}">[{m.group(1)}]</a></sup>', t)

STATE = {"ok": ("✓", "Compatible documentado"), "bad": ("✕", "Incompatible documentado"), "nd": ("?", "Información insuficiente o no determinada")}

def head(title, depth, extra_css=None, accent=None, accent_soft=None):
    pre = "../" * depth
    style = ""
    if accent:
        style = f' style="--accent:{accent};--accent-soft:{accent_soft}"'
    links = f'<link rel="stylesheet" href="{pre}assets/css/styles.css">'
    if extra_css:
        links += f'\n<link rel="stylesheet" href="{pre}assets/css/{extra_css}">'
    return (f'<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{html.escape(title)}</title>\n'
            f'<meta name="description" content="CHEM SAFE: fichas educativas de seguridad química consultables mediante código QR.">\n'
            f'<link rel="icon" href="{pre}assets/img/favicon.svg" type="image/svg+xml">\n{links}\n</head>\n<body{style}>\n')

def topbar(depth, hero_inside=False):
    pre = "../" * depth
    return (f'<header class="topbar"><div class="wrap">'
            f'<a class="school" href="{pre}index.html" title="Colegio San Luis Maristas"><img src="{pre}assets/img/logo-maristas.png" alt="Logo del Colegio San Luis Maristas" width="40" height="40"></a>'
            f'<a class="brand" href="{pre}index.html">{BRAND_SVG}<span>CHEM SAFE<small>Colegio San Luis Maristas</small></span></a>'
            f'<nav aria-label="Principal"><a href="{pre}index.html">Inicio</a><a href="{pre}etiquetas.html">Etiquetas</a></nav>'
            f'</div></header>')

FOOTER = ('<footer class="site"><div class="wrap">'
          '<p><strong>CHEM SAFE</strong> · Colegio San Luis Maristas. Prototipo escolar con fines educativos. Las fichas <strong>no reemplazan la Ficha de Datos de Seguridad (FDS) '
          'oficial</strong> del producto específico que tienes en el laboratorio. Ante una emergencia, avisa al docente y llama a los servicios de emergencia.</p>'
          '</div></footer>')

def picto_imgs(s):
    return "".join(f'<figure class="pict" style="margin:0"><img src="../assets/img/{p}.svg" alt="Pictograma GHS05: corrosión"><figcaption>GHS05<br>Corrosión</figcaption></figure>' for p in s["pictos"])

def hazard_icon(cls):
    if cls == "none":
        return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M8 12.5l3 3 5-6"/></svg>'
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3 2.5 20h19z"/><path d="M12 10v4.5M12 17.2v.1"/></svg>'

def sec(n, inner, featured=False):
    sid, title = SECTIONS[n - 1]
    cls = "sec featured" if featured else "sec"
    return (f'<section class="{cls}" id="{sid}" aria-labelledby="{sid}-h"><h2 id="{sid}-h"><span class="num">{n}</span><span class="ttl">{title}</span>'
            f'<a class="toplink" href="#menu">↑ Menú</a></h2>\n{inner}\n</section>\n')

def dl(rows):
    return '<dl class="dl">' + "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in rows) + "</dl>"

def ul(items):
    return "<ul>" + "".join(f"<li>{fmt(i)}</li>" for i in items) + "</ul>"

def matrix_html(rows):
    out = ['<div class="legend" role="list">']
    for k in ("ok", "bad", "nd"):
        out.append(f'<span role="listitem"><span class="st {k}" aria-hidden="true">{STATE[k][0]}</span>{STATE[k][1]}</span>')
    out.append("</div><div class=\"matrix\">")
    for st, fam, why, refs in rows:
        out.append(f'<div class="mrow {st}"><span class="st {st}" aria-hidden="true">{STATE[st][0]}</span>'
                   f'<div><span class="fam">{fam}</span><span class="lbl">{STATE[st][1]}</span></div>'
                   f'<div class="why">{why}{cites(refs)}</div></div>')
    out.append("</div>")
    return "".join(out)

def ficha(s):
    others = [o for o in SUBSTANCES if o["slug"] != s["slug"]]
    h = head(f'{s["name"]} ({s["formula_plain"]}) · CHEM SAFE', 1, accent=s["accent"], accent_soft=s["accent_soft"])
    h += topbar(1)
    # Encabezado
    h += (f'<div class="hero"><div class="wrap"><p class="kicker">Ficha de seguridad educativa · CHEM SAFE</p>'
          f'<h1>{s["name"]}</h1><div class="hero-row">'
          f'<span class="formula">{s["formula"]}</span>'
          f'<span class="chip">CAS {s["cas"]}</span>'
          f'<span class="hazard-badge {"none" if s["hazard_class"]=="none" else ""}">{hazard_icon(s["hazard_class"])}{s["hazard"]}</span>'
          f'</div></div></div>')
    h += '<main class="wrap">'
    # Información general
    h += ('<div class="facts" aria-label="Información general">'
          f'<div class="fact"><div class="k">Fórmula</div><div class="v">{s["formula"]}</div></div>'
          f'<div class="fact"><div class="k">Número CAS</div><div class="v">{s["cas"]}</div></div>'
          f'<div class="fact"><div class="k">Masa molar</div><div class="v">{s["molar"]}</div></div>'
          f'<div class="fact"><div class="k">Palabra de advertencia</div><div class="v">{s["signal"] or "Ninguna"}</div></div></div>')
    h += ('<div class="notice"><strong>Ficha educativa</strong>Esta ficha no reemplaza la FDS oficial del producto específico. '
          'Los riesgos dependen de la concentración y de la presentación del compuesto.</div>')
    # Menú
    h += '<h2 class="menu-title" id="menu">Secciones de la ficha</h2><ul class="tiles">'
    for i, (sid, t) in enumerate(SECTIONS, 1):
        feat = " featured" if i == 8 else ""
        h += (f'<li><a class="tile{feat}" href="#{sid}"><span class="ico">{icon(f"i{i}")}</span>'
              f'<span class="n">Sección {i}</span><span class="t">{t}</span></a></li>')
    h += "</ul>"

    # 1 Identificación
    usos = ul(s["usos"]) + cites(s["usos_refs"])
    h += sec(1, dl([
        ("Nombre", f'<strong class="formula-big" style="font-size:1.3rem">{s["name"]}</strong>'),
        ("Fórmula química", f'<span class="formula-big">{s["formula"]}</span>'),
        ("Nomenclatura sistemática", s["sistematica"]),
        ("Nomenclatura tradicional", s["tradicional"]),
        ("Número CAS", f'{s["cas"]}{cites("2" if s["slug"]=="acido-sulfurico" else "1" if s["slug"]=="hidroxido-de-sodio" else "2")}'),
        ("Número CE", s["ec"]),
        ("Identificador PubChem", f'CID {s["cid"]}'),
        ("Masa molar", s["molar"]),
        ("Usos habituales", usos),
    ]))

    # 2 Peligros
    hz = s["hazards"]
    if s["pictos"]:
        body = f'<div class="picts">{picto_imgs(s)}<span class="signal">{s["signal"]}</span></div>'
        body += ('<div class="scroll-x"><table class="t"><thead><tr><th>Clase y categoría</th><th>Código</th><th>Indicación de peligro</th></tr></thead><tbody>'
                 + "".join(f"<tr><td>{a}</td><td><strong>{b}</strong></td><td>{c}</td></tr>" for a, b, c in hz["clasif"])
                 + f'</tbody></table></div><p style="font-size:.85rem;color:var(--muted)">Clasificación según el SGA/GHS{cites(hz["class_refs"])}. '
                 'El pictograma mostrado es un dibujo simplificado; los pictogramas oficiales están publicados por UNECE.</p>')
    else:
        body = ('<div class="picts"><div class="nopict">Sin pictogramas de peligro GHS. Las FDS consultadas lo indican como sustancia '
                f'no clasificada{cites(hz["class_refs"])}.</div><span class="signal none">Sin palabra de advertencia</span></div>')
    body += f'<h3>Riesgos para la salud</h3>{ul(hz["salud"])}<p style="font-size:.85rem;color:var(--muted)">Fuentes:{cites(hz["salud_refs"])}</p>'
    body += f'<h3>Riesgos físicos</h3>{ul(hz["fisicos"])}<p style="font-size:.85rem;color:var(--muted)">Fuentes:{cites(hz["fisicos_refs"])}</p>'
    body += f'<h3>Riesgos ambientales</h3><p>{fmt(hz["ambiente"])}</p>'
    body += f'<h3>Advertencias principales</h3><p>{hz["advertencias"]}</p>'
    body += f'<div class="notice"><strong>Concentración y presentación</strong>{fmt(s["concentration_note"])}</div>'
    h += sec(2, body)

    # 3 Composición
    body = ('<div class="scroll-x"><table class="t"><thead><tr><th>Componente</th><th>Fórmula</th><th>Pureza o concentración</th></tr></thead><tbody>'
            + "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}{cites(d)}</td></tr>" for a, b, c, d in s["comp_rows"])
            + "</tbody></table></div>" + ul(s["comp_notes"]))
    h += sec(3, body)

    # 4 Primeros auxilios
    fa = s["fa"]
    body = dl([("Exposición ocular", fa["ojos"]), ("Contacto con la piel", fa["piel"]), ("Inhalación", fa["inhalacion"]),
               ("Ingestión", fa["ingestion"]), ("Síntomas relevantes", fa["sintomas"])])
    body += f'<div class="alert"><strong>Asistencia médica urgente:</strong> {fa["urgente"]}</div>'
    body += f'<p style="font-size:.85rem;color:var(--muted)">Fuentes:{cites(fa["refs"])} Estas medidas son generales; sigue siempre las indicaciones de la FDS del producto y las de tu docente.</p>'
    h += sec(4, body)

    # 5 Manipulación y almacenamiento
    st = s["storage"]
    body = f'<h3>Condiciones de almacenamiento</h3>{ul(st["cond"])}<h3>Precauciones de manipulación</h3>{ul(st["manip"])}'
    body += dl([("Materiales de recipientes", fmt(st["envases"])), ("Condiciones que deben evitarse", st["evitar"]), ("Recomendaciones de segregación", st["segreg"])])
    body += f'<p style="font-size:.85rem;color:var(--muted)">Fuentes:{cites(st["refs"])}</p>'
    h += sec(5, body)

    # 6 EPP
    p = s["ppe"]
    body = dl([("Protección ocular", p["ojos"]), ("Protección de manos", p["manos"]), ("Protección corporal", p["cuerpo"]),
               ("Ventilación y controles", p["vent"])]) + f'<h3>Recomendaciones preventivas</h3>{ul(p["reco"])}'
    body += f'<p style="font-size:.85rem;color:var(--muted)">Fuentes:{cites(p["refs"])}</p>'
    h += sec(6, body)

    # 7 Propiedades
    cards = []
    for k, v, c, r, ok in s["props"]:
        cls = "pcard" if ok else "pcard nd"
        cond = f'<div class="c">{c}</div>' if c else ""
        cards.append(f'<div class="{cls}"><div class="k">{k}</div><div class="v">{v}</div>{cond}<div class="c">{cites(r).strip()}</div></div>')
    body = '<div class="cards three">' + "".join(cards) + "</div>"
    body += '<p style="font-size:.88rem;color:var(--muted)">Los valores provienen de FDS de fabricantes y pueden variar ligeramente según el grado y la concentración. Donde hay diferencias entre fuentes se muestra el intervalo.</p>'
    h += sec(7, body)

    # 8 Compatibilidad
    body = ('<div class="alert"><strong>Importante.</strong> No se asume compatibilidad por falta de información. '
            'Nunca mezcles sustancias «para comprobar» si son compatibles.</div>')
    body += dl([("Estabilidad química", s["stability"]), ("Reactividad conocida", s["reactivity"]),
                ("Condiciones que deben evitarse", s["conditions"]), ("Riesgos de reacciones peligrosas", s["danger_reactions"]),
                ("Productos de descomposición peligrosos", s["decomposition"]),
                ("Almacenamiento separado", s["separate"])])
    body += f'<p style="font-size:.85rem;color:var(--muted)">Fuentes:{cites(s["stab_refs"])}</p>'
    body += "<h3>Matriz visual de compatibilidad</h3>" + matrix_html(s["matrix"])
    # Matriz cruzada de las 3 sustancias
    body += "<h3>Entre las sustancias de CHEM SAFE</h3>" + cross_table(highlight=s["slug"])
    h += sec(8, body, featured=True)

    # 9 Emergencias
    e = s["emerg"]
    body = (f'<h3>Riesgos ante derrames</h3><p>{fmt(e["derrames"])}</p><h3>Precauciones iniciales</h3>{ul(e["precauciones"])}'
            f'<h3>Riesgos en caso de incendio</h3><p>{fmt(e["incendio"])}</p><h3>Medidas generales de emergencia</h3><p>{e["medidas"]}</p>'
            f'<h3>Gestión segura de residuos</h3><p>{e["residuos"]}</p>'
            f'<p style="font-size:.85rem;color:var(--muted)">Fuentes:{cites(e["refs"])}</p>')
    h += sec(9, body)

    # Referencias
    h += ('<section class="sec" id="referencias" aria-labelledby="ref-h"><h2 id="ref-h"><span class="num" style="background:var(--green)">✎</span>Referencias'
          '<a class="toplink" href="#menu">↑ Menú</a></h2>'
          f'<p class="meta"><span>Versión de la ficha: <strong>{VERSION}</strong></span><span>Última actualización: <strong>{UPDATED}</strong></span></p>'
          '<ol class="refs" style="list-style:none">')
    for i, (txt, url) in enumerate(s["refs"], 1):
        h += f'<li id="ref{i}"><span class="id">[{i}]</span> {html.escape(txt)} <a href="{url}" target="_blank" rel="noopener">{html.escape(url)}</a></li>'
    h += ('</ol><div class="notice"><strong>Datos confirmados y datos no disponibles</strong>Los valores se tomaron de las fuentes listadas. '
          'Lo que no aparece en ellas se marca como «No determinado en las fuentes consultadas». '
          'Las consultas directas a PubChem, ECHA y OSHA están pendientes de verificación por el equipo antes de la entrega final.</div>'
          '<p class="noprint"><button class="btn ghost" type="button" data-print>Imprimir esta ficha</button></p></section>')
    h += '</main>' + FOOTER + '<script src="../assets/js/app.js"></script>\n</body>\n</html>\n'
    return h

def cross_table(highlight=None):
    names = [(s["slug"], s["formula"]) for s in SUBSTANCES]
    t = ['<div class="scroll-x"><table class="xmatrix" aria-label="Compatibilidad entre las tres sustancias"><thead><tr><th></th>']
    for _, f in names:
        t.append(f"<th>{f}</th>")
    t.append("</tr></thead><tbody>")
    for rs, rf in names:
        t.append(f"<tr><th>{rf}</th>")
        for cs, cf in names:
            if rs == cs:
                t.append('<td class="diag">—</td>')
                continue
            key = (rs, cs) if (rs, cs) in CROSS else (cs, rs)
            st, note = CROSS[key]
            t.append(f'<td class="{st}"><span class="st {st}" aria-hidden="true">{STATE[st][0]}</span><br>{note}</td>')
        t.append("</tr>")
    t.append("</tbody></table></div>")
    t.append('<p style="font-size:.85rem;color:var(--muted)">Base: incompatibilidades listadas en FDS del ácido sulfúrico (bases fuertes y haluros). La pareja H₂SO₄ – NaCl se refiere al ácido concentrado. '
             'Sin información sobre la pareja NaOH – NaCl: no se asume compatibilidad.</p>')
    return "".join(t)

def index():
    h = head("CHEM SAFE · Fichas de seguridad química con QR", 0)
    h += topbar(0)
    h += ('<main class="wrap"><section class="intro"><h1>Escanea la etiqueta.<br>Conoce el riesgo.</h1>'
          '<p>CHEM SAFE reúne fichas digitales de seguridad para las sustancias de nuestro laboratorio. Cada frasco lleva un código QR que abre su ficha en el celular.</p></section>')
    h += '<h2 class="h2" style="margin-top:0">Sustancias</h2><div class="subs">'
    for s in SUBSTANCES:
        hz = "Peligro · Corrosivo" if s["hazard_class"] == "bad" else "Sin clasificación GHS"
        cls = "bad" if s["hazard_class"] == "bad" else "ok"
        h += (f'<a class="sub" style="--accent:{s["accent"]};--accent-soft:{s["accent_soft"]}" href="fichas/{s["slug"]}.html">'
              f'<span class="f">{s["formula"]}</span><span class="nm">{s["name"]}</span><span class="cas">CAS {s["cas"]}</span>'
              f'<span class="hz {cls}">{hz}</span></a>')
    h += '</div>'
    h += ('<h2 class="h2">Cómo se usa</h2><ol class="how"><li><strong>Identifica</strong><br>Lee el nombre y la fórmula de la etiqueta.</li>'
          '<li><strong>Escanea</strong><br>Apunta la cámara al código QR.</li>'
          '<li><strong>Consulta</strong><br>Revisa peligros, EPP, primeros auxilios y compatibilidad.</li></ol>')
    h += ('<h2 class="h2">Compatibilidad entre sustancias</h2>'
          '<p style="max-width:62ch">Resumen de las tres sustancias iniciales. Los estados se basan en incompatibilidades documentadas en FDS. '
          'Lo que no está documentado queda como «sin información».</p>' + 
          '<div class="legend"><span><span class="st ok">✓</span>Compatible documentado</span><span><span class="st bad">✕</span>Incompatible documentado</span><span><span class="st nd">?</span>Información insuficiente</span></div>'
          + cross_table())
    h += ('<h2 class="h2">Etiquetas para imprimir</h2><p style="max-width:62ch">Genera las etiquetas con el QR una vez que el sitio esté publicado y verificado.</p>'
          '<p><a class="btn" href="etiquetas.html">Ir a las etiquetas</a></p></main>')
    h += FOOTER + '</body>\n</html>\n'
    return h

def etiquetas():
    h = head("Etiquetas · CHEM SAFE", 0, extra_css="labels.css")
    h += topbar(0)
    h += ('<main class="wrap"><section class="intro" style="padding-bottom:10px"><h1 style="font-size:clamp(1.8rem,6vw,2.6rem)">Etiquetas con código QR</h1>'
          '<p>Los códigos QR solo se generan cuando escribes la URL pública del sitio y confirmas que los enlaces funcionan.</p></section>')
    h += ('<section class="controls" aria-label="Configuración"><label class="lb" for="base-url">URL pública del sitio (GitHub Pages)</label>'
          '<div class="row"><input id="base-url" type="url" inputmode="url" placeholder="https://tu-usuario.github.io/chem-safe/" autocomplete="off">'
          '<button class="btn" id="apply" type="button">Generar QR</button></div><p id="status" role="status"></p>'
          '<p style="margin:10px 0 4px;font-size:.9rem"><strong>Enlaces que codifican los QR:</strong></p><ul id="links"></ul>'
          '<label class="ck"><input type="checkbox" id="confirm" disabled><span>Abrí cada enlace y cada uno muestra la ficha correcta.</span></label>'
          '<button class="btn" id="print" type="button" disabled>Imprimir etiquetas</button></section>')
    h += '<div class="sheet" aria-label="Vista previa de etiquetas">'
    for s in SUBSTANCES:
        pic = ('<img src="assets/img/ghs05.svg" alt="Pictograma GHS05: corrosión">' if s["pictos"]
               else '<div class="nopic">Sin pictograma</div>')
        sig = f'<b>{s["signal"]}</b>' if s["signal"] else "<b>Sin clasificación</b>"
        h += (f'<article class="label" style="--accent:{s["accent"]}"><div class="info"><p class="nm">{s["name"]}</p>'
              f'<p class="fm">{s["formula"]}</p>'
              f'<p class="nom"><b>Sistemática:</b> {s["sistematica"]}<br><b>Tradicional:</b> {s["tradicional"]}</p>'
              '<div class="school-mark"><img src="assets/img/logo-maristas.png" alt="" width="20" height="20"><span>Colegio San Luis Maristas</span></div></div>'
              f'<div class="side"><div class="qr" data-qr="{s["slug"]}"></div><div class="scan">Escanea para ver la ficha</div></div>'
              f'<div class="foot">{pic}<div class="w">{sig}{s["label_warning"]}</div></div></article>')
    h += '</div></main>' + FOOTER
    h += ('<script src="assets/js/qrcode.js"></script>\n<script src="assets/js/config.js"></script>\n<script src="assets/js/labels.js"></script>\n</body>\n</html>\n')
    return h

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

if __name__ == "__main__":
    write("index.html", index())
    write("etiquetas.html", etiquetas())
    for s in SUBSTANCES:
        write(f"fichas/{s['slug']}.html", ficha(s))
    write(".nojekyll", "")
    write("assets/img/favicon.svg",
          '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#263B35"/>'
          '<g fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 6h8M13.5 6v7L8 22.5a2 2 0 0 0 1.7 3h12.6a2 2 0 0 0 1.7-3L18.5 13V6"/><path d="M10.5 19h11"/></g></svg>')
    print("Sitio generado en", os.path.abspath(ROOT))
