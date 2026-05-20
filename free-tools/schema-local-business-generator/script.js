'use strict';
const PT=(document.documentElement.lang||'').toLowerCase().startsWith('pt');
const L=(e,p)=>PT?p:e;
function show(id){document.getElementById(id).classList.remove('hidden')}
function hide(id){document.getElementById(id).classList.add('hidden')}
function showFlex(id){const el=document.getElementById(id);el.classList.remove('hidden');el.classList.add('flex')}
function hideFlex(id){const el=document.getElementById(id);el.classList.add('hidden');el.classList.remove('flex')}
function val(id){return (document.getElementById(id).value||'').trim()}
function buildSchema(){
  const name=val('biz-name');const type=val('biz-type')||'LocalBusiness';
  const street=val('street');const city=val('city');const region=val('region');const postal=val('postal');const country=val('country')||'PT';
  const phone=val('phone');const url=val('website');const desc=val('description');
  if(!name||!city){alert(L('Business name and city are required.','Nome do negócio e cidade são obrigatórios.'));return null}
  const addr={'@type':'PostalAddress','addressLocality':city,'addressCountry':country};
  if(street)addr.streetAddress=street;
  if(region)addr.addressRegion=region;
  if(postal)addr.postalCode=postal;
  const o={'@context':'https://schema.org','@type':type,'name':name,'address':addr};
  if(phone)o.telephone=phone;
  if(url)o.url=url.startsWith('http')?url:'https://'+url;
  if(desc)o.description=desc;
  return JSON.stringify(o,null,2);
}
async function copyText(text){
  try{await navigator.clipboard.writeText(text);alert(L('Copied to clipboard!','Copiado!'));}catch(e){alert(L('Select and copy manually.','Copie manualmente.'))}
}
async function runTool(){
  if(typeof window.trackEvent==='function')window.trackEvent('tool_used');
  showFlex('spinner');hide('result-box');hide('error-box');
  try{
    const json=buildSchema();if(!json)return;
    const esc=json.replace(/&/g,'&amp;').replace(/</g,'&lt;');
    document.getElementById('result-box').innerHTML=`<div class="bg-slate-900 border border-indigo-500/30 rounded-2xl p-5">
      <p class="text-xs font-bold uppercase text-indigo-400 mb-3">${L('JSON-LD snippet','Snippet JSON-LD')}</p>
      <p class="text-xs text-slate-500 mb-2">${L('Paste inside a &lt;script type="application/ld+json"&gt; tag in your site header or footer.','Cole dentro de &lt;script type="application/ld+json"&gt; no cabeçalho ou rodapé do site.')}</p>
      <div class="copy-row"><textarea id="out-json" readonly>${esc}</textarea></div>
      <button type="button" onclick="copyText(document.getElementById('out-json').value)" class="mt-3 w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-xl px-6 py-3">${L('Copy JSON-LD','Copiar JSON-LD')}</button>
    </div>
    <div class="bg-gradient-to-br from-slate-900 to-ink border-2 border-signal/40 rounded-2xl p-6 text-center">
      <h3 class="text-xl font-bold mb-2">${L('We implement schema for you','Implementamos schema por si')}</h3>
      <p class="text-slate-400 text-sm mb-4">${L('InfoWeb sites ship with local SEO basics baked in.','Sites InfoWeb incluem SEO local desde o início.')}</p>
      <a href="https://infoweb.sousadev.com/?utm_source=freetool&utm_medium=schema_local_business_generator&utm_campaign=result_cta#pricing" target="_blank" class="inline-flex bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-xl px-6 py-3">${L('See Website Plans','Ver planos')}</a></div>
    <p class="text-center"><button type="button" onclick="resetTool()" class="text-sm text-slate-500 underline">${L('Generate again','Gerar de novo')}</button></p>`;
    show('result-box');document.getElementById('output-section').scrollIntoView({behavior:'smooth'});
    if(typeof window.trackEvent==='function')window.trackEvent('tool_result_shown');
  }catch(e){show('error-box')}finally{hideFlex('spinner')}
}
function resetTool(){hide('result-box');window.scrollTo({top:0,behavior:'smooth'})}
