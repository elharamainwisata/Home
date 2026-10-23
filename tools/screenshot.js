const puppeteer = require('puppeteer-core');
(async () => {
  const [url, out, w, mobile] = process.argv.slice(2);
  const b = await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless:'new'});
  const p = await b.newPage();
  await p.setViewport({width:+w, height:900, deviceScaleFactor:1, isMobile:mobile==='1', hasTouch:mobile==='1'});
  await p.goto(url, {waitUntil:'networkidle2', timeout:90000});
  await new Promise(r=>setTimeout(r,1500));
  for (let y=0; y< await p.evaluate(()=>document.documentElement.scrollHeight); y+=600){ await p.evaluate(v=>window.scrollTo(0,v), y); await new Promise(r=>setTimeout(r,250)); }
  await p.evaluate(()=>window.scrollTo(0,0)); await new Promise(r=>setTimeout(r,2500));
  const dbg = await p.evaluate(()=>({ti:[...document.querySelectorAll('.ti-widget')].map(e=>[e.offsetHeight,getComputedStyle(e).opacity]), imgs:[...document.querySelectorAll('.ehc img')].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src.slice(-60)).slice(0,8)}));
  console.log(JSON.stringify(dbg));
  const H = await p.evaluate(()=>document.documentElement.scrollHeight);
  const secs = await p.evaluate(()=>[...document.querySelectorAll('.ehc section, .ehc-hero')].map(s=>({id:s.id||s.className, top:Math.round(s.getBoundingClientRect().top+scrollY), h:Math.round(s.offsetHeight), w:Math.round(s.offsetWidth)})));
  const sw = await p.evaluate(()=>({sw:document.documentElement.scrollWidth, cw:document.documentElement.clientWidth}));
  console.log(JSON.stringify({H, sw, secs}));
  for (let y=0, i=0; y<H && i<14; y+=1400, i++) {
    await p.screenshot({path:`${out}_${String(i).padStart(2,'0')}.png`, clip:{x:0,y,width:+w,height:Math.min(1400,H-y)}, captureBeyondViewport:true});
  }
  await b.close();
})();
