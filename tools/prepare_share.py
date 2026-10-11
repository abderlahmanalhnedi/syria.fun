"""Optional local Chromium export of original SVG brand artwork. Dev: Playwright."""
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

parser=argparse.ArgumentParser()
parser.add_argument('--browser')
parser.add_argument('--base',default='http://127.0.0.1:8000/')
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
svg='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630"><rect width="1200" height="630" fill="#101c2c"/><circle cx="1030" cy="150" r="190" fill="none" stroke="#d8ae68" stroke-opacity=".18"/><circle cx="1030" cy="150" r="160" fill="none" stroke="#d8ae68" stroke-opacity=".18"/><path d="M860 470V250a95 95 0 0 1 190 0v220M908 470V250a47 47 0 0 1 94 0v220M830 470h250" fill="none" stroke="#d8ae68" stroke-width="9"/><text x="85" y="265" fill="#f8f7f3" font-family="Inter,sans-serif" font-size="100" font-weight="700">syria<tspan fill="#d8ae68">.fun</tspan></text><text x="85" y="348" fill="#c6d9d3" font-family="Cairo,sans-serif" font-size="38">Places. Flavours. Stories.</text><text x="85" y="430" fill="#c6d9d3" font-family="Cairo,sans-serif" font-size="32">اكتشف سوريا بطريقة مختلفة</text><path d="M85 480h570" stroke="#d8ae68" stroke-opacity=".5"/></svg>'''
(root/'assets/images/share.svg').write_text(svg,encoding='utf-8')
with sync_playwright() as p:
    options={'headless':True}
    if args.browser: options['executable_path']=args.browser
    browser=p.chromium.launch(**options)
    page=browser.new_page(viewport={'width':1200,'height':630},device_scale_factor=1)
    page.goto(args.base)
    page.set_content('<html><head><link rel="stylesheet" href="'+args.base.rstrip('/')+'/assets/css/fonts.css"><style>html,body{margin:0}svg{display:block;width:1200px;height:630px}</style></head><body>'+svg+'</body></html>')
    page.evaluate('() => document.fonts.ready')
    page.screenshot(path=str(root/'assets/images/share.jpg'),type='jpeg',quality=90)
    page.set_viewport_size({'width':180,'height':180})
    page.goto(args.base.rstrip('/')+'/assets/icons/favicon.svg')
    page.screenshot(path=str(root/'assets/icons/apple-touch-icon.png'))
    browser.close()
print('Exported share.jpg and apple-touch-icon.png from original brand artwork.')
