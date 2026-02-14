#!/bin/bash
# Polygon 链上数据导出工具 - 环境配置脚本

echo "=============================================="
echo "Polygon 链上数据导出工具 - 环境配置"
echo "=============================================="

# 检查 Python 版本
echo ""
echo "检查 Python 环境..."

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo "已检测到 $PYTHON_VERSION"
else
    echo "错误: 未找到 Python3，请先安装 Python3"
    exit 1
fi

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 创建虚拟环境
echo ""
echo "创建虚拟环境..."

if [ -d "venv" ]; then
    echo "虚拟环境已存在，跳过创建"
else
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        echo "虚拟环境创建成功"
    else
        echo "错误: 创建虚拟环境失败"
        exit 1
    fi
fi

# 激活虚拟环境并安装依赖
echo ""
echo "安装依赖..."

source venv/bin/activate

pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "依赖安装成功"
else
    echo "错误: 依赖安装失败"
    exit 1
fi

deactivate

echo ""
echo "=============================================="
echo "环境配置完成!"
echo ""
echo "使用方法:"
echo "  1. 运行 ./start.sh 启动程序"
echo ""
echo "可选: 设置 Polygonscan API Key 以获得更好的体验"
echo "  export POLYGONSCAN_API_KEY='你的API密钥'"
echo "  或在运行时输入"
echo "=============================================="
