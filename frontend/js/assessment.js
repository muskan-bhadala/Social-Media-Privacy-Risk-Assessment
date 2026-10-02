let Q=[],cats={},answers={},radar;
const WORST={vis:'PUBLIC',bad:'YES',good:'NO'};
async function init(){
  const d=await api('/api/questions');Q=d.questions;cats=d.categories;const root=document.getElementById('form');let cur='';
  Q.forEach(q=>{
    if(q.category_name!==cur){cur=q.category_name;root.append(h('h3','Category '+q.letter+': '+cur));}
    const row=h('div','','q'),lab=h('label',q.text);lab.htmlFor=q.id;
    const s=document.createElement('select');s.id=q.id;s.add(new Option('-- choose --',''));q.options.forEach(o=>s.add(new Option(o,o)));
    row.append(lab,s);root.append(row);
  });
}
function collect(){const a={};for(const q of Q){const v=document.getElementById(q.id).value;if(!v)return null;a[q.id]=v;}return a;}
document.getElementById('demo').onclick=()=>{ // fictional demo profile: almost everything risky, email private
  Q.forEach(q=>{const s=document.getElementById(q.id);const bad=q.options.includes('PUBLIC')?'PUBLIC':(/verify|review|use|enabled|strip|unique/i.test(q.text)?'NO':'YES');s.value=bad;});
  document.getElementById('b2').value='PRIVATE';
};
document.getElementById('go').onclick=async()=>{
  const err=document.getElementById('err');err.textContent='';answers=collect();
  if(!answers){err.textContent='Please answer every question.';return;}
  try{const r=await post('/api/assessment',{answers});show(r);}catch(e){err.textContent=e.message;}
};
function show(r){
  document.getElementById('result').hidden=false;
  document.getElementById('score').textContent=r.overall_score+' / 100';
  const l=document.getElementById('level');l.textContent=r.risk_level;l.className=r.risk_level;
  document.getElementById('report').href='/api/assessment/'+r.assessment_id+'/report';
  const labels=Object.keys(r.category_scores).map(k=>cats[k]);
  if(radar)radar.destroy();
  if(window.Chart)radar=new Chart(document.getElementById('radar'),{type:'radar',data:{labels,datasets:[{label:'Risk (higher = more exposure)',data:Object.values(r.category_scores),backgroundColor:'rgba(179,38,30,.25)',borderColor:'#b3261e'}]},options:{scales:{r:{min:0,max:100}}}});
  const f=document.getElementById('findings');f.replaceChildren(...r.findings.slice(0,8).map(x=>h('li',x.severity+': '+x.description)));
  const rc=document.getElementById('recs');rc.replaceChildren(...r.recommendations.map(x=>h('li',x.priority+': '+x.recommendation)));
  const fx=document.getElementById('fixes');fx.replaceChildren(...r.recommendations.map(x=>{
    const w=h('div'),c=document.createElement('input');c.type='checkbox';c.checked=true;c.value=x.finding_type;c.id='fx'+x.finding_type;
    const lb=h('label',' '+x.recommendation);lb.htmlFor=c.id;w.append(c,lb);return w;}));
}
document.getElementById('sim').onclick=async()=>{
  const fixes=[...document.querySelectorAll('#fixes input:checked')].map(i=>i.value);
  const out=document.getElementById('simout');
  try{const s=await post('/api/assessment/simulate-improvement',{answers,fixes});
    out.replaceChildren(h('p','Current: '+s.before.score+'/100 '+s.before.level),h('p','Simulated: '+s.after.score+'/100 '+s.after.level),h('p','Risk reduction: '+s.risk_reduction+' points'),h('small',s.disclaimer));}
  catch(e){out.textContent=e.message;}
};
init();
