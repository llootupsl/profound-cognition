#!/bin/bash
# 作者：阿洋
# Profound Cognition - macOS/Linux 安装脚本
#
# 用法: bash install.sh
# 默认: bash install.sh --scope user
# 可选: bash install.sh --scope project

set -e

REPO_URL="https://github.com/llootupsl/profound-cognition.git"
SKILL_NAME="profound-cognition"
SCOPE="user"

while [ $# -gt 0 ]; do
    case "$1" in
        --scope)
            shift
            SCOPE="${1:-user}"
            ;;
        user|project)
            SCOPE="$1"
            ;;
        *)
            echo "未知参数: $1" >&2
            echo "用法: bash install.sh [--scope user|project]" >&2
            exit 1
            ;;
    esac
    shift
done

if [ "$SCOPE" = "user" ]; then
    TARGET="$HOME/.claude/skills/$SKILL_NAME"
elif [ "$SCOPE" = "project" ]; then
    TARGET="$(pwd)/.claude/skills/$SKILL_NAME"
else
    TARGET="$HOME/.claude/skills/$SKILL_NAME"
fi

echo ""
echo "正在安装 Profound Cognition 技能"
echo "安装路径: $TARGET"
echo ""

if [ -d "$TARGET" ]; then
    echo "已存在，正在更新..."
    cd "$TARGET" && git pull origin master
    echo "更新完成！"
else
    echo "正在下载..."
    mkdir -p "$(dirname "$TARGET")"
    git clone "$REPO_URL" "$TARGET"
    echo "安装完成！"
fi

echo ""
echo "使用方式："
echo "直接在对话中输入分析问题，框架自动激活。"
echo "示例: 分析《三体》中黑暗森林法则的哲学基础"
echo ""
