#!/usr/bin/env python3
"""Gera as páginas do site a partir de src/ (sections/, data.json, style.css, app.js).
Uso: python3 src/build.py   (na raiz do repositório). Saída: *.html, assets/, sitemap.xml, robots.txt.
Mude BASE se o endereço do site for outro."""
import json, re, os, html
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE='https://palflinho.github.io/biblioteca_infinita/'
LASTMOD='2026-11-18'
SITE='A Biblioteca Infinita'
D=json.load(open('src/data.json',encoding='utf-8'))
SEC={os.path.basename(f)[:-5]:open('src/sections/'+f,encoding='utf-8').read() for f in os.listdir('src/sections')}

PAGES=[
 dict(slug='index',nav='Início',title='A Biblioteca Infinita: jogo para crianças com dislexia',
      desc='Jogo educativo para crianças de 6 a 10 anos com dislexia: uma história na Biblioteca, jogos de letras e sílabas e relatório para o adulto.'),
 dict(slug='projeto',nav='O projeto',title='O projeto e a situação atual | A Biblioteca Infinita',
      desc='O que é A Biblioteca Infinita, para quem foi feita, o que não é e em que ponto o protótipo está hoje.',
      sections=['projeto','situacao'],tiles='o,l'),
 dict(slug='historia',nav='A história',title='A história do jogo | A Biblioteca Infinita',
      desc='A premissa de mapear os caminhos da Biblioteca, o ciclo de um andar e as regras que protegem a brincadeira.',
      sections=['historia'],tiles='b,d'),
 dict(slug='personagens',nav='Personagens',title='Personagens do jogo | A Biblioteca Infinita',
      desc='A Biblioteca, a bibliotecária, o menino e os rascunhos dos próximos personagens que a criança encontra.',
      sections=['personagens'],tiles='p,q'),
 dict(slug='andares',nav='Os andares',title='Os dez andares da Biblioteca | A Biblioteca Infinita',
      desc='Cada um dos dez andares: o jogo, o cenário, quem está perdido, a frase da história e o pedaço do mapa.',
      sections=['andares'],tiles='m,n'),
 dict(slug='jogos',nav='Os jogos',title='Jogos de letras, sílabas e ritmo | A Biblioteca Infinita',
      desc='Acha a Letra, Esprema a Sílaba, Quem Sumiu e Segue o Ritmo: o que a criança faz em cada jogo e o que ele treina.',
      sections=['jogos'],tiles='u,w'),
 dict(slug='como-funciona',nav='Como funciona',title='Como o jogo funciona | A Biblioteca Infinita',
      desc='Da calibração à Sala de Entrada, dos andares à revisão e ao relatório para o adulto: a jornada completa da criança.',
      sections=['jornada','adulto'],tiles='a,e',h1='Da calibração ao relatório',lead='Os passos que a criança percorre dentro do jogo e o que o adulto recebe no fim.'),
 dict(slug='dificuldade',nav='Dificuldade',title='Dificuldade adaptativa no jogo | A Biblioteca Infinita',
      desc='Duas réguas separadas, uma para o conteúdo e outra para a velocidade, e uma demonstração interativa de como o jogo se ajusta.',
      sections=['dificuldade'],tiles='b,p'),
 dict(slug='ciencia',nav='Ciência',title='Base científica e limites | A Biblioteca Infinita',
      desc='O que a pesquisa sustenta, o que é hipótese e por que ainda não se sabe se o jogo melhora a leitura.',
      sections=['ciencia'],tiles='d,q'),
]
BY={p['slug']:p for p in PAGES}
def url(p): return BASE if p['slug']=='index' else BASE+p['slug']+'.html'
def href(p): return 'index.html' if p['slug']=='index' else p['slug']+'.html'

GROUPS=[('A história',['historia','personagens','andares']),('O jogo',['jogos','como-funciona','dificuldade'])]
def nav(cur):
    def a(slug,label=None):
        p=BY[slug];c=' aria-current="page"' if slug==cur else ''
        return '<a href="%s"%s>%s</a>'%(href(p),c,label or p['nav'])
    li=['<li>%s</li>'%a('index'),'<li>%s</li>'%a('projeto')]
    for name,slugs in GROUPS:
        here=' has-current' if cur in slugs else ''
        li.append('<li class="dd%s"><button class="dd-btn" type="button" aria-expanded="false" aria-haspopup="true">%s</button><ul class="sub">%s</ul></li>'%(here,name,''.join('<li>%s</li>'%a(s) for s in slugs)))
    li.append('<li>%s</li>'%a('ciencia'))
    li.append('<li class="dd tools"><button class="dd-btn" type="button" aria-expanded="false" aria-haspopup="true">Leitura</button><ul class="sub"><li><button class="tbtn" id="fontBtn" type="button" aria-pressed="false">Fonte OpenDyslexic</button></li><li><button class="tbtn" id="roomy" type="button" aria-pressed="false">Mais espaço</button></li></ul></li>')
    return '<header class="site-header"><div class="in hbar"><a class="brand" href="index.html" aria-label="A Biblioteca Infinita, página inicial"><svg viewBox="0 0 32 32" width="30" height="30" aria-hidden="true"><rect x="3" y="6" width="7" height="21" rx="2" fill="#ff6f61"/><rect x="12" y="3" width="7" height="24" rx="2" fill="#4cc9f0"/><rect x="21" y="8" width="8" height="19" rx="2" fill="#ffc83d"/></svg><span>A Biblioteca <b>Infinita</b></span></a><button class="burger" id="burger" type="button" aria-expanded="false" aria-controls="menu"><span class="sr">Abrir o </span>menu</button><nav id="menu" aria-label="Principal"><ul>%s</ul></nav></div></header>'%''.join(li)

def head(p):
    t=html.escape(p['title']);d=html.escape(p['desc'],quote=True);u=url(p)
    ld=[{"@context":"https://schema.org","@type":"WebPage","@id":u+'#webpage',"url":u,"name":p['title'],"description":p['desc'],"inLanguage":"pt-BR","isPartOf":{"@id":BASE+'#website'}}]
    if p['slug']=='index':
        ld.append({"@context":"https://schema.org","@type":"WebSite","@id":BASE+'#website',"url":BASE,"name":SITE,"description":p['desc'],"inLanguage":"pt-BR",
          "creator":[{"@type":"Person","name":"Kennya Lacerda"},{"@type":"Person","name":"Paulo Cavalheiro"},{"@type":"Person","name":"Lucas Weber"}]})
    else:
        ld.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
          {"@type":"ListItem","position":1,"name":"Início","item":BASE},{"@type":"ListItem","position":2,"name":p['nav'],"item":u}]})
    return '''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>%s</title>
<meta name="description" content="%s">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="author" content="Kennya Lacerda, Paulo Cavalheiro e Lucas Weber">
<meta name="theme-color" content="#1a1450">
<link rel="canonical" href="%s">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<meta property="og:type" content="website">
<meta property="og:site_name" content="%s">
<meta property="og:locale" content="pt_BR">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s">
<meta property="og:image" content="%sog-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="A Biblioteca Infinita: título do jogo sobre um céu noturno com estantes coloridas">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%s">
<meta name="twitter:description" content="%s">
<meta name="twitter:image" content="%sog-image.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;700;800&family=Lexend:wght@400;500;600&display=swap">
<link rel="stylesheet" href="assets/style.css">
<script type="application/ld+json">%s</script>
</head>
<body>
<a class="skip" href="#conteudo">Ir para o conteúdo</a>
'''%(t,d,u,SITE,t,d,u,BASE,t,d,BASE,json.dumps(ld,ensure_ascii=False))

def foot(cur):
    cols=''.join('<li><a href="%s">%s</a></li>'%(href(p),p['nav']) for p in PAGES)
    return '''<footer class="site-footer"><div class="in">
<div class="dots" aria-hidden="true"><i style="background:var(--coral)"></i><i style="background:var(--lamp)"></i><i style="background:var(--mint)"></i><i style="background:var(--sky)"></i><i style="background:var(--grape)"></i></div>
<nav aria-label="Mapa do site"><ul class="fnav">%s</ul></nav>
<p><strong>A Biblioteca Infinita</strong> é um projeto em desenvolvimento por Kennya Lacerda, Paulo Cavalheiro e Lucas Weber. Feito com Unity e C#. Os textos de história, as ilustrações deste site e os valores de dificuldade são provisórios. As capturas de tela vêm do protótipo, com arte provisória.</p>
<p class="small">O jogo não diagnostica nem trata dislexia e não substitui avaliação com profissionais.</p>
</div></footer>
<script src="assets/app.js" defer></script>
</body>
</html>
'''%cols

# ---------- transformações do conteúdo extraído ----------
def parse(slug):
    raw=SEC[slug]; cls=re.match(r'<!--(\w+)-->',raw).group(1); body=raw.split('-->',1)[1]
    return cls,body
def promote(b):
    def rep(m):
        style=re.sub(r'font-size:(1\.7rem|2rem);?','',m.group(1)).strip().strip(';')
        return '<h2 class="sub"%s>%s</h2>'%(' style="%s"'%style if style else '',m.group(2))
    return re.sub(r'<h3 style="([^"]*font-size:(?:1\.7rem|2rem)[^"]*)">(.*?)</h3>',rep,b,flags=re.S)
def table_labels(b):
    def one(m):
        t=m.group(0);heads=[re.sub('<.*?>','',h) for h in re.findall(r'<th>(.*?)</th>',t,re.S)]
        def row(r):
            i=[0]
            def td(x):
                l=heads[i[0]] if i[0]<len(heads) else '';i[0]+=1
                return '<td data-label="%s">'%html.escape(l)
            return re.sub(r'<td>',td,r.group(0))
        return re.sub(r'<tr>.*?</tr>',row,t,flags=re.S)
    return re.sub(r'<table>.*?</table>',one,b,flags=re.S)
def imgdims(b): return b.replace('<img src=','<img width="540" height="960" src=')
def strip_head(body):
    eb=re.search(r'<span class="eyebrow">(.*?)</span>',body); h2=re.search(r'<h2>(.*?)</h2>',body,re.S); lead=re.search(r'<p class="lead"[^>]*>(.*?)</p>',body,re.S)
    for m in (eb,h2,lead):
        if m: body=body.replace(m.group(0),'',1)
    return (eb.group(1) if eb else ''),(h2.group(1) if h2 else ''),(lead.group(1) if lead else ''),body
INSERT={
 'projeto':('<div class="grid"','<h2 class="sub">Para quem, o que é e o que não é</h2>\n    '),
 'ciencia':('<div class="scroll-x"','<h2 class="sub">Decisão por decisão</h2>\n    '),
 'jornada':('<ol class="steps"','<h2 class="sub">Os sete passos</h2>\n    '),
}
def static_personagens(body):
    def card(c,draft):
        return '<div class="card char%s">%s<div><span class="tag">%s</span><h3>%s</h3><p>%s</p>%s</div></div>'%(' draft' if draft else '',D['AV'][c[0]],c[2],c[1],c[3],('<p class="quote">%s</p>'%c[4]) if len(c)>4 and c[4] else '')
    cast=''.join(card(c,False) for c in D['CAST']);dr=''.join(card(c,True) for c in D['DRAFT'])
    return '''<h2 class="sub">No jogo hoje</h2><div class="grid">%s</div>
    <h2 class="sub" style="margin-top:1.4em">Rascunhos para os próximos andares</h2><div class="grid">%s</div>'''%(cast,dr)
def static_andares():
    out=[]
    for f in D['FL']:
        pag='Nenhum: este andar só observa.' if not f['pag'] else ('A definir.' if f['pag']=='a definir' else f['pag'])
        out.append('''<li><details%s><summary><span class="n" style="background:%s">%d</span><span><strong>%s</strong><small>%s</small></span></summary><dl><div><dt>O que pratica</dt><dd>%s</dd></div><div><dt>Cenário</dt><dd>%s</dd></div><div><dt>Quem está perdido</dt><dd>%s</dd></div><div><dt>Frase da história</dt><dd>%s</dd></div><div><dt>Pedaço do mapa</dt><dd>%s</dd></div><div><dt>Cena no jogo</dt><dd>%s</dd></div></dl></details></li>'''%(
          ' open' if f['n']==1 else '',D['C'][f['c']],f['n'],f['nome'],f['jogo'],f['hab'],f['uni'],f['pes'],f['fr'],pag,'Já existe (provisória).' if f['cena'] else 'Ainda não escrita.'))
    return '<ol class="floors2" aria-label="Andares, do mais alto ao mais baixo">%s</ol>'%''.join(reversed(out))

NEXT={'index':['projeto','historia','jogos'],'projeto':['historia','como-funciona'],'historia':['personagens','andares'],'personagens':['andares','jogos'],'andares':['jogos','como-funciona'],
 'jogos':['como-funciona','dificuldade'],'como-funciona':['dificuldade','ciencia'],'dificuldade':['ciencia','projeto'],'ciencia':['projeto','historia']}
BLURB={'projeto':'O que é o jogo, para quem é e em que ponto está.','historia':'A premissa de mapear os caminhos da Biblioteca.','personagens':'Quem a criança encontra em cada andar.','andares':'Os dez andares, um a um.',
 'jogos':'O que a criança faz em cada jogo.','como-funciona':'Da calibração ao relatório do adulto.','dificuldade':'Duas réguas e uma demonstração para clicar.','ciencia':'O que a pesquisa sustenta e o que não.'}
COL={'projeto':'--coral','historia':'--grape','personagens':'--pink','andares':'--sky','jogos':'--mint','como-funciona':'--lamp','dificuldade':'--grape','ciencia':'--sky'}
def cards(slugs):
    return '<div class="grid">%s</div>'%''.join('<a class="card link" href="%s" style="--c:var(%s)"><span class="tag">%s</span><h3>%s</h3><p>%s</p><span class="more">Abrir</span></a>'%(href(BY[s]),COL[s],BY[s]['nav'],{'projeto':'O projeto','historia':'A história','personagens':'Os personagens','andares':'Os dez andares','jogos':'Os quatro jogos','como-funciona':'Como o jogo funciona','dificuldade':'Dificuldade que se ajusta','ciencia':'Base científica'}[s],BLURB[s]) for s in slugs)

def breadcrumb(p):
    return '<nav class="crumbs" aria-label="Você está em"><ol><li><a href="index.html">Início</a></li><li aria-current="page">%s</li></ol></nav>'%p['nav']

def build_page(p):
    s=p['slug'];out=[head(p),nav(s),'<main id="conteudo">']
    if s=='index':
        out.append(home())
    else:
        first=True;bands=[]
        for sec in p['sections']:
            cls,body=parse(sec);eb,h2,lead,rest=strip_head(body)
            rest=table_labels(imgdims(promote(rest)))
            if sec in INSERT:
                key,ins=INSERT[sec];rest=rest.replace(key,ins+key,1)
            if sec=='personagens':
                rest=re.sub(r'<div class="grid" id="cast".*?</div>\s*<h3.*?</h3>\s*<div class="grid" id="castDraft"></div>',lambda m:static_personagens(rest),rest,flags=re.S)
            if sec=='andares':
                rest=re.sub(r'<div class="tower".*?</div>\s*</div>',lambda m:'<div class="tower2">%s</div>'%static_andares(),rest,flags=re.S)
            if sec=='jogos':
                rest=rest.replace('<div class="grid">\n      <div class="card"><h3>Se você errar','<h2 class="sub">Quando a criança erra ou empaca</h2>\n    <div class="grid">\n      <div class="card"><h3>Se você errar',1)
            if first:
                h1=p.get('h1') or h2;ld=p.get('lead') or lead
                tiles=p.get('tiles','b,d')
                out.append('<header class="band night pagehead"><div class="layer" data-p="0.15" data-stars="45" aria-hidden="true"></div><div class="layer" data-p="0.3" data-tiles="%s" aria-hidden="true"></div><div class="in">%s<span class="eyebrow">%s</span><h1>%s</h1><p class="lead">%s</p></div></header>'%(tiles,breadcrumb(p),eb or p['nav'],h1,ld))
                out.append('<section class="band %s">%s</section>'%(cls,rest.strip()))
                first=False
            else:
                out.append('<section class="band %s" id="%s">%s</section>'%(cls,sec,table_labels(imgdims(promote(body.strip())))))
        out.append('<section class="band paper next"><div class="in"><h2 class="sub">Continue explorando</h2>%s</div></section>'%cards(NEXT[s]))
    out.append('</main>');out.append(foot(s))
    open(s+'.html','w',encoding='utf-8').write('\n'.join(out))

def home():
    logo=''.join('<span class="b" style="color:%s;transform:rotate(%ddeg)">%s</span>'%(['#ff6f61','#ffc83d','#2fd1b5','#4cc9f0','#9b5de5','#ff8fc7'][i%6],(2 if i%2 else -2),ch) for i,ch in enumerate('Infinita'))
    return '''<header class="band night hero" id="topo">
  <div class="layer" data-p="0.05" data-stars="70" aria-hidden="true"></div>
  <div class="layer" data-p="0.12" aria-hidden="true"><div class="moon"></div></div>
  <div class="layer" data-p="0.18" aria-hidden="true"><div class="shelf far" data-shelf="far"></div></div>
  <div class="layer" data-p="0.3" data-tiles="b,d,p,q,o,m,n" aria-hidden="true"></div>
  <div class="layer" data-p="0.45" aria-hidden="true"><div class="shelf mid" data-shelf="mid"></div></div>
  <div class="in">
    <h1><span class="b">A</span> <span class="b">Biblioteca</span><span class="row2">%s</span></h1>
    <p class="lead">A porta se fechou e a Biblioteca é enorme! Para achar a saída, você ajuda pessoas que se perderam, e cada uma entrega um pedaço do mapa. No caminho, você treina letras, sílabas, atenção e ritmo, sem nota e sem susto.</p>
    <div class="cta"><a class="btn" href="historia.html">Conhecer a história</a><a class="btn alt" href="jogos.html">Ver os jogos</a></div>
    <ul class="chips"><li class="chip warn">Protótipo em desenvolvimento</li><li class="chip warn">Ainda não testado com crianças</li><li class="chip">Crianças de 6 a 10 anos</li><li class="chip">Celular e tablet</li></ul>
  </div>
</header>
<section class="band sun"><div class="in">
  <span class="eyebrow">Em poucas palavras</span>
  <h2>Um jogo para praticar, não para ser avaliado</h2>
  <p class="lead">A Biblioteca Infinita é um jogo educativo para crianças do 1º ao 5º ano com dislexia. São quatro jogos curtos de letras, sílabas, atenção visual e ritmo, dentro de uma Biblioteca com dez andares. A dificuldade se ajusta a cada criança, e um relatório separado mostra ao adulto o que aconteceu.</p>
  <p>O jogo não diagnostica nem trata dislexia. Ele é um protótipo: ainda não foi testado com crianças, e nenhum estudo mostra que melhora a leitura. <a href="projeto.html">Veja a situação atual</a> e <a href="ciencia.html">o que a pesquisa sustenta</a>.</p>
</div></section>
<section class="band sky"><div class="in">
  <span class="eyebrow">Explore o site</span>
  <h2>Escolha por onde começar</h2>
  %s
</div></section>'''%(logo,cards(['historia','personagens','andares','jogos','como-funciona','dificuldade','ciencia','projeto']))

for p in PAGES: build_page(p)

# ---------- ativos e arquivos de SEO ----------
os.makedirs('assets',exist_ok=True)
open('assets/style.css','w',encoding='utf-8').write(open('src/style.css',encoding='utf-8').read())
open('assets/app.js','w',encoding='utf-8').write(open('src/app.js',encoding='utf-8').read())
open('favicon.svg','w',encoding='utf-8').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="8" fill="#1a1450"/><rect x="5" y="9" width="6" height="16" rx="1.5" fill="#ff6f61"/><rect x="13" y="6" width="6" height="19" rx="1.5" fill="#4cc9f0"/><rect x="21" y="11" width="6" height="14" rx="1.5" fill="#ffc83d"/></svg>')
urls=''.join('<url><loc>%s</loc><lastmod>%s</lastmod></url>'%(url(p),LASTMOD) for p in PAGES)
open('sitemap.xml','w',encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>\n'%urls)
open('robots.txt','w').write('User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n'%BASE)
p404=dict(slug='404',nav='Página não encontrada',title='Página não encontrada | A Biblioteca Infinita',desc='Esta página não existe. Volte ao início do site de A Biblioteca Infinita.')
h=head(p404).replace('<meta name="robots" content="index,follow,max-image-preview:large">','<meta name="robots" content="noindex">').replace('<link rel="canonical" href="%s404.html">'%BASE,'')
open('404.html','w',encoding='utf-8').write(h+nav('')+'<main id="conteudo"><header class="band night pagehead"><div class="layer" data-p="0.15" data-stars="45" aria-hidden="true"></div><div class="in"><span class="eyebrow">Ops</span><h1>Essa página se perdeu na Biblioteca</h1><p class="lead">Mas o caminho de volta é fácil.</p><div class="cta"><a class="btn" href="index.html">Voltar ao início</a></div></div></header></main>'+foot(''))
print('ok',len(PAGES),'páginas')
