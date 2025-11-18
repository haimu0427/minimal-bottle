#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
基础示例 - 展示Minimal Bottle的核心功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bottle_minimal import route, run, template, request, response

# 基础路由示例
@route('/')
def index():
    """首页"""
    return '''
    <h1>Welcome to Minimal Bottle!</h1>
    <p><a href="/hello/World">Say Hello</a></p>
    <p><a href="/form">Form Example</a></p>
    <p><a href="/json">JSON Example</a></p>
    '''

@route('/hello/<name>')
def hello(name):
    """动态路由示例"""
    return template('''
    <h1>Hello {{name}}!</h1>
    <p><a href="/">Back to Home</a></p>
    ''', name=name)

@route('/hello/<name:int>')
def hello_number(name):
    """带过滤器的路由示例"""
    return f'You entered number: {name}'

# 表单处理示例
@route('/form')
def form():
    """显示表单"""
    return '''
    <h1>Form Example</h1>
    <form method="POST" action="/submit">
        <p>Name: <input type="text" name="name" /></p>
        <p>Age: <input type="text" name="age" /></p>
        <p><input type="submit" value="Submit" /></p>
    </form>
    <p><a href="/">Back to Home</a></p>
    '''

@route('/submit', method='POST')
def submit():
    """处理表单提交"""
    name = request.forms.get('name', 'Unknown')
    age = request.forms.get('age', 'Unknown')
    
    return f'''
    <h1>Form Submitted!</h1>
    <p>Name: {name}</p>
    <p>Age: {age}</p>
    <p><a href="/form">Back to Form</a></p>
    <p><a href="/">Back to Home</a></p>
    '''

# JSON处理示例
@route('/json')
def json_example():
    """JSON响应示例"""
    response.set_header('Content-Type', 'application/json')
    return '{"message": "Hello JSON!", "status": "success"}'

@route('/api/data')
def api_data():
    """API数据示例"""
    data = {
        'users': [
            {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
            {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'}
        ],
        'total': 2
    }
    response.set_header('Content-Type', 'application/json')
    import json
    return json.dumps(data)

# 错误处理示例
@route('/error')
def trigger_error():
    """触发错误"""
    raise Exception("This is a test error!")

if __name__ == '__main__':
    print("Starting Minimal Bottle Basic Example...")
    print("Visit http://localhost:8080 to see the demo")
    run(host='localhost', port=8080, quiet=False)