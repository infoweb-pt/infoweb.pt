'use strict';
const PT=(document.documentElement.lang||'').toLowerCase().startsWith('pt');
const L=(e,p)=>PT?p:e;
function show(id){document.getElementById(id).classList.remove('hidden')}
function hide(id){document.getElementById(id).classList.add('hidden')}
function showFlex(id){const el=document.getElementById(id);el.classList.remove('hidden');el.classList.add('flex')}
function hideFlex(id){const el=document.getElementById(id);el.classList.add('hidden');el.classList.remove('flex')}
function toSlug(raw){
  return raw.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase()
    .replace(/[^a-z0-9\s-]/g,'').trim().replace(/\s+/g,'-').replace(/-+/g,'-').replace(/^-|-$/g,'');
}
async function copyText(t,id){try{await navigator.clipboard.writeText(t);const b=document.getElementById(id);if(b){const o=b.textContent;b.textContent=L('Copied!','Copiado!');setTimeout(()=>b.textContent=o,2000)}}catch(e){alert(L('Copy failed.','Falha ao copiar.'))}}
async function runTool(){
  const text=document.getElementById('text-in').value;
  const slug=toSlug(text);
  if(!slug){alert(L('Enter some text first.','Escreva algum texto primeiro.'));return}
  if(typeof window.trackEvent==='function')window.trackEvent('tool_used');
  showFlex('spinner');hide('result-box');
  try{
    document.getElementById('result-box').innerHTML=`<div class="bg-slate-900 border border-violet-500/30 rounded-2xl p-5"><p class="text-xs font-bold uppercase text-violet-400 mb-2">${L('SEO-friendly slug','Slug amigável para SEO')}</p><div class="copy-row"><input readonly id="out-slug" value="${slug}"/><button type="button" id="btn-slug" onclick="copyText(document.getElementById('out-slug').value,'btn-slug')" class="shrink-0 bg-violet-600 hover:bg-violet-500 text-white font-semibold rounded-xl px-4 py-2 text-sm">${L('Copy','Copiar')}</button></div><p class="text-xs text-slate-500 mt-3">${L('Use in URLs like: /services/'+slug,'Use em URLs como: /servicos/'+slug)}</p></div>
    <div class="bg-gradient-to-br from-slate-900 to-ink border-2 border-signal/40 rounded-2xl p-6 text-center mt-4"><h3 class="text-xl font-bold mb-2">${L('Clean URLs on a managed site','URLs limpas num site gerido')}</h3><a href="https://infoweb.sousadev.com/?utm_source=freetool&utm_medium=url_slug_generator&utm_campaign=result_cta#pricing" target="_blank" class="inline-flex bg-violet-600 hover:bg-violet-500 text-white font-bold rounded-xl px-6 py-3">${L('See Website Plans','Ver planos')}</a></div>`;
    show('result-box');
    if(typeof window.trackEvent==='function')window.trackEvent('tool_result_shown');
  }finally{hideFlex('spinner')}
}
