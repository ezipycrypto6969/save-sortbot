const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1080}});
const v={
 'gym-lime':{kind:'gym',bg:'#C6F432',disc:'#1D1F26',band:'#C6F432',mood:'happy'},
 'gym-dark':{kind:'gym',bg:'#1D1F26',disc:'#C6F432',band:'#C6F432',mood:'smug'},
 'kitchen':{kind:'kitchen',bg:'#C2410C',disc:'#FFD27A',band:'#FFD27A',mood:'happy',y:250},
 'hypecheck':{kind:'hype',bg:'#10121C',disc:'#E0480C',band:'#FFE14A',mood:'suspicious'}};
for(const [k,o] of Object.entries(v)){await p.goto('file://'+path.join(__dirname,'pfp.html'));await p.evaluate(o=>window.make(o),o);
await p.screenshot({path:path.join(__dirname,`savesort-${k}-pfp.png`)});}
await b.close();})();
