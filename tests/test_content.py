import copy
import importlib.util
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('build',Path(__file__).resolve().parents[1]/'scripts/build.py')
build=importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)

class PublicationGate(unittest.TestCase):
    def setUp(self):
        self.items=build.load('items.json')
        self.groups=build.load('groups.json')
        self.sources=build.load('sources.json')
    def test_curated_seed_passes(self):
        self.assertTrue(build.validate(self.items,self.groups,self.sources))
    def test_unsourced_content_rejected(self):
        self.items[0]['source']='missing'
        with self.assertRaises(ValueError): build.validate(self.items,self.groups,self.sources)
    def test_drafts_rejected(self):
        self.items[0]['status']='draft'
        with self.assertRaises(ValueError): build.validate(self.items,self.groups,self.sources)
    def test_unread_source_rejected(self):
        self.sources['epf']['access']='search snippet only'
        with self.assertRaises(ValueError): build.validate(self.items,self.groups,self.sources)
    def test_unsafe_source_url_rejected(self):
        self.sources['epf']['url']='javascript:alert(1)'
        with self.assertRaises(ValueError): build.validate(self.items,self.groups,self.sources)
    def test_inline_script_escape(self):
        self.assertNotIn('</script>',build.embedded({'text':'</script><script>alert(1)</script>'}))
    def test_missing_scope_rejected(self):
        self.items[0]['scope']=''
        with self.assertRaises(ValueError): build.validate(self.items,self.groups,self.sources)

if __name__=='__main__': unittest.main()
