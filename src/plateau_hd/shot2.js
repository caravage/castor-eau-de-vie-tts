const {chromium}=require('playwright');
const [,,file,w,h,dpr,out,transp]=process.argv;
(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:+w,height:+h},deviceScaleFactor:+dpr});
await pg.goto('file://'+process.cwd()+'/'+file);await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(600);
await pg.screenshot({path:out,clip:{x:0,y:0,width:+w,height:+h},omitBackground:transp==='1'});await b.close();})();
