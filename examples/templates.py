#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
模板示例 - 展示Minimal Bottle的模板功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bottle_minimal import route, run, template, view

# 创建模板目录
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
os.makedirs(TEMPLATE_DIR, exist_ok=True)

# 创建示例模板文件
layout_template = '''<!DOCTYPE html>
<html>
<head>
    <title>{{title}} - Minimal Bottle</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .nav { background: #f0f0f0; padding: 10px; margin-bottom: 20px; }
        .nav a { margin-right: 15px; text-decoration: none; color: #333; }
        .nav a:hover { color: #007bff; }
        .content { background: white; padding: 20px; border: 1px solid #ddd; }
        .footer { margin-top: 40px; padding: 20px; text-align: center; color: #666; }
    </style>
</head>
<body>
    <div class="nav">
        <a href="/">Home</a>
        <a href="/users">Users</a>
        <a href="/products">Products</a>
        <a href="/inline">Inline Template</a>
    </div>
    <div class="content">
        {{!content}}
    </div>
    <div class="footer">
        <p>Minimal Bottle Template Example</p>
    </div>
</body>
</html>'''

user_list_template = '''<h1>User List</h1>
% for user in users:
    <div style="border: 1px solid #ccc; padding: 10px; margin: 10px 0;">
        <h3>{{user.name}}</h3>
        <p>Email: {{user.email}}</p>
        <p>Age: {{user.age}}</p>
        <p>Active: {{'Yes' if user.active else 'No'}}</p>
    </div>
% end
<p><a href="/">Back to Home</a></p>'''

product_list_template = '''<h1>Product Catalog</h1>
<table border="1" cellpadding="10" cellspacing="0">
    <tr>
        <th>Name</th>
        <th>Price</th>
        <th>Category</th>
        <th>Stock</th>
    </tr>
    % for product in products:
    <tr>
        <td>{{product.name}}</td>
        <td>${{product.price}}</td>
        <td>{{product.category}}</td>
        <td>{{product.stock}}</td>
    </tr>
    % end
</table>
<p><a href="/">Back to Home</a></p>'''

# 写入模板文件
with open(os.path.join(TEMPLATE_DIR, 'layout.html'), 'w', encoding='utf-8') as f:
    f.write(layout_template)

with open(os.path.join(TEMPLATE_DIR, 'user_list.html'), 'w', encoding='utf-8') as f:
    f.write(user_list_template)

with open(os.path.join(TEMPLATE_DIR, 'product_list.html'), 'w', encoding='utf-8') as f:
    f.write(product_list_template)

# 使用模板的视图函数
@route('/')
def index():
    """首页使用模板"""
    content = '''
    <h1>Welcome to Template Examples</h1>
    <p>This page demonstrates the template functionality of Minimal Bottle.</p>
    <p>Features:</p>
    <ul>
        <li>Layout templates</li>
        <li>Variable substitution</li>
        <li>Control structures (for loops, if statements)</li>
        <li>Inline templates</li>
    </ul>
    '''
    return template('layout.html', title='Home', content=content)

@route('/users')
def users():
    """用户列表使用模板"""
    users_data = [
        {'name': 'Alice Johnson', 'email': 'alice@example.com', 'age': 28, 'active': True},
        {'name': 'Bob Smith', 'email': 'bob@example.com', 'age': 32, 'active': False},
        {'name': 'Carol Davis', 'email': 'carol@example.com', 'age': 25, 'active': True},
        {'name': 'David Wilson', 'email': 'david@example.com', 'age': 29, 'active': True}
    ]
    
    content = template('user_list.html', users=users_data)
    return template('layout.html', title='Users', content=content)

@route('/products')
def products():
    """产品列表使用模板"""
    products_data = [
        {'name': 'Laptop', 'price': 999.99, 'category': 'Electronics', 'stock': 15},
        {'name': 'Coffee Mug', 'price': 12.50, 'category': 'Kitchen', 'stock': 50},
        {'name': 'Book: Python Guide', 'price': 29.99, 'category': 'Books', 'stock': 25},
        {'name': 'Wireless Mouse', 'price': 25.00, 'category': 'Electronics', 'stock': 30}
    ]
    
    content = template('product_list.html', products=products_data)
    return template('layout.html', title='Products', content=content)

@route('/inline')
def inline_template():
    """内联模板示例"""
    data = {
        'title': 'Inline Template Demo',
        'items': ['Apple', 'Banana', 'Cherry', 'Date'],
        'user': {'name': 'John Doe', 'role': 'admin'}
    }
    
    # 内联模板
    inline_tpl = '''
    <h1>{{title}}</h1>
    <h2>User: {{user.name}} ({{user.role}})</h2>
    <h3>Fruit List:</h3>
    <ul>
    % for item in items:
        <li>{{item}}</li>
    % end
    </ul>
    <p>This template is defined inline, not in a separate file.</p>
    '''
    
    return template(inline_tpl, **data)

# 使用装饰器的模板示例
@route('/profile/<name>')
@view('layout.html')
def profile(name):
    """使用view装饰器"""
    content = f'''
    <h1>User Profile: {name}</h1>
    <p>This page uses the @view decorator to automatically apply the layout template.</p>
    <p>The view decorator is a convenient way to wrap your view functions with templates.</p>
    '''
    return {'title': f'Profile: {name}', 'content': content}

if __name__ == '__main__':
    print("Starting Minimal Bottle Template Example...")
    print(f"Templates directory: {TEMPLATE_DIR}")
    print("Visit http://localhost:8080 to see the demo")
    run(host='localhost', port=8080, quiet=False)