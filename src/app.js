/* A Biblioteca Infinita: scripts do site. Tudo aqui é melhoria: o conteúdo e a navegação funcionam sem JavaScript. */
(function(){
'use strict';
var COLORS=['#ff6f61','#ffc83d','#2fd1b5','#4cc9f0','#9b5de5','#ff8fc7'];
var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function rng(seed){return function(){seed=(seed*16807)%2147483647;return (seed-1)/2147483646}}

/* estrelas e letras-bloco (decoração, aria-hidden) */
document.querySelectorAll('[data-stars]').forEach(function(el,k){
  var n=parseInt(el.getAttribute('data-stars'),10)||40,r=rng(7+k*5);
  for(var i=0;i<n;i++){var s=document.createElement('i');s.className='star';var z=1+r()*3;
    s.style.cssText='left:'+(r()*100)+'%;top:'+(r()*100)+'%;width:'+z+'px;height:'+z+'px;animation-delay:'+(r()*3)+'s';el.appendChild(s)}
});
var POS=[[88,10,60,-10],[4,72,56,8],[66,6,48,12],[80,56,70,-6],[93,34,50,9],[52,66,44,-12],[40,4,38,6]];
var POS2=[[3,22,58,-8],[90,14,64,10],[84,66,52,-6],[8,74,48,12]];
document.querySelectorAll('[data-tiles]').forEach(function(el){
  var letters=el.getAttribute('data-tiles').split(','),pos=letters.length>4?POS:POS2;
  letters.forEach(function(l,i){var t=pos[i%pos.length],d=document.createElement('div');d.className='tile';d.textContent=l;
    d.style.cssText='left:'+t[0]+'%;top:'+t[1]+'%;width:'+t[2]+'px;height:'+t[2]+'px;font-size:'+(t[2]*.62)+'px;background:'+COLORS[i%COLORS.length]+';transform:rotate('+t[3]+'deg);animation-delay:'+(i*.6)+'s';el.appendChild(d)});
});
document.querySelectorAll('[data-shelf]').forEach(function(sh,k){
  var r=rng(k+3);for(var i=0;i<26;i++){var b=document.createElement('i');b.style.height=(35+r()*65)+'%';b.style.background=COLORS[Math.floor(r()*COLORS.length)];sh.appendChild(b)}
});

/* demonstração das duas réguas */
(function(){
  var demo=document.getElementById('demo');if(!demo)return;
  var MAXL=4,st,stage=document.getElementById('stage'),LET=['b','d','p','q','o'];
  for(var i=0;i<5;i++){var d=document.createElement('div');d.className='drop';d.textContent=LET[i];d.style.left=(8+i*19)+'%';d.style.background=COLORS[i];d.style.animationDelay=(-i*1.1)+'s';stage.appendChild(d)}
  function reset(){st={lvl:0,hs:0,es:0,sp:2,log:[]}}
  function bar(id,n,val){var el=document.getElementById(id);el.innerHTML='';for(var i=0;i<n;i++){var b=document.createElement('b');if(val>=i+1)b.className='on';else if(val>=i+.5)b.className='half';el.appendChild(b)}}
  function render(){
    bar('lvlBar',MAXL+1,st.lvl+1);bar('spdBar',10,st.sp);
    document.getElementById('lvlTxt').textContent='nível '+st.lvl+' de '+MAXL;
    document.getElementById('spdTxt').textContent='índice '+Math.floor(st.sp)+' de 10';
    document.getElementById('streakTxt').textContent='acertos seguidos: '+st.hs+' · erros seguidos: '+st.es;
    var secs=(7-Math.floor(st.sp)*0.5).toFixed(1);
    stage.querySelectorAll('.drop').forEach(function(x){x.style.setProperty('--d',secs+'s')});
    var lg=document.getElementById('log');lg.innerHTML='';
    st.log.slice(-3).forEach(function(t){var li=document.createElement('li');li.textContent=t;lg.appendChild(li)});
  }
  function act(a){
    if(a==='reset'){reset();render();return}
    var hit=a==='fast-hit'||a==='slow-hit',msg=[];
    if(hit){st.es=0;st.hs++;if(st.hs>=2){if(st.lvl<MAXL){st.lvl++;msg.push('2 acertos seguidos: o conteúdo sobe.')}else msg.push('2 acertos seguidos: já está no último nível.');st.hs=0}else msg.push('1 acerto: o conteúdo se mantém.')}
    else{st.hs=0;st.es++;if(st.es>=2){if(st.lvl>0){st.lvl--;msg.push('2 erros seguidos: o conteúdo desce.')}else msg.push('2 erros seguidos: já está no primeiro nível.');st.es=0}else msg.push('1 erro: o conteúdo se mantém.')}
    var dl=a==='fast-hit'?1:a==='slow-hit'?0:a==='err-fast'?-.5:-1;
    st.sp=Math.max(0,Math.min(10,st.sp+dl));
    msg.push(a==='fast-hit'?'Acerto rápido: a queda acelera.':a==='slow-hit'?'Acerto devagar: a queda se mantém.':a==='err-fast'?'Erro muito rápido (provável chute): a queda desacelera só meio degrau.':'Erro: a queda desacelera.');
    st.log.push(msg.join(' '));render();
  }
  reset();render();
  demo.addEventListener('click',function(e){var b=e.target.closest('button[data-a]');if(b)act(b.getAttribute('data-a'))});
})();

/* parallax por rolagem */
(function(){
  if(reduce)return;
  var items=[].slice.call(document.querySelectorAll('[data-p]')),ticking=false;
  if(!items.length)return;
  function upd(){
    var vh=innerHeight;
    items.forEach(function(el){
      var host=el.closest('section,header')||el,r=host.getBoundingClientRect();
      if(r.bottom<-200||r.top>vh+200)return;
      var k=parseFloat(el.getAttribute('data-p')),off=(r.top+r.height/2-vh/2)*k*-1;
      el.style.transform='translate3d(0,'+off.toFixed(1)+'px,0)'+(el.classList.contains('phone')?' rotate('+getComputedStyle(el).getPropertyValue('--r')+')':'');
    });
    ticking=false;
  }
  addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(upd)}},{passive:true});
  addEventListener('resize',upd);upd();
})();

/* leitura: fonte OpenDyslexic e mais espaço (guardado só neste navegador) */
(function(){
  var root=document.documentElement,fb=document.getElementById('fontBtn'),rb=document.getElementById('roomy');
  function get(k){try{return localStorage.getItem(k)}catch(e){return null}}
  function set(k,v){try{localStorage.setItem(k,v)}catch(e){}}
  function od(on){root.classList.toggle('od',on);if(fb){fb.setAttribute('aria-pressed',String(on));fb.textContent=on?'Fonte padrão':'Fonte OpenDyslexic'}set('bi.od',on?'1':'0')}
  function roomy(on){root.classList.toggle('roomy',on);if(rb)rb.setAttribute('aria-pressed',String(on));set('bi.roomy',on?'1':'0')}
  if(get('bi.od')==='1')od(true);if(get('bi.roomy')==='1')roomy(true);
  if(fb)fb.addEventListener('click',function(){od(!root.classList.contains('od'))});
  if(rb)rb.addEventListener('click',function(){roomy(!root.classList.contains('roomy'))});
})();

/* menu: botão no celular e submenus por teclado e toque */
(function(){
  var burger=document.getElementById('burger'),menu=document.getElementById('menu'),header=document.querySelector('.site-header');
  if(!burger||!menu)return;
  function closeSub(except){menu.querySelectorAll('.dd.open').forEach(function(li){if(li!==except){li.classList.remove('open');li.querySelector('.dd-btn').setAttribute('aria-expanded','false')}})}
  burger.addEventListener('click',function(){var o=!header.classList.contains('menu-open');header.classList.toggle('menu-open',o);burger.setAttribute('aria-expanded',String(o))});
  menu.querySelectorAll('.dd-btn').forEach(function(b){
    b.addEventListener('click',function(){var li=b.parentNode,o=!li.classList.contains('open');closeSub(li);li.classList.toggle('open',o);b.setAttribute('aria-expanded',String(o))});
  });
  document.addEventListener('click',function(e){if(!menu.contains(e.target)&&!burger.contains(e.target)){closeSub();}});
  document.addEventListener('keydown',function(e){
    if(e.key!=='Escape')return;
    var open=menu.querySelector('.dd.open');
    if(open){var b=open.querySelector('.dd-btn');closeSub();b.focus()}
    else if(header.classList.contains('menu-open')){header.classList.remove('menu-open');burger.setAttribute('aria-expanded','false');burger.focus()}
  });
})();
})();
