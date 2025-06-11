# Ollama API 测试项目

这是一个用于测试 Ollama API 功能的 Python 项目。该项目提供了基本的 API 调用示例，包括模型列表获取、文本生成和对话功能。

## 环境要求

- Python 3.7+
- Ollama 服务
- requests 库

## 安装步骤

### 1. 安装 Ollama

#### Windows 用户
1. 访问 [Ollama 官方下载页面](https://ollama.ai/download)
2. 下载 Windows 安装包
3. 运行安装程序
4. 安装完成后，Ollama 服务会自动启动

#### Linux 用户
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### macOS 用户
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. 安装项目依赖

```bash
pip install -r requirements.txt
```

### 3. 下载模型

本项目默认使用 tinyllama 模型，您可以通过以下命令下载：

```bash
ollama pull tinyllama
```

## 使用方法

1. 确保 Ollama 服务正在运行
2. 运行测试程序：

```bash
python test_ollama.py
```

## 功能说明

程序包含以下主要功能：

1. 获取可用模型列表
2. 文本生成测试
3. 对话功能测试

## 配置说明

在 `test_ollama.py` 中，您可以修改以下配置：

- `base_url`: Ollama 服务的地址（默认：http://localhost:11436）
- `model`: 使用的模型名称（默认：tinyllama）
- 生成参数：temperature、top_p 等

## 常见问题

1. 如果遇到连接错误，请确保：
   - Ollama 服务正在运行
   - 端口号配置正确
   - 防火墙设置允许连接

2. 如果模型无法加载，请确保：
   - 已经通过 `ollama pull` 命令下载了相应的模型
   - 模型名称拼写正确

## 注意事项

- 确保有足够的系统资源运行 Ollama 服务
- 首次运行模型时可能需要较长时间
- 建议使用支持 CUDA 的 GPU 来提升性能
