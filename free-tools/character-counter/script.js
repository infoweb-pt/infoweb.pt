'use strict';
const PT=(document.documentElement.lang||'').toLowerCase().startsWith('pt');
const L=(e,p)=>PT?p:e;
function count(){
  const t=document.getElementById('text-in').value;
  const chars=t.length;const words=(t.trim()?t.trim().split(/\s+/).length:0);const lines=(t?t.split(/\n/).length:0);
  const el=document.getElementById('live-stats');
  if(!el)return;
  const titleOk=chars<=60?'char-ok':chars<=70?'char-warn':'char-bad';
  const metaOk=chars<=160?'char-ok':chars<=180?'char-warn':'char-bad';
  el.innerHTML=`<div class="grid grid-cols-3 gap-3 text-center mb-4"><div class="bg-slate-800 rounded-xl p-3"><p class="text-2xl font-bold">${chars}</p><p class="text-xs text-slate-400">${L('Characters','Caracteres')}</p></div><div class="bg-slate-800 rounded-xl p-3"><p class="text-2xl font-bold">${words}</p><p class="text-xs text-slate-400">${L('Words','Palavras')}</p></div><div class="bg-slate-800 rounded-xl p-3"><p class="text-2xl font-bold">${lines}</p><p class="text-xs text-slate-400">${L('Lines','Linhas')}</p></div></div>
  <p class="text-sm text-slate-400">${L('Google title target','Alvo título Google')}: <span class="${titleOk}">${chars}/60</span> · ${L('Meta description target','Alvo meta description')}: <span class="${metaOk}">${chars}/160</span></p>`;
}
document.addEventListener('DOMContentLoaded',()=>{
  const ta=document.getElementById('text-in');
  if(ta){ta.addEventListener('input',count);count();}
  if(typeof window.trackEvent==='function')window.trackEvent('tool_used');
});
