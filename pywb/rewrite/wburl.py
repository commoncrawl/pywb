#!/usr/bin/python

"""
WbUrl represents the standard wayback archival url format.
A regular url is a subset of the WbUrl (latest replay).

The WbUrl expresses the common interface for interacting
with the wayback machine.

There WbUrl may represent one of the following forms:

query form: [/modifier]/[timestamp][-end_timestamp]*/<url>

modifier, timestamp and end_timestamp are optional

*/example.com
20101112030201*/http://example.com
2009-2015*/http://example.com
/cdx/*/http://example.com

url query form: used to indicate query across urls
same as query form but with a final *
*/example.com*
20101112030201*/http://example.com*


replay form:
20101112030201/http://example.com
20101112030201im_/http://example.com

latest_replay: (no timestamp)
http://example.com

Additionally, the BaseWbUrl provides the base components
(url, timestamp, end_timestamp, modifier, type) which
can be used to provide a custom representation of the
wayback url format.

"""

import re
import rfc3987


#=================================================================
class BaseWbUrl(object):
    QUERY = 'query'
    URL_QUERY = 'url_query'
    REPLAY = 'replay'
    LATEST_REPLAY = 'latest_replay'

    def __init__(self, url='', mod='',
                 timestamp='', end_timestamp='', type=None):

        self.url = url
        self.timestamp = timestamp
        self.end_timestamp = end_timestamp
        self.mod = mod
        self.type = type


#=================================================================
class WbUrl(BaseWbUrl):
    # Regexs
    # ======================
    QUERY_REGEX = re.compile('^(?:([\w\-:]+)/)?(\d*)(?:-(\d+))?\*/?(.*)$')
    REPLAY_REGEX = re.compile('^(\d*)([a-z]+_)?/{0,3}(.*)$')

    DEFAULT_SCHEME = 'http://'
    # ======================

    def __init__(self, url):
        super(WbUrl, self).__init__()

        self.original_url = url

        if not any(f(url) for f in [self._init_query, self._init_replay]):
            raise Exception('Invalid WbUrl: ', url)

        if len(self.url) == 0:
            raise Exception('Invalid WbUrl: ', url)

        # protocol agnostic url -> http://
        # no protocol -> http://
        inx = self.url.find(':/')
        if inx < 0:
            self.url = self.DEFAULT_SCHEME + self.url
        else:
            inx += 2
            if inx < len(self.url) and self.url[inx] != '/':
                self.url = self.url[:inx] + '/' + self.url[inx:]

        # BUG?: adding upper() because rfc3987 lib
        # rejects lower case %-encoding
        # %2F is fine, but %2f -- standard supports either
        matcher = rfc3987.match(self.url.upper(), 'IRI')

        if not matcher:
            raise Exception('Bad Request Url: ' + self.url)

    # Match query regex
    # ======================
    def _init_query(self, url):
        query = self.QUERY_REGEX.match(url)
        if not query:
            return None

        res = query.groups('')

        self.mod = res[0]
        self.timestamp = res[1]
        self.end_timestamp = res[2]
        self.url = res[3]
        if self.url.endswith('*'):
            self.type = self.URL_QUERY
            self.url = self.url[:-1]
        else:
            self.type = self.QUERY
        return True

    # Match replay regex
    # ======================
    def _init_replay(self, url):
        replay = self.REPLAY_REGEX.match(url)
        if not replay:
            return None

        res = replay.groups('')

        self.timestamp = res[0]
        self.mod = res[1]
        self.url = res[2]
        if self.timestamp:
            self.type = self.REPLAY
        else:
            self.type = self.LATEST_REPLAY

        return True

    def set_replay_timestamp(self, timestamp):
        self.timestamp = timestamp
        self.type = self.REPLAY

    # Str Representation
    # ====================
    def to_str(self, **overrides):
        atype = overrides.get('type', self.type)
        mod = overrides.get('mod', self.mod)
        timestamp = overrides.get('timestamp', self.timestamp)
        end_timestamp = overrides.get('end_timestamp', self.end_timestamp)
        url = overrides.get('url', self.url)

        if atype == self.QUERY or atype == self.URL_QUERY:
            tsmod = ''
            if mod:
                tsmod += mod + "/"
            if timestamp:
                tsmod += timestamp
            if end_timestamp:
                tsmod += '-' + end_timestamp

            tsmod += "*/" + url
            if atype == self.URL_QUERY:
                tsmod += "*"
            return tsmod
        else:
            tsmod = timestamp + mod
            if len(tsmod) > 0:
                return tsmod + "/" + url
            else:
                return url

    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return str((self.type, self.timestamp, self.mod, self.url, str(self)))
