// XSS-safe helpers: always textContent, never innerHTML with data
function h(tag, text, cls){const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(cls)e.className=cls;return e;}
async function api(path, opts){const r=await fetch(path,opts);const d=await r.json();if(!r.ok)throw new Error(d.error||'Request failed');return d;}
const post=(p,b)=>api(p,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)});
