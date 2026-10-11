"""Run a supplied local axe-core distribution across both languages and themes."""
import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

parser=argparse.ArgumentParser()
parser.add_argument('--base',default='http://127.0.0.1:8000/')
parser.add_argument('--browser')
parser.add_argument('--axe',required=True)
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
results=[]
with sync_playwright() as p:
    options={'headless':True}
    if args.browser: options['executable_path']=args.browser
    browser=p.chromium.launch(**options)
    for width in (390,1440):
        context=browser.new_context(viewport={'width':width,'height':1000},bypass_csp=True)
        # CSP bypass is confined to the audit context so the external QA script can run.
        for language in ('ar','en'):
            for theme in ('light','dark'):
                page=context.new_page()
                page.add_init_script(f'localStorage.setItem("syria.theme",JSON.stringify("{theme}"))')
                for path in ('index.html','explore.html','food.html','culture.html','quiz.html','favorites.html','about.html','credits.html','search.html','places/deir-ez-zor.html','dishes/maarouk.html','stories/crafts.html'):
                    page.goto(args.base.rstrip('/')+'/'+path+'?lang='+language)
                    page.wait_for_selector('body.ready')
                    page.evaluate('() => document.querySelectorAll("img").forEach(i=>i.loading="eager")')
                    page.wait_for_function('() => document.fonts.status==="loaded" && Array.from(document.images).every(i=>i.complete)')
                    page.add_script_tag(path=args.axe)
                    result=page.evaluate('async () => { const r=await axe.run(document,{runOnly:{type:"tag",values:["wcag2a","wcag2aa","wcag21aa","wcag22aa","best-practice"]}}); return {version:r.testEngine.version, violations:r.violations.map(v=>({id:v.id,impact:v.impact,description:v.description,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))})),incomplete:r.incomplete.map(v=>v.id)}; }')
                    result.update(path=path,language=language,theme=theme,width=width)
                    results.append(result)
                    if result['violations']: print('VIOLATIONS',path,language,theme,width,json.dumps(result['violations'],ensure_ascii=True))
                page.close()
        context.close()
    # Check interactive states as well as initial pages.
    context=browser.new_context(bypass_csp=True,viewport={'width':390,'height':900})
    page=context.new_page()
    for path,state in [('explore.html','dialog'),('quiz.html?quiz=cities','question'),('quiz.html?quiz=cities','feedback'),('quiz.html?quiz=cities','results'),('favorites.html','saved')]:
        separator='&' if '?' in path else '?'
        page.goto(args.base.rstrip('/')+'/'+path+separator+'lang=en')
        page.wait_for_selector('body.ready')
        if state=='dialog': page.locator('[data-preview="damascus"]').click()
        if state=='feedback': page.locator('[data-option="1"]').click()
        if state=='results':
            for _ in range(5):
                page.locator('[data-option="0"]').click();page.locator('.quiz-next').click()
        if state=='saved':
            page.goto(args.base.rstrip('/')+'/explore.html?lang=en');page.wait_for_selector('body.ready')
            page.locator('[data-favorite="damascus"]').click()
            page.goto(args.base.rstrip('/')+'/favorites.html?lang=en');page.wait_for_selector('body.ready')
        page.add_script_tag(path=args.axe)
        result=page.evaluate('async () => {const r=await axe.run();return {violations:r.violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))})),incomplete:r.incomplete.map(v=>v.id)}}')
        result.update(path=path,state=state,width=390,language='en',theme='light')
        results.append(result)
        if result['violations']: print('VIOLATIONS',state,json.dumps(result['violations']))
    browser.close()
(root/'.qa/axe-results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
violations=sum(len(r['violations']) for r in results)
print(f'AXE: {len(results)} states checked; {violations} rule violations.')
raise SystemExit(1 if violations else 0)
