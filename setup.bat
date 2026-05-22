@echo off
chcp 65001 >nul
echo =====================================
echo   PDF Converter - 环境安装
echo =====================================
echo.

:: 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Python，请先安装 Python 3.10+
    echo 下载地址: https://www.python.org/downloads/
    echo 或运行: winget install Python.Python.3.12
    pause
    exit /b 1
)

echo [1/2] 升级 pip...
python -m pip install --upgrade pip -q

echo [2/2] 安装依赖...
pip install -r requirements.txt

echo.
echo =====================================
echo   安装完成！
echo   命令: conv   单文件转换
echo         conv   批量转换
echo =====================================
echo.
echo 用法示例:
echo   conv report.pdf
echo   conv D:\pdfs\
echo   conv report.pdf -f txt
echo.
pause
