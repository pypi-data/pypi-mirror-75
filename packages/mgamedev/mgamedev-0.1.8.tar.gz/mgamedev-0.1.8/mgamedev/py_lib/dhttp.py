# encodint:utf8

import requests
from contextlib import closing
import json
import sys
import logging
if sys.version_info < (3, 0):
    from urlparse import urljoin  # noqa
else:
    from urllib.parse import urljoin  # noqa

DEFAULT_HTTP_TIMEOUT = 5


def get_fullurl(baseurl, relurl):
    return urljoin(baseurl, relurl)


class _HttpRequest(object):
    def __init__(self):
        pass

    def execute(self, url, dicparams, method, **kwads):
        try:
            ret = None
            mname = method.upper()
            if mname == "POST":
                ret = requests.post(url, json=dicparams, **kwads)
            elif mname == "GET":
                ret = requests.get(url, params=dicparams, **kwads)

            if ret.status_code == 200:
                return (True, ret.text)
            else:
                logging.error(
                    "Httprequest <method=%s url=%s> raise error!", method, url)

        except requests.exceptions.ConnectionError as identifier:

            logging.error("Http <method=%s url=%s> raise error! \n%s",
                          method, url,
                          str(identifier))
        return (False, None)


class DHttp(object):

    _baseurl = ""

    @classmethod
    def set_baseurl(cls, host):
        cls._baseurl = host

    @classmethod
    def http_get(cls, relurl, dicparams, **kwads):
        (issuc, resp) = _HttpRequest().execute(get_fullurl(cls._baseurl, relurl),
                                               dicparams, "GET", **kwads)
        if issuc:
            try:
                return json.loads(resp, encoding="utf-8")
            except (TypeError, json.decoder.JSONDecodeError) as dec_err:
                logging.error("json decode error")
            else:
                pass

    @classmethod
    def http_post(cls, relurl, dicparams, **kwads):
        (issuc, resp) = _HttpRequest().execute(get_fullurl(cls._baseurl, relurl),
                                               dicparams, "POST", **kwads)
        if issuc:
            try:
                return json.loads(resp, encoding="utf-8")
            except (TypeError, json.JSONDecodeError) as dec_err:
                logging.error("json decode error")
            else:
                pass

    @classmethod
    def download_file(cls, relurl, tarf, process_cb=None, **kwads):
        with closing(requests.get(relurl, stream=True, verify=False)) as r:
            fsize = int(r.headers['content-length'])
            chunk_size = 1024
            nsize = 0
            with open(tarf, "wb") as fp:
                for data in r.iter_content(chunk_size=chunk_size):
                    psize = len(data)
                    nsize += psize
                    fp.write(data)
                    if hasattr(process_cb, '__call__'):
                        process_cb(nsize, fsize)


if __name__ == "__main__":
    DHttp.set_baseurl("https://api.heyzf.com")
    resp = DHttp.http_post("/v1/wstrade/takeout/cargolist?min=1&max=20",
                           {"sign": "123!@#xlmake", "ver": "1.1.1"}, verify=False)
