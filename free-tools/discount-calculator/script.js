'use strict';
const PT=(document.documentElement.lang||'').toLowerCase().startsWith('pt');
const L=(e,p)=>PT?p:e;
const fmt=new Intl.NumberFormat(PT?'pt-PT':'en-GB',{style:'currency',currency:'EUR'});
function show(id){document.getElementById(id).classList.remove('hidden')}
function hide(id){document.getElementById(id).classList.add('hidden')}
function showFlex(id){const el=document.getElementById(id);el.classList.remove('hidden');el.classList.add('flex')}
function hideFlex(id){const el=document.getElementById(id);el.classList.add('hidden');el.classList.remove('flex')}
async function runTool(){
  const price=parseFloat(String(document.getElementById('orig-price').value).replace(',','.'));
  const pct=parseFloat(String(document.getElementById('discount-pct').value).replace(',','.'));
  if(!Number.isFinite(price)||price<=0||!Number.isFinite(pct)||pct<=0||pct>=100){alert(L('Enter a valid price and discount between 0 and 100.','Introduza preço e desconto válidos (0–100).'));return}
  if(typeof window.trackEvent==='function')window.trackEvent('tool_used');
  showFlex('spinner');hide('result-box');hide('error-box');
  try{
    const final=price*(1-pct/100);const saved=price-final;
    document.getElementById('result-box').innerHTML=`<div class="bg-slate-900 border border-rose-500/30 rounded-2xl p-5 grid grid-cols-2 gap-4 text-center">
      <div class="bg-slate-800 rounded-xl p-4"><p class="text-2xl font-bold text-rose-400">${fmt.format(final)}</p><p class="text-xs text-slate-400">${L('Sale price','Preço final')}</p></div>
      <div class="bg-slate-800 rounded-xl p-4"><p class="text-2xl font-bold text-white">${fmt.format(saved)}</p><p class="text-xs text-slate-400">${L('You save','Poupa')}</p></div></div>
      <div class="bg-slate-800 rounded-xl p-4 text-center"><p class="text-sm text-slate-400">${L('Original','Original')}: <span class="line-through">${fmt.format(price)}</span> · ${pct}% ${L('off','de desconto')}</p>
      <p class="text-sm text-slate-300 mt-2" id="promo-copy"></p></div>
      <div class="bg-gradient-to-br from-slate-900 to-ink border-2 border-signal/40 rounded-2xl p-6 text-center">
      <h3 class="text-xl font-bold mb-2">${L('Promote it on your site','Promova no seu site')}</h3>
      <a href="https://infoweb.sousadev.com/?utm_source=freetool&utm_medium=discount_calculator&utm_campaign=result_cta#pricing" target="_blank" class="inline-flex bg-rose-600 hover:bg-rose-500 text-white font-bold rounded-xl px-6 py-3">${L('See Website Plans','Ver planos')}</a></div>
      <p class="text-center"><button type="button" onclick="resetTool()" class="text-sm text-slate-500 underline">${L('Calculate again','Calcular de novo')}</button></p>`;
    document.getElementById('promo-copy').textContent=L(`Now ${fmt.format(final)} — was ${fmt.format(price)} (${pct}% off)`,`Agora ${fmt.format(final)} — era ${fmt.format(price)} (${pct}% desconto)`);
    show('result-box');document.getElementById('output-section').scrollIntoView({behavior:'smooth'});
    if(typeof window.trackEvent==='function')window.trackEvent('tool_result_shown');
  }catch(e){show('error-box')}finally{hideFlex('spinner')}
}
function resetTool(){hide('result-box');document.getElementById('orig-price').value='';document.getElementById('discount-pct').value='';window.scrollTo({top:0,behavior:'smooth'})}
