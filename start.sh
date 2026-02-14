#!/bin/bash
# Polygon 链上数据导出工具 - 启动脚本

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "错误: 虚拟环境不存在，请先运行 ./install.sh"
    exit 1
fi

# 激活虚拟环境并运行程序
source venv/bin/activate
python3 evm_transfer_analyzer.py
deactivate
