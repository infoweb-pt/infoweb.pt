'use strict';
const PT=(document.documentElement.lang||'').toLowerCase().startsWith('pt');
const L=(e,p)=>PT?p:e;
const fmt=new Intl.NumberFormat(PT?'pt-PT':'en-GB',{style:'currency',currency:'EUR'});
const pctFmt=new Intl.NumberFormat(PT?'pt-PT':'en-GB',{style:'percent',maximumFractionDigits:1});
function show(id){document.getElementById(id).classList.remove('hidden')}
function hide(id){document.getElementById(id).classList.add('hidden')}
function showFlex(id){const el=document.getElementById(id);el.classList.remove('hidden');el.classList.add('flex')}
function hideFlex(id){const el=document.getElementById(id);el.classList.add('hidden');el.classList.remove('flex')}
async function runTool(){
  const ing=parseFloat(String(document.getElementById('ingredient-cost').value).replace(',','.'));
  const menu=parseFloat(String(document.getElementById('menu-price').value).replace(',','.'));
  if(!Number.isFinite(ing)||ing<0||!Number.isFinite(menu)||menu<=0){alert(L('Enter ingredient cost and menu price.','Introduza custo dos ingredientes e preço de menu.'));return}
  if(ing>=menu){alert(L('Menu price must be higher than ingredient cost.','O preço de menu deve ser superior ao custo dos ingredientes.'));return}
  if(typeof window.trackEvent==='function')window.trackEvent('tool_used');
  showFlex('spinner');hide('result-box');hide('error-box');
  try{
    const foodCostPct=ing/menu;const margin=menu-ing;const marginPct=margin/menu;
    const target30=ing/0.3;
    document.getElementById('result-box').innerHTML=`<div class="bg-slate-900 border border-orange-500/30 rounded-2xl p-5 grid grid-cols-2 gap-4 text-center">
      <div class="bg-slate-800 rounded-xl p-4"><p class="text-2xl font-bold text-orange-400">${pctFmt.format(foodCostPct)}</p><p class="text-xs text-slate-400">${L('Food cost %','Custo alimentar %')}</p></div>
      <div class="bg-slate-800 rounded-xl p-4"><p class="text-2xl font-bold text-white">${pctFmt.format(marginPct)}</p><p class="text-xs text-slate-400">${L('Gross margin %','Margem bruta %')}</p></div></div>
      <div class="bg-slate-800 rounded-xl p-4 text-sm text-slate-300">${L('Gross profit per plate','Lucro bruto por prato')}: <strong>${fmt.format(margin)}</strong><br/>
      ${L('Menu price for 30% food cost','Preço para 30% custo alimentar')}: <strong>${fmt.format(target30)}</strong></div>
      <p class="text-center"><button type="button" onclick="resetTool()" class="text-sm text-slate-500 underline">${L('Calculate again','Calcular de novo')}</button></p>`;
    show('result-box');document.getElementById('output-section').scrollIntoView({behavior:'smooth'});
    if(typeof window.trackEvent==='function')window.trackEvent('tool_result_shown');
  }catch(e){show('error-box')}finally{hideFlex('spinner')}
}
function resetTool(){hide('result-box');document.getElementById('ingredient-cost').value='';document.getElementById('menu-price').value='';window.scrollTo({top:0,behavior:'smooth'})}
