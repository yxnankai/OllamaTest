@echo off
echo 正在安装依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo 安装依赖失败！
    pause
    exit /b 1
)

echo 正在打包程序...
python build.py
if errorlevel 1 (
    echo 打包失败！
    pause
    exit /b 1
)

echo 完成！
pause 