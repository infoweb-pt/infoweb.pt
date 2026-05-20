'use strict';
const PT=(document.documentElement.lang||'').toLowerCase().startsWith('pt');
const L=(e,p)=>PT?p:e;
const fmt=new Intl.NumberFormat(PT?'pt-PT':'en-GB',{style:'currency',currency:'EUR'});
function show(id){document.getElementById(id).classList.remove('hidden')}
function hide(id){document.getElementById(id).classList.add('hidden')}
function showFlex(id){const el=document.getElementById(id);el.classList.remove('hidden');el.classList.add('flex')}
function hideFlex(id){const el=document.getElementById(id);el.classList.add('hidden');el.classList.remove('flex')}
async function runTool(){
  const bill=parseFloat(String(document.getElementById('bill').value).replace(',','.'));
  const people=parseInt(document.getElementById('people').value,10);
  const tipPct=parseFloat(String(document.getElementById('tip-pct').value).replace(',','.'))||0;
  if(!Number.isFinite(bill)||bill<=0||!Number.isFinite(people)||people<1){alert(L('Enter bill amount and number of people.','Introduza conta e número de pessoas.'));return}
  if(typeof window.trackEvent==='function')window.trackEvent('tool_used');
  showFlex('spinner');hide('result-box');hide('error-box');
  try{
    const tip=bill*(tipPct/100);const total=bill+tip;const each=total/people;
    document.getElementById('result-box').innerHTML=`<div class="bg-slate-900 border border-teal-500/30 rounded-2xl p-5 grid grid-cols-2 gap-4 text-center">
      <div class="bg-slate-800 rounded-xl p-4"><p class="text-2xl font-bold text-teal-400">${fmt.format(each)}</p><p class="text-xs text-slate-400">${L('Per person','Por pessoa')}</p></div>
      <div class="bg-slate-800 rounded-xl p-4"><p class="text-2xl font-bold text-white">${fmt.format(total)}</p><p class="text-xs text-slate-400">${L('Total with tip','Total com gorjeta')}</p></div></div>
      <div class="bg-slate-800 rounded-xl p-4 text-sm text-slate-300 text-center">${L('Tip amount','Gorjeta')}: <strong>${fmt.format(tip)}</strong> (${tipPct}%)</div>
      <p class="text-center"><button type="button" onclick="resetTool()" class="text-sm text-slate-500 underline">${L('Calculate again','Calcular de novo')}</button></p>`;
    show('result-box');document.getElementById('output-section').scrollIntoView({behavior:'smooth'});
    if(typeof window.trackEvent==='function')window.trackEvent('tool_result_shown');
  }catch(e){show('error-box')}finally{hideFlex('spinner')}
}
function resetTool(){hide('result-box');['bill','people','tip-pct'].forEach(id=>document.getElementById(id).value='');document.getElementById('tip-pct').value='10';window.scrollTo({top:0,behavior:'smooth'})}
document.addEventListener('DOMContentLoaded',()=>{if(!document.getElementById('tip-pct').value)document.getElementById('tip-pct').value='10'});
