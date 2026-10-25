const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1400,height:1000}});
await pg.goto('file://'+process.cwd()+'/../table-du-castor.html');await pg.waitForTimeout(400);
const out=await pg.evaluate(()=>{setup(3);return {pieces:Object.values(S.pieces).filter(p=>!p.in),TW,TH,SIZE}});
fs.writeFileSync('table_pieces.json',JSON.stringify(out));
const c={};out.pieces.forEach(p=>{const k=p.k==='tok'?p.kind:p.k;c[k]=(c[k]||0)+1});console.log(c);await b.close()})();
