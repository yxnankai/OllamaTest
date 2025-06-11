import requests
import json

def test_ollama_api():
    # Ollama API 基础 URL
    base_url = "http://localhost:11434"
    
    # 测试模型列表
    def list_models():
        response = requests.get(f"{base_url}/api/tags")
        return response.json()
    
    # 测试模型生成
    def generate_text(prompt, model="tinyllama"):
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9
            }
        }
        try:
            response = requests.post(f"{base_url}/api/generate", json=data)
            response.raise_for_status()  # 检查响应状态
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API 请求错误: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"错误详情: {e.response.text}")
            return None
    
    # 测试对话
    def chat(message, model="tinyllama"):
        data = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ],
            "stream": False
        }
        try:
            response = requests.post(f"{base_url}/api/chat", json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API 请求错误: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"错误详情: {e.response.text}")
            return None

    # 运行测试
    try:
        # 测试获取模型列表
        print("获取可用模型列表：")
        models = list_models()
        print(json.dumps(models, indent=2, ensure_ascii=False))
        
        # 测试文本生成
        print("\n测试文本生成：")
        prompt = "用中文解释什么是人工智能"
        result = generate_text(prompt)
        if result:
            print(f"输入: {prompt}")
            print(f"输出: {result.get('response', '')}")
            if 'error' in result:
                print(f"错误信息: {result['error']}")
        
        # 测试对话
        print("\n测试对话功能：")
        message = "explain how to use ollama"
        chat_result = chat(message)
        if chat_result:
            print(f"用户: {message}")
            print(f"AI: {chat_result.get('message', {}).get('content', '')}")
            if 'error' in chat_result:
                print(f"错误信息: {chat_result['error']}")
        
    except requests.exceptions.ConnectionError:
        print("错误：无法连接到 Ollama 服务。请确保 Ollama 服务正在运行。")
    except Exception as e:
        print(f"发生错误：{str(e)}")

if __name__ == "__main__":
    test_ollama_api() 