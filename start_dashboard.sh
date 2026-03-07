#!/bin/bash

# TwinReadmit Dashboard 启动脚本
# 用于快速启动优化后的 UI

echo "🚀 启动 TwinReadmit Dashboard..."
echo ""

# 检查是否在正确的目录
if [ ! -f "dashboard/ui_app.py" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    echo "   当前目录: $(pwd)"
    echo "   期望目录: /Users/zhuricardo/Desktop/hackathon"
    exit 1
fi

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "⚠️  警告: 未找到虚拟环境"
    echo "   正在创建虚拟环境..."
    python3 -m venv .venv
fi

# 激活虚拟环境
echo "📦 激活虚拟环境..."
source .venv/bin/activate

# 检查依赖
echo "🔍 检查依赖..."
if ! python -c "import shiny" 2>/dev/null; then
    echo "📥 安装依赖..."
    pip install -r requirements.txt
fi

# 启动应用
echo ""
echo "✨ 启动应用..."
echo "   地址: http://localhost:8001"
echo "   按 Ctrl+C 停止"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

shiny run dashboard/ui_app.py --reload --port 8001
