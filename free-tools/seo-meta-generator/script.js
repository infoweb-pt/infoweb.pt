'use strict';
const PT=(document.documentElement.lang||'').toLowerCase().startsWith('pt');
const L=(e,p)=>PT?p:e;
function show(id){document.getElementById(id).classList.remove('hidden')}
function hide(id){document.getElementById(id).classList.add('hidden')}
function showFlex(id){const el=document.getElementById(id);el.classList.remove('hidden');el.classList.add('flex')}
function hideFlex(id){const el=document.getElementById(id);el.classList.add('hidden');el.classList.remove('flex')}
function lenClass(n,max){if(n<=max)return 'char-ok';if(n<=max+15)return 'char-warn';return 'char-bad'}
async function copyText(t,id){try{await navigator.clipboard.writeText(t);const b=document.getElementById(id);if(b){const o=b.textContent;b.textContent=L('Copied!','Copiado!');setTimeout(()=>b.textContent=o,2000)}}catch(e){alert(L('Copy failed.','Falha ao copiar.'))}}
function titles(biz,topic,loc){
  const locBit=loc?` ${loc.trim()}`:'';
  const base=[`${topic.trim()} | ${biz.trim()}`,`${biz.trim()} — ${topic.trim()}`,`${topic.trim()} — ${biz.trim()}${locBit}`];
  return base.map(t=>t.slice(0,60));
}
function descriptions(biz,topic,loc){
  const locBit=loc?` ${loc.trim()}.`:'';
  const lines=[
    `${biz.trim()} — ${topic.trim()}.${locBit} Book online, see services & contact us in seconds.`,
    `Looking for ${topic.trim().toLowerCase()}? ${biz.trim()} helps local customers${locBit} Fast site, clear offers & easy contact.`,
    `${topic.trim()} at ${biz.trim()}${locBit} Trusted local business — prices, hours & how to reach us on one page.`
  ];
  return lines.map(d=>d.slice(0,160));
}
async function runTool(){
  const biz=document.getElementById('biz').value.trim();
  const topic=document.getElementById('topic').value.trim();
  const loc=document.getElementById('loc').value.trim();
  if(!biz||!topic){alert(L('Enter business name and page topic.','Introduza nome do negócio e tema da página.'));return}
  if(typeof window.trackEvent==='function')window.trackEvent('tool_used');
  showFlex('spinner');hide('result-box');
  try{
    const ts=titles(biz,topic,loc);const ds=descriptions(biz,topic,loc);
    let html='';
    ts.forEach((t,i)=>{
      const n=t.length;
      html+=`<div class="bg-slate-900 border border-emerald-500/30 rounded-2xl p-5 mb-4"><p class="text-xs font-bold uppercase text-emerald-400 mb-2">${L('Title option','Opção de título')} ${i+1} <span class="${lenClass(n,60)}">(${n}/60)</span></p><div class="copy-row"><input readonly id="t${i}" value="${t.replace(/"/g,'&quot;')}"/><button type="button" id="bt${i}" onclick="copyText(document.getElementById('t${i}').value,'bt${i}')" class="shrink-0 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-xl px-4 py-2 text-sm">${L('Copy','Copiar')}</button></div></div>`;
    });
    ds.forEach((d,i)=>{
      const n=d.length;
      html+=`<div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 mb-4"><p class="text-xs font-bold uppercase text-slate-400 mb-2">${L('Meta description','Meta description')} ${i+1} <span class="${lenClass(n,160)}">(${n}/160)</span></p><div class="copy-row"><textarea readonly id="d${i}">${d}</textarea><button type="button" id="bd${i}" onclick="copyText(document.getElementById('d${i}').value,'bd${i}')" class="shrink-0 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-xl px-4 py-2 text-sm">${L('Copy','Copiar')}</button></div></div>`;
    });
    html+=`<div class="bg-gradient-to-br from-slate-900 to-ink border-2 border-signal/40 rounded-2xl p-6 text-center"><h3 class="text-xl font-bold mb-2">${L('Put these on a fast website','Publique num site rápido')}</h3><p class="text-slate-400 text-sm mb-4">${L('Titles and meta tags only work if Google can crawl a real page.','Títulos e meta só funcionam se o Google conseguir indexar uma página real.')}</p><a href="https://infoweb.sousadev.com/?utm_source=freetool&utm_medium=seo_meta_generator&utm_campaign=result_cta#pricing" target="_blank" class="inline-flex bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl px-6 py-3">${L('See Website Plans','Ver planos')}</a></div>`;
    document.getElementById('result-box').innerHTML=html;show('result-box');
    if(typeof window.trackEvent==='function')window.trackEvent('tool_result_shown');
  }finally{hideFlex('spinner')}
}
