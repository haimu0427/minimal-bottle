# 贡献指南

感谢您对Minimal Bottle项目的关注！我们欢迎各种形式的贡献。

## 如何贡献

### 报告问题
- 使用GitHub Issue tracker报告bug
- 提供详细的复现步骤
- 包含Python版本和操作系统信息
- 提供最小化的复现代码

### 提交代码
1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的修改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### 代码规范
- 遵循PEP 8编码规范
- 保持代码简洁明了
- 添加适当的注释
- 确保所有测试通过
- 保持零依赖的原则

## 开发设置

```bash
# 克隆项目
git clone https://github.com/haimu0427/minimal-bottle.git
cd minimal-bottle

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -e .[dev]

# 运行测试
python -m pytest tests/ -v

# 运行代码检查
flake8 bottle_minimal.py
```

## 测试

### 运行所有测试
```bash
python -m pytest tests/ -v
```

### 运行特定测试
```bash
python -m pytest tests/test_bottle_minimal.py::TestRouter -v
```

### 覆盖率测试
```bash
python -m pytest tests/ --cov=bottle_minimal --cov-report=html
```

## 项目原则

### 零依赖
- **不要**添加任何外部依赖
- 仅使用Python标准库
- 保持单文件实现

### 极简主义
- 保持代码简洁
- 移除不必要的功能
- 优先考虑可读性

### 教育价值
- 代码应该易于理解
- 添加清晰的注释
- 提供良好的示例

## 可以贡献的内容

### Bug修复
- 修复路由问题
- 修复模板解析错误
- 修复静态文件服务问题

### 功能增强
- 改进错误消息
- 优化性能
- 增加文档

### 测试
- 添加更多测试用例
- 提高测试覆盖率
- 添加集成测试

### 文档
- 改进README
- 添加更多示例
- 创建教程

## 提交信息规范

使用清晰的提交信息：

```
类型: 简短描述

详细说明（可选）

Fixes #123
```

类型包括：
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `test`: 测试相关
- `refactor`: 代码重构
- `perf`: 性能优化

## 发布流程

1. 更新版本号
2. 更新CHANGELOG
3. 创建发布标签
4. 上传到PyPI

## 行为准则

- 友善和尊重
- 欢迎新手
- 耐心解答问题
- 建设性反馈

## 联系方式

- GitHub Issues: 报告bug和请求功能
- GitHub Discussions: 一般讨论
- Email: contact@minimalbottle.org

## 许可证

通过贡献代码，您同意您的贡献将在MIT许可证下发布。

再次感谢您的贡献！