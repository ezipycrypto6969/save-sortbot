const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1080}});
const v={dark:{bg:'#1D1F26',disc:'#C6F432',band:'#C6F432',mood:'smug'},lime:{bg:'#C6F432',disc:'#1D1F26',band:'#C6F432',mood:'happy'}};
for(const [k,o] of Object.entries(v)){await p.goto('file://'+path.join(__dirname,'pfp.html'));await p.evaluate(o=>window.make(o),o);
await p.screenshot({path:path.join(__dirname,`savesort-gym-pfp-${k}.png`)});}
await b.close();})();
