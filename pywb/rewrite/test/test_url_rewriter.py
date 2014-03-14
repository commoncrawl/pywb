"""
# UrlRewriter tests
>>> do_rewrite('other.html', '20131010/http://example.com/path/page.html', 'https://web.archive.org/web/')
'https://web.archive.org/web/20131010/http://example.com/path/other.html'

>>> do_rewrite('file.js', '20131010/http://example.com/path/page.html', 'https://web.archive.org/web/', 'js_')
'https://web.archive.org/web/20131010js_/http://example.com/path/file.js'

>>> do_rewrite('/other.html', '20130907*/http://example.com/path/page.html', '/coll/')
'/coll/20130907*/http://example.com/other.html'

>>> do_rewrite('./other.html', '20130907*/http://example.com/path/page.html', '/coll/')
'/coll/20130907*/http://example.com/path/other.html'

>>> do_rewrite('../other.html', '20131112im_/http://example.com/path/page.html', '/coll/')
'/coll/20131112im_/http://example.com/other.html'

>>> do_rewrite('../../other.html', '*/http://example.com/index.html', 'localhost:8080/')
'localhost:8080/*/http://example.com/other.html'

>>> do_rewrite('path/../../other.html', '*/http://example.com/index.html', 'localhost:8080/')
'localhost:8080/*/http://example.com/other.html'

>>> do_rewrite('http://some-other-site.com', '20101226101112/http://example.com/index.html', 'localhost:8080/')
'localhost:8080/20101226101112/http://some-other-site.com'

>>> do_rewrite(r'http:\/\/some-other-site.com', '20101226101112/http://example.com/index.html', 'localhost:8080/')
'localhost:8080/20101226101112/http:\\\\/\\\\/some-other-site.com'

>>> do_rewrite('../../other.html', '2020/http://example.com/index.html', '/')
'/2020/http://example.com/other.html'

>>> do_rewrite('../../other.html', '2020/http://example.com/index.html', '')
'2020/http://example.com/other.html'

>>> do_rewrite('', '20131010010203/http://example.com/file.html', '/web/')
'/web/20131010010203/http://example.com/file.html'

>>> do_rewrite('#anchor', '20131010/http://example.com/path/page.html', 'https://web.archive.org/web/')
'#anchor'

>>> do_rewrite('mailto:example@example.com', '20131010/http://example.com/path/page.html', 'https://web.archive.org/web/')
'mailto:example@example.com'

>>> UrlRewriter('19960708im_/http://domain.example.com/path.txt', '/abc/').get_abs_url()
'/abc/19960708im_/'

>>> UrlRewriter('2013id_/example.com/file/path/blah.html', '/123/').get_timestamp_url('20131024')
'/123/20131024id_/http://example.com/file/path/blah.html'


# HttpsUrlRewriter tests
>>> HttpsUrlRewriter(None, None).rewrite('https://example.com/abc')
'http://example.com/abc'

>>> HttpsUrlRewriter(None, None).rewrite('http://example.com/abc')
'http://example.com/abc'

"""


from pywb.rewrite.url_rewriter import UrlRewriter, HttpsUrlRewriter


def do_rewrite(rel_url, base_url, prefix, mod = None):
    rewriter = UrlRewriter(base_url, prefix)
    return rewriter.rewrite(rel_url, mod)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
