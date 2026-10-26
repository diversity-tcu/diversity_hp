const {chromium} = require('C:/Users/shayashi/AppData/Local/OpenAI/Codex/runtimes/cua_node/a9ba6825a525118c/bin/node_modules/playwright');
const assert = require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 try {
  for (const width of [1440,390]) {
   const page=await browser.newPage({viewport:{width,height:900}});
   for (const route of ['', 'library/mado/']) {
    await page.goto('http://localhost:4321/diversity_hp/'+route);
    await page.evaluate(()=>document.fonts.ready);
    const before=await page.locator('.siteHeader').boundingBox();
    await page.evaluate(()=>window.scrollTo(0,650));
    await page.waitForTimeout(150);
    const after=await page.locator('.siteHeader').boundingBox();
    const bar=await page.locator('.siteHeader_bar').boundingBox();
    assert.equal(Math.round(after.y),0, 'Header stays at viewport top');
    assert.equal(Math.round(after.height),Math.round(before.height));
    assert.equal(Math.round(bar.y+bar.height),Math.round(after.y+after.height));
    assert.equal(await page.locator('.siteHeader_bar').count(),1);
    const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
    assert.equal(overflow,false,'No horizontal overflow');
    if (width===390) {
     await page.locator('.siteHeader_menuTrigger').click();
     await page.locator('.siteHeader_nav.open .gMenu').waitFor({state:'visible'});
     await page.locator('.siteHeader_menuTrigger').click();
    }
    await page.screenshot({path:`tmp/header-check/${width}-${route?'mado':'home'}-scrolled.png`});
    console.log(JSON.stringify({width,route,headerTop:after.y,headerHeight:after.height,barBottom:bar.y+bar.height}));
   }
   await page.close();
  }
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
