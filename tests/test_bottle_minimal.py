#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Minimal Bottle 测试套件
"""

import sys
import os
import unittest
import tempfile
import shutil

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bottle_minimal import (
    Bottle, Router, Request, Response, HTTPError, HTTPResponse,
    route, get, post, template, static_file, html_escape, tob, touni
)

class TestHelpers(unittest.TestCase):
    """测试辅助函数"""
    
    def test_tob(self):
        """测试tob函数"""
        self.assertEqual(tob('hello'), b'hello')
        self.assertEqual(tob(b'hello'), b'hello')
        self.assertEqual(tob(None), b'')
        self.assertEqual(tob(123), b'123')
    
    def test_touni(self):
        """测试touni函数"""
        self.assertEqual(touni(b'hello'), 'hello')
        self.assertEqual(touni('hello'), 'hello')
        self.assertEqual(touni(None), '')
        self.assertEqual(touni(123), '123')
    
    def test_html_escape(self):
        """测试HTML转义"""
        self.assertEqual(html_escape('<script>'), '<script>')
        self.assertEqual(html_escape('"quote"'), '"quote"')
        self.assertEqual(html_escape("'quote'"), '&#039;quote&#039;')
        self.assertEqual(html_escape('&'), '&')

class TestRouter(unittest.TestCase):
    """测试路由器"""
    
    def setUp(self):
        self.router = Router()
    
    def test_static_route(self):
        """测试静态路由"""
        def handler(): return "static"
        self.router.add('/test', 'GET', handler)
        
        environ = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/test'}
        target, args = self.router.match(environ)
        self.assertEqual(target, handler)
        self.assertEqual(args, {})
    
    def test_dynamic_route(self):
        """测试动态路由"""
        def handler(): return "dynamic"
        self.router.add('/user/<name>', 'GET', handler)
        
        environ = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/user/john'}
        target, args = self.router.match(environ)
        self.assertEqual(target, handler)
        self.assertEqual(args, {'name': 'john'})
    
    def test_int_filter(self):
        """测试整数过滤器"""
        def handler(): return "int"
        self.router.add('/item/<id:int>', 'GET', handler)
        
        environ = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/item/123'}
        target, args = self.router.match(environ)
        self.assertEqual(target, handler)
        self.assertEqual(args, {'id': 123})
    
    def test_float_filter(self):
        """测试浮点数过滤器"""
        def handler(): return "float"
        self.router.add('/price/<amount:float>', 'GET', handler)
        
        environ = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/price/19.99'}
        target, args = self.router.match(environ)
        self.assertEqual(target, handler)
        self.assertEqual(args, {'amount': 19.99})
    
    def test_404_error(self):
        """测试404错误"""
        environ = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/nonexistent'}
        with self.assertRaises(HTTPError) as cm:
            self.router.match(environ)
        self.assertEqual(cm.exception.status, 404)

class TestRequest(unittest.TestCase):
    """测试请求对象"""
    
    def test_basic_request(self):
        """测试基本请求"""
        environ = {
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': '/test',
            'QUERY_STRING': 'name=john&age=25'
        }
        request = Request(environ)
        
        self.assertEqual(request.method, 'GET')
        self.assertEqual(request.path, '/test')
        self.assertEqual(request.query, {'name': 'john', 'age': '25'})
    
    def test_post_request(self):
        """测试POST请求"""
        # 模拟POST数据
        post_data = b'name=alice&city=london'
        
        environ = {
            'REQUEST_METHOD': 'POST',
            'PATH_INFO': '/submit',
            'CONTENT_TYPE': 'application/x-www-form-urlencoded',
            'CONTENT_LENGTH': str(len(post_data)),
            'wsgi.input': tempfile.BytesIO(post_data)
        }
        request = Request(environ)
        
        self.assertEqual(request.method, 'POST')
        forms = request.forms
        self.assertEqual(forms, {'name': 'alice', 'city': 'london'})
    
    def test_header_access(self):
        """测试头部访问"""
        environ = {
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': '/',
            'HTTP_USER_AGENT': 'TestBrowser/1.0',
            'HTTP_ACCEPT': 'text/html'
        }
        request = Request(environ)
        
        self.assertEqual(request.get_header('User-Agent'), 'TestBrowser/1.0')
        self.assertEqual(request.get_header('Accept'), 'text/html')
        self.assertEqual(request.get_header('Non-Existent'), None)

class TestResponse(unittest.TestCase):
    """测试响应对象"""
    
    def test_basic_response(self):
        """测试基本响应"""
        response = Response()
        self.assertEqual(response.status, 200)
        self.assertEqual(response.body, '')
        self.assertEqual(response.headers, {})
    
    def test_header_manipulation(self):
        """测试头部操作"""
        response = Response()
        response.set_header('Content-Type', 'text/html')
        response.set_header('Custom-Header', 'test-value')
        
        self.assertEqual(response.get_header('Content-Type'), 'text/html')
        self.assertEqual(response.get_header('Custom-Header'), 'test-value')
        self.assertEqual(response.get_header('Non-Existent'), None)

class TestBottleApp(unittest.TestCase):
    """测试Bottle应用"""
    
    def setUp(self):
        self.app = Bottle()
    
    def test_route_decorator(self):
        """测试路由装饰器"""
        @self.app.route('/test')
        def test_handler():
            return 'test response'
        
        # 模拟WSGI环境
        environ = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/test'}
        response_data = self.app._handle(environ)
        self.assertEqual(response_data, [b'test response'])
    
    def test_route_with_params(self):
        """测试带参数的路由"""
        @self.app.route('/hello/<name>')
        def hello_handler(name):
            return f'Hello {name}!'
        
        environ = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/hello/world'}
        response_data = self.app._handle(environ)
        self.assertEqual(response_data, [b'Hello world!'])
    
    def test_error_handling(self):
        """测试错误处理"""
        @self.app.route('/error')
        def error_handler():
            raise HTTPError(500, 'Test error')
        
        environ = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/error'}
        response_data = self.app._handle(environ)
        # 应该返回错误页面
        self.assertIn(b'Error 500', response_data[0])
    
    def test_custom_error_handler(self):
        """测试自定义错误处理"""
        @self.app.error(404)
        def custom_404(error):
            return 'Custom 404 - Page not found'
        
        environ = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/nonexistent'}
        response_data = self.app._handle(environ)
        self.assertEqual(response_data, [b'Custom 404 - Page not found'])

class TestTemplate(unittest.TestCase):
    """测试模板系统"""
    
    def test_simple_template(self):
        """测试简单模板"""
        result = template('Hello {{name}}!', name='World')
        self.assertEqual(result, 'Hello World!')
    
    def test_template_with_loop(self):
        """测试带循环的模板"""
        tpl = '''
% for item in items:
  - {{item}}
% end
'''
        result = template(tpl, items=['apple', 'banana', 'cherry'])
        self.assertIn('- apple', result)
        self.assertIn('- banana', result)
        self.assertIn('- cherry', result)
    
    def test_template_with_condition(self):
        """测试带条件的模板"""
        tpl = '''
% if user:
  Hello {{user}}!
% else:
  Hello Guest!
% end
'''
        result = template(tpl, user='John')
        self.assertIn('Hello John!', result)
        
        result = template(tpl, user=None)
        self.assertIn('Hello Guest!', result)

class TestStaticFile(unittest.TestCase):
    """测试静态文件服务"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(self.test_file, 'w') as f:
            f.write('Test content')
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_static_file_serving(self):
        """测试静态文件服务"""
        response = static_file('test.txt', root=self.temp_dir)
        self.assertIsInstance(response, HTTPResponse)
        self.assertEqual(response.headers['Content-Type'], 'text/plain')
        self.assertEqual(response.headers['Content-Length'], '12')  # 'Test content'
    
    def test_static_file_security(self):
        """测试静态文件安全性"""
        # 尝试访问父目录
        with self.assertRaises(HTTPError) as cm:
            static_file('../etc/passwd', root=self.temp_dir)
        self.assertEqual(cm.exception.status, 403)
    
    def test_static_file_not_found(self):
        """测试文件不存在"""
        with self.assertRaises(HTTPError) as cm:
            static_file('nonexistent.txt', root=self.temp_dir)
        self.assertEqual(cm.exception.status, 404)

class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_request_response_cycle(self):
        """测试完整的请求响应周期"""
        app = Bottle()
        
        @app.route('/api/test')
        def api_test():
            return {'message': 'API test successful', 'status': 'ok'}
        
        # 模拟WSGI调用
        environ = {
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': '/api/test',
            'QUERY_STRING': ''
        }
        
        def start_response(status, headers):
            self.assertEqual(status, '200 OK')
            self.assertIn(('Content-Type', 'text/html; charset=UTF-8'), headers)
        
        response_data = app(environ, start_response)
        self.assertIn(b'API test successful', response_data[0])

if __name__ == '__main__':
    # 运行所有测试
    unittest.main(verbosity=2)