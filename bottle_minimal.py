#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Minimal Bottle - A stripped-down version of Bottle web framework.
Only includes core routing, templates, static files, and basic WSGI server.
"""

import sys
import os
import re
import json
import threading
import mimetypes
import email.utils
from io import BytesIO
from urllib.parse import urljoin, urlencode, quote as urlquote
from http.cookies import SimpleCookie
from collections.abc import MutableMapping as DictMixin
from wsgiref.simple_server import make_server

__version__ = '0.1-minimal'

# Helper functions
def tob(s, enc='utf8'):
    if isinstance(s, str):
        return s.encode(enc)
    return b'' if s is None else bytes(s)

def touni(s, enc='utf8', err='strict'):
    if isinstance(s, (bytes, bytearray)):
        return str(s, enc, err)
    return "" if s is None else str(s)

def html_escape(string):
    return string.replace('&', '&').replace('<', '<').replace('>', '>')\
                 .replace('"', '"').replace("'", '&#039;')

def makelist(data):
    if isinstance(data, (tuple, list, set, dict)):
        return list(data)
    elif data:
        return [data]
    return []

# Exceptions
class BottleException(Exception):
    pass

class HTTPError(BottleException):
    def __init__(self, status=500, body=None, **headers):
        self.status = status
        self.body = body or 'Unknown Error'
        self.headers = headers

class HTTPResponse(BottleException):
    def __init__(self, body='', status=200, headers=None, **more_headers):
        self.body = body
        self.status = status
        self.headers = headers or {}
        self.headers.update(more_headers)

# Routing
def _re_flatten(p):
    if '(' not in p:
        return p
    return re.sub(r'(\\*)(\(\?P<[^>]+>|\((?!\?))', lambda m: m.group(0) if
                  len(m.group(1)) % 2 else m.group(1) + '(?:', p)

class Router:
    def __init__(self):
        self.static = {}
        self.dyna_routes = {}
        self.dyna_regexes = {}
        self.builder = {}
        self.filters = {
            're': lambda conf: (_re_flatten(conf or '[^/]+'), None, None),
            'int': lambda conf: (r'-?\d+', int, lambda x: str(int(x))),
            'float': lambda conf: (r'-?[\d.]+', float, lambda x: str(float(x))),
            'path': lambda conf: (r'.+?', None, None)
        }

    rule_syntax = re.compile('(\\\\*)'
        '(?:(?::([a-zA-Z_][a-zA-Z_0-9]*)?()(?:#(.*?)#)?)'
          '|(?:<([a-zA-Z_][a-zA-Z_0-9]*)?(?::([a-zA-Z_]*)'
            '(?::((?:\\\\.|[^\\\\>])+)?)?)?>))')

    def _itertokens(self, rule):
        offset, prefix = 0, ''
        for match in self.rule_syntax.finditer(rule):
            prefix += rule[offset:match.start()]
            g = match.groups()
            if len(g[0]) % 2:  # Escaped wildcard
                prefix += match.group(0)[len(g[0]):]
                offset = match.end()
                continue
            if prefix:
                yield prefix, None, None
            name, filtr, conf = g[4:7] if g[2] is None else g[1:4]
            yield name, filtr or 'default', conf or None
            offset, prefix = match.end(), ''
        if offset <= len(rule) or prefix:
            yield prefix + rule[offset:], None, None

    def add(self, rule, method, target, name=None):
        anons = 0
        keys = []
        pattern = ''
        filters = []
        builder = []
        is_static = True

        for key, mode, conf in self._itertokens(rule):
            if mode:
                is_static = False
                if mode == 'default': mode = 're'
                mask, in_filter, out_filter = self.filters[mode](conf)
                if not key:
                    pattern += '(?:%s)' % mask
                    key = 'anon%d' % anons
                    anons += 1
                else:
                    pattern += '(?P<%s>%s)' % (key, mask)
                    keys.append(key)
                if in_filter: filters.append((key, in_filter))
                builder.append((key, out_filter or str))
            elif key:
                pattern += re.escape(key)
                builder.append((None, key))

        self.builder[rule] = builder
        if name: self.builder[name] = builder

        if is_static:
            self.static.setdefault(method, {})[rule] = (target, None)
            return

        try:
            re_pattern = re.compile('^(%s)$' % pattern)
            re_match = re_pattern.match
        except re.error as e:
            raise ValueError("Could not add Route: %s (%s)" % (rule, e))

        if filters:
            def getargs(path):
                url_args = re_match(path).groupdict()
                for name, wildcard_filter in filters:
                    try:
                        url_args[name] = wildcard_filter(url_args[name])
                    except ValueError:
                        raise HTTPError(400, 'Path has wrong format.')
                return url_args
        elif re_pattern.groupindex:
            def getargs(path):
                return re_match(path).groupdict()
        else:
            getargs = None

        flatpat = _re_flatten(pattern)
        whole_rule = (rule, flatpat, target, getargs)

        self.dyna_routes.setdefault(method, []).append(whole_rule)
        self._compile(method)

    def _compile(self, method):
        all_rules = self.dyna_routes[method]
        comborules = self.dyna_regexes[method] = []
        maxgroups = 99
        for x in range(0, len(all_rules), maxgroups):
            some = all_rules[x:x + maxgroups]
            combined = (flatpat for (_, flatpat, _, _) in some)
            combined = '|'.join('(^%s$)' % flatpat for flatpat in combined)
            combined = re.compile(combined).match
            rules = [(target, getargs) for (_, _, target, getargs) in some]
            comborules.append((combined, rules))

    def match(self, environ):
        verb = environ['REQUEST_METHOD'].upper()
        path = environ['PATH_INFO'] or '/'

        methods = ('HEAD', 'GET', 'ANY') if verb == 'HEAD' else (verb, 'ANY')

        for method in methods:
            if method in self.static and path in self.static[method]:
                target, getargs = self.static[method][path]
                return target, getargs(path) if getargs else {}
            elif method in self.dyna_regexes:
                for combined, rules in self.dyna_regexes[method]:
                    match = combined(path)
                    if match:
                        target, getargs = rules[match.lastindex - 1]
                        return target, getargs(path) if getargs else {}

        raise HTTPError(404, "Not found: " + repr(path))

    def build(self, _name, *anons, **query):
        builder = self.builder.get(_name)
        if not builder:
            raise ValueError("No route with that name: %s" % _name)
        try:
            for i, value in enumerate(anons):
                query['anon%d' % i] = value
            url = ''.join([f(query.pop(n)) if n else f for (n, f) in builder])
            return url if not query else url + '?' + urlencode(query, doseq=True)
        except KeyError as E:
            raise ValueError('Missing URL argument: %r' % E.args[0])

# Request and Response
class Request:
    def __init__(self, environ):
        self.environ = environ
        self._body = None

    @property
    def path(self):
        return '/' + self.environ.get('PATH_INFO', '').lstrip('/')

    @property
    def method(self):
        return self.environ.get('REQUEST_METHOD', 'GET').upper()

    @property
    def query(self):
        get = {}
        pairs = self.environ.get('QUERY_STRING', '').split('&')
        for pair in pairs:
            if not pair: continue
            nv = pair.split('=', 1)
            if len(nv) != 2: nv.append('')
            get[nv[0]] = nv[1]
        return get

    @property
    def forms(self):
        forms = {}
        if self.method in ('POST', 'PUT'):
            content_type = self.environ.get('CONTENT_TYPE', '')
            if content_type.startswith('application/x-www-form-urlencoded'):
                body = self.body.read().decode('utf8')
                for pair in body.split('&'):
                    if not pair: continue
                    nv = pair.split('=', 1)
                    if len(nv) != 2: nv.append('')
                    forms[nv[0]] = nv[1]
        return forms

    @property
    def params(self):
        params = {}
        params.update(self.query)
        params.update(self.forms)
        return params

    @property
    def body(self):
        if self._body is None:
            try:
                read_func = self.environ['wsgi.input'].read
            except KeyError:
                self._body = BytesIO()
                return self._body
            self._body = BytesIO()
            while True:
                chunk = read_func(8192)
                if not chunk: break
                self._body.write(chunk)
            self._body.seek(0)
        self._body.seek(0)
        return self._body

    def get_header(self, name, default=None):
        key = name.replace('-', '_').upper()
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            key = 'HTTP_' + key
        return self.environ.get(key, default)

class Response:
    def __init__(self):
        self.status = 200
        self.headers = {}
        self.body = ''

    def set_header(self, name, value):
        self.headers[name] = value

    def get_header(self, name, default=None):
        return self.headers.get(name, default)

# Thread-local request and response
_local = threading.local()

def request():
    return getattr(_local, 'request', None)

def response():
    return getattr(_local, 'response', None)

# Application
class Bottle:
    def __init__(self):
        self.routes = []
        self.router = Router()
        self.error_handler = {}

    def route(self, path=None, method='GET', callback=None, name=None):
        if callable(path): path, callback = None, path
        
        def decorator(callback):
            for rule in makelist(path) or ['/' + callback.__name__]:
                for verb in makelist(method):
                    self.routes.append((rule, verb.upper(), callback, name))
                    self.router.add(rule, verb.upper(), callback, name)
            return callback
        
        return decorator(callback) if callback else decorator

    def get(self, path=None, callback=None, **options):
        return self.route(path, 'GET', callback, **options)

    def post(self, path=None, callback=None, **options):
        return self.route(path, 'POST', callback, **options)

    def error(self, code=500, callback=None):
        def decorator(callback):
            self.error_handler[int(code)] = callback
            return callback
        return decorator(callback) if callback else decorator

    def _handle(self, environ):
        _local.request = Request(environ)
        _local.response = Response()
        
        try:
            route, args = self.router.match(environ)
            out = route(**args)
        except HTTPResponse as e:
            out = e
        except HTTPError as e:
            handler = self.error_handler.get(e.status, self._default_error)
            out = handler(e)
        except Exception as e:
            handler = self.error_handler.get(500, self._default_error)
            out = handler(HTTPError(500, str(e)))
        
        return self._cast(out)

    def _cast(self, out):
        resp = response()
        
        if isinstance(out, HTTPResponse):
            resp.status = out.status
            resp.headers.update(out.headers)
            out = out.body
        
        if out is None:
            out = ''
        
        if isinstance(out, str):
            out = out.encode('utf8')
        
        if isinstance(out, bytes):
            if 'Content-Type' not in resp.headers:
                resp.headers['Content-Type'] = 'text/html; charset=UTF-8'
            resp.headers['Content-Length'] = str(len(out))
            return [out]
        
        if hasattr(out, 'read'):
            if 'Content-Type' not in resp.headers:
                resp.headers['Content-Type'] = 'application/octet-stream'
            return out
        
        # Assume iterable
        return out

    def _default_error(self, e):
        return '<h1>Error %s</h1><p>%s</p>' % (e.status, e.body)

    def wsgi(self, environ, start_response):
        out = self._cast(self._handle(environ))
        resp = response()
        
        status = '%d OK' % resp.status
        headers = list(resp.headers.items())
        
        start_response(status, headers)
        return out

    def __call__(self, environ, start_response):
        return self.wsgi(environ, start_response)

# Template system
class SimpleTemplate:
    def __init__(self, source=None, name=None, lookup=None):
        self.source = source
        self.name = name
        self.lookup = lookup or ['./', './views/']
        if not source and name:
            self.load_template()
        self.prepare()

    def load_template(self):
        for path in self.lookup:
            filepath = os.path.join(path, self.name)
            if os.path.isfile(filepath):
                with open(filepath, 'rb') as f:
                    self.source = f.read().decode('utf8')
                return
            for ext in ['tpl', 'html']:
                filepath = os.path.join(path, self.name + '.' + ext)
                if os.path.isfile(filepath):
                    with open(filepath, 'rb') as f:
                        self.source = f.read().decode('utf8')
                    return
        raise ValueError('Template not found: %s' % self.name)

    def prepare(self):
        if not self.source:
            raise ValueError('No template source')
        self.code = self.translate(self.source)

    def translate(self, source):
        code = []
        indent = 0
        lines = source.splitlines(True)
        
        for line in lines:
            if line.strip().startswith('%'):
                cmd = line.strip()[1:].strip()
                if cmd.startswith('if') or cmd.startswith('for') or cmd.startswith('while') or cmd.startswith('def'):
                    code.append('  ' * indent + cmd + ':')
                    indent += 1
                elif cmd.startswith('elif') or cmd.startswith('else'):
                    indent = max(0, indent - 1)
                    code.append('  ' * indent + cmd + ':')
                    indent += 1
                elif cmd == 'end':
                    indent = max(0, indent - 1)
                else:
                    code.append('  ' * indent + cmd)
            elif '{{' in line:
                parts = []
                pos = 0
                for match in re.finditer(r'\{\{(.*?)\}\}', line):
                    parts.append(repr(line[pos:match.start()]))
                    parts.append('str(' + match.group(1) + ')')
                    pos = match.end()
                parts.append(repr(line[pos:]))
                code.append('  ' * indent + '_stdout.append(' + ' + '.join(parts) + ')')
            else:
                code.append('  ' * indent + '_stdout.append(%r)' % line)
        
        return '\n'.join(code)

    def render(self, **kwargs):
        env = {'_stdout': []}
        env.update(kwargs)
        exec(self.code, env)
        return ''.join(env['_stdout'])

def template(tpl, **kwargs):
    if '\n' in tpl or ('{{' in tpl and '}}' in tpl):
        # Inline template
        t = SimpleTemplate(source=tpl)
    else:
        # Template file
        t = SimpleTemplate(name=tpl)
    return t.render(**kwargs)

def view(tpl_name, **defaults):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, dict):
                tplvars = defaults.copy()
                tplvars.update(result)
                return template(tpl_name, **tplvars)
            return result
        return wrapper
    return decorator

# Static file serving
def static_file(filename, root, mimetype=True, download=False):
    root = os.path.join(os.path.abspath(root), '')
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    
    if not filename.startswith(root):
        raise HTTPError(403, "Access denied.")
    if not os.path.isfile(filename):
        raise HTTPError(404, "File does not exist.")
    
    if mimetype is True:
        mimetype, _ = mimetypes.guess_type(filename)
    
    headers = {}
    if mimetype:
        headers['Content-Type'] = mimetype
    
    if download:
        headers['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(filename)
    
    stats = os.stat(filename)
    headers['Content-Length'] = str(stats.st_size)
    headers['Last-Modified'] = email.utils.formatdate(stats.st_mtime, usegmt=True)
    
    return HTTPResponse(open(filename, 'rb'), headers=headers)

# Server
class WSGIRefServer:
    def __init__(self, host='127.0.0.1', port=8080, **options):
        self.host = host
        self.port = port
        self.options = options

    def run(self, app):
        srv = make_server(self.host, self.port, app)
        print("Bottle server starting up (using wsgiref)...")
        print("Listening on http://%s:%d/" % (self.host, self.port))
        print("Hit Ctrl-C to quit.")
        srv.serve_forever()

def run(app=None, host='127.0.0.1', port=8080, server='wsgiref', quiet=False):
    app = app or Bottle()
    if server == 'wsgiref':
        server = WSGIRefServer(host=host, port=port)
    server.run(app)

# Shortcuts
app = Bottle()

def route(path=None, method='GET', callback=None, **options):
    return app.route(path, method, callback, **options)

def get(path=None, callback=None, **options):
    return app.get(path, callback, **options)

def post(path=None, callback=None, **options):
    return app.post(path, callback, **options)

def error(code=500, callback=None):
    return app.error(code, callback)