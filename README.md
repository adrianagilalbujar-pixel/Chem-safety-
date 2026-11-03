# CHEM SAFE — fichas digitales de seguridad química con QR

Prototipo escolar: sitio web estático (HTML + CSS + JavaScript, sin servidores ni bases de datos) compatible con GitHub Pages.

## Contenido

| Ruta | Qué es |
|---|---|
| `index.html` | Página principal: sustancias, cómo se usa y matriz de compatibilidad entre las tres sustancias |
| `fichas/acido-sulfurico.html` | Ficha de H₂SO₄ |
| `fichas/hidroxido-de-sodio.html` | Ficha de NaOH |
| `fichas/cloruro-de-sodio.html` | Ficha de NaCl |
| `etiquetas.html` | Etiquetas imprimibles (100 × 62 mm) y generador de QR |
| `assets/` | Logo del colegio, CSS, JavaScript (incluye `qrcode.js`, MIT, incluido localmente), pictograma e icono |
| `fuente-generador/` | Script Python y datos con los que se generaron las páginas (opcional) |

Todas las rutas son **relativas**, por lo que funcionan en `https://usuario.github.io/nombre-repo/`.

## Publicar en GitHub Pages

1. Crea una cuenta en <https://github.com> y un repositorio **público** nuevo, por ejemplo `chem-safe`.
2. Pulsa **Add file → Upload files** y arrastra **el contenido** de esta carpeta (no la carpeta contenedora): `index.html`, `etiquetas.html`, `fichas/`, `assets/`, `.nojekyll`, `README.md`.
   Confirma con **Commit changes**.
3. Ve a **Settings → Pages**. En *Build and deployment* elige **Deploy from a branch**, rama `main`, carpeta `/ (root)` y guarda.
4. Espera uno o dos minutos. La dirección será `https://TU-USUARIO.github.io/chem-safe/`.

## Verificar antes de imprimir (importante)

1. Abre `https://TU-USUARIO.github.io/chem-safe/` y cada ficha desde tu celular.
2. Abre `etiquetas.html`, escribe la URL base (con `https://`) y pulsa **Generar QR**.
3. Abre cada enlace que aparece bajo el campo. Cuando las tres fichas carguen bien, marca la casilla y pulsa **Imprimir etiquetas**.
4. Escanea una etiqueta impresa con el celular para confirmar que abre la ficha correcta.

Los QR **no se generan** hasta que escribes una URL `https://`. Para no tener que escribirla cada vez, edita `assets/js/config.js` y pon tu URL en `CHEMSAFE_BASE_URL`; también puedes abrir `etiquetas.html?base=https://TU-USUARIO.github.io/chem-safe/`.

## Qué falta verificar por el equipo

- **Consulta directa de PubChem, ECHA y OSHA.** Los datos de esta versión se contrastaron con Fichas de Datos de Seguridad (FDS) de varios fabricantes y proveedores (lista completa al final de cada ficha). Las páginas de PubChem/ECHA/OSHA no se consultaron directamente; los números CAS, CE y CID aparecen como identificadores, pero conviene confirmarlos allí.
- **Pictograma GHS05.** Es un dibujo simplificado. Para uso definitivo, descarga los pictogramas oficiales de UNECE y reemplaza `assets/img/ghs05.svg` (mismo nombre de archivo).
- **Nomenclatura.** La sistemática y la tradicional siguen convenciones escolares; que tu docente confirme cuál usa tu curso.
- **FDS del frasco real.** Las fichas son educativas y no reemplazan la FDS del producto específico.

## Modificar o añadir sustancias

Los textos están en `fuente-generador/data.py`. Para regenerar todo el sitio desde la raíz del repositorio:

```
python3 fuente-generador/build.py .
```

Añade una nueva sustancia copiando uno de los bloques de `data.py` y agregándolo a la lista `SUBSTANCES`. Regla del proyecto: **no escribir ningún dato que no esté respaldado por una fuente citada**; lo desconocido se marca como «No determinado en las fuentes consultadas» y la compatibilidad nunca se asume.
