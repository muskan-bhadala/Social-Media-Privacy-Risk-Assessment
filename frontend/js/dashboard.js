(async()=>{
  const s=await api('/api/dashboard/stats'),cards=document.getElementById('cards');
  [['Synthetic profiles',s.profiles],['Average risk score',s.avg_score],['Critical profiles',s.distribution.CRITICAL],['Assessments on this server',s.user_assessments]]
    .forEach(([k,v])=>{const c=h('div','','card');c.append(h('b',String(v)),h('span',k));cards.append(c);});
  if(!window.Chart)return;
  const mk=(id,type,labels,data,color,opt)=>new Chart(document.getElementById(id),{type,data:{labels,datasets:[{data,backgroundColor:color}]},options:Object.assign({plugins:{legend:{display:type==='doughnut'}}},opt||{})});
  mk('c1','bar',Object.keys(s.category_avg),Object.values(s.category_avg),'#0b5c6b',{scales:{y:{min:0,max:100}}});
  mk('c2','doughnut',Object.keys(s.distribution),Object.values(s.distribution),['#2e8b57','#c9a227','#d9772b','#b3261e']);
  mk('c3','bar',s.top_weaknesses.map(w=>w.text),s.top_weaknesses.map(w=>w.percent),'#d9772b',{indexAxis:'y'});
  mk('c4','bar',Object.keys(s.controls_enabled_pct),Object.values(s.controls_enabled_pct),'#2e8b57',{scales:{y:{min:0,max:100}}});
})();
