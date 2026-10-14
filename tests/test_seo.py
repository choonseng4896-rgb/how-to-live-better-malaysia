import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.articles, self.canonical, self.text = [], [], []
        self.meta, self.details = {}, {}
        self.script = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'article': self.articles.append(attrs.get('id'))
        if tag == 'meta': self.meta[attrs.get('name', attrs.get('property'))] = attrs.get('content')
        if tag == 'link' and attrs.get('rel') == 'canonical': self.canonical.append(attrs.get('href'))
        if tag == 'details': self.details[attrs.get('id')] = attrs
        if tag == 'script': self.script = True

    def handle_endtag(self, tag):
        if tag == 'script': self.script = False

    def handle_data(self, data):
        if not self.script: self.text.append(data)

class SearchAndSeoArtifacts(unittest.TestCase):
    def setUp(self):
        self.html = (ROOT / 'dist/index.html').read_text(encoding='utf-8')
        self.page = PageParser()
        self.page.feed(self.html)
        self.items = json.loads((ROOT / 'content/items.json').read_text(encoding='utf-8'))

    def test_every_article_is_in_initial_html(self):
        self.assertEqual(set(self.page.articles), {'tip-' + str(i['id']) for i in self.items})
        text = ' '.join(self.page.text)
        for item in self.items: self.assertIn(item['body'], text)

    def test_source_directory_is_collapsed(self):
        self.assertNotIn('open', self.page.details['source-directory'])

    def test_region_filter_and_calculator_removed(self):
        self.assertNotIn('id="region"', self.html)
        self.assertNotIn('id="budget"', self.html)

    def test_canonical_and_sharing_metadata(self):
        self.assertEqual(self.page.canonical, ['https://choonseng4896-rgb.github.io/how-to-live-better-malaysia/'])
        self.assertTrue(self.page.meta['description'])
        self.assertEqual(self.page.meta['og:type'], 'website')

    def test_structured_data_matches_content(self):
        schema = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', self.html, re.S).group(1))
        self.assertEqual(len(schema['mainEntity']['itemListElement']), len(self.items))
        self.assertEqual(schema['@type'], 'CollectionPage')

    def test_sitemap_lists_only_canonical_page(self):
        tree = ET.fromstring((ROOT / 'dist/sitemap.xml').read_text())
        locations = tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
        self.assertEqual(len(locations), 1)
        self.assertNotIn('?q=', locations[0].text)

if __name__ == '__main__': unittest.main()
