const {chromium}=require('playwright');const fs=require('fs');
const FF=`@font-face{font-family:"IM Fell English SC";src:url(file:///tmp/claude-0/-home-claude/185e68c8-c4f4-58ca-9d98-ad93a0ae0f4d/scratchpad/tts/node_modules/@fontsource/im-fell-english-sc/files/im-fell-english-sc-latin-400-normal.woff2)}
@font-face{font-family:"IM Fell English";src:url(file:///tmp/claude-0/-home-claude/185e68c8-c4f4-58ca-9d98-ad93a0ae0f4d/scratchpad/tts/node_modules/@fontsource/im-fell-english/files/im-fell-english-latin-400-normal.woff2)}
@font-face{font-family:"IM Fell English";font-style:italic;src:url(file:///tmp/claude-0/-home-claude/185e68c8-c4f4-58ca-9d98-ad93a0ae0f4d/scratchpad/tts/node_modules/@fontsource/im-fell-english/files/im-fell-english-latin-400-italic.woff2)}
@font-face{font-family:"Alegreya Sans";font-weight:400;src:url(file:///tmp/claude-0/-home-claude/185e68c8-c4f4-58ca-9d98-ad93a0ae0f4d/scratchpad/tts/node_modules/@fontsource/alegreya-sans/files/alegreya-sans-latin-400-normal.woff2)}
@font-face{font-family:"Alegreya Sans";font-weight:500;src:url(file:///tmp/claude-0/-home-claude/185e68c8-c4f4-58ca-9d98-ad93a0ae0f4d/scratchpad/tts/node_modules/@fontsource/alegreya-sans/files/alegreya-sans-latin-500-normal.woff2)}
@font-face{font-family:"Alegreya Sans";font-weight:700;src:url(file:///tmp/claude-0/-home-claude/185e68c8-c4f4-58ca-9d98-ad93a0ae0f4d/scratchpad/tts/node_modules/@fontsource/alegreya-sans/files/alegreya-sans-latin-700-normal.woff2)}`;
(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1400,height:1000}});
await pg.goto('file://'+process.cwd()+'/table_tts.html');await pg.waitForTimeout(500);
await pg.evaluate(ff=>{const st=document.createElement('style');st.textContent=ff;document.head.appendChild(st)},FF);
const svg=await pg.evaluate(()=>{let s=document.getElementById('printed').outerHTML;
  s=s.replace(/<circle cx="[0-9.]+" cy="[0-9.]+" r="15" fill="none" stroke="#2A2418" stroke-dasharray="2 3" opacity="\.35"><\/circle>/g,'');
  s=s.replace('Prix de Paris · plafond par point','Prix de Paris · plafond par peau').replace('Lac Supérieur · qualité 2 à 5','Lac Supérieur').replace('Dernières commandes','Commission : dernier mois').replace('>Équipiers<','>Voyageurs<').replace('>Jetons de prix<','><').replace(' · prix fixé à l’arrivée : milieu entre le plus bas et le plus haut des joueurs, arrondi en bas',' · prix fixé à l’arrivée').replace('cliquer pour piocher · déposer un jeton dessus pour le remettre','piochez sans regarder').replace('glisser pour piocher · déposer dessus pour remettre','').replace('>à poser avec une peau sur un navire<','><');
  s=s.replace(/Situations, équipiers et cartes de navire/g,'Associé, recrues, congés et cartes de navire');
  return s});
const css=await pg.evaluate(()=>[...document.styleSheets].map(ss=>{try{return [...ss.cssRules].map(r=>r.cssText).join('\n')}catch(e){return ''}}).join('\n'));
const shots=[['table_full',-178,28,1431,979,3],['pmat_0',-257,1216,465,300,4],['pmat_1',357,1216,465,300,4],['pmat_2',971,1216,465,300,4]];
for(const [n,x,y,w,h,k] of shots){
  const isMat=n.startsWith('pmat');const svgN=isMat?svg:svg.replace(/<g class="pmat">[\s\S]*?<\/g><!--\/pmat-->/g,'');
  const html='<!doctype html><html><head><meta charset="utf-8"><style>'+FF+css+'html,body{margin:0;background:'+(isMat?'transparent':'#231B15')+'}#printed{display:block}</style></head><body>'+svgN.replace(/<svg([^>]*)id="printed"([^>]*)>/,(m)=>m.replace(/width="[^"]*"/,'').replace(/height="[^"]*"/,'').replace(/viewBox="[^"]*"/,''))+'</body></html>';
  await pg.setViewportSize({width:Math.round(w*k),height:Math.round(h*k)});await pg.setContent(html);
  await pg.evaluate(([x,y,w,h,k])=>{const s=document.getElementById('printed');s.setAttribute('viewBox',x+' '+y+' '+w+' '+h);s.setAttribute('width',w*k);s.setAttribute('height',h*k);s.style.width=w*k+'px';s.style.height=h*k+'px'},[x,y,w,h,k]);
  await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(300);
  await pg.screenshot({omitBackground:isMat,path:'img/'+n+'.png',clip:{x:0,y:0,width:Math.round(w*k),height:Math.round(h*k)}});}
await b.close();console.log('ok')})();
