import os
import logging
import requests
import webbrowser
import threading
import time
import traceback
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 配置日志
logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def is_ollama_running():
    """检查 Ollama 服务是否在运行"""
    try:
        logging.info("正在检查 Ollama 服务状态...")
        response = requests.get('http://localhost:11434/api/tags', timeout=2)
        logging.info(f"Ollama 服务响应状态码: {response.status_code}")
        logging.info(f"Ollama 服务响应内容: {response.text}")
        
        if response.status_code == 200:
            logging.info("Ollama 服务正在运行")
            return True
        else:
            logging.warning(f"Ollama 服务返回非 200 状态码: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError as e:
        logging.error(f"连接 Ollama 服务失败: {str(e)}")
        return False
    except Exception as e:
        logging.error(f"检查 Ollama 服务时出错: {str(e)}")
        logging.error(traceback.format_exc())
        return False

def open_browser():
    """打开浏览器"""
    time.sleep(1.5)  # 等待服务器启动
    try:
        webbrowser.open('http://localhost:5000')
        logging.info("已打开浏览器")
    except Exception as e:
        logging.error(f"打开浏览器时出错: {str(e)}")

@app.route('/')
def index():
    """渲染主页"""
    try:
        return render_template('index.html')
    except Exception as e:
        logging.error(f"渲染主页时出错: {str(e)}")
        return str(e), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """处理聊天请求"""
    try:
        data = request.get_json()
        logging.debug(f"收到请求数据: {data}")
        
        if not data or 'message' not in data:
            error_msg = "无效的请求数据"
            logging.error(error_msg)
            return jsonify({'error': error_msg}), 400
        
        message = data['message']
        logging.info(f"收到聊天请求: {message}")
        
        # 检查 Ollama 服务是否运行
        if not is_ollama_running():
            error_msg = "Ollama 服务未运行，请确保 Ollama 已正确启动"
            logging.error(error_msg)
            return jsonify({'error': error_msg}), 503
        
        try:
            # 调用 Ollama API
            api_url = 'http://localhost:11434/api/generate'
            api_data = {
                'model': 'tinyllama',
                'prompt': message,
                'stream': False
            }
            logging.debug(f"发送请求到 Ollama API: {api_url}")
            logging.debug(f"请求数据: {api_data}")
            
            response = requests.post(
                api_url,
                json=api_data,
                timeout=30
            )
            
            logging.debug(f"Ollama API 响应状态码: {response.status_code}")
            logging.debug(f"Ollama API 响应内容: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                logging.info("成功获取 Ollama 响应")
                return jsonify({'response': result.get('response', '')})
            else:
                error_msg = f"Ollama API 返回错误: {response.status_code}"
                logging.error(error_msg)
                logging.error(f"错误响应: {response.text}")
                return jsonify({'error': error_msg}), 500
                
        except requests.exceptions.RequestException as e:
            error_msg = f"调用 Ollama API 时出错: {str(e)}"
            logging.error(error_msg)
            logging.error(traceback.format_exc())
            return jsonify({'error': error_msg}), 500
            
    except Exception as e:
        error_msg = f"处理聊天请求时出错: {str(e)}"
        logging.error(error_msg)
        logging.error(traceback.format_exc())
        return jsonify({'error': error_msg}), 500

def main():
    """主函数"""
    try:
        # 检查 Ollama 服务状态
        if not is_ollama_running():
            logging.warning("启动时检测到 Ollama 服务未运行")
        else:
            logging.info("启动时检测到 Ollama 服务正在运行")
        
        # 在新线程中打开浏览器
        threading.Thread(target=open_browser, daemon=True).start()
        
        # 启动 Flask 应用
        app.run(host='0.0.0.0', port=5000, debug=False)
    except Exception as e:
        error_msg = f"程序运行出错: {str(e)}"
        logging.error(error_msg)
        logging.error(traceback.format_exc())
        print(error_msg)

if __name__ == '__main__':
    main() 