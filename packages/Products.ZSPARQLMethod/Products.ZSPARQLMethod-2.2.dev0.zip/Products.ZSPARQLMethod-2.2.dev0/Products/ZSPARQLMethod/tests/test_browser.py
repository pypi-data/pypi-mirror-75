#XXXX TODO: the tests from test_browser.py need to be fixed

import unittest
from mock import patch
import wsgi_intercept
from Products.ZSPARQLMethod.tests.zope_wsgi import WsgiApp, css, csstext, parse_html
from webob import Request
from Products.ZSPARQLMethod.Method import sparql
from Products.ZSPARQLMethod.Method import ZSPARQLMethod
from Products.ZSPARQLMethod.tests.test_method import EIONET_RDF
import Products.ZSPARQLMethod.tests.mock_db as mock_db

try:
    import simplejson as json
except ImportError:
    import json

try:
    import wsgi_intercept.mechanize_intercept as mechanize_intercept
    Browser = mechanize_intercept.Browser
except ImportError:
    from mechanize import Browser as MechanizeBrowser
    from wsgi_intercept.urllib_intercept import WSGI_HTTPHandler, WSGI_HTTPSHandler

    class Browser(MechanizeBrowser):
        """
        A version of the mechanize browser class that
        installs the WSGI intercept handler
        """
        handler_classes = MechanizeBrowser.handler_classes.copy()
        handler_classes['http'] = WSGI_HTTPHandler
        handler_classes['https'] = WSGI_HTTPSHandler


class BrowserTest(unittest.TestCase):
    """"""
    __name__ = 'BrowserTest'

    def setUp(self):
        self.method = ZSPARQLMethod('sq', "Test Method", "")
        self.method.endpoint_url = "https://cr.eionet.europa.eu/sparql"
        self.method.query = mock_db.GET_LANG_BY_NAME
        self.method.arg_spec = u"lang_name:string"

        self.app = WsgiApp(self.method)

        wsgi_intercept.add_wsgi_intercept('test', 80, lambda: self.app)
        self.browser = Browser()
        # disable robots
        self.browser.set_handle_robots(False)
        self.validate_patch = patch('AccessControl.SecurityManagement'
                                    '.SecurityManager.validate')
        self.validate_patch.start().return_value = True

        self.mock_db = mock_db.MockSparql()
        self.mock_db.start()


    def tearDown(self):
        self.mock_db.stop()
        self.validate_patch.stop()
        wsgi_intercept.remove_wsgi_intercept('test', 80)

    @unittest.skip
    def test_manage_edit(self):
        br = self.browser
        br.addheaders = br.addheaders + [('Connection','keep-alive')]

        br.open('http://test/manage_edit_html')

        br._factory.is_html = True
        br.select_form(name='edit-method')
        br['title'] = "My awesome method"
        br['endpoint_url'] = "http://dbpedia.org/sparql"
        br['query'] = "New query value"
        br['arg_spec'] = "confirm:boolean"
        br.submit()

        self.assertEqual(self.method.title, "My awesome method")
        self.assertEqual(self.method.endpoint_url, "http://dbpedia.org/sparql")
        self.assertEqual(self.method.query, "New query value")
        self.assertEqual(self.method.arg_spec, "confirm:boolean")

    @unittest.skip
    def test_query_test_page(self):
        self.method.query = mock_db.GET_LANG_NAMES
        self.method.arg_spec = u""
        br = self.browser

        page = parse_html(br.open('http://test/test_html').read())
        table = css(page, 'table.sparql-results')[0]

        table_headings = [e.text for e in css(table, 'thead th')]
        self.assertEqual(table_headings, ['lang_url', 'name'])

        table_data = [[td.text for td in css(tr, 'td')]
                      for tr in css(table, 'tbody tr')]
        self.assertEqual(len(table_data), 45)
        lang_da_url = 'http://rdfdata.eionet.europa.eu/eea/languages/da'
        self.assertEqual(table_data[7], ['<'+lang_da_url+'>', '"Danish"@en'])

    @unittest.skip
    def test_with_literal_argument(self):
        br = self.browser
        br.addheaders = br.addheaders + [('lang_name', 'Danish'), ('Connection','keep-alive')]

        br.open('http://test/test_html')

        br._factory.is_html = True
        br.select_form(name='method-arguments')
        br['lang_name'] = "Danish"

        page = parse_html(br.submit().read())
        self.assertEqual(csstext(page, 'table.sparql-results tbody td'),
                         u"<http://rdfdata.eionet.europa.eu/eea/languages/da>")

    @unittest.skip
    def test_autofill_submitted_argument(self):
        br = self.browser
        br.addheaders = br.addheaders + [('lang_name', 'Danish'), ('Connection','keep-alive')]
        br.open('http://test/test_html')

        br._factory.is_html = True
        br.select_form(name='method-arguments')
        br['lang_name'] = "Danish"

        br.submit()

        br._factory.is_html = True
        br.select_form(name='method-arguments')
        self.assertEqual(br['lang_name'], "Danish")

    @unittest.skip
    def test_REST_query(self):
        req = Request.blank('http://test/?lang_name=Danish')
        response = req.get_response(self.app)

        self.assertEqual(response.headers['Content-Type'], 'application/json')
        json_response = json.loads(response.body)
        danish_iri = sparql.IRI(EIONET_RDF+'/languages/da')
        self.assertEqual(json_response['rows'], [[danish_iri.n3()]])


# HEADERS = {
#     'lang_name': 'Danish',
#     'title': 'My awesome method',
#     'endpoint_url': 'http://dbpedia.org/sparql',
#     'query': 'New query value',
#     'arg_spec': 'confirm:boolean'
# }