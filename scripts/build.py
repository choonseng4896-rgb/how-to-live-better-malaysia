# -*- coding: utf-8 -*-
"""Validate source metadata and render a self-contained static page. No dependencies."""
import argparse
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

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='Verify generated files match source without rewriting')
    args=parser.parse_args()
    items, groups, sources = load('items.json'),load('groups.json'),load('sources.json')
    validate(items,groups,sources)
    active_groups=[g for g in groups if any(i['category']==g['key'] for i in items)]
    source_links={k:[v['publisher']+' · '+v['title'],v['url']] for k,v in sources.items()}
    html=(ROOT/'templates/index.html').read_text(encoding='utf-8')
    replacements={'__ITEMS__':embedded(items),'__GROUPS__':embedded(active_groups),'__SOURCES__':embedded(source_links),'__COUNT__':str(len(items)),'__TOPICS__':str(len(active_groups)),'__REPO__':REPO}
    for token,value in replacements.items(): html=html.replace(token,value)
    outputs={'dist/index.html':html,'dist/data.json':json.dumps(items,ensure_ascii=False,indent=2)+'\n'}
    for name,content in outputs.items():
        path=ROOT/name
        if args.check:
            require(path.exists() and path.read_text(encoding='utf-8')==content,f'{name} is out of date; run python3 scripts/build.py')
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(content,encoding='utf-8')
    print(f'Validated {len(items)} entries, {len(sources)} sources, {len(active_groups)} active topics. Link presence is not a factual correctness check.')

if __name__=='__main__': main()
