import tempfile
import unittest
from assets import AssetStore
from reader import EvidenceView
from local_http import serve, request
from fixture_course import AssetOrigin, Course
from capture_probe import inspect_page
from scope import permits


class CaptureTests(unittest.TestCase):
    def test_browser_loads_cross_origin_course(self):
        asset_site = AssetOrigin()
        with tempfile.TemporaryDirectory() as directory, serve(asset_site) as assets:
            course_site = Course(assets)
            with serve(course_site) as base:
                result = inspect_page(base, directory)
                self.assertIn('授权课程 A', result['visible'])
                self.assertEqual(result['frames'], 2)
                self.assertEqual(result['top_response']['status'], 200)
                self.assertTrue(any(path == '/lesson' for method, path, body in course_site.requests))
                self.assertTrue(any(path == '/frame' for method, path in asset_site.requests))

    def test_same_basename_has_independent_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            store = AssetStore(directory)
            first = store.capture('http://one/shared.svg', b'blue', 200, 'image/svg+xml')
            second = store.capture('http://two/shared.svg', b'green', 200, 'image/svg+xml')
            self.assertNotEqual(first['blob'], second['blob'])
            with serve(EvidenceView(store)) as base:
                self.assertEqual(request(base + '/blob/' + first['blob']).body, b'blue')
                self.assertEqual(request(base + '/blob/invalid').status, 404)

    def test_origin_includes_port(self):
        self.assertFalse(permits('http://site:82/a', ['http://site:81']))
        self.assertFalse(permits('data:text/html,x', ['http://site']))
