#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
静态文件示例 - 展示Minimal Bottle的静态文件服务功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bottle_minimal import route, run, static_file, template

# 创建静态文件目录
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')
os.makedirs(STATIC_DIR, exist_ok=True)

# 创建CSS目录
CSS_DIR = os.path.join(STATIC_DIR, 'css')
os.makedirs(CSS_DIR, exist_ok=True)

# 创建JS目录
JS_DIR = os.path.join(STATIC_DIR, 'js')
os.makedirs(JS_DIR, exist_ok=True)

# 创建图片目录
IMG_DIR = os.path.join(STATIC_DIR, 'images')
os.makedirs(IMG_DIR, exist_ok=True)

# 创建示例CSS文件
css_content = '''
body {
    font-family: 'Arial', sans-serif;
    margin: 0;
    padding: 20px;
    background-color: #f5f5f5;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    background: white;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

h1 {
    color: #333;
    border-bottom: 2px solid #007bff;
    padding-bottom: 10px;
}

.nav {
    background: #007bff;
    padding: 15px;
    margin: -20px -20px 20px -20px;
    border-radius: 8px 8px 0 0;
}

.nav a {
    color: white;
    text-decoration: none;
    margin-right: 20px;
    padding: 8px 16px;
    border-radius: 4px;
    transition: background-color 0.3s;
}

.nav a:hover {
    background-color: rgba(255,255,255,0.2);
}

.file-list {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 4px;
    margin: 20px 0;
}

.file-item {
    padding: 10px;
    margin: 5px 0;
    background: white;
    border-left: 4px solid #007bff;
    border-radius: 4px;
}

.download-btn {
    background: #28a745;
    color: white;
    padding: 10px 20px;
    text-decoration: none;
    border-radius: 4px;
    display: inline-block;
    margin: 10px 0;
}

.download-btn:hover {
    background: #218838;
}

.image-gallery {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin: 20px 0;
}

.image-item {
    text-align: center;
}

.image-item img {
    max-width: 200px;
    max-height: 150px;
    border-radius: 4px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}
'''

# 创建示例JS文件
js_content = '''
function showMessage(message) {
    alert(message);
}

function loadFileInfo(filename) {
    console.log('Loading file:', filename);
    // 这里可以添加AJAX请求来获取文件信息
}

// 页面加载完成后的初始化
document.addEventListener('DOMContentLoaded', function() {
    console.log('Static files demo page loaded');
    
    // 为下载按钮添加事件监听
    const downloadButtons = document.querySelectorAll('.download-btn');
    downloadButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            console.log('Downloading:', this.href);
        });
    });
});
'''

# 创建示例HTML文件
demo_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Static Files Demo</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <div class="container">
        <div class="nav">
            <a href="/">Home</a>
            <a href="/static/demo.html">Demo Page</a>
            <a href="#" onclick="showMessage('Hello from JavaScript!')">Test JS</a>
        </div>
        
        <h1>Static Files Demo</h1>
        <p>This page demonstrates static file serving with Minimal Bottle.</p>
        
        <h2>Features Demonstrated:</h2>
        <ul>
            <li>CSS styling from static files</li>
            <li>JavaScript functionality</li>
            <li>Image serving</li>
            <li>File downloads</li>
        </ul>
        
        <p><a href="/" class="download-btn">Back to Main Demo</a></p>
    </div>
    
    <script src="/static/js/app.js"></script>
</body>
</html>
'''

# 写入静态文件
with open(os.path.join(CSS_DIR, 'style.css'), 'w', encoding='utf-8') as f:
    f.write(css_content)

with open(os.path.join(JS_DIR, 'app.js'), 'w', encoding='utf-8') as f:
    f.write(js_content)

with open(os.path.join(STATIC_DIR, 'demo.html'), 'w', encoding='utf-8') as f:
    f.write(demo_html)

# 创建示例文本文件
text_content = '''Minimal Bottle Static Files Demo
================================

This is a sample text file served by Minimal Bottle's static file functionality.

Features:
- Zero dependencies
- Single file implementation
- WSGI compatible
- Thread safe
- Template support
- Static file serving

Created for educational purposes to demonstrate web framework concepts.
'''

with open(os.path.join(STATIC_DIR, 'sample.txt'), 'w', encoding='utf-8') as f:
    f.write(text_content)

# 创建JSON配置文件示例
json_content = '''{
    "framework": "Minimal Bottle",
    "version": "0.1-minimal",
    "features": [
        "routing",
        "templating",
        "static_files",
        "error_handling"
    ],
    "dependencies": [],
    "license": "MIT"
}'''

with open(os.path.join(STATIC_DIR, 'config.json'), 'w', encoding='utf-8') as f:
    f.write(json_content)

# 路由定义
@route('/')
def index():
    """首页显示静态文件信息"""
    files_info = [
        {'name': 'CSS文件', 'path': '/static/css/style.css', 'type': 'Stylesheet'},
        {'name': 'JavaScript文件', 'path': '/static/js/app.js', 'type': 'Script'},
        {'name': 'HTML演示页', 'path': '/static/demo.html', 'type': 'HTML'},
        {'name': '文本文件', 'path': '/static/sample.txt', 'type': 'Text'},
        {'name': 'JSON配置', 'path': '/static/config.json', 'type': 'JSON'},
    ]
    
    html = '''
    <h1>Static Files Demo</h1>
    <p>This example demonstrates static file serving capabilities.</p>
    
    <h2>Available Static Files:</h2>
    <div class="file-list">
    '''
    
    for file_info in files_info:
        html += f'''
        <div class="file-item">
            <strong>{file_info['name']}</strong> ({file_info['type']})<br>
            <a href="{file_info['path']}" target="_blank">View</a> | 
            <a href="{file_info['path']}" download>Download</a>
        </div>
        '''
    
    html += '''
    </div>
    
    <h2>Direct Links:</h2>
    <ul>
        <li><a href="/static/demo.html">View Demo HTML Page</a></li>
        <li><a href="/download/sample.txt">Download Sample Text File</a></li>
        <li><a href="/download/config.json">Download Config JSON</a></li>
    </ul>
    
    <h2>Image Gallery:</h2>
    <p><em>Note: This demo doesn't include actual images, but shows the structure.</em></p>
    '''
    
    return template(html)

@route('/static/<filename:path>')
def serve_static(filename):
    """服务静态文件"""
    return static_file(filename, root=STATIC_DIR)

@route('/download/<filename:path>')
def download_file(filename):
    """下载文件（强制下载）"""
    return static_file(filename, root=STATIC_DIR, download=True)

@route('/info/<filename:path>')
def file_info(filename):
    """显示文件信息"""
    import os
    import mimetypes
    from datetime import datetime
    
    file_path = os.path.join(STATIC_DIR, filename)
    
    if not os.path.exists(file_path):
        return f'File not found: {filename}'
    
    stat = os.stat(file_path)
    mimetype, _ = mimetypes.guess_type(file_path)
    
    info = f'''
    <h1>File Information</h1>
    <p><strong>Filename:</strong> {filename}</p>
    <p><strong>Path:</strong> {file_path}</p>
    <p><strong>Size:</strong> {stat.st_size} bytes</p>
    <p><strong>Modified:</strong> {datetime.fromtimestamp(stat.st_mtime)}</p>
    <p><strong>MIME Type:</strong> {mimetype or 'unknown'}</p>
    
    <p>
        <a href="/static/{filename}">View File</a> | 
        <a href="/download/{filename}">Download</a> | 
        <a href="/">Back to Home</a>
    </p>
    '''
    
    return template(info)

if __name__ == '__main__':
    print("Starting Minimal Bottle Static Files Example...")
    print(f"Static files directory: {STATIC_DIR}")
    print("Visit http://localhost:8080 to see the demo")
    run(host='localhost', port=8080, quiet=False)