.. _http:

httplib
=======

python2 PSL for http client.

usage
-----

BaseHTTPServer/CGIHTTPServer/SimpleHTTPServer/cookielib/Cookie
==============================================================

python2 PSL for http server.

usage
-----

import::

    import BaseHTTPServer

class HTTPConnection::

    HTTPConnection(host, port=None, strict=None, timeout=<object object>, source_address=None)
    # methods:
    request(self, method, url, body=None, headers={})
    getresponse(self, buffering=False) # 返回HTTPResponse对象

class HTTPSConnection::

    HTTPSConnection(HTTPConnection)
    HTTPSConnection(host, port=None, key_file=None, cert_file=None, strict=None, timeout=<object object>, source_address=None)
    # methods:
    connect()

class HTTPResponse::

    HTTPResponse(sock, debuglevel=0, strict=0, method=None, buffering=False)
    # methods:
    read(self, amt=None)

class BaseHTTPServer::

    用于实现http的基本的server.参考SocketServer标准库.

class BaseHttpRequestHandler::

    BaseHTTPRequestHandler(SocketServer.StreamRequestHandler)

class HTTPServer::

    HTTPServer(SocketServer.TCPServer)
    HTTPServer(server_address, RequestHandlerClass, bind_and_activate=True)
    # methods:
    serve_forever(self, poll_interval=0.5)

http
====

python3 PSL for http.

usage
-----

httplib2
========

https://github.com/httplib2/httplib2

install
-------

install from pypi::

    $ pip install httplib2

usage
-----

-------------------------------------------------------------------------------

urlparse/urllib/urllib2
=======================

python2 PSL for url.

usage
-----

import::

    import urlparse

functions::

    urlparse.urlparse(url, scheme='', allow_fragments=True) # 返回urlparse.ParseResult类
    # 返回: (scheme, netloc, path, params, query, fragment)
    urlparse.ParseResult(self, scheme, netloc, path, params, query, fragment)

    urlparse.urljoin(base, url, allow_fragements=True)

urllib
======

python3 PSL for url.

usage
-----


urllib3
=======

https://github.com/shazow/urllib3

install
-------

install from pypi::

    $ pip install urllib3

usage
-----

-------------------------------------------------------------------------------

requests
========

`<https://github.com/kennethreitz/requests>`_

从http/https获取内容.

install
-------

install from pypi::

    $ pip install requests

usage
-----

import::

    import requests

function request::

    # requests.api定义了下列方法来发起请求,返回requests.Response类型的对象。
    requests.reqeust(method, url, **kwargs) # 实际调用session.request()
    get(url, params=None, **kwargs)
    post(url, data=None, json=None, **kwargs)
    put(url, data=None, **kwargs)
    patch(url, data=None, **kwargs)
    delete(url, **kwargs)
    head(url, **kwargs)
    options(url, **kwargs)
    # multipart/form-data # 用于上传文本和二进制文件，用post方法

    # **kwargs参数参考requests.Request类
    # dict/bytes
    params={} # 用于get的url中
    # dict/bytes/file
    data={} # 用于post/put/patch的body中
    # dict
    headers={}
    cookies={}
    files={}
    proxies=None

    # json
    json='{}' # 用于post的body中

    # tuple
    auth=('user', 'password') # 参考requests.auth包.
    # tuple or string
    cert=(cert.pem, key.pem)
    # tuple or float
    timeout=(connect timeout, read timeout) # None表示永久等待．

    # bool
    allow_redirects=True # 是否重定向
    stream=True
    # bool or string
    verify=True # 是否验证SSL

class Response::

    r.close()
    r.iter_content(chunk_size=1, decode_unicode=False)
    r.iter_lines(chunk_size=512, decode_unicode=None, delimiter=None)
    r.json(**kwargs) # 返回dict / [dict1, dict2, ...]
    r.raise_for_status()
    # Data:
    r.content # 返回str类型, 通过json.loads转化为dict.
    r.text # 返回unicode类型
    r.headers # 返回headers
    r.apparent_encoding
    r.is_permanent_redirect
    r.is_redirect
    r.links
    r.ok # True/False
    r.status_code # ok:200
    r.url # 返回URL
    r.history
    # other data
    r.encoding # 查看或设置编码
    r.raw
    r.cookies
    r.elapsed.seconds/microseconds/days

class Sessions::

    from requests.sessions import Session
    会话对象让你能够跨请求保持某些参数。它也会在同一个 Session实例发出的所有请求之间保持cookie.

    # methods:
    requests.reqeust(method, url, **kwargs)
    get(url, params=None, **kwargs)
    post(url, data=None, json=None, **kwargs)
    put(url, data=None, **kwargs)
    patch(url, data=None, **kwargs)
    delete(url, **kwargs)
    head(url, **kwargs)
    options(url, **kwargs)

class Auth::

    身份认证．

    from requests.auth import HTTPBasicAuth
    auth = HTTPBasicAuth(username, password)

    from requests.auth import HTTPProxyAuth
    HTTPProxyAuth(HTTPBasicAuth)

    from requests.auth import HTTPDigestAuth

-------------------------------------------------------------------------------

bs4
===

`<https://www.crummy.com/software/BeautifulSoup/>`_

从XML和HTML文件中提取数据

使用BeautifulSoup处理后文档都是unicode格式，输出都是utf-8格式。

install
-------

install from pypi::

    $ pip install beautifulsoup4

install from binary::

    $ sudo apt-get install Python-bs4

usage
-----

import::

    from bs4 import BeautifulSoup

class BeautifulSoup::

    BeautifulSoup(markup='', features=None, builder=None, parse_only=None, from_encoding=None, exclude_encodings=None, **kwargs)
    soup = BeautifulSoup(r.content, 'lxml') # 返回BeautifulSoup类型对象, 默认html格式
    soup = BeautifulSoup(r.content, "xml") # xml格式
    soup = BeautifulSoup(r.content, "lxml-xml") # 同上
    soup = BeautifulSoup(r.content, "html5lib") # html5格式
    # BeautifulSoup 解析出的python对象有四类： Tag, NavigableString, BeautifulSoup, Comment
    prettify(self, encoding=None, formatter='minimal')
    print(soup.prettify()) # 格式化后以unicode编码输出
    get_text(self, separator=u'', strip=False, types=(<class 'bs4.element.NavigableString'>, <class 'bs4.element.CData'>))
    soup.get_text() # 获取tag中所有内容，以unicode字符串返回
    find(self, name=None, attrs={}, recursive=True, text=None, **kwargs) # 搜索当前节点和子孙节点，查找第一个,返回一个Tag对象
    find_all(self, name=None, attrs={}, recursive=True, text=None, limit=None, **kwargs) # 搜索所有节点，返回Tag对象的列表
    find_parent(self, name=None, attrs={}, **kwargs) # 搜索当前节点的父辈节点
    find_parents(self, name=None, attrs={}, limit=None, **kwargs) # 搜索当前节点的父辈节点
    find_next_sibling(self, name=None, attrs={}, text=None, **kwargs) # 往后搜索当前节点兄弟节点
    find_previous_sibling(self, name=None, attrs={}, text=None, **kwargs) # 往前搜索当前节点的兄弟节点

class Tag::

    tag = soup.<tag-name> # 返回一个Tag类型对象
    tag = soup.<tag-name>.<tag-name>...
    tag.name # tag名字
    tag.attrs # tag类型有很多属性,字典类型
    tag.contents # 将tag子节点以列表方式输出
    tag.children
    tag.parent
    tag.next_sibling # 返回下一个兄弟节点
    tag.previous_sibling # 返回上一个兄弟节点
    tag.next_element # 返回下一个字符串或tag
    tag.previous_element # 返回上一个字符串或tag

class NavigableString::

    ns = tag.string # 返回一个NavigableString类型对象
    unicode(ns) # 转换成unicode
    ns.replace_with(self, replace_with) # 修改内容

class Comment::

    # Comment, 一个特殊的NavigableString对象,只针对有注释的Tag
    comment = soup.<tag-with-comment>.string # 返回Comment类型对象

-------------------------------------------------------------------------------

HTMLParser
==========

python2 PSL for html/xml.

usage
-----

htmlentitydefs
==============

python2 PSL for html.

usage
-----

html
====

python3 PSL for html/xml

python3中更名为html.parser

usage
-----

xml
===

PSL for xml.

usage
-----

lxml
====

`<https://github.com/lxml/lxml>`_

XML和HTML的解析器

install
-------

usage
-----

import::

    from lxml import etree

functions::

    etree.fromstring(text, parser=None, base_url=None) #text是一个string，返回xml的根节点lxml.etree._Element类型的迭代器
    etree.Element(_tag, attrib=None, nsmap=None, **_extra) # 创建一个Element对象,_tag指定节点，比如xml。

    xml_root = etree.Element('xml')
    html_root = etree.Element('html')
    etree.SubElement(_parent, _tag, attrib=None, nsmap=None, **_extra) #往父节点添加子节点，返回Element实例
    tmp_root = etree.SubElement(xml_root, _tag)

html5lib
========

`<https://github.com/html5lib/html5lib-python>`_

install
-------

usage
-----

xmltodict
=========

`<https://github.com/martinblech/xmltodict>`_

install
-------

usage
-----

