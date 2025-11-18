# Minimal Bottle - 极简Web框架

一个从Bottle框架精简而来的轻量级Python Web框架，仅包含核心功能，单文件500行左右, 适合学习和快速原型开发。

## 特点

- 🚀 **零依赖**：仅使用Python标准库
- 📦 **单文件实现**：所有功能集成在一个文件中
- 🎯 **功能完整**：包含路由、模板、静态文件服务等核心功能
- 🔧 **WSGI兼容**：符合Python Web服务器网关接口标准
- 📖 **学习友好**：代码简洁，易于理解Web框架工作原理

## 快速开始

```python
from bottle_minimal import route, run

@route('/hello/<name>')
def hello(name):
    return f'Hello {name}!'

@route('/')
def index():
    return 'Welcome to Minimal Bottle!'

if __name__ == '__main__':
    run(host='localhost', port=8080)
```

## 功能特性

### 路由系统
- 静态路由：`/path/to/resource`
- 动态路由：`/user/<name>` 或 `/user/:name`
- 路由过滤器：`<id:int>`, `<price:float>`, `<path:path>`
- 多种HTTP方法：GET, POST, PUT, DELETE

### 请求处理
```python
from bottle_minimal import request

@route('/submit', method='POST')
def submit():
    name = request.forms.get('name')
    age = request.query.get('age')
    return f'Name: {name}, Age: {age}'
```

### 模板系统
```python
from bottle_minimal import template, view

# 内联模板
@route('/hello/<name>')
def hello(name):
    return template('Hello {{name}}!', name=name)

# 模板装饰器
@route('/user/<name>')
@view('user_template')
def user(name):
    return {'name': name, 'age': 25}
```

### 静态文件服务
```python
from bottle_minimal import static_file

@route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root='./static')
```

### 错误处理
```python
from bottle_minimal import error

@error(404)
def error404(error):
    return '页面未找到'

@error(500)
def error500(error):
    return '服务器内部错误'
```

## 项目结构

```
minimal-bottle/
├── bottle_minimal.py    # 核心框架代码
├── examples/            # 示例代码
│   ├── basic.py        # 基础示例
│   ├── templates.py    # 模板示例
│   └── static_files.py # 静态文件示例
├── tests/              # 测试文件
├── docs/               # 文档
├── LICENSE             # 许可证
├── README.md           # 项目说明
└── requirements.txt    # 依赖（空，因为是零依赖）
```

## 安装

无需安装，直接下载 `bottle_minimal.py` 即可使用：

```bash
wget https://raw.githubusercontent.com/yourusername/minimal-bottle/main/bottle_minimal.py
```

## 运行示例

```bash
# 运行基础示例
python examples/basic.py

# 运行模板示例
python examples/templates.py

# 运行静态文件示例
python examples/static_files.py
```

## 与完整版Bottle的区别

| 功能 | Minimal Bottle | 完整版Bottle |
|------|----------------|---------------|
| 文件大小 | ~540行 | ~4000+行 |
| 依赖 | 零依赖 | 部分功能需要额外库 |
| 插件系统 | ❌ | ✅ |
| 多服务器支持 | 仅WSGIRef | 支持多种服务器 |
| 高级模板功能 | 基础功能 | 完整功能 |
| 数据库插件 | ❌ | ✅ |
| 表单验证 | ❌ | ✅ |
| JSON处理 | 基础 | 高级 |
| 文件上传 | ❌ | ✅ |
| Cookies处理 | ❌ | ✅ |
| Sessions | ❌ | ✅ |

## 适用场景

- ✅ **学习Web框架原理**
- ✅ **快速原型开发**
- ✅ **嵌入式Web服务**
- ✅ **微服务架构**
- ✅ **教学演示**
- ❌ **大型生产环境**
- ❌ **复杂业务逻辑**
- ❌ **高并发场景**

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 致谢

感谢Bottle框架的作者们，这个极简版本基于他们的优秀工作。
