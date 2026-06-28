#!/usr/bin/env bash
# 作者：阿洋
# ==============================================================================
# Profound Cognition v5.1.0 - Font Download Script
# 下载排版管线所需的全部字体文件
#
# 字体清单:
#   1. 霞鹜文楷 (LXGW WenKai) Regular     - 正文字体
#   2. 未来荧黑 (Glow Sans SC) Normal      - 标题/无衬线字体
#   3. Fragment Mono Regular               - 代码/等宽字体
#
# 用法:
#   cd profound-cognition-release-v3
#   bash output/fonts/fetch_fonts.sh
# ==============================================================================

set -euo pipefail

# --- 确定脚本所在目录（字体输出目录） ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FONTS_DIR="$SCRIPT_DIR"

echo "╔══════════════════════════════════════════════════╗"
echo "║  Profound Cognition v5.1.0 - Font Downloader       ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "Fonts will be saved to: $FONTS_DIR"
echo ""

# --- 确保字体目录存在 ---
mkdir -p "$FONTS_DIR"

# --- 检测下载工具 (curl 优先，wget 备选) ---
DOWNLOAD_TOOL=""
if command -v curl &>/dev/null; then
    DOWNLOAD_TOOL="curl"
elif command -v wget &>/dev/null; then
    DOWNLOAD_TOOL="wget"
else
    echo "ERROR: Neither curl nor wget is available."
    echo "       Please install curl or wget and retry."
    exit 1
fi
echo "[INFO] Using download tool: $DOWNLOAD_TOOL"
echo ""

# --- 辅助函数：获取文件大小（跨平台兼容） ---
get_file_size() {
    local f="$1"
    if [ -f "$f" ]; then
        wc -c < "$f" 2>/dev/null | tr -d ' '
    else
        echo "0"
    fi
}

# --- 辅助函数：下载文件 ---
# 参数: $1=URL  $2=输出路径  $3=描述文本
# 返回: 0=成功  1=失败
download_file() {
    local url="$1"
    local output="$2"
    local desc="$3"

    echo "  Downloading: $desc"
    echo "    URL:  $url"
    echo "    Dest: $output"

    local rc=0
    if [ "$DOWNLOAD_TOOL" = "curl" ]; then
        curl -fSL --connect-timeout 30 --max-time 900 --retry 3 --retry-delay 5 \
            -o "$output" "$url" || rc=$?
    else
        wget -q --timeout=30 --tries=3 --retry-connrefused \
            -O "$output" "$url" || rc=$?
    fi

    if [ $rc -ne 0 ]; then
        echo "    ERROR: Download failed (exit code: $rc)"
        rm -f "$output"
        return 1
    fi

    if [ ! -f "$output" ] || [ ! -s "$output" ]; then
        echo "    ERROR: Downloaded file is empty or missing"
        rm -f "$output"
        return 1
    fi

    local sz
    sz=$(get_file_size "$output")
    echo "    OK: Downloaded successfully ($sz bytes)"
    return 0
}

# ==============================================================================
# 1. 霞鹜文楷 (LXGW WenKai) Regular
#    GitHub: https://github.com/lxgw/LxgwWenKai
#    License: SIL Open Font License 1.1
# ==============================================================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[1/3] 霞鹜文楷 (LXGW WenKai) - Regular"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

WENKAI_URL="https://github.com/lxgw/LxgwWenKai/releases/download/v1.522/LXGWWenKai-Regular.ttf"
WENKAI_FILE="$FONTS_DIR/LXGWWenKai-Regular.ttf"

if download_file "$WENKAI_URL" "$WENKAI_FILE" "LXGW WenKai Regular"; then
    echo "  => 霞鹜文楷 Regular: SUCCESS"
else
    echo "  => 霞鹜文楷 Regular: FAILED"
fi
echo ""

# ==============================================================================
# 2. 未来荧黑 (Glow Sans SC) Normal
#    GitHub: https://github.com/welai/glow-sans
#    License: SIL Open Font License 1.1
#    注: 此字体仅提供 OTF 格式，从 v0.92 版本的 Normal 包中提取 Book 字重
# ==============================================================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[2/3] 未来荧黑 (Glow Sans SC) - Normal"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

GLOW_ZIP_URL="https://github.com/welai/glow-sans/releases/download/v0.92/GlowSansSC-Normal-v0.92.zip"
GLOW_TMP_ZIP="$FONTS_DIR/.glow_sans_tmp.zip"
GLOW_OTF_FILE="$FONTS_DIR/GlowSansSC-Normal-Book.otf"

if download_file "$GLOW_ZIP_URL" "$GLOW_TMP_ZIP" "Glow Sans SC Normal (zip archive)"; then
    if command -v unzip &>/dev/null; then
        echo "  Extracting: GlowSansSC-Normal-Book.otf ..."
        if unzip -o "$GLOW_TMP_ZIP" "GlowSansSC-Normal-Book.otf" -d "$FONTS_DIR/" >/dev/null 2>&1; then
            rm -f "$GLOW_TMP_ZIP"
            if [ -f "$GLOW_OTF_FILE" ] && [ -s "$GLOW_OTF_FILE" ]; then
                sz=$(get_file_size "$GLOW_OTF_FILE")
                echo "    OK: Extracted successfully ($sz bytes)"
                echo "  => 未来荧黑 Normal: SUCCESS"
            else
                echo "    ERROR: Extracted file is empty or missing"
                echo "  => 未来荧黑 Normal: FAILED"
            fi
        else
            rm -f "$GLOW_TMP_ZIP"
            echo "    ERROR: unzip failed - GlowSansSC-Normal-Book.otf not found in archive"
            echo "  => 未来荧黑 Normal: FAILED"
        fi
    else
        rm -f "$GLOW_TMP_ZIP"
        echo "    ERROR: 'unzip' command not found. Please install unzip."
        echo "  => 未来荧黑 Normal: FAILED"
    fi
else
    echo "  => 未来荧黑 Normal: FAILED"
fi
echo ""

# ==============================================================================
# 3. Fragment Mono Regular
#    GitHub: https://github.com/weiweihuanghuang/fragment-mono
#    License: SIL Open Font License 1.1
# ==============================================================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[3/3] Fragment Mono - Regular"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

FRAG_ZIP_URL="https://github.com/weiweihuanghuang/fragment-mono/releases/download/1.21/fragment-mono-1.21.zip"
FRAG_TMP_ZIP="$FONTS_DIR/.fragment_tmp.zip"
FRAG_TMP_DIR="$FONTS_DIR/.fragment_extract"
FRAG_TTF_FILE="$FONTS_DIR/FragmentMono-Regular.ttf"
FRAG_ITALIC_FILE="$FONTS_DIR/FragmentMono-Italic.ttf"

if download_file "$FRAG_ZIP_URL" "$FRAG_TMP_ZIP" "Fragment Mono (zip archive)"; then
    if command -v unzip &>/dev/null; then
        echo "  Extracting: FragmentMono-Regular.ttf ..."
        # 创建临时解压目录
        mkdir -p "$FRAG_TMP_DIR"
        unzip -o "$FRAG_TMP_ZIP" -d "$FRAG_TMP_DIR" >/dev/null 2>&1
        rm -f "$FRAG_TMP_ZIP"

        # 在解压目录中查找 TTF 文件
        FOUND_REGULAR=$(find "$FRAG_TMP_DIR" -name "FragmentMono-Regular.ttf" -type f 2>/dev/null | head -1)
        if [ -n "$FOUND_REGULAR" ]; then
            mv "$FOUND_REGULAR" "$FRAG_TTF_FILE"
            sz=$(get_file_size "$FRAG_TTF_FILE")
            echo "    OK: Extracted FragmentMono-Regular.ttf ($sz bytes)"
        else
            echo "    WARNING: FragmentMono-Regular.ttf not found in archive"
        fi

        # 同时提取斜体（如果有的话）
        FOUND_ITALIC=$(find "$FRAG_TMP_DIR" -name "FragmentMono-Italic.ttf" -type f 2>/dev/null | head -1)
        if [ -n "$FOUND_ITALIC" ]; then
            mv "$FOUND_ITALIC" "$FRAG_ITALIC_FILE"
            sz=$(get_file_size "$FRAG_ITALIC_FILE")
            echo "    OK: Extracted FragmentMono-Italic.ttf ($sz bytes)"
        fi

        # 清理临时目录
        rm -rf "$FRAG_TMP_DIR"

        if [ -f "$FRAG_TTF_FILE" ] && [ -s "$FRAG_TTF_FILE" ]; then
            echo "  => Fragment Mono: SUCCESS"
        else
            echo "  => Fragment Mono: FAILED"
        fi
    else
        rm -f "$FRAG_TMP_ZIP"
        echo "    ERROR: 'unzip' command not found. Please install unzip."
        echo "  => Fragment Mono: FAILED"
    fi
else
    echo "  => Fragment Mono: FAILED"
fi
echo ""

# ==============================================================================
# 下载结果汇总
# ==============================================================================
echo "╔══════════════════════════════════════════════════╗"
echo "║  Download Summary                               ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

FAILED=0

check_font() {
    local file="$1"
    local label="$2"
    if [ -f "$file" ] && [ -s "$file" ]; then
        local sz
        sz=$(get_file_size "$file")
        printf "  [OK]    %s\n" "$label"
        printf "          %s (%s bytes)\n" "$(basename "$file")" "$sz"
    else
        printf "  [FAIL]  %s\n" "$label"
        printf "          %s - MISSING\n" "$(basename "$file")"
        FAILED=$((FAILED + 1))
    fi
}

check_font "$WENKAI_FILE"   "霞鹜文楷 LXGW WenKai Regular"
check_font "$GLOW_OTF_FILE" "未来荧黑 Glow Sans SC Normal"
check_font "$FRAG_TTF_FILE" "Fragment Mono Regular"

echo ""
if [ "$FAILED" -eq 0 ]; then
    echo "SUCCESS: All 3 fonts are ready."
    echo ""
    echo "Fonts directory: $FONTS_DIR"
    echo ""
    echo "Files:"
    ls -lh "$FONTS_DIR"/*.ttf "$FONTS_DIR"/*.otf 2>/dev/null || true
    exit 0
else
    echo "WARNING: $FAILED font(s) failed to download."
    echo ""
    echo "Troubleshooting:"
    echo "  - Check your internet connection"
    echo "  - Ensure GitHub is accessible from your network"
    echo "  - Try running the script again (downloads are retried 3 times)"
    exit 1
fi