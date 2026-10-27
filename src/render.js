const {chromium}=require('playwright');const fs=require('fs');const M=JSON.parse(fs.readFileSync('manifest.json')).manifest;
(async()=>{const b=await chromium.launch();const pg=await b.newPage();
for(const [n,w,h] of M){await pg.setViewportSize({width:w,height:h});await pg.goto('file://'+process.cwd()+'/html/'+n+'.html');await pg.evaluate(()=>document.fonts.ready);await pg.screenshot({omitBackground:/^canot_/.test(n),path:'img/'+n+'.png',clip:{x:0,y:0,width:w,height:h}})}
await b.close();console.log('rendu',M.length)})();
