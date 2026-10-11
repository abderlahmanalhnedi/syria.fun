"""Validate committed static documents and bilingual data. Dev: pip install html5lib."""
import json
import re
import subprocess
import sys
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse, unquote
import html5lib

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'assets/data'
def project_files():
    for directory, folders, filenames in os.walk(ROOT):
        folders[:] = [name for name in folders if name not in ('.git','.qa','__pycache__','node_modules','.venv')]
        for filename in filenames:
            yield Path(directory)/filename
files=list(project_files())
translations=json.loads((DATA/'translations.json').read_text(encoding='utf-8'))
for key,value in translations.items():
    assert set(value)=={'ar','en'} and all(value.values()),key
items=[]
for name,count in [('destinations',10),('foods',10),('culture',9)]:
    group=json.loads((DATA/f'{name}.json').read_text(encoding='utf-8'))
    assert len(group)>=count
    for item in group:
        assert re.fullmatch('[a-z][a-z0-9-]+',item['id'])
        assert item['category'] in translations
        assert item['source'].startswith('https://')
        for field in ('name','description','body','subtitle','highlights','fact'):
            assert set(item[field])=={'ar','en'} and all(item[field].values()),(item['id'],field)
        items.append(item)
assert len({item['id'] for item in items})==len(items)
quizzes=json.loads((DATA/'quizzes.json').read_text(encoding='utf-8'))
assert len(quizzes)==4
for quiz in quizzes:
    assert len(quiz['questions'])>=5
    for question in quiz['questions']:
        for field in ('prompt','options','explanation'): assert set(question[field])=={'ar','en'}
        assert len(question['options']['ar'])==len(question['options']['en'])==4
        assert isinstance(question['answer'],int) and 0<=question['answer']<4
print('PASS: 29 bilingual records, translation dictionaries, 4 quizzes / 20 questions')

namespace={'h':'http://www.w3.org/1999/xhtml'}
pages=[path for path in files if path.suffix=='.html']
for path in pages:
    source=path.read_text(encoding='utf-8')
    tree=html5lib.parse(source,treebuilder='etree',namespaceHTMLElements=True)
    parser=html5lib.HTMLParser(strict=True)
    parser.parse(source)
    ids=[node.attrib['id'] for node in tree.iter() if 'id' in node.attrib]
    assert len(ids)==len(set(ids)),(path,'duplicate id')
    assert len(tree.findall('.//h:h1',namespace))==1,path
    assert tree.attrib.get('lang')=='ar' and tree.attrib.get('dir')=='rtl',path
    canon=tree.find('.//h:link[@rel="canonical"]',namespace)
    assert canon is not None and canon.attrib['href'].startswith('https://syria.fun/'),path
    assert tree.find('.//h:meta[@name="description"]',namespace) is not None,path
    for script in tree.findall('.//h:script[@type="application/ld+json"]',namespace):
        assert json.loads(script.text)['@context']=='https://schema.org'
    for node in tree.iter():
        for attr,value in node.attrib.items():
            if attr in ('data-i18n','data-i18n-placeholder','data-i18n-aria-label','data-i18n-alt','data-i18n-title'):
                assert value in translations,(path,value)
            if attr.startswith('on'): raise AssertionError((path,'inline event handler'))
            if attr in ('href','src') and value and not value.startswith(('https:','http:','#','data:')):
                target=unquote(urlparse(value).path)
                if target:
                    assert (path.parent/target).is_file(),(path,target)
        if node.tag.endswith('}img'):
            assert all(attr in node.attrib for attr in ('width','height','alt')),(path,'image dimensions/alt')
print(f'PASS: {len(pages)} HTML5 documents, heading structure, unique IDs, internal targets, SEO and images')
ET.parse(ROOT/'sitemap.xml')
assert (ROOT/'CNAME').read_text().strip()=='syria.fun'
required=['index.html','about.html','explore.html','culture.html','food.html','quiz.html','favorites.html','search.html','credits.html','404.html','.nojekyll','robots.txt','sitemap.xml','README.md','PHOTO_CREDITS.md','LICENSE','docs/ARCHITECTURE.md','docs/DEPLOYMENT.md','docs/CONTENT_GUIDE.md']
for filename in required: assert (ROOT/filename).exists(),filename
for path in (ROOT/'assets/js').glob('*.js'):
    text=path.read_text()
    assert not re.search(r'\.innerHTML\s*=|\beval\s*\(|new Function\s*\(',text),path
print('PASS: required files, valid XML, custom domain, safe DOM source checks')

# Use Node when present; otherwise browser_tests imports every module in Chrome.
import shutil
node=shutil.which('node')
if not node:
    try:
        import playwright
        candidate=Path(playwright.__file__).parent/'driver/node.exe'
        if candidate.is_file(): node=str(candidate)
    except ImportError: pass
if node:
    for path in (ROOT/'assets/js').glob('*.js'):
        subprocess.run([node,'--check',str(path)],check=True,capture_output=True)
    print('PASS: JavaScript syntax checked with Node')
else: print('NOT EXECUTED: standalone JS syntax check; run browser_tests for module parsing')

secret=re.compile(r'gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{32,}')
for path in files:
    if path.suffix in ('.html','.js','.json','.md','.yml','.py','.txt','.css'):
        assert not secret.search(path.read_text(encoding='utf-8')),(path,'possible secret')
print('PASS: common credential patterns absent from project files')
