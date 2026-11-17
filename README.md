# A Biblioteca Infinita: site

Site do jogo educativo **A Biblioteca Infinita**, para crianças de 6 a 10 anos com dislexia (protótipo em desenvolvimento, ainda sem teste com crianças). Este repositório só tem o site; o código do jogo fica em outro repositório, privado.

## Páginas

`index.html` (início) · `projeto.html` · `historia.html` · `personagens.html` · `andares.html` · `jogos.html` · `como-funciona.html` · `dificuldade.html` · `ciencia.html` · `404.html`

## Estrutura

```
*.html            páginas geradas (é o que o GitHub Pages publica)
assets/           style.css e app.js (cópias geradas de src/)
img/  fonts/      capturas do protótipo (arte provisória) e OpenDyslexic
favicon.svg  og-image.png  sitemap.xml  robots.txt  .nojekyll
src/              fonte: build.py, style.css, app.js, sections/ (textos) e data.json (andares e personagens)
```

## Como editar

1. Edite os textos em `src/sections/*.html`, os dados de andares e personagens em `src/data.json`, o estilo em `src/style.css` e o comportamento em `src/app.js`. Títulos, descrições e a ordem das páginas ficam no início de `src/build.py` (lista `PAGES`).
2. Rode `python3 src/build.py` na raiz (só precisa de Python 3). Ele regenera as páginas, `assets/`, `sitemap.xml` e `robots.txt`.
3. Faça commit em `main`. O Pages republica sozinho (Settings ▸ Pages ▸ Deploy from a branch ▸ `main` ▸ `/ (root)`).

Se o endereço do site mudar (domínio próprio, outro nome de repositório), troque `BASE` em `src/build.py` e rode o build: os links canônicos, o sitemap e a imagem de compartilhamento dependem dele.

## SEO e acessibilidade

Um `<h1>` por página, títulos de até 60 caracteres e descrições únicas, link canônico, Open Graph e Twitter Card com `og-image.png`, dados estruturados (JSON-LD), `sitemap.xml`, `robots.txt`, `404.html`, atributos `alt` e `lang="pt-BR"`. O menu agrupa as páginas em submenus (sem barra de rolagem), funciona por teclado (Esc fecha) e vira botão no celular. As tabelas viram cartões em telas estreitas. O conteúdo e a navegação funcionam sem JavaScript; o JavaScript só acrescenta o fundo animado, a demonstração da dificuldade, o menu no celular e as opções de leitura (fonte OpenDyslexic e mais espaço).

## Créditos

OpenDyslexic (Bitstream Vera License), Baloo 2 e Lexend (SIL OFL, via Google Fonts). As ilustrações dos personagens são SVG deste site e não existem no jogo.
