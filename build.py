import os
import sys
import shutil
import subprocess
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def build_exe():
    """打包成 exe"""
    try:
        logging.info("开始打包...")
        
        # 检查必要的目录
        if not os.path.exists('templates'):
            logging.error("templates 目录不存在")
            return False
        if not os.path.exists('static'):
            logging.error("static 目录不存在")
            return False
        
        # 清理旧的构建文件
        if os.path.exists('build'):
            logging.info("清理 build 目录...")
            shutil.rmtree('build')
        if os.path.exists('dist'):
            logging.info("清理 dist 目录...")
            shutil.rmtree('dist')
        
        # 使用 PyInstaller 打包
        cmd = [
            'pyinstaller',
            '--noconfirm',
            '--clean',
            '--add-data', 'templates;templates',
            '--add-data', 'static;static',
            '--hidden-import', 'flask',
            '--hidden-import', 'flask_cors',
            '--hidden-import', 'requests',
            '--name', 'OllamaChat',
            '--log-level', 'DEBUG',
            'app.py'
        ]
        
        logging.info(f"执行命令: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        logging.info("打包完成！")
        logging.info("可执行文件位于 dist/OllamaChat 目录下")
        return True
        
    except subprocess.CalledProcessError as e:
        logging.error(f"打包失败: {e}")
        logging.error(f"错误输出: {e.stderr}")
        return False
    except Exception as e:
        logging.error(f"发生错误: {e}")
        return False

if __name__ == '__main__':
    if not build_exe():
        sys.exit(1) 