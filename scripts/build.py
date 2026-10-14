# -*- coding: utf-8 -*-
"""Validate source metadata and render a self-contained static page. No dependencies."""
import argparse
import html as html_module
import datetime as dt
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REPO = 'https://github.com/choonseng4896-rgb/how-to-live-better-malaysia'

def load(name):
    return json.loads((ROOT / 'content' / name).read_text(encoding='utf-8'))

def require(test, message):
    if not test:
        raise ValueError(message)

def date(value):
    return dt.date.fromisoformat(value)

def malaysia_today(instant=None):
    instant = instant or dt.datetime.now(dt.timezone.utc)
    return instant.astimezone(dt.timezone(dt.timedelta(hours=8))).date()

def validate(items, groups, sources):
    require(isinstance(items, list) and items, 'items must be a nonempty list')
    keys = {g['key'] for g in groups}
    require(len(keys) == len(groups), 'duplicate category')
    ids = set()
    for key, source in sources.items():
        for field in ['publisher', 'title', 'url', 'checked_at', 'access', 'locator', 'limitations']:
            require(isinstance(source.get(field), str) and source[field].strip(), f'{key}: missing {field}')
        url = urlparse(source['url'])
        require(url.scheme == 'https' and url.hostname and not url.username and not url.password, f'{key}: HTTPS source required')
        require(source['access'] == '正文已读取', f'{key}: source body must be read before inclusion')
        require(date(source['checked_at']) <= malaysia_today(), f'{key}: future check date')
        if source.get('published_or_updated'):
            date(source['published_or_updated'])
    for item in items:
        require(type(item.get('id')) is int and item['id'] > 0 and item['id'] not in ids, 'invalid or duplicate id')
        ids.add(item['id'])
        require(item.get('category') in keys, f'{item["id"]}: invalid category')
        require(item.get('source') in sources, f'{item["id"]}: missing registered source')
        require(item.get('status') == 'sourced', f'{item["id"]}: drafts cannot be published')
        for field in ['title','body','action','action_type','cost','region','period','claim_locator','scope','review_status']:
            require(isinstance(item.get(field),str) and item[field].strip(), f'{item["id"]}: missing {field}')
        require(date(item['last_verified']) <= malaysia_today(), 'future verification date')
        require(date(item['review_after']) >= date(item['last_verified']), 'review date before verification')
        require(item['last_verified'] == sources[item['source']]['checked_at'], 'source/item verification dates disagree')
    return True

def embedded(value):
    # Never let source content terminate the inline script, even in a contributor PR.
    return json.dumps(value,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026').replace('\u2028','\\u2028').replace('\u2029','\\u2029')

def static_card(item, group, sources):
    e = html_module.escape
    s = sources[item['source']]
    return f'''<article class="card" id="tip-{item['id']}"><div class="card-top"><span>#{item['id']:02d} · {e(group['title'])}</span><button class="save" type="button" data-id="{item['id']}" aria-pressed="false" aria-label="收藏：{e(item['title'])}">☆</button></div><h3><a class="permalink" href="#tip-{item['id']}">{e(item['title'])}</a></h3><p>{e(item['body'])}</p><details style="font-size:12px;margin-bottom:16px"><summary>来源、范围与核验记录</summary><p>支持位置：{e(item['claim_locator'])}<br>适用范围：{e(item['scope'])}<br>资料版本：{e(item['period'])}<br>正文核对：{e(item['last_verified'])} · 建议复核期限：{e(item['review_after'])}<br>审核状态：{e(item['review_status'])}<br>核对日期不保证规则此后没有变化。</p><a href="{e(s['url'])}" target="_blank" rel="noopener noreferrer">{e(s['publisher'])} · {e(s['title'])} ↗</a></details><div class="action"><b>可选动作 · 编辑者建议</b>{e(item['action'])}</div><div class="card-foot"><span>{e(item['cost'])} · {e(item['region'])}</span><a class="source-type" href="{e(s['url'])}" target="_blank" rel="noopener noreferrer">一手来源 ↗</a></div></article>'''

def render_static(items, groups, sources):
    e = html_module.escape
    return ''.join(f'<section class="topic" id="topic-{e(g["key"])}"><div class="section-title"><span>{e(g["number"])} /</span><h2>{e(g["headline"])}</h2></div><div class="cards">'+''.join(static_card(i,g,sources) for i in items if i['category']==g['key'])+'</div></section>' for g in groups)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='Verify generated files match source without rewriting')
    args=parser.parse_args()
    items, groups, sources = load('items.json'),load('groups.json'),load('sources.json')
    validate(items,groups,sources)
    active_groups=[g for g in groups if any(i['category']==g['key'] for i in items)]
    source_links={k:[v['publisher']+' · '+v['title'],v['url']] for k,v in sources.items()}
    html=(ROOT/'templates/index.html').read_text(encoding='utf-8')
    canonical = 'https://choonseng4896-rgb.github.io/how-to-live-better-malaysia/'
    e = html_module.escape
    schema = {'@context':'https://schema.org','@type':'CollectionPage','name':'马来西亚生活指南 · 好好生活','url':canonical,'inLanguage':'zh-Hans','description':'逐项附来源的马来西亚社区生活指南。','mainEntity':{'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':n+1,'name':i['title'],'url':canonical+'#tip-'+str(i['id'])} for n,i in enumerate(items)]}}
    nav = '<a href="#top">↗ 全部生活建议</a>'+''.join(f'<a href="#topic-{e(g["key"])}">{e(g["number"])} {e(g["title"])}</a>' for g in active_groups)
    source_html = ''.join(f'<a href="{e(v["url"])}" target="_blank" rel="noopener noreferrer">{e(v["publisher"])} · {e(v["title"])} ↗</a>' for v in sources.values())
    app = (ROOT/'templates/app.js').read_text(encoding='utf-8')
    replacements={'__STATIC_CONTENT__':render_static(items,active_groups,sources),'__STATIC_NAV__':nav,'__STATIC_SOURCES__':source_html,'__SCHEMA__':embedded(schema),'__APP__':app,'__ITEMS__':embedded(items),'__GROUPS__':embedded(active_groups),'__SOURCES__':embedded(source_links),'__COUNT__':str(len(items)),'__TOPICS__':str(len(active_groups)),'__REPO__':REPO}
    for token,value in replacements.items(): html=html.replace(token,value)
    outputs={'dist/index.html':html,'dist/data.json':json.dumps(items,ensure_ascii=False,indent=2)+'\n',
        'dist/sitemap.xml':'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>'+canonical+'</loc></url></urlset>\n',
        'dist/.nojekyll':''} 
    for name,content in outputs.items():
        path=ROOT/name
        if args.check:
            require(path.exists() and path.read_text(encoding='utf-8')==content,f'{name} is out of date; run python3 scripts/build.py')
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(content,encoding='utf-8')
    print(f'Validated {len(items)} entries, {len(sources)} sources, {len(active_groups)} active topics. Link presence is not a factual correctness check.')

if __name__=='__main__': main()
