<!-- 作者：阿洋 -->

# 字体方案 — 多平台排版字体配置

## 中文正文字体优先级
| 优先级 | 字体名称 | 适用平台 | 特点 |
|--------|---------|---------|------|
| 1 | 未来荧黑（Glow Sans SC） | Windows/macOS/Linux | 现代感强，字重丰富，开源免费 |
| 2 | 霞鹜文楷（LXGW WenKai） | Windows/macOS/Linux | 手写风格，阅读舒适，开源免费 |
| 3 | 思源黑体（Source Han Sans SC） | Windows/macOS/Linux | 覆盖完整，多字重，Adobe+Google联合开发 |
| 4 | 微软雅黑（Microsoft YaHei） | Windows | 系统默认，兼容性好 |
| 5 | 苹方（PingFang SC） | macOS/iOS | 系统默认，优化屏幕显示 |
| 6 | 宋体（SimSun） | Windows | 系统默认，传统印刷风格 |

## 英文正文字体优先级
| 优先级 | 字体名称 | 适用平台 | 特点 |
|--------|---------|---------|------|
| 1 | Source Serif 4 | Windows/macOS/Linux | Adobe开源，衬线体，适合长文阅读 |
| 2 | Charter | Windows/macOS/Linux | 经典衬线体，开源免费 |
| 3 | Georgia | Windows/macOS | 屏幕优化的衬线体 |
| 4 | Times New Roman | Windows/macOS | 通用学术字体 |

## 代码块字体优先级
| 优先级 | 字体名称 | 适用平台 | 特点 |
|--------|---------|---------|------|
| 1 | Fragment Mono | Windows/macOS/Linux | 开源等宽字体，现代设计 |
| 2 | JetBrains Mono | Windows/macOS/Linux | 编程专用，连字支持 |
| 3 | Cascadia Code | Windows | 微软开源，连字支持 |
| 4 | Consolas | Windows | Windows默认等宽字体 |
| 5 | Fira Code | Windows/macOS/Linux | 开源，连字支持 |

## 特殊场景字体
| 场景 | 字体 | 说明 |
|------|------|------|
| 复古风格 | Fusion Pixel Font | 像素风格中文字体 |
| 古籍排版 | LuaTeX-CN | TeX中文排版引擎，支持竖排和古籍 |
| 数学公式 | Latin Modern Math | Unicode数学字体 |
| 书法风格 | 演示悠然小楷 | 手写小楷风格 |

## 字体安装指引

### Windows
```powershell
# 未来荧黑
winget install GlowSansSC

# 思源黑体
winget install Adobe.SourceHanSansSC

# JetBrains Mono
winget install JetBrains.Mono
```

### macOS
```bash
# 未来荧黑
brew install --cask font-glow-sans-sc

# 思源黑体
brew install --cask font-source-han-sans

# JetBrains Mono
brew install --cask font-jetbrains-mono
```

### Linux
```bash
# 未来荧黑
sudo apt install fonts-glow-sans-sc

# 思源黑体
sudo apt install fonts-noto-cjk

# JetBrains Mono
sudo apt install fonts-jetbrains-mono
```

## 字体穷尽尝试策略
当指定字体不可用时，按以下优先级穷尽尝试：

1. 中文正文：Glow Sans SC → LXGW WenKai → Source Han Sans SC → Microsoft YaHei/PingFang SC → SimSun
2. 英文正文：Source Serif 4 → Charter → Georgia → Times New Roman
3. 代码块：Fragment Mono → JetBrains Mono → Cascadia Code → Consolas → monospace
4. 特殊场景：指定字体不可用 → 使用对应类别穷尽尝试字体 → 标注字体缺失

## 完整字体库清单（v3 扩充）

### 中文字体全字重

| 字体名称 | 类型 | 字重覆盖 | 开源 | 许可 | 适用场景 |
|---------|------|---------|------|------|---------|
| 思源黑体（Source Han Sans SC） | 黑体 | ExtraLight / Light / Normal / Regular / Medium / Bold / Heavy | ✅ | SIL OFL 1.1 | 屏幕显示、UI 设计 |
| 思源宋体（Source Han Serif SC） | 宋体 | ExtraLight / Light / Regular / Medium / SemiBold / Bold / Heavy | ✅ | SIL OFL 1.1 | 印刷品、长文排版 |
| 霞鹜文楷（LXGW WenKai） | 楷体 | Light / Regular / Bold / Mono | ✅ | SIL OFL 1.1 | 手写风格、舒适阅读 |
| 得意黑（Smiley Sans） | 黑体 | Regular | ✅ | SIL OFL 1.1 | 现代感、品牌设计 |
| 站酷系列 | 多风格 | 多字重（庆科黄油体/快乐体/文艺体/高端黑/仓耳渔阳体等） | ✅ | SIL OFL 1.1 | 创意排版、标题设计 |
| 江城圆体 | 圆体 | Regular | ✅ | SIL OFL 1.1 | 亲和力、轻松风格 |
| LXGW Bright | 宋体/明体 | Regular / Medium / SemiBold | ✅ | SIL OFL 1.1 | 学术排版、古籍风格 |
| LXGW Marker Gothic | 黑体 | Regular | ✅ | SIL OFL 1.1 | 标记、标签设计 |

### 英文字体

| 字体名称 | 类型 | 特点 | 许可 | 适用场景 |
|---------|------|------|------|---------|
| JetBrains Mono | 等宽 | 编程专用，连字支持，138 种语言 | SIL OFL 1.1 | 代码块、IDE |
| Fragment Mono | 等宽 | 开源等宽，现代设计，基于 URW Gothic | SIL OFL 1.1 | 代码块、终端 |
| Noto Sans | 无衬线 | Google 开源，覆盖全球书写系统 | SIL OFL 1.1 | 多语言正文 |
| Noto Serif | 衬线 | Google 开源，覆盖全球书写系统 | SIL OFL 1.1 | 多语言印刷 |

### 像素字体

| 字体名称 | 类型 | 特点 | 许可 | 适用场景 |
|---------|------|------|------|---------|
| Fusion Pixel | 像素黑体 | 12px 中文像素字体，等宽 | SIL OFL 1.1 | 复古风格、游戏 UI、终端 |

## 场景路由表

| 场景 | 中文首选 | 中文备选 | 英文首选 | 英文备选 |
|------|---------|---------|---------|---------|
| 屏幕显示（screen） | 思源黑体 Regular | 得意黑 | Noto Sans | Inter |
| 打印输出（print） | 思源宋体 Regular | LXGW Bright | Noto Serif | Source Serif 4 |
| 古典风格（classical） | 思源宋体 SemiBold | LXGW Bright | Noto Serif | Georgia |
| 手写风格（handwriting） | 霞鹜文楷 Regular | 演示悠然小楷 | — | — |
| 代码展示（code） | — | — | JetBrains Mono | Fragment Mono |
| 多语言混合（multilingual） | 思源黑体 | 思源宋体 | Noto Sans | Noto Serif |
| 创意设计（creative） | 站酷系列 | 江城圆体 | Fragment Mono | — |
| 复古像素（retro） | Fusion Pixel | — | — | — |

## Typst模板字体声明
```typst
#set text(
  font: (
    "Glow Sans SC",
    "LXGW WenKai",
    "Source Han Sans SC",
    "Noto Sans CJK SC",
    "Microsoft YaHei",
    "PingFang SC",
    "SimSun",
  ),
  lang: "zh",
)

#show raw.where(block: true): set text(
  font: (
    "Fragment Mono",
    "JetBrains Mono",
    "Cascadia Code",
    "Consolas",
    "Fira Code",
  ),
  size: 9pt,
)
```

## 字体版权验证规则

```yaml
font_copyright_policy:
  rule_1: "所有推荐字体均为 SIL OFL 1.1 开源许可，可自由使用、修改、分发"
  rule_2: "商业字体（如方正、汉仪、华康等）不在推荐列表中，避免版权风险"
  rule_3: "版权不确定 → 退回开源等价字体：若用户提出某字体但无法确认许可，自动替换为最接近的 OFL 字"
  rule_4: "Typst 模板中仅声明 OFL 字体，商业字体由用户自行添加"
  rule_5: "字体嵌入 PDF 时仅嵌入 OFL 字体的子集（subset），不违反许可条款"
  exhaust_retry_map:
    商业黑体: "思源黑体（Source Han Sans SC, OFL）"
    商业宋体: "思源宋体（Source Han Serif SC, OFL）"
    商业楷体: "霞鹜文楷（LXGW WenKai, OFL）"
    商业圆体: "江城圆体（OFL）"
    商业等宽: "JetBrains Mono（OFL）"
```