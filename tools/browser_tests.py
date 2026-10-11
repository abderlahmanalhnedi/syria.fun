"""End-to-end acceptance checks. Dev-only dependency: pip install playwright."""
import argparse
import json
import os
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--base', default='http://127.0.0.1:8000/')
parser.add_argument('--browser', default=os.environ.get('CHROME_PATH'))
args = parser.parse_args()
BASE = args.base.rstrip('/')+'/'
QA=ROOT/'.qa'; QA.mkdir(exist_ok=True)
checks=[]
errors=[]
def record(name):
    checks.append(name)
    print('PASS:',name)
def ready(page, path):
    page.goto(BASE+path)
    page.wait_for_selector('body.ready')
def screenshot(page, name):
    page.evaluate('() => document.querySelectorAll("img").forEach(img => img.loading="eager")')
    page.wait_for_function('() => Array.from(document.images).every(img => img.complete)')
    page.evaluate('async () => { await Promise.all(Array.from(document.querySelectorAll(".hero-content")).flatMap(node => node.getAnimations().map(animation => animation.finished.catch(()=>{})))); }')
    page.screenshot(path=str(QA/name),full_page=True)

with sync_playwright() as p:
    options={'headless':True}
    if args.browser: options['executable_path']=args.browser
    browser=p.chromium.launch(**options)
    context=browser.new_context(viewport={'width':1440,'height':1000},color_scheme='light')
    page=context.new_page()
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.on('console',lambda msg:errors.append(msg.text) if msg.type=='error' else None)
    ready(page,'index.html')
    assert page.locator('html').get_attribute('lang')=='ar'
    assert page.locator('html').get_attribute('dir')=='rtl'
    assert page.locator('h1').inner_text()=='اكتشف سوريا بطريقة مختلفة'
    assert page.locator('#app-error').is_hidden()
    screenshot(page,'home-ar-desktop.png')
    record('Arabic default, RTL, and homepage content')
    page.locator('#language-toggle').click()
    assert page.locator('html').get_attribute('lang')=='en'
    assert page.locator('html').get_attribute('dir')=='ltr'
    assert 'Discover Syria' in page.title()
    page.reload();page.wait_for_selector('body.ready')
    assert page.locator('html').get_attribute('lang')=='en'
    ready(page,'explore.html')
    assert page.locator('html').get_attribute('lang')=='en'
    record('Language switching, metadata, persistence across reload and navigation')
    page.locator('#theme-toggle').click()
    assert page.locator('html').get_attribute('data-theme')=='dark'
    page.reload();page.wait_for_selector('body.ready')
    assert page.locator('html').get_attribute('data-theme')=='dark'
    page.locator('#theme-toggle').click()
    record('Dark/light theme and persistence')
    assert page.locator('#catalog-grid .card').count()==10
    page.locator('#catalog-search').fill('دِمَشْق')
    assert page.locator('#catalog-grid .card').count()==1
    assert page.locator('#catalog-grid .card').get_attribute('data-id')=='damascus'
    page.locator('#clear-search').click()
    page.locator('[data-filter="coast"]').click()
    assert page.locator('#catalog-grid .card').count()==2
    page.locator('#catalog-search').fill('not-a-real-place')
    assert page.locator('#no-results').is_visible()
    page.locator('#clear-search').click()
    assert page.locator('#catalog-grid .card').count()==10
    record('Arabic diacritics normalization, category filters, no-results, reset')
    ready(page,'search.html?q=Umayyad')
    assert page.locator('#catalog-grid .card[data-id="damascus"]').count()==1
    page.locator('#catalog-search').fill('سماق')
    assert page.locator('#catalog-grid .card[data-id="fattoush"]').count()==1
    page.locator('#clear-search').click()
    assert page.locator('#catalog-grid .card').count()==29
    page.locator('[data-filter="cultures"]').click()
    assert page.locator('#catalog-grid .card').count()==9
    record('Global search across landmarks, food and culture, query links')
    ready(page,'explore.html')
    page.locator('[data-favorite="damascus"]').click()
    assert page.locator('[data-favorite="damascus"]').get_attribute('aria-pressed')=='true'
    page.locator('[data-preview="damascus"]').click()
    assert page.locator('#detail-dialog').is_visible()
    assert page.locator('#dialog-title').inner_text()=='Damascus'
    assert page.evaluate('document.activeElement.matches("[data-close-dialog]")')
    page.keyboard.press('Shift+Tab')
    assert page.evaluate('document.activeElement.closest("#detail-dialog") !== null')
    page.keyboard.press('Escape')
    assert page.locator('#detail-dialog').is_hidden()
    assert page.evaluate('document.activeElement.dataset.preview')=='damascus'
    record('Native dialog focus, focus trapping, Escape, and focus restoration')
    ready(page,'stories/crafts.html')
    page.locator('[data-favorite="crafts"]').click()
    ready(page,'favorites.html')
    assert page.locator('#favorites-grid .card').count()==2
    page.reload();page.wait_for_selector('body.ready')
    assert page.locator('#favorites-grid .card').count()==2
    page.locator('[data-favorite="damascus"]').click()
    page.locator('[data-favorite="crafts"]').click()
    assert page.locator('#favorites-empty').is_visible()
    assert page.locator('[data-favorites-count]').inner_text()=='0'
    record('Place and culture favorites, persistence, removal, count and empty state')
    quizzes=json.loads((ROOT/'assets/data/quizzes.json').read_text(encoding='utf-8'))
    for quiz in quizzes:
        ready(page,'quiz.html?quiz='+quiz['id'])
        for question in quiz['questions']:
            choice=page.locator(f'[data-option="{question["answer"]}"]')
            choice.focus();page.keyboard.press('Enter')
            assert page.locator('.quiz-feedback').is_visible()
            assert page.locator('.quiz-option.correct').count()==1
            assert page.locator('.quiz-option:disabled').count()==4
            page.locator('.quiz-next').click()
        assert page.locator('.result-score').inner_text()=='5 / 5'
        assert page.evaluate('document.activeElement.classList.contains("quiz-question")')
        page.locator('#quiz-panel .button.primary').click()
        wrong=(quiz['questions'][0]['answer']+1)%4
        page.locator(f'[data-option="{wrong}"]').click()
        assert page.locator('.quiz-option.incorrect').count()==1
        page.locator('.quiz-next').click()
        for question in quiz['questions'][1:]:
            page.locator(f'[data-option="{(question["answer"]+1)%4}"]').click()
            page.locator('.quiz-next').click()
        assert page.locator('.result-score').inner_text()=='0 / 5'
        assert '5 / 5' in page.locator('.best-score').inner_text()
    record('All 4 quizzes: perfect and zero scores, feedback, progress, keyboard, restart, best score')
    ready(page,'quiz.html?quiz=cities&lang=ar')
    page.locator('[data-option="0"]').click()
    page.locator('#language-toggle').click()
    assert 'Correct answer' in page.locator('.quiz-feedback').inner_text()
    assert page.locator('.quiz-option.correct').count()==1
    record('Language switch preserves quiz answer and progress')
    for width in (320,375,390,768,1024,1440,1920):
        page.set_viewport_size({'width':width,'height':900})
        for language in ('ar','en'):
            for path in ('index.html','explore.html','food.html','culture.html','quiz.html','favorites.html','about.html','places/deir-ez-zor.html','dishes/maarouk.html'):
                ready(page,path+'?lang='+language)
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'Overflow {width} {language} {path}'
            ready(page,'index.html?lang='+language)
            if width in (390,1440): screenshot(page,f'home-{language}-{width}.png')
        if width<1000:
            page.locator('#menu-toggle').click()
            assert page.locator('#main-navigation').is_visible()
            assert page.locator('#menu-toggle').get_attribute('aria-expanded')=='true'
            page.keyboard.press('Escape')
            assert page.locator('#menu-toggle').get_attribute('aria-expanded')=='false'
            page.locator('#menu-toggle').click()
            page.locator('#main-navigation a[href="food.html"]').click()
            page.wait_for_selector('body.ready')
            assert 'food.html' in page.url
    record('RTL/LTR layouts at 320,375,390,768,1024,1440,1920px; mobile menu and navigation')
    page.set_viewport_size({'width':1440,'height':1000})
    ready(page,'index.html?lang=en')
    page.locator('#theme-toggle').click()
    screenshot(page,'home-en-dark.png')
    page.emulate_media(reduced_motion='reduce')
    assert page.locator('html').evaluate('node=>getComputedStyle(node).scrollBehavior')=='auto'
    record('Reduced-motion preference')
    # Crawl every real page and local link, including nested relative assets.
    paths=[str(file.relative_to(ROOT)).replace('\\','/') for file in ROOT.rglob('*.html') if '.qa' not in file.parts and file.name!='404.html']
    for path in paths:
        ready(page,path+'?lang=ar')
        assert page.locator('h1').count()==1,path
        assert page.locator('meta[name="description"]').get_attribute('content'),path
        assert page.locator('link[rel="canonical"]').get_attribute('href').startswith('https://syria.fun/'),path
        assert page.locator('main').count()==1,path
        for link in page.locator('a[href]').evaluate_all('(nodes)=>nodes.map(n=>n.href)'):
            if link.startswith(BASE):
                response=context.request.get(link.split('#')[0])
                assert response.status==200,(path,link,response.status)
    record(f'{len(paths)} pages: internal links, local assets, heading structure, canonical metadata')
    assert not errors,errors
    record('No browser JavaScript or console errors in normal-use checks')
    # Fault scenarios have their own expected-error contexts.
    fault=browser.new_context(color_scheme='light')
    fp=fault.new_page()
    fp.route('**/assets/images/*webp',lambda route:route.abort())
    ready(fp,'explore.html')
    fp.evaluate('() => document.querySelectorAll("img").forEach(img => img.loading="eager")')
    fp.wait_for_function('() => Array.from(document.images).filter(i=>i.dataset.failed).length >= 10')
    assert fp.locator('img[data-failed]').first.get_attribute('src').endswith('fallback.svg')
    assert 'رسم توضيحي' in fp.locator('img[data-failed]').first.get_attribute('alt')
    fp.set_viewport_size({'width':390,'height':900})
    ready(fp,'index.html?lang=en')
    fp.wait_for_selector('.hero-image[data-failed]')
    assert fp.locator('.hero-image').get_attribute('src').endswith('fallback.svg')
    assert fp.locator('.hero picture source').count()==0
    assert 'Illustration' in fp.locator('.hero-caption').inner_text()
    record('Unavailable photographs use local SVG fallback')
    blocked=browser.new_context()
    blocked.add_init_script('Object.defineProperty(window,"localStorage",{get(){throw new DOMException("Blocked","SecurityError")}})')
    bp=blocked.new_page();ready(bp,'explore.html')
    bp.locator('[data-favorite="damascus"]').click()
    assert bp.locator('[data-favorite="damascus"]').get_attribute('aria-pressed')=='true'
    bp.locator('#language-toggle').click()
    assert bp.locator('html').get_attribute('lang')=='en'
    record('Unavailable LocalStorage does not break interaction')
    offline=browser.new_context();op=offline.new_page()
    op.route('**/assets/data/translations.json',lambda route:route.fulfill(status=503,body='unavailable'))
    op.goto(BASE+'explore.html')
    op.wait_for_selector('#app-error:not([hidden])')
    assert op.locator('#catalog-grid .card').count()==10
    assert op.locator('#main-navigation a[href="food.html"]').count()==1
    op.unroute('**/assets/data/translations.json')
    op.locator('#retry-load').click();op.wait_for_selector('body.ready')
    record('Data loading failure preserves static content; retry recovers')
    corrupt=browser.new_context();cp=corrupt.new_page()
    cp.add_init_script('localStorage.setItem("syria.favorites","{broken");localStorage.setItem("syria.language","123");localStorage.setItem("syria.score.cities","999")')
    ready(cp,'favorites.html')
    assert cp.locator('#favorites-empty').is_visible()
    record('Malformed saved preferences and unknown favorite IDs are guarded')
    nojs=browser.new_context(java_script_enabled=False);np=nojs.new_page()
    np.goto(BASE+'explore.html')
    assert np.locator('#catalog-grid .card').count()==10
    assert np.locator('noscript').is_visible()
    record('Static content and navigation with JavaScript disabled')
    browser.close()
(QA/'browser-results.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2),encoding='utf-8')
print(f'Completed {len(checks)} acceptance groups.')
