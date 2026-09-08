# AML-CS website

Sitio estático del Applied Math and Computer Science Lab (Universidad del Norte).
No necesita Hugo ni Jekyll: es HTML, CSS y JS puros, listo para GitHub Pages.

## Cómo publicar

1. Borra el contenido anterior del repo `AML-CS.github.io` (o crea una rama nueva).
2. Copia **todo** lo que hay en esta carpeta en la raíz del repo.
3. `git add -A && git commit -m "Nuevo diseño" && git push`
4. En Settings → Pages asegúrate de que la fuente sea la rama `master`/`main`, carpeta `/ (root)`.

## Estructura

- `index.html` — portada
- `projects/` — proyectos y financiadores (Banco de la República, Minciencias)
- `publications/` — lista completa con filtros
- `people/`, `talks/`, `resources/`, `wrf-baq-0.5km/`
- `assets/css/site.css` — todo el diseño
- `assets/js/site.js` — menú móvil, animación del hero, filtros de publicaciones
- `assets/img/` — logo, fotos y figuras

## Cómo editar

- **Publicaciones y contenido**: el sitio se genera con `build.py` (incluido). Edita la lista `PUBS`
  o los textos en ese archivo y ejecuta `python3 build.py` para regenerar todas las páginas.
  También puedes editar los `.html` directamente si es un cambio pequeño.
- **Logos de patrocinadores**: en `assets/img/sponsors/`.
- **Fotos de estudiantes**: `assets/img/people/`, cuadradas (480×480).
