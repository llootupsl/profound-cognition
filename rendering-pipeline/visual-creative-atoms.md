<!-- 作者：阿洋 -->

# 视觉创意原子库 (Visual Creative Atoms, VCA)

> **定位**: 渲染管道的视觉创意原子化能力库，为所有渲染模块提供可复用的艺术流派风格、生成式艺术、数据可视风格、品牌视觉元素原子。
> **强制规则**: 所有渲染模块的视觉创意元素必须从本原子库选取原子，不得自行声明视觉风格参数。
> **DLP 对接**: 每个原子通过 `visual_dna.color_scheme` / `visual_dna.font_scheme` / `visual_dna.line_style` 字段与 Design Language Protocol (DLP) 对接，由 Taste-Skill 仲裁。
> **融入来源**: techarticleimage-skill（25 种艺术流派风格 + 反 AI 廉价感机制）、algorithmic-art-skill（生成式艺术 + 极简几何 + 高级渐变）

---

## 方法论原理

视觉创意原子库基于"原子化设计"与"生成式艺术"双理论基础：将视觉创意系统分解为最小不可分割的原子单元（艺术流派/生成式艺术/数据可视风格/品牌视觉元素），每个原子封装 SVG/Canvas/Matplotlib 多轨实现，确保跨引擎视觉一致性。原子库融入 techarticleimage-skill 的 25 种真实艺术流派风格能力与 algorithmic-art-skill 的生成式艺术能力，为渲染管线提供经过审美校准的视觉创意原子。

### 反 AI 廉价感总原则

> **融入来源**: techarticleimage-skill — 反 AI 廉价感机制

AI 生成图片的常见问题（过度平滑、缺乏肌理、配色同质化、构图模板化）源于训练数据的统计平均。本原子库通过以下总原则对抗 AI 廉价感：

1. **肌理注入**: 每个艺术流派原子必须包含肌理/噪点/手绘抖动参数，对抗 AI 的过度平滑
2. **配色锚定**: 配色必须锚定真实艺术流派的代表性作品，禁止 AI 凭空生成的"安全配色"
3. **构图破局**: 禁止居中对称的模板化构图，采用艺术流派标志性的不对称/对角线/网格破局构图
4. **细节密度**: 保持艺术流派的标志性细节密度（如构成主义的几何块状密度、极简主义的留白密度），对抗 AI 的"平均化"细节

### 风格先锋不油腻原则

> **融入来源**: algorithmic-art-skill — 风格先锋不油腻

生成式艺术原子必须遵循"先锋不油腻"原则：

1. **克制装饰**: 避免过度装饰，每个生成式艺术原子最多使用 3 种视觉元素
2. **参数可控**: 所有生成参数（粒子数/迭代次数/噪声频率）必须可调，默认值经过审美校准
3. **高级渐变**: 使用 HSL 色彩空间渐变而非 RGB 线性渐变，避免"塑料感"
4. **极简几何**: 生成式艺术原子的基础形状必须为极简几何（圆/线/三角/方），禁止复杂路径

---

## 一、艺术流派风格原子（VCA-ART）

> **融入来源**: techarticleimage-skill — 25 种真实艺术流派风格（本库选取 10 个最核心的）
> **DLP 对接**: 每个艺术流派原子映射到 `visual_dna.color_scheme` 的五色板，由 Taste-Skill 根据 `content_theme` 和 `design_language` 选择匹配的艺术流派。
> **反 AI 廉价感**: 每个艺术流派原子必须标注"反 AI 廉价感要点"，说明如何避免 AI 生成图片的常见问题。

### VCA-ART-001: 极简主义（Minimalism）

- **原子 ID**: VCA-ART-001
- **风格描述**: 极简几何形状，大量留白，单色或双色，灵感来自 Dieter Rams 的"Less but better"设计哲学。核心视觉特征是"减法美学"——去除一切非必要元素，只保留功能与本质。几何形状以圆/方/线为主，留白占比 ≥ 60%，色彩限制在 1-2 色。
- **配色方案**:
  - 主色: `#1A1A1A`（Off-Black，非纯黑）
  - 辅色: `#F5F5F5`（Off-White，非纯白）
  - 强调色: `#E63946`（克制红，仅用于关键强调）
  - 背景色: `#FAFAFA`（纸白）
  - 文本色: `#1A1A1A`
- **生成代码模板**:
  ```svg
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600">
    <!-- 极简主义：大量留白 + 单个几何焦点 -->
    <rect width="800" height="600" fill="#FAFAFA"/>
    <!-- 留白占比 60%+，仅左下角放置几何元素 -->
    <circle cx="200" cy="420" r="80" fill="#1A1A1A"/>
    <!-- 极细线条辅助 -->
    <line x1="100" y1="500" x2="700" y2="500" stroke="#1A1A1A" stroke-width="1"/>
    <!-- 克制强调色：右上角小圆点 -->
    <circle cx="680" cy="120" r="6" fill="#E63946"/>
    <!-- 极简文字标签 -->
    <text x="100" y="540" font-family="Inter, sans-serif" font-size="12" fill="#1A1A1A" letter-spacing="2">MINIMALISM</text>
  </svg>
  ```
- **适用场景**: 科技产品封面、极简主义设计文章、Dieter Rams 风格产品介绍、L1-极简审美等级场景
- **与 DLP 对接规则**: 映射到 `visual_dna.color_scheme` 的主色 `#1A1A1A` + 背景色 `#FAFAFA`。当 `design_language == "学术严谨"` 或 `aesthetic_level == "L1-极简"` 时优先匹配此原子。与 DLP-linear（Linear App 界面）和 DLP-aesop（Aesop 官网）的极简基因兼容。留白参数映射到 `visual_dna.grid_system` 的间距系统，强制使用 `3xl`（64px）以上间距。
- **反 AI 廉价感要点**:
  - **对抗过度平滑**: 在几何边缘添加 0.5px 的微抖动（`stroke-dasharray="0.5,0.3"`），模拟印刷质感
  - **对抗配色同质化**: 严格限制 2 色为主，强调色面积 ≤ 1%，禁止 AI 常见的"三色均衡"配色
  - **对抗构图模板化**: 几何焦点必须偏移中心（左下/右上），禁止居中对称构图
  - **对抗细节平均化**: 留白占比强制 ≥ 60%，AI 倾向于填满画面，此处强制反向操作

---

### VCA-ART-002: 构成主义（Constructivism）

- **原子 ID**: VCA-ART-002
- **风格描述**: 几何块状组合，红黑配色，强烈对角线，灵感来自 El Lissitzky 的 Proun 系列。核心视觉特征是"几何革命"——用矩形/三角形/圆形的动态组合表达力量与运动，对角线构图打破静态平衡，红黑配色传达激进与权威。
- **配色方案**:
  - 主色: `#CC0000`（革命红）
  - 辅色: `#1A1A1A`（墨黑）
  - 强调色: `#F5F5F5`（纸白，作为负空间）
  - 背景色: `#E8E4DC`（米灰，模拟旧纸张）
  - 文本色: `#1A1A1A`
- **生成代码模板**:
  ```svg
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600">
    <!-- 构成主义：红黑几何 + 对角线构图 -->
    <rect width="800" height="600" fill="#E8E4DC"/>
    <!-- 对角线分割 -->
    <polygon points="0,0 400,0 200,600 0,600" fill="#CC0000"/>
    <!-- 黑色矩形块 -->
    <rect x="450" y="150" width="200" height="120" fill="#1A1A1A" transform="rotate(-15 550 210)"/>
    <!-- 白色圆形（负空间） -->
    <circle cx="650" cy="450" r="70" fill="#F5F5F5"/>
    <!-- 对角线线条 -->
    <line x1="50" y1="550" x2="750" y2="50" stroke="#1A1A1A" stroke-width="3"/>
    <!-- 构成主义文字（倾斜） -->
    <text x="480" y="400" font-family="Impact, sans-serif" font-size="28" fill="#1A1A1A" transform="rotate(-15 480 400)" font-weight="bold">КОНСТРУКТИВИЗМ</text>
  </svg>
  ```
- **适用场景**: 革命性主题文章、设计史介绍、激进观点表达、政治/社会议题封面
- **与 DLP 对接规则**: 映射到 `visual_dna.color_scheme` 的主色 `#CC0000` + 辅色 `#1A1A1A`。当 `content_theme` 含"革命/激进/变革/先锋"关键词时优先匹配此原子。与 DLP-ted（TED 演讲幻灯片）的强对比基因兼容。对角线角度参数映射到 `visual_dna.line_style`，强制使用 15°-45° 倾斜。
- **反 AI 廉价感要点**:
  - **对抗过度平滑**: 在几何块状边缘添加纸张纹理叠加（`<filter>` 噪点），模拟 1920s 印刷质感
  - **对抗配色同质化**: 红黑配色为硬性约束，禁止 AI 添加"调和色"（如灰色过渡）
  - **对抗构图模板化**: 强制对角线构图（15°-45°），禁止水平/垂直的静态构图
  - **对抗细节平均化**: 几何块状大小必须有 3:1 以上的对比比，禁止等大几何排列

---

### VCA-ART-003: 瑞士风格（Swiss Style）

- **原子 ID**: VCA-ART-003
- **风格描述**: 网格驱动，无衬线字体，不对称布局，灵感来自 Josef Müller-Brockmann 的海报设计。核心视觉特征是"网格即秩序"——所有元素严格对齐到网格系统，无衬线字体（Helvetica/Akzidenz-Grotesk）传递客观理性，不对称布局创造动态张力。
- **配色方案**:
  - 主色: `#1A1A1A`（墨黑）
  - 辅色: `#E63946`（瑞士红）
  - 强调色: `#006BA6`（数据蓝）
  - 背景色: `#FFFFFF`（纯白，瑞士风格允许纯白背景）
  - 文本色: `#1A1A1A`
- **生成代码模板**:
  ```svg
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600">
    <!-- 瑞士风格：网格驱动 + 不对称布局 -->
    <rect width="800" height="600" fill="#FFFFFF"/>
    <!-- 网格辅助线（极淡） -->
    <g stroke="#E5E5E5" stroke-width="0.5" opacity="0.5">
      <line x1="100" y1="0" x2="100" y2="600"/>
      <line x1="400" y1="0" x2="400" y2="600"/>
      <line x1="700" y1="0" x2="700" y2="600"/>
      <line x1="0" y1="150" x2="800" y2="150"/>
      <line x1="0" y1="450" x2="800" y2="450"/>
    </g>
    <!-- 大字标题（左对齐，跨网格） -->
    <text x="100" y="200" font-family="Helvetica, Arial, sans-serif" font-size="72" font-weight="bold" fill="#1A1A1A">SWISS</text>
    <text x="100" y="270" font-family="Helvetica, Arial, sans-serif" font-size="72" font-weight="bold" fill="#E63946">STYLE</text>
    <!-- 不对称色块 -->
    <rect x="400" y="350" width="300" height="100" fill="#006BA6"/>
    <!-- 小字说明（网格对齐） -->
    <text x="100" y="500" font-family="Helvetica, Arial, sans-serif" font-size="14" fill="#1A1A1A">Grid-Driven Design / Müller-Brockmann</text>
    <text x="100" y="520" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#6B7280">International Typographic Style, 1950s</text>
  </svg>
  ```
- **适用场景**: 设计系统文档、国际主义风格文章、Müller-Brockmann 风格海报、科技产品规范
- **与 DLP 对接规则**: 映射到 `visual_dna.grid_system` 的网格系统（强制 12 列栅格）+ `visual_dna.font_scheme` 的无衬线字体族。当 `design_language == "科技前沿"` 时优先匹配此原子。与 DLP-linear（Linear App）和 DLP-gov-uk（GOV.UK Design System）的网格驱动基因兼容。字体强制映射到 Helvetica/Arial 无衬线栈。
- **反 AI 廉价感要点**:
  - **对抗过度平滑**: 网格线必须可见（opacity 0.3-0.5），AI 倾向于隐藏网格，此处强制显化网格
  - **对抗配色同质化**: 瑞士红 `#E63946` 为标志性色彩，禁止替换为 AI 常见的"柔和红"
  - **对抗构图模板化**: 不对称布局为硬性约束，标题左对齐 + 色块右下角，禁止居中对称
  - **对抗细节平均化**: 字号必须有 6:1 以上的对比比（72px 标题 vs 12px 说明），禁止等大文字排列

---

### VCA-ART-004: 孟菲斯（Memphis）

- **原子 ID**: VCA-ART-004
- **风格描述**: 鲜艳色彩，几何图案混搭，打破常规，灵感来自 Ettore Sottsass 的 Memphis Group。核心视觉特征是"反叛拼贴"——波点/锯齿/不规则几何混搭，高饱和撞色，刻意打破网格秩序，传递 1980s 的玩乐与反叛精神。
- **配色方案**:
  - 主色: `#FF6B6B`（珊瑚红）
  - 辅色: `#4ECDC4`（薄荷绿）
  - 强调色: `#FFE66D`（明黄）
  - 背景色: `#F0F0F0`（浅灰）
  - 文本色: `#1A1A1A`
  - 补充色: `#A06CD5`（紫罗兰）、`#6C5CE7`（靛蓝）
- **生成代码模板**:
  ```svg
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600">
    <!-- 孟菲斯：几何混搭 + 撞色 -->
    <rect width="800" height="600" fill="#F0F0F0"/>
    <!-- 波点图案 -->
    <pattern id="dots" x="0" y="0" width="30" height="30" patternUnits="userSpaceOnUse">
      <circle cx="15" cy="15" r="4" fill="#4ECDC4"/>
    </pattern>
    <rect x="50" y="50" width="200" height="150" fill="url(#dots)"/>
    <!-- 锯齿三角形 -->
    <polygon points="350,100 450,100 400,200" fill="#FFE66D"/>
    <polygon points="350,200 450,200 400,300" fill="#FF6B6B"/>
    <!-- 不规则圆形 -->
    <ellipse cx="650" cy="150" rx="80" ry="60" fill="#A06CD5" transform="rotate(20 650 150)"/>
    <!-- 锯齿线条 -->
    <polyline points="100,350 150,300 200,350 250,300 300,350 350,300 400,350" fill="none" stroke="#6C5CE7" stroke-width="4"/>
    <!-- 混搭几何 -->
    <rect x="500" y="350" width="120" height="120" fill="#FF6B6B" transform="rotate(15 560 410)"/>
    <circle cx="700" cy="450" r="50" fill="#4ECDC4"/>
    <!-- 孟菲斯文字 -->
    <text x="50" y="550" font-family="Courier New, monospace" font-size="24" fill="#1A1A1A" font-weight="bold">MEMPHIS STYLE</text>
  </svg>
  ```
- **适用场景**: 创意设计文章、1980s 复古主题、玩乐品牌介绍、青年文化内容
- **与 DLP 对接规则**: 映射到 `visual_dna.color_scheme` 的多色板（突破五色板限制，允许 6-7 色）。当 `content_theme` 含"创意/设计/艺术/复古/玩乐"关键词且 `target_audience == "youth"` 时优先匹配此原子。与 DLP-ted（TED 演讲幻灯片）的活泼基因部分兼容。字体映射到等宽字体族（Courier New），传递复古感。
- **反 AI 廉价感要点**:
  - **对抗过度平滑**: 几何边缘必须保留"手工感"——轻微旋转（5°-20°）和偏移，禁止完美对齐
  - **对抗配色同质化**: 强制撞色（珊瑚红+薄荷绿+明黄），禁止 AI 常见的"同色系渐变"
  - **对抗构图模板化**: 几何元素必须"散落式"分布，禁止网格对齐，刻意制造视觉混乱
  - **对抗细节平均化**: 图案混搭为硬性约束（波点+锯齿+圆形+矩形至少 4 种），禁止单一图案重复

---

### VCA-ART-005: 包豪斯（Bauhaus）

- **原子 ID**: VCA-ART-005
- **风格描述**: 基本几何形（圆/三角/方），原色（红黄蓝），功能主义，灵感来自 Walter Gropius 的 Bauhaus 学院。核心视觉特征是"几何即功能"——圆/三角/方三种基本几何形代表宇宙的基本形态，红/黄/蓝三原色代表色彩的纯粹本质，形式追随功能。
- **配色方案**:
  - 主色: `#E63946`（包豪斯红）
  - 辅色: `#F4D35E`（包豪斯黄）
  - 强调色: `#1D3557`（包豪斯蓝）
  - 背景色: `#F5F1E8`（米白，模拟包豪斯纸张）
  - 文本色: `#1A1A1A`
- **生成代码模板**:
  ```svg
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600">
    <!-- 包豪斯：基本几何 + 三原色 -->
    <rect width="800" height="600" fill="#F5F1E8"/>
    <!-- 圆形（蓝） -->
    <circle cx="250" cy="250" r="120" fill="#1D3557"/>
    <!-- 三角形（黄） -->
    <polygon points="550,150 700,400 400,400" fill="#F4D35E"/>
    <!-- 正方形（红） -->
    <rect x="300" y="420" width="160" height="160" fill="#E63946"/>
    <!-- 几何叠加（半透明） -->
    <circle cx="550" cy="450" r="80" fill="#1D3557" opacity="0.3"/>
    <!-- 包豪斯文字 -->
    <text x="100" y="550" font-family="Futura, Century Gothic, sans-serif" font-size="20" fill="#1A1A1A" font-weight="bold" letter-spacing="3">BAUHAUS 1919</text>
  </svg>
  ```
- **适用场景**: 设计教育内容、包豪斯学派介绍、几何美学文章、现代主义设计史
- **与 DLP 对接规则**: 映射到 `visual_dna.color_scheme` 的三原色板（红/黄/蓝）。当 `content_theme` 含"设计/教育/几何/现代主义/包豪斯"关键词时优先匹配此原子。与 DLP-ted（TED 演讲幻灯片）的几何基因兼容。字体映射到 Futura/Century Gothic 几何无衬线栈，传递包豪斯的几何美学。
- **反 AI 廉价感要点**:
  - **对抗过度平滑**: 几何形边缘添加微妙的纸张纹理叠加，模拟 1920s 印刷质感
  - **对抗配色同质化**: 严格限制三原色（红/黄/蓝），禁止 AI 添加"过渡色"或"调和色"
  - **对抗构图模板化**: 三种几何形必须分散分布且部分重叠，禁止等距排列
  - **对抗细节平均化**: 几何形大小必须有明显对比（大圆+中三角+小方），禁止等大几何排列

---

### VCA-ART-006: 装饰艺术（Art Deco）

- **原子 ID**: VCA-ART-006
- **风格描述**: 对称几何，金色/深色，奢华感，灵感来自 Chrysler Building 的装饰艺术建筑。核心视觉特征是"几何奢华"——对称的放射状/扇形/阶梯几何，金色与深色的强对比，传递 1920s 的奢华与摩登。
- **配色方案**:
  - 主色: `#D4AF37`（装饰金）
  - 辅色: `#1A1A1A`（深黑）
  - 强调色: `#8B0000`（深红）
  - 背景色: `#1A1A1A`（深黑背景）
  - 文本色: `#D4AF37`
- **生成代码模板**:
  ```svg
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600">
    <!-- 装饰艺术：对称几何 + 金黑对比 -->
    <rect width="800" height="600" fill="#1A1A1A"/>
    <!-- 放射状对称几何（中心轴 x=400） -->
    <g fill="#D4AF37">
      <!-- 中心扇形 -->
      <path d="M 400 300 L 300 150 A 200 200 0 0 1 500 150 Z"/>
      <!-- 阶梯几何（左） -->
      <polygon points="200,400 300,400 300,350 350,350 350,300 200,300"/>
      <!-- 阶梯几何（右，镜像） -->
      <polygon points="600,400 500,400 500,350 450,350 450,300 600,300"/>
      <!-- 顶部放射线 -->
      <line x1="400" y1="300" x2="400" y2="100" stroke="#D4AF37" stroke-width="2"/>
      <line x1="400" y1="300" x2="300" y2="120" stroke="#D4AF37" stroke-width="2"/>
      <line x1="400" y1="300" x2="500" y2="120" stroke="#D4AF37" stroke-width="2"/>
    </g>
    <!-- 深红强调 -->
    <circle cx="400" cy="300" r="20" fill="#8B0000"/>
    <!-- 装饰艺术文字（对称） -->
    <text x="400" y="500" font-family="Didot, Bodoni, serif" font-size="28" fill="#D4AF37" text-anchor="middle" letter-spacing="8">ART DECO</text>
    <text x="400" y="530" font-family="Didot, Bodoni, serif" font-size="12" fill="#D4AF37" text-anchor="middle" letter-spacing="4">1925 · CHRYSLER</text>
  </svg>
  ```
- **适用场景**: 奢侈品牌内容、1920s 主题文章、建筑美学介绍、高端产品封面
- **与 DLP 对接规则**: 映射到 `visual_dna.color_scheme` 的金黑配色（主色 `#D4AF37` + 背景色 `#1A1A1A`）。当 `content_theme` 含"奢华/高端/复古/建筑/装饰"关键词且 `aesthetic_level == "L3-沉浸"` 时优先匹配此原子。与 DLP-aesop（Aesop 官网）的高端基因部分兼容。字体映射到 Didot/Bodoni 衬线栈，传递奢华感。
- **反 AI 廉价感要点**:
  - **对抗过度平滑**: 金色几何边缘添加微妙的渐变（`#D4AF37` → `#B8860B`），模拟金属质感，避免 AI 的"扁平金色"
  - **对抗配色同质化**: 金黑对比为硬性约束，禁止 AI 添加"柔和过渡色"
  - **对抗构图模板化**: 强制对称构图（中心轴 x=400），但对称内部必须有放射状/阶梯状的复杂几何，禁止简单对称
  - **对抗细节平均化**: 放射线/阶梯/扇形至少 3 种几何元素组合，禁止单一几何重复

---

### VCA-ART-007: 野兽派（Brutalism）

- **原子 ID**: VCA-ART-007
- **风格描述**: 粗糙纹理，高对比，原始感，灵感来自 Le Corbusier 的 béton brut（清水混凝土）建筑。核心视觉特征是"粗野真实"——暴露的材质纹理（混凝土/钢材），高对比的黑白排版，刻意粗糙的边缘，反装饰的功能主义极致。
- **配色方案**:
  - 主色: `#1A1A1A`（混凝土黑）
  - 辅色: `#A8A8A8`（混凝土灰）
  - 强调色: `#FF4500`（警示橙，仅用于关键强调）
  - 背景色: `#C8C8C8`（清水混凝土色）
  - 文本色: `#1A1A1A`
- **生成代码模板**:
  ```svg
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600">
    <!-- 野兽派：粗糙纹理 + 高对比 -->
    <defs>
      <!-- 混凝土纹理滤镜 -->
      <filter id="concrete">
        <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="3" result="noise"/>
        <feColorMatrix in="noise" type="matrix" values="0 0 0 0 0.78 0 0 0 0 0.78 0 0 0 0 0.78 0 0 0 0.3 0"/>
        <feComposite operator="in" in2="SourceGraphic"/>
      </filter>
    </defs>
    <!-- 混凝土背景 -->
    <rect width="800" height="600" fill="#C8C8C8" filter="url(#concrete)"/>
    <!-- 粗野大字标题（左对齐，无修饰） -->
    <text x="50" y="200" font-family="Courier New, monospace" font-size="96" font-weight="bold" fill="#1A1A1A">BRUTAL</text>
    <!-- 粗糙分割线 -->
    <rect x="50" y="250" width="700" height="8" fill="#1A1A1A"/>
    <!-- 警示橙强调块 -->
    <rect x="50" y="300" width="200" height="60" fill="#FF4500"/>
    <text x="60" y="340" font-family="Courier New, monospace" font-size="20" fill="#1A1A1A" font-weight="bold">RAW</text>
    <!-- 粗野正文（等宽字体） -->
    <text x="50" y="450" font-family="Courier New, monospace" font-size="14" fill="#1A1A1A">BÉTON BRUT · LE CORBUSIER · 1952</text>
    <text x="50" y="470" font-family="Courier New, monospace" font-size="14" fill="#A8A8A8">UNITÉ D'HABITATION · MARSEILLE</text>
  </svg>
  ```
- **适用场景**: 建筑设计文章、野兽派美学介绍、反装饰主义内容、Web Brutalism 设计
- **与 DLP 对接规则**: 映射到 `visual_dna.color_scheme` 的灰阶配色（主色 `#1A1A1A` + 背景色 `#C8C8C8`）。当 `content_theme` 含"建筑/野兽派/粗野/混凝土/反装饰"关键词时优先匹配此原子。与 DLP-gov-uk（GOV.UK Design System）的功能主义基因部分兼容。字体映射到 Courier New 等宽栈，传递粗野感。
- **反 AI 廉价感要点**:
  - **对抗过度平滑**: 强制使用 `feTurbulence` 噪点滤镜模拟混凝土纹理，AI 倾向于平滑背景，此处强制粗糙
  - **对抗配色同质化**: 灰阶为主 + 单一警示橙强调，禁止 AI 添加"温暖色调"
  - **对抗构图模板化**: 大字标题左对齐 + 粗糙分割线，禁止圆角/阴影/渐变
  - **对抗细节平均化**: 字号对比极端（96px 标题 vs 14px 正文），禁止中等字号填充

---

### VCA-ART-008: 未来主义（Futurism）

- **原子 ID**: VCA-ART-008
- **风格描述**: 动态线条，速度感，金属色，灵感来自 Boccioni 的"独特形式的连续性"雕塑。核心视觉特征是"动态速度"——斜线/放射线表达运动，金属银/铬色传递机械感，重复线条制造速度模糊，传递 1910s 对速度与机械的崇拜。
- **配色方案**:
  - 主色: `#C0C0C0`（金属银）
  - 辅色: `#1A1A1A`（机械黑）
  - 强调色: `#FF6600`（速度橙）
  - 背景色: `#2C2C2C`（深灰，机械感）
  - 文本色: `#C0C0C0`
- **生成代码模板**:
  ```svg
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600">
    <!-- 未来主义：动态线条 + 金属色 -->
    <rect width="800" height="600" fill="#2C2C2C"/>
    <!-- 速度线（重复斜线） -->
    <g stroke="#C0C0C0" stroke-width="2" opacity="0.6">
      <line x1="0" y1="600" x2="400" y2="0"/>
      <line x1="100" y1="600" x2="500" y2="0"/>
      <line x1="200" y1="600" x2="600" y2="0"/>
      <line x1="300" y1="600" x2="700" y2="0"/>
      <line x1="400" y1="600" x2="800" y2="0"/>
    </g>
    <!-- 金属银几何（动态形态） -->
    <polygon points="300,300 500,200 600,350 450,450 250,400" fill="#C0C0C0" opacity="0.8"/>
    <!-- 速度橙强调线 -->
    <line x1="100" y1="500" x2="700" y2="100" stroke="#FF6600" stroke-width="4"/>
    <!-- 重复三角形（速度模糊） -->
    <g fill="#C0C0C0" opacity="0.4">
      <polygon points="500,200 540,180 520,240"/>
      <polygon points="540,180 580,160 560,220"/>
      <polygon points="580,160 620,140 600,200"/>
    </g>
    <!-- 未来主义文字（倾斜，速度感） -->
    <text x="100" y="550" font-family="Impact, sans-serif" font-size="36" fill="#C0C0C0" transform="rotate(-10 100 550)" font-weight="bold">FUTURISMO</text>
  </svg>
  ```
- **适用场景**: 科技前沿文章、速度/运动主题、机械美学介绍、未来主义艺术史
- **与 DLP 对接规则**: 映射到 `visual_dna.color_scheme` 的金属配色（主色 `#C0C0C0` + 背景色 `#2C2C2C`）。当 `content_theme` 含"未来/科技/速度/机械/运动"关键词且 `design_language == "科技前沿"` 时优先匹配此原子。与 DLP-linear（Linear App）的科技基因部分兼容。动效参数映射到 `visual_dna.motion_profile`，强制使用速度感动效（斜向滑入）。
- **反 AI 廉价感要点**:
  - **对抗过度平滑**: 金属银几何添加渐变（`#C0C0C0` → `#808080`），模拟金属反射，避免 AI 的"扁平银色"
  - **对抗配色同质化**: 金属银+机械黑+速度橙为硬性约束，禁止 AI 添加"柔和蓝紫"
  - **对抗构图模板化**: 强制斜线构图（-10° 到 -45°），禁止水平/垂直静态构图
  - **对抗细节平均化**: 速度线必须有疏密变化（左侧密集，右侧稀疏），禁止等距排列

---

### VCA-ART-009: 达达主义（Dadaism）

- **原子 ID**: VCA-ART-009
- **风格描述**: 拼贴风格，随机排版，反传统，灵感来自 Hannah Höch 的 photomontage 拼贴艺术。核心视觉特征是"反叛拼贴"——看似随机的图文拼贴，打破排版规则，刻意制造视觉冲突，传递 1916s 的反战与反传统精神。
- **配色方案**:
  - 主色: `#1A1A1A`（墨黑）
  - 辅色: `#F5E6D3`（旧报纸黄）
  - 强调色: `#CC0000`（达达红）
  - 背景色: `#E8E0D0`（泛黄纸）
  - 文本色: `#1A1A1A`
- **生成代码模板**:
  ```svg
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600">
    <!-- 达达主义：拼贴风格 + 随机排版 -->
    <rect width="800" height="600" fill="#E8E0D0"/>
    <!-- 拼贴元素（随机角度/位置） -->
    <g transform="rotate(-8 200 150)">
      <rect x="100" y="100" width="200" height="120" fill="#F5E6D3" stroke="#1A1A1A" stroke-width="1"/>
      <text x="110" y="140" font-family="Times New Roman, serif" font-size="24" fill="#1A1A1A">DADA</text>
      <text x="110" y="170" font-family="Times New Roman, serif" font-size="14" fill="#1A1A1A">anti-art</text>
    </g>
    <!-- 随机文字块（倾斜） -->
    <g transform="rotate(15 500 200)">
      <rect x="420" y="150" width="180" height="80" fill="#CC0000"/>
      <text x="430" y="200" font-family="Impact, sans-serif" font-size="28" fill="#F5E6D3">CUT</text>
    </g>
    <!-- 拼贴碎片（不规则） -->
    <polygon points="300,350 450,320 420,450 280,430" fill="#1A1A1A" opacity="0.8"/>
    <polygon points="500,380 650,360 630,480 480,470" fill="#F5E6D3" stroke="#1A1A1A" stroke-width="2"/>
    <!-- 随机文字（多角度） -->
    <text x="350" y="400" font-family="Courier New, monospace" font-size="18" fill="#F5E6D3" transform="rotate(-20 350 400)">collage</text>
    <text x="550" y="420" font-family="Times New Roman, serif" font-size="22" fill="#1A1A1A" transform="rotate(10 550 420)">1916</text>
    <!-- 达达主义签名 -->
    <text x="100" y="550" font-family="Courier New, monospace" font-size="12" fill="#1A1A1A">HÖCH · HAUSMANN · 1919</text>
  </svg>
  ```
- **适用场景**: 艺术史文章、反传统主题、拼贴艺术介绍、实验性设计内容
- **与 DLP 对接规则**: 映射到 `visual_dna.color_scheme` 的旧纸配色（主色 `#1A1A1A` + 背景色 `#E8E0D0`）。当 `content_theme` 含"达达/拼贴/反传统/实验/前卫"关键词时优先匹配此原子。字体映射到混合字体栈（Times New Roman + Impact + Courier New），传递拼贴感。
- **反 AI 廉价感要点**:
  - **对抗过度平滑**: 拼贴元素边缘添加不规则裁切（`clip-path`），模拟剪刀裁剪质感
  - **对抗配色同质化**: 旧报纸黄+墨黑+达达红为硬性约束，禁止 AI 添加"现代洁净配色"
  - **对抗构图模板化**: 强制随机角度（-20° 到 +15°）和随机位置，禁止网格对齐
  - **对抗细节平均化**: 拼贴元素大小/角度/字体必须各不相同，禁止统一化处理

---

### VCA-ART-010: 极简几何（Minimal Geometry）

- **原子 ID**: VCA-ART-010
- **风格描述**: 纯粹几何，渐变色，现代感，灵感来自 Carlos Cruz-Diez 的色彩动力学艺术。核心视觉特征是"几何渐变"——纯粹几何形（圆/线/带）配合 HSL 色彩空间渐变，创造视觉振动与色彩流动感，传递现代主义的色彩探索。
- **配色方案**:
  - 主色: `#6366F1`（靛蓝渐变起点）
  - 辅色: `#EC4899`（粉红渐变终点）
  - 强调色: `#10B981`（翠绿，对比色）
  - 背景色: `#0F172A`（深蓝黑，渐变背景）
  - 文本色: `#F8FAFC`
- **生成代码模板**:
  ```svg
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600">
    <!-- 极简几何：纯粹几何 + HSL渐变 -->
    <defs>
      <!-- HSL色彩空间渐变（靛蓝→粉红） -->
      <linearGradient id="geoGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#6366F1"/>
        <stop offset="50%" stop-color="#8B5CF6"/>
        <stop offset="100%" stop-color="#EC4899"/>
      </linearGradient>
      <!-- 翠绿对比渐变 -->
      <linearGradient id="geoGrad2" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#10B981"/>
        <stop offset="100%" stop-color="#059669"/>
      </linearGradient>
    </defs>
    <!-- 深蓝黑背景 -->
    <rect width="800" height="600" fill="#0F172A"/>
    <!-- 渐变几何带（Cruz-Diez 风格） -->
    <rect x="100" y="100" width="300" height="400" fill="url(#geoGrad1)" opacity="0.9"/>
    <!-- 翠绿对比线 -->
    <rect x="500" y="150" width="8" height="300" fill="url(#geoGrad2)"/>
    <!-- 渐变圆形 -->
    <circle cx="650" cy="300" r="80" fill="url(#geoGrad1)" opacity="0.7"/>
    <!-- 极简文字 -->
    <text x="100" y="550" font-family="Space Grotesk, sans-serif" font-size="14" fill="#F8FAFC" letter-spacing="4">CRUZ-DIEZ · COLOR DYNAMICS</text>
  </svg>
  ```
- **适用场景**: 现代艺术文章、色彩理论介绍、科技产品封面、L3-沉浸审美等级场景
- **与 DLP 对接规则**: 映射到 `visual_dna.color_scheme` 的渐变色板（主色 `#6366F1` + 辅色 `#EC4899`）。当 `content_theme` 含"色彩/几何/渐变/现代/动力学"关键词且 `aesthetic_level == "L3-沉浸"` 时优先匹配此原子。与 DLP-linear（Linear App）和 DLP-stripe-press（Stripe Press）的现代基因兼容。字体映射到 Space Grotesk 几何无衬线栈。
- **反 AI 廉价感要点**:
  - **对抗过度平滑**: 渐变必须使用 HSL 色彩空间（靛蓝→紫→粉红），禁止 RGB 线性渐变（AI 常见的"塑料渐变"）
  - **对抗配色同质化**: 渐变终点必须为对比色（粉红 vs 翠绿），禁止 AI 常见的"同色系渐变"
  - **对抗构图模板化**: 几何形必须有重叠/部分裁切，禁止完整居中排列
  - **对抗细节平均化**: 渐变带+对比线+渐变圆至少 3 种几何组合，禁止单一几何重复

---

## 二、生成式艺术原子（VCA-GEN）

> **融入来源**: algorithmic-art-skill — 极简几何、生成纹理、高级渐变
> **DLP 对接**: 每个生成式艺术原子映射到 `visual_dna.color_scheme` 的配色方案，由 Taste-Skill 根据 `aesthetic_level` 选择生成式艺术的复杂度参数。
> **风格先锋不油腻**: 所有生成式艺术原子遵循克制装饰原则，默认参数经过审美校准。

### VCA-GEN-001: 流场（Flow Field）

- **原子 ID**: VCA-GEN-001
- **风格描述**: 基于 Perlin 噪声的粒子流场，柔和曲线，适合背景。核心生成原理是在 2D 空间中生成 Perlin 噪声场，粒子沿噪声场的梯度方向流动，形成柔和的流线轨迹。流场密度可控，低密度适合背景，高密度适合主视觉。
- **配色方案**:
  - 主色: `#6366F1`（靛蓝，流线主色）
  - 辅色: `#EC4899`（粉红，流线辅色）
  - 强调色: `#10B981`（翠绿，高亮流线）
  - 背景色: `#0F172A`（深蓝黑）
  - 文本色: `#F8FAFC`
- **生成代码模板**:
  ```python
  # Matplotlib 流场生成模板
  import numpy as np
  import matplotlib.pyplot as plt
  from matplotlib.collections import LineCollection

  # 参数配置（审美校准默认值）
  width, height = 800, 600
  num_particles = 500        # 粒子数（低密度=背景，高密度=主视觉）
  num_steps = 100            # 流动步数
  noise_scale = 0.005        # 噪声频率（越小越柔和）
  line_width = 0.5           # 线宽（克制装饰）
  alpha = 0.3                # 透明度（叠加效果）

  # 配色（HSL色彩空间）
  colors = ['#6366F1', '#EC4899', '#10B981']
  bg_color = '#0F172A'

  # 生成 Perlin 噪声场（简化实现）
  def perlin_noise(x, y, seed=42):
      np.random.seed(seed)
      return np.sin(x * noise_scale) * np.cos(y * noise_scale) * np.pi

  # 粒子流动
  fig, ax = plt.subplots(figsize=(8, 6), facecolor=bg_color)
  ax.set_facecolor(bg_color)

  for i in range(num_particles):
      x, y = np.random.uniform(0, width), np.random.uniform(0, height)
      xs, ys = [x], [y]
      for _ in range(num_steps):
          angle = perlin_noise(x, y) * 2 * np.pi
          x += np.cos(angle) * 2
          y += np.sin(angle) * 2
          xs.append(x)
          ys.append(y)
      color = colors[i % len(colors)]
      ax.plot(xs, ys, color=color, linewidth=line_width, alpha=alpha)

  ax.set_xlim(0, width)
  ax.set_ylim(0, height)
  ax.axis('off')
  plt.savefig('flow_field.png', dpi=150, bbox_inches='tight', facecolor=bg_color)
  plt.close()
  ```
- **Canvas 实现模板**（动态向量场，体现粒子沿 Perlin 噪声梯度流动 + 渐隐轨迹）:
  ```html
  <!DOCTYPE html>
  <html lang="zh-CN">
  <head><meta charset="UTF-8"><title>VCA-GEN-001 流场 Canvas 实现</title></head>
  <body>
  <canvas id="flowField" width="800" height="600"></canvas>
  <script>
  // 参数配置区（审美校准默认值）
  const config = {
    width: 800, height: 600,
    numParticles: 500,      // 粒子数（克制装饰，≤2000）
    noiseScale: 0.005,      // 噪声频率（越小越柔和）
    stepSize: 2,            // 流动步长
    lineWidth: 0.5,         // 线宽（≤0.5px 避免油腻）
    alpha: 0.3,             // 透明度（≤0.3）
    fadeAlpha: 0.04,        // 轨迹渐隐速度
    colors: ['#6366F1', '#EC4899', '#10B981'],  // 3 色限制
    bgColor: '#0F172A'
  };
  const canvas = document.getElementById('flowField');
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = config.bgColor;
  ctx.fillRect(0, 0, config.width, config.height);

  // Perlin 噪声向量场（基于正余弦梯度插值）
  function flowAngle(x, y, t) {
    return (Math.sin(x * config.noiseScale + t) +
            Math.cos(y * config.noiseScale * 1.3 + t * 0.7)) * Math.PI;
  }

  // 粒子初始化
  const particles = [];
  for (let i = 0; i < config.numParticles; i++) {
    particles.push({
      x: Math.random() * config.width,
      y: Math.random() * config.height,
      color: config.colors[i % config.colors.length]
    });
  }

  let time = 0;
  function animate() {
    // 渐隐轨迹：半透明背景叠加形成拖尾
    ctx.fillStyle = `rgba(15, 23, 42, ${config.fadeAlpha})`;
    ctx.fillRect(0, 0, config.width, config.height);
    time += 0.005;
    particles.forEach(p => {
      const angle = flowAngle(p.x, p.y, time);
      const px = p.x, py = p.y;
      p.x += Math.cos(angle) * config.stepSize;
      p.y += Math.sin(angle) * config.stepSize;
      // 边界回绕
      if (p.x < 0 || p.x > config.width || p.y < 0 || p.y > config.height) {
        p.x = Math.random() * config.width;
        p.y = Math.random() * config.height;
        return;
      }
      ctx.strokeStyle = p.color;
      ctx.globalAlpha = config.alpha;
      ctx.lineWidth = config.lineWidth;
      ctx.beginPath();
      ctx.moveTo(px, py);
      ctx.lineTo(p.x, p.y);
      ctx.stroke();
    });
    ctx.globalAlpha = 1;
    requestAnimationFrame(animate);
  }
  animate();
  </script>
  </body>
  </html>
  ```
- **适用场景**: 文章背景纹理、封面装饰、数据可视化背景、L3-沉浸审美等级场景
- **与 DLP 对接规则**: 映射到 `visual_dna.color_scheme` 的主色/辅色/强调色作为流线颜色。当 `aesthetic_level == "L3-沉浸"` 时优先匹配此原子作为背景纹理。粒子数参数映射到 `visual_dna.grid_system` 的信息密度——L1 用 200 粒子（极淡背景）、L2 用 500 粒子（标准背景）、L3 用 1000 粒子（主视觉）。与 DLP-plotivy（Plotly 美学模板）的数据可视化基因兼容。
- **风格先锋不油腻要点**:
  - 线宽强制 ≤ 0.5px，透明度 ≤ 0.3，避免"油腻"的粗线叠加
  - 粒子数默认 500（克制装饰），禁止超过 2000（过度装饰）
  - 配色限制 3 色，禁止多色流场

---

### VCA-GEN-002: 粒子系统（Particle System）

- **原子 ID**: VCA-GEN-002
- **风格描述**: 粒子聚集/分散动画，适合数据可视化。核心生成原理是模拟粒子在引力/斥力场中的运动，粒子可聚集为簇或分散为云，形成动态的视觉焦点。适合作为数据可视化的动态背景或交互式数据点的视觉增强。
- **配色方案**:
  - 主色: `#3B82F6`（数据蓝，粒子主色）
  - 辅色: `#F59E0B`（琥珀色，高亮粒子）
  - 强调色: `#EF4444`（红色，异常粒子）
  - 背景色: `#1E293B`（深石板灰）
  - 文本色: `#F1F5F9`
- **生成代码模板**:
  ```svg
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600">
    <!-- 粒子系统：聚集/分散 -->
    <rect width="800" height="600" fill="#1E293B"/>
    <!-- 粒子簇（聚集态） -->
    <g fill="#3B82F6" opacity="0.7">
      <circle cx="400" cy="300" r="3"/>
      <circle cx="395" cy="295" r="2.5"/>
      <circle cx="405" cy="305" r="2.5"/>
      <circle cx="390" cy="310" r="2"/>
      <circle cx="410" cy="290" r="2"/>
      <circle cx="385" cy="300" r="1.5"/>
      <circle cx="415" cy="300" r="1.5"/>
      <circle cx="400" cy="285" r="1.5"/>
      <circle cx="400" cy="315" r="1.5"/>
    </g>
    <!-- 分散粒子 -->
    <g fill="#3B82F6" opacity="0.4">
      <circle cx="200" cy="150" r="2"/>
      <circle cx="600" cy="180" r="2"/>
      <circle cx="150" cy="450" r="1.5"/>
      <circle cx="650" cy="480" r="1.5"/>
      <circle cx="300" cy="100" r="1"/>
      <circle cx="500" cy="500" r="1"/>
    </g>
    <!-- 高亮粒子（琥珀色） -->
    <g fill="#F59E0B" opacity="0.9">
      <circle cx="400" cy="300" r="4"/>
      <circle cx="250" cy="200" r="2.5"/>
      <circle cx="550" cy="400" r="2.5"/>
    </g>
    <!-- 异常粒子（红色） -->
    <circle cx="700" cy="120" r="3" fill="#EF4444" opacity="0.8"/>
    <!-- 粒子连线（极淡） -->
    <g stroke="#3B82F6" stroke-width="0.3" opacity="0.2">
      <line x1="400" y1="300" x2="250" y2="200"/>
      <line x1="400" y1="300" x2="550" y2="400"/>
    </g>
  </svg>
  ```
- **Canvas 实现模板**（动态粒子系统，体现粒子聚集/分散动画 + 生命周期）:
  ```html
  <!DOCTYPE html>
  <html lang="zh-CN">
  <head><meta charset="UTF-8"><title>VCA-GEN-002 粒子系统 Canvas 实现</title></head>
  <body>
  <canvas id="particleSystem" width="800" height="600"></canvas>
  <script>
  // 参数配置区
  const config = {
    width: 800, height: 600,
    numParticles: 150,      // 粒子数
    maxLife: 200,           // 生命周期
    attractStrength: 0.05,  // 引力强度
    repelRadius: 80,        // 斥力半径（聚集/分散切换）
    particleRadius: 2.5,    // 粒子半径（≤4px）
    bgColor: '#1E293B',
    mainColor: '#3B82F6',
    highlightColor: '#F59E0B',
    exceptionColor: '#EF4444'
  };
  const canvas = document.getElementById('particleSystem');
  const ctx = canvas.getContext('2d');
  const centerX = config.width / 2;
  const centerY = config.height / 2;

  // 粒子类：含位置/速度/生命周期
  class Particle {
    constructor() { this.reset(); }
    reset() {
      this.x = centerX + (Math.random() - 0.5) * 20;
      this.y = centerY + (Math.random() - 0.5) * 20;
      this.vx = (Math.random() - 0.5) * 2;
      this.vy = (Math.random() - 0.5) * 2;
      this.life = config.maxLife;
      this.type = Math.random() < 0.1 ? 'highlight' :
                  (Math.random() < 0.05 ? 'exception' : 'main');
    }
    update() {
      // 引力指向中心，形成聚集/分散动态
      const dx = centerX - this.x;
      const dy = centerY - this.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist > config.repelRadius) {
        this.vx += (dx / dist) * config.attractStrength;
        this.vy += (dy / dist) * config.attractStrength;
      } else {
        // 近距离斥力，形成分散
        this.vx -= (dx / dist) * config.attractStrength * 0.5;
        this.vy -= (dy / dist) * config.attractStrength * 0.5;
      }
      this.vx *= 0.96; this.vy *= 0.96; // 阻尼
      this.x += this.vx; this.y += this.vy;
      this.life--;
      if (this.life <= 0) this.reset();
    }
    draw() {
      const color = this.type === 'highlight' ? config.highlightColor :
                    (this.type === 'exception' ? config.exceptionColor : config.mainColor);
      const alpha = Math.min(1, this.life / config.maxLife) * 0.7;
      ctx.fillStyle = color;
      ctx.globalAlpha = alpha;
      ctx.beginPath();
      ctx.arc(this.x, this.y, config.particleRadius, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  const particles = [];
  for (let i = 0; i < config.numParticles; i++) particles.push(new Particle());

  function animate() {
    ctx.fillStyle = `rgba(30, 41, 59, 0.15)`;
    ctx.fillRect(0, 0, config.width, config.height);
    particles.forEach(p => { p.update(); p.draw(); });
    ctx.globalAlpha = 1;
    requestAnimationFrame(animate);
  }
  animate();
  </script>
  </body>
  </html>
  ```
- **适用场景**: 数据可视化背景、交互式数据点、科技产品封面、网络关系图装饰
- **与 DLP 对接规则**: 映射到 `visual_dna.color_scheme` 的主色作为粒子颜色。当 `design_language == "科技前沿"` 时优先匹配此原子。粒子大小参数映射到 `visual_dna.line_style` 的线条粗细——数据线 2px 对应粒子半径 2-3px。与 DLP-plotivy（Plotly 美学模板）和 DLP-scienceplots（SciencePlots 风格）的数据可视化基因兼容。
- **风格先锋不油腻要点**:
  - 粒子半径强制 ≤ 4px，透明度 ≤ 0.7，避免"油腻"的大粒子
  - 连线透明度 ≤ 0.2，避免"蜘蛛网"视觉混乱
  - 配色限制 3 色（主色+高亮+异常），禁止多色粒子

---

### VCA-GEN-003: Voronoi 图（Voronoi Diagram）

- **原子 ID**: VCA-GEN-003
- **风格描述**: 空间分割，有机细胞感，适合封面。核心生成原理是在 2D 空间中随机分布种子点，每个种子点占据其最近邻区域，形成有机的细胞状分割。Voronoi 图的边界自然且不可预测，适合作为封面的几何背景。
- **配色方案**:
  - 主色: `#8B5CF6`（紫罗兰，细胞主色）
  - 辅色: `#06B6D4`（青色，细胞辅色）
  - 强调色: `#F59E0B`（琥珀色，边界高亮）
  - 背景色: `#1E1B4B`（深靛蓝）
  - 文本色: `#E0E7FF`
- **生成代码模板**:
  ```python
  # Matplotlib Voronoi 图生成模板
  import numpy as np
  import matplotlib.pyplot as plt
  from scipy.spatial import Voronoi, voronoi_plot_2d

  # 参数配置
  num_seeds = 25           # 种子点数（克制装饰）
  line_width = 0.8         # 边界线宽
  line_color = '#F59E0B'   # 边界色
  bg_color = '#1E1B4B'

  # 配色（HSL色彩空间）
  cell_colors = ['#8B5CF6', '#06B6D4', '#7C3AED', '#0891B2', '#6D28D9']

  # 生成随机种子点
  np.random.seed(42)
  points = np.random.uniform(0.1, 0.9, size=(num_seeds, 2))

  # 生成 Voronoi 图
  vor = Voronoi(points)
  fig, ax = plt.subplots(figsize=(8, 6), facecolor=bg_color)
  ax.set_facecolor(bg_color)

  # 绘制 Voronoi 区域
  voronoi_plot_2d(vor, ax=ax, show_points=False, show_vertices=False,
                  line_colors=line_color, line_width=line_width,
                  line_alpha=0.6)

  # 填充细胞颜色
  for i, region_idx in enumerate(vor.point_region):
      region = vor.regions[region_idx]
      if -1 not in region and len(region) > 0:
          polygon = [vor.vertices[v] for v in region]
          color = cell_colors[i % len(cell_colors)]
          ax.fill(*zip(*polygon), color=color, alpha=0.3)

  ax.set_xlim(0, 1)
  ax.set_ylim(0, 1)
  ax.axis('off')
  plt.savefig('voronoi.png', dpi=150, bbox_inches='tight', facecolor=bg_color)
  plt.close()
  ```
- **Canvas 实现模板**（动态 Voronoi 图，体现种子点漂移 + 像素级区域划分）:
  ```html
  <!DOCTYPE html>
  <html lang="zh-CN">
  <head><meta charset="UTF-8"><title>VCA-GEN-003 Voronoi 图 Canvas 实现</title></head>
  <body>
  <canvas id="voronoi" width="800" height="600"></canvas>
  <script>
  // 参数配置区
  const config = {
    width: 800, height: 600,
    numSeeds: 25,           // 种子点数（克制装饰，≤50）
    cellColors: ['#8B5CF6', '#06B6D4', '#7C3AED', '#0891B2', '#6D28D9'],
    borderColor: '#F59E0B', // 边界高亮色
    bgColor: '#1E1B4B',
    animateSeeds: true,     // 种子点缓慢漂移
    driftSpeed: 0.3
  };
  const canvas = document.getElementById('voronoi');
  const ctx = canvas.getContext('2d');

  // 种子点初始化（含漂移速度）
  const seeds = [];
  for (let i = 0; i < config.numSeeds; i++) {
    seeds.push({
      x: Math.random() * config.width,
      y: Math.random() * config.height,
      vx: (Math.random() - 0.5) * config.driftSpeed,
      vy: (Math.random() - 0.5) * config.driftSpeed,
      color: config.cellColors[i % config.cellColors.length]
    });
  }

  // 像素级 Voronoi 计算：每个像素找最近种子点
  function drawVoronoi() {
    const imageData = ctx.createImageData(config.width, config.height);
    const data = imageData.data;
    for (let y = 0; y < config.height; y++) {
      for (let x = 0; x < config.width; x++) {
        let minDist = Infinity, secondDist = Infinity, nearest = 0;
        for (let i = 0; i < seeds.length; i++) {
          const dx = x - seeds[i].x, dy = y - seeds[i].y;
          const dist = dx * dx + dy * dy;
          if (dist < minDist) {
            secondDist = minDist; minDist = dist; nearest = i;
          } else if (dist < secondDist) {
            secondDist = dist;
          }
        }
        const hex = seeds[nearest].color.replace('#', '');
        const r = parseInt(hex.substr(0, 2), 16);
        const g = parseInt(hex.substr(2, 2), 16);
        const b = parseInt(hex.substr(4, 2), 16);
        // 边界检测：最近与次近距离接近时绘制边界
        const isEdge = (Math.sqrt(secondDist) - Math.sqrt(minDist)) < 1.5;
        const idx = (y * config.width + x) * 4;
        if (isEdge) {
          data[idx] = 245; data[idx + 1] = 158; data[idx + 2] = 11;
        } else {
          data[idx] = r; data[idx + 1] = g; data[idx + 2] = b;
        }
        data[idx + 3] = 200;
      }
    }
    ctx.fillStyle = config.bgColor;
    ctx.fillRect(0, 0, config.width, config.height);
    ctx.putImageData(imageData, 0, 0);
  }

  function animate() {
    // 种子点漂移
    if (config.animateSeeds) {
      seeds.forEach(s => {
        s.x += s.vx; s.y += s.vy;
        if (s.x < 0 || s.x > config.width) s.vx *= -1;
        if (s.y < 0 || s.y > config.height) s.vy *= -1;
      });
    }
    drawVoronoi();
    requestAnimationFrame(animate);
  }
  animate();
  </script>
  </body>
  </html>
  ```
- **适用场景**: 文章封面、有机几何装饰、空间分割可视化、L3-沉浸审美等级场景
- **与 DLP 对接规则**: 映射到 `visual_dna.color_scheme` 的多色板作为细胞填充色。当 `aesthetic_level == "L3-沉浸"` 时优先匹配此原子作为封面背景。种子点数参数映射到 `visual_dna.grid_system` 的信息密度——L1 用 15 点（极简）、L2 用 25 点（标准）、L3 用 40 点（密集）。与 DLP-nature-figure（Nature 图表规范）的有机几何基因兼容。
- **风格先锋不油腻要点**:
  - 种子点数默认 25（克制装饰），禁止超过 50（过度密集）
  - 细胞填充透明度 ≤ 0.3，避免"色块堆砌"
  - 边界线宽 ≤ 0.8px，避免"粗框油腻"

---

### VCA-GEN-004: Perlin 噪声（Perlin Noise）

- **原子 ID**: VCA-GEN-004
- **风格描述**: 有机纹理生成，适合背景纹理。核心生成原理是 Ken Perlin 发明的梯度噪声算法，生成连续平滑的伪随机纹理。Perlin 噪声的"有机感"源于其多倍频叠加（octaves），每个倍频增加细节层次，模拟自然纹理（云/雾/大理石/地形）。
- **配色方案**:
  - 主色: `#475569`（石板灰，纹理主色）
  - 辅色: `#334155`（深石板灰，纹理暗部）
  - 强调色: `#64748B`（浅石板灰，纹理亮部）
  - 背景色: `#1E293B`（深石板灰背景）
  - 文本色: `#E2E8F0`
- **生成代码模板**:
  ```python
  # Matplotlib Perlin 噪声纹理生成模板
  import numpy as np
  import matplotlib.pyplot as plt

  # 参数配置
  width, height = 800, 600
  scale = 0.02          # 噪声频率（越小越柔和）
  octaves = 4           # 倍频数（越多细节越丰富）
  persistence = 0.5     # 持续度（每倍频振幅衰减）
  lacunarity = 2.0      # 间隙度（每倍频频率增长）

  # 配色（灰阶纹理）
  cmap_colors = ['#1E293B', '#334155', '#475569', '#64748B', '#94A3B8']
  from matplotlib.colors import LinearSegmentedColormap
  cmap = LinearSegmentedColormap.from_list('perlin', cmap_colors)

  # 简化 Perlin 噪声生成
  def perlin_noise_2d(width, height, scale, octaves, persistence, lacunarity, seed=42):
      np.random.seed(seed)
      noise = np.zeros((height, width))
      amplitude = 1.0
      frequency = scale
      for _ in range(octaves):
          x = np.arange(width) * frequency
          y = np.arange(height) * frequency
          xx, yy = np.meshgrid(x, y)
          # 简化：使用正弦函数模拟梯度噪声
          layer = np.sin(xx) * np.cos(yy) + np.sin(xx * 1.3) * np.cos(yy * 1.7) * 0.5
          noise += layer * amplitude
          amplitude *= persistence
          frequency *= lacunarity
      # 归一化到 0-1
      noise = (noise - noise.min()) / (noise.max() - noise.min())
      return noise

  # 生成纹理
  noise = perlin_noise_2d(width, height, scale, octaves, persistence, lacunarity)

  # 绘制
  fig, ax = plt.subplots(figsize=(8, 6), facecolor='#1E293B')
  ax.imshow(noise, cmap=cmap, aspect='auto')
  ax.axis('off')
  plt.savefig('perlin_noise.png', dpi=150, bbox_inches='tight', facecolor='#1E293B')
  plt.close()
  ```
- **Canvas 实现模板**（动态 Perlin 噪声，体现多倍频叠加 + 平滑随机纹理）:
  ```html
  <!DOCTYPE html>
  <html lang="zh-CN">
  <head><meta charset="UTF-8"><title>VCA-GEN-004 Perlin 噪声 Canvas 实现</title></head>
  <body>
  <canvas id="perlinNoise" width="800" height="600"></canvas>
  <script>
  // 参数配置区
  const config = {
    width: 800, height: 600,
    scale: 0.02,            // 噪声频率（越小越柔和）
    octaves: 4,             // 倍频数（≤6 避免过度细节）
    persistence: 0.5,       // 持续度（每倍频振幅衰减）
    lacunarity: 2.0,        // 间隙度（每倍频频率增长）
    timeStep: 0.5,          // 时间步进（动画）
    gradientColors: ['#1E293B', '#334155', '#475569', '#64748B', '#94A3B8']
  };
  const canvas = document.getElementById('perlinNoise');
  const ctx = canvas.getContext('2d');

  // Perlin 噪声梯度表（置换数组 + 梯度向量）
  const perm = new Array(512);
  const gradVec = [];
  for (let i = 0; i < 256; i++) {
    perm[i] = perm[i + 256] = Math.floor(Math.random() * 256);
    const angle = Math.random() * Math.PI * 2;
    gradVec.push([Math.cos(angle), Math.sin(angle)]);
  }
  function fade(t) { return t * t * t * (t * (t * 6 - 15) + 10); }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function dotGrad(gx, gy, x, y) {
    const idx = (perm[gx & 255] + gy) & 255;
    const g = gradVec[idx % gradVec.length];
    return x * g[0] + y * g[1];
  }
  function perlin2D(x, y) {
    const x0 = Math.floor(x), y0 = Math.floor(y);
    const xf = x - x0, yf = y - y0;
    const u = fade(xf), v = fade(yf);
    return lerp(
      lerp(dotGrad(x0, y0, xf, yf), dotGrad(x0 + 1, y0, xf - 1, yf), u),
      lerp(dotGrad(x0, y0 + 1, xf, yf - 1), dotGrad(x0 + 1, y0 + 1, xf - 1, yf - 1), u),
      v
    );
  }

  // 多倍频叠加（fractal Brownian motion）
  function fractalNoise(x, y, t) {
    let total = 0, amplitude = 1, frequency = config.scale, maxVal = 0;
    for (let i = 0; i < config.octaves; i++) {
      total += perlin2D(x * frequency + t, y * frequency) * amplitude;
      maxVal += amplitude;
      amplitude *= config.persistence;
      frequency *= config.lacunarity;
    }
    return (total / maxVal + 1) * 0.5; // 归一化到 0-1
  }

  function hexToRgb(hex) {
    const h = hex.replace('#', '');
    return [parseInt(h.substr(0,2),16), parseInt(h.substr(2,2),16), parseInt(h.substr(4,2),16)];
  }
  const gradRgb = config.gradientColors.map(hexToRgb);
  function colorAt(t) {
    const scaled = t * (gradRgb.length - 1);
    const i = Math.floor(scaled);
    const f = scaled - i;
    const c1 = gradRgb[i], c2 = gradRgb[Math.min(i + 1, gradRgb.length - 1)];
    return [lerp(c1[0],c2[0],f), lerp(c1[1],c2[1],f), lerp(c1[2],c2[2],f)];
  }

  let time = 0;
  function animate() {
    const imageData = ctx.createImageData(config.width, config.height);
    const data = imageData.data;
    for (let y = 0; y < config.height; y++) {
      for (let x = 0; x < config.width; x++) {
        const n = fractalNoise(x, y, time);
        const [r, g, b] = colorAt(n);
        const idx = (y * config.width + x) * 4;
        data[idx] = r; data[idx + 1] = g; data[idx + 2] = b; data[idx + 3] = 255;
      }
    }
    ctx.putImageData(imageData, 0, 0);
    time += config.timeStep;
    requestAnimationFrame(animate);
  }
  animate();
  </script>
  </body>
  </html>
  ```
- **适用场景**: 背景纹理、有机纹理装饰、自然主题文章、L2-标准审美等级场景
- **与 DLP 对接规则**: 映射到 `visual_dna.color_scheme` 的灰阶配色作为纹理色调。当 `aesthetic_level == "L2-标准"` 时优先匹配此原子作为背景纹理。倍频数参数映射到 `visual_dna.grid_system` 的信息密度——L1 用 2 倍频（极简）、L2 用 4 倍频（标准）、L3 用 6 倍频（丰富）。与 DLP-kami（Kami 纸质美学）的有机纹理基因兼容。
- **风格先锋不油腻要点**:
  - 倍频数默认 4（克制装饰），禁止超过 6（过度细节）
  - 纹理透明度 ≤ 0.3（作为背景时），避免"喧宾夺主"
  - 配色限制灰阶 5 色，禁止彩色噪声

---

### VCA-GEN-005: L-system（Lindenmayer System）

- **原子 ID**: VCA-GEN-005
- **风格描述**: 分形植物生成，适合装饰元素。核心生成原理是 Aristid Lindenmayer 提出的形式语法系统，通过字符串重写规则递归生成分形结构。L-system 最经典的用途是生成逼真的植物/树木形态，其自相似的分支结构具有数学美感。
- **配色方案**:
  - 主色: `#16A34A`（植物绿，主干色）
  - 辅色: `#22C55E`（亮绿，分支色）
  - 强调色: `#FACC15`（花黄色，叶尖色）
  - 背景色: `#FDFDFD`（纸白）
  - 文本色: `#1A1A1A`
- **生成代码模板**:
  ```python
  # Matplotlib L-system 分形植物生成模板
  import matplotlib.pyplot as plt
  import numpy as np

  # 参数配置
  iterations = 4         # 迭代次数（克制装饰）
  angle = 25             # 分支角度（度）
  length = 1.0           # 初始线段长度
  length_decay = 0.7     # 长度衰减率

  # 配色
  trunk_color = '#16A34A'
  branch_color = '#22C55E'
  leaf_color = '#FACC15'
  bg_color = '#FDFDFD'

  # L-system 规则（植物）
  rules = {
      'F': 'FF+[+F-F-F]-[-F+F+F]',
      'X': 'F-[[X]+X]+F[+FX]-X'
  }
  axiom = 'X'

  # 生成 L-system 字符串
  def generate_lsystem(axiom, rules, iterations):
      result = axiom
      for _ in range(iterations):
          result = ''.join(rules.get(c, c) for c in result)
      return result

  # 绘制 L-system
  def draw_lsystem(lstring, angle, length, length_decay):
      fig, ax = plt.subplots(figsize=(8, 6), facecolor=bg_color)
      ax.set_facecolor(bg_color)

      x, y = 0, 0
      direction = 90  # 向上
      stack = []
      depths = [0]
      depth = 0

      for char in lstring:
          if char == 'F':
              rad = np.radians(direction)
              new_x = x + length * np.cos(rad)
              new_y = y + length * np.sin(rad)
              color = trunk_color if depth == 0 else (branch_color if depth < 3 else leaf_color)
              lw = 2.0 if depth == 0 else (1.0 if depth < 3 else 0.5)
              ax.plot([x, new_x], [y, new_y], color=color, linewidth=lw, alpha=0.8)
              x, y = new_x, new_y
          elif char == '+':
              direction += angle
          elif char == '-':
              direction -= angle
          elif char == '[':
              stack.append((x, y, direction, length, depth))
              length *= length_decay
              depth += 1
          elif char == ']':
              x, y, direction, length, depth = stack.pop()

      ax.set_aspect('equal')
      ax.axis('off')
      plt.savefig('lsystem.png', dpi=150, bbox_inches='tight', facecolor=bg_color)
      plt.close()

  # 生成并绘制
  lstring = generate_lsystem(axiom, rules, iterations)
  draw_lsystem(lstring, angle, length, length_decay)
  ```
- **Canvas 实现模板**（动态 L-system，体现字符串重写递归 + 逐帧生长动画）:
  ```html
  <!DOCTYPE html>
  <html lang="zh-CN">
  <head><meta charset="UTF-8"><title>VCA-GEN-005 L-system Canvas 实现</title></head>
  <body>
  <canvas id="lsystem" width="800" height="600"></canvas>
  <script>
  // 参数配置区
  const config = {
    width: 800, height: 600,
    iterations: 4,          // 迭代次数（≤5 避免过度密集）
    angle: 25,              // 分支角度（度）
    length: 8,              // 初始线段长度
    lengthDecay: 0.7,       // 长度衰减率
    trunkColor: '#16A34A',  // 主干色
    branchColor: '#22C55E', // 分支色
    leafColor: '#FACC15',   // 叶尖色
    bgColor: '#FDFDFD',
    rules: { 'F': 'FF+[+F-F-F]-[-F+F+F]', 'X': 'F-[[X]+X]+F[+FX]-X' },
    axiom: 'X',
    growSpeed: 3            // 每帧绘制字符数（生长动画）
  };
  const canvas = document.getElementById('lsystem');
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = config.bgColor;
  ctx.fillRect(0, 0, config.width, config.height);

  // L-system 字符串重写生成
  function generate(axiom, rules, iterations) {
    let result = axiom;
    for (let i = 0; i < iterations; i++) {
      result = result.split('').map(c => rules[c] || c).join('');
    }
    return result;
  }
  const lstring = generate(config.axiom, config.rules, config.iterations);

  // 绘制状态（海龟图形）
  let charIndex = 0;
  let x = config.width / 2, y = config.height - 50;
  let direction = 90, length = config.length, depth = 0;
  const stack = [];

  function drawStep() {
    const steps = config.growSpeed;
    for (let s = 0; s < steps && charIndex < lstring.length; s++) {
      const char = lstring[charIndex++];
      if (char === 'F') {
        // F：前进并绘制线段
        const rad = direction * Math.PI / 180;
        const nx = x + length * Math.cos(rad);
        const ny = y + length * Math.sin(rad);
        const color = depth === 0 ? config.trunkColor :
                      (depth < 3 ? config.branchColor : config.leafColor);
        const lw = depth === 0 ? 2.0 : (depth < 3 ? 1.0 : 0.5);
        ctx.strokeStyle = color;
        ctx.lineWidth = lw;
        ctx.globalAlpha = 0.8;
        ctx.beginPath();
        ctx.moveTo(x, y); ctx.lineTo(nx, ny); ctx.stroke();
        x = nx; y = ny;
      } else if (char === '+') {
        direction += config.angle;        // 左转
      } else if (char === '-') {
        direction -= config.angle;        // 右转
      } else if (char === '[') {
        // 压栈：保存当前状态
        stack.push({x, y, direction, length, depth});
        length *= config.lengthDecay; depth++;
      } else if (char === ']') {
        // 出栈：恢复状态
        const st = stack.pop();
        x = st.x; y = st.y; direction = st.direction;
        length = st.length; depth = st.depth;
      }
    }
    ctx.globalAlpha = 1;
    if (charIndex < lstring.length) requestAnimationFrame(drawStep);
  }
  drawStep();
  </script>
  </body>
  </html>
  ```
- **适用场景**: 装饰元素、自然主题文章、分形几何介绍、L2-标准审美等级场景
- **与 DLP 对接规则**: 映射到 `visual_dna.color_scheme` 的绿色系配色作为植物色调。当 `content_theme` 含"自然/植物/分形/数学/生长"关键词时优先匹配此原子。迭代次数参数映射到 `visual_dna.grid_system` 的信息密度——L1 用 3 迭代（极简）、L2 用 4 迭代（标准）、L3 用 5 迭代（丰富）。与 DLP-kami（Kami 纸质美学）和 DLP-newyorker（The New Yorker）的自然基因兼容。
- **风格先锋不油腻要点**:
  - 迭代次数默认 4（克制装饰），禁止超过 5（过度密集）
  - 线宽随深度递减（2.0→1.0→0.5），避免"等粗油腻"
  - 配色限制 3 色（主干+分支+叶尖），禁止多色植物

---

### VCA-GEN-006: 几何分形（Geometric Fractal）

- **原子 ID**: VCA-GEN-006
- **风格描述**: 递归几何图形，适合品牌元素。核心生成原理是通过递归函数重复绘制几何形，每次递归缩小尺寸并旋转/平移，形成自相似的分形结构。经典分形包括 Sierpinski 三角形、Koch 雪花、Dragon 曲线，具有数学严谨性与视觉冲击力。
- **配色方案**:
  - 主色: `#7C3AED`（科技紫，分形主色）
  - 辅色: `#06B6D4`（青色，分形辅色）
  - 强调色: `#F59E0B`（琥珀色，分形高亮）
  - 背景色: `#0F172A`（深蓝黑）
  - 文本色: `#F8FAFC`
- **生成代码模板**:
  ```svg
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600">
    <!-- 几何分形：Sierpinski 三角形（递归） -->
    <rect width="800" height="600" fill="#0F172A"/>

    <!-- Sierpinski 三角形（3层递归） -->
    <g fill="none" stroke-width="1">
      <!-- 第0层：大三角 -->
      <polygon points="400,100 200,450 600,450" stroke="#7C3AED" stroke-width="2"/>
      <!-- 第1层：3个中三角 -->
      <polygon points="400,100 300,275 500,275" stroke="#06B6D4" stroke-width="1.5"/>
      <polygon points="300,275 200,450 400,450" stroke="#06B6D4" stroke-width="1.5"/>
      <polygon points="500,275 400,450 600,450" stroke="#06B6D4" stroke-width="1.5"/>
      <!-- 第2层：9个小三角 -->
      <polygon points="400,100 350,187 450,187" stroke="#F59E0B" stroke-width="1"/>
      <polygon points="350,187 300,275 400,275" stroke="#F59E0B" stroke-width="1"/>
      <polygon points="450,187 400,275 500,275" stroke="#F59E0B" stroke-width="1"/>
      <polygon points="300,275 250,362 350,362" stroke="#F59E0B" stroke-width="1"/>
      <polygon points="350,362 300,450 400,450" stroke="#F59E0B" stroke-width="1"/>
      <polygon points="400,275 350,362 450,362" stroke="#F59E0B" stroke-width="1"/>
      <polygon points="450,362 400,450 500,450" stroke="#F59E0B" stroke-width="1"/>
      <polygon points="500,275 450,362 550,362" stroke="#F59E0B" stroke-width="1"/>
      <polygon points="550,362 500,450 600,450" stroke="#F59E0B" stroke-width="1"/>
    </g>

    <!-- 分形文字 -->
    <text x="100" y="550" font-family="Space Grotesk, sans-serif" font-size="14" fill="#F8FAFC" letter-spacing="3">SIERPINSKI · RECURSIVE GEOMETRY</text>
  </svg>
  ```
- **Canvas 实现模板**（动态几何分形，体现递归自相似 + 旋转动画）:
  ```html
  <!DOCTYPE html>
  <html lang="zh-CN">
  <head><meta charset="UTF-8"><title>VCA-GEN-006 几何分形 Canvas 实现</title></head>
  <body>
  <canvas id="fractal" width="800" height="600"></canvas>
  <script>
  // 参数配置区
  const config = {
    width: 800, height: 600,
    maxDepth: 3,            // 递归深度（≤4 避免过度密集）
    mainColor: '#7C3AED',   // 分形主色
    auxColor: '#06B6D4',    // 分形辅色
    highlightColor: '#F59E0B', // 分形高亮
    bgColor: '#0F172A',
    rotateSpeed: 0.005,     // 旋转动画速度
    type: 'sierpinski'      // 分形类型：sierpinski / koch
  };
  const canvas = document.getElementById('fractal');
  const ctx = canvas.getContext('2d');

  let rotation = 0;

  // Sierpinski 三角形递归绘制
  function drawSierpinski(x1, y1, x2, y2, x3, y3, depth, maxDepth) {
    const color = depth === 0 ? config.mainColor :
                  (depth === 1 ? config.auxColor : config.highlightColor);
    const lw = depth === 0 ? 2.0 : (depth === 1 ? 1.5 : 1.0);
    ctx.strokeStyle = color;
    ctx.lineWidth = lw;
    ctx.globalAlpha = 0.85;
    ctx.beginPath();
    ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.lineTo(x3, y3); ctx.closePath();
    ctx.stroke();
    if (depth < maxDepth) {
      // 递归：3 个子三角形
      const mx1 = (x1 + x2) / 2, my1 = (y1 + y2) / 2;
      const mx2 = (x2 + x3) / 2, my2 = (y2 + y3) / 2;
      const mx3 = (x1 + x3) / 2, my3 = (y1 + y3) / 2;
      drawSierpinski(x1, y1, mx1, my1, mx3, my3, depth + 1, maxDepth);
      drawSierpinski(mx1, my1, x2, y2, mx2, my2, depth + 1, maxDepth);
      drawSierpinski(mx3, my3, mx2, my2, x3, y3, depth + 1, maxDepth);
    }
  }

  // Koch 雪花边递归
  function drawKoch(x1, y1, x2, y2, depth, maxDepth) {
    if (depth === maxDepth) {
      ctx.lineTo(x2, y2);
      return;
    }
    const dx = (x2 - x1) / 3, dy = (y2 - y1) / 3;
    const xa = x1 + dx, ya = y1 + dy;
    const xb = x1 + 2 * dx, yb = y1 + 2 * dy;
    const angle = Math.atan2(dy, dx) - Math.PI / 3;
    const segLen = Math.sqrt(dx * dx + dy * dy);
    const xc = xa + Math.cos(angle) * segLen;
    const yc = ya + Math.sin(angle) * segLen;
    drawKoch(x1, y1, xa, ya, depth + 1, maxDepth);
    drawKoch(xa, ya, xc, yc, depth + 1, maxDepth);
    drawKoch(xc, yc, xb, yb, depth + 1, maxDepth);
    drawKoch(xb, yb, x2, y2, depth + 1, maxDepth);
  }

  function animate() {
    ctx.fillStyle = config.bgColor;
    ctx.fillRect(0, 0, config.width, config.height);
    ctx.save();
    ctx.translate(config.width / 2, config.height / 2);
    ctx.rotate(rotation);
    ctx.translate(-config.width / 2, -config.height / 2);
    if (config.type === 'sierpinski') {
      drawSierpinski(400, 120, 200, 460, 600, 460, 0, config.maxDepth);
    } else {
      ctx.strokeStyle = config.mainColor;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(300, 200);
      drawKoch(300, 200, 500, 200, 0, config.maxDepth);
      drawKoch(500, 200, 400, 380, 0, config.maxDepth);
      drawKoch(400, 380, 300, 200, 0, config.maxDepth);
      ctx.stroke();
    }
    ctx.restore();
    ctx.globalAlpha = 1;
    rotation += config.rotateSpeed;
    requestAnimationFrame(animate);
  }
  animate();
  </script>
  </body>
  </html>
  ```
- **适用场景**: 品牌元素、科技产品装饰、数学美学文章、L2-标准审美等级场景
- **与 DLP 对接规则**: 映射到 `visual_dna.color_scheme` 的科技配色作为分形色调。当 `design_language == "科技前沿"` 时优先匹配此原子作为品牌元素。递归深度参数映射到 `visual_dna.grid_system` 的信息密度——L1 用 2 层（极简）、L2 用 3 层（标准）、L3 用 4 层（密集）。与 DLP-linear（Linear App）和 DLP-stripe-press（Stripe Press）的科技基因兼容。
- **风格先锋不油腻要点**:
  - 递归深度默认 3 层（克制装饰），禁止超过 4 层（过度密集）
  - 线宽随深度递减（2.0→1.5→1.0），避免"等粗油腻"
  - 配色限制 3 色（主色+辅色+高亮），禁止多色分形

---

## 三、数据可视风格原子（VCA-DATA）

> **融入来源**: techarticleimage-skill — 数据可视风格 + 反 AI 廉价感机制
> **DLP 对接**: 每个数据可视风格原子映射到 `visual_dna.color_scheme` 的数据色板，由 Taste-Skill 根据 `output_type` 和 `content_theme` 选择匹配的数据可视风格。
> **反 AI 廉价感**: 数据可视风格原子必须标注"反 AI 廉价感要点"，说明如何避免 AI 生成图表的常见问题。

### VCA-DATA-001: 经济学人风格（Economist Style）

- **原子 ID**: VCA-DATA-001
- **风格描述**: 红蓝灰配色，网格线极淡，数据标签直接标注。核心视觉特征是"编辑级数据可视化"——Economist 红作为强调色，数据蓝作为主数据色，网格线极淡（opacity 0.1），数据标签直接标注在数据点旁而非使用图例，传递杂志级数据新闻的权威感。
- **配色方案**:
  - 主色: `#006BA6`（Economist 数据蓝）
  - 辅色: `#E3120B`（Economist 红，强调色）
  - 强调色: `#3D3D3D`（深灰，次要数据）
  - 背景色: `#FDFDFD`（纸白）
  - 文本色: `#1A1A1A`
  - 网格线: `#E5E5E5`（极淡灰）
- **生成代码模板**:
  ```python
  # Matplotlib 经济学人风格图表模板
  import matplotlib.pyplot as plt
  import numpy as np

  # 配色（Economist 风格）
  colors = {
      'primary': '#006BA6',    # 数据蓝
      'accent': '#E3120B',     # Economist 红
      'secondary': '#3D3D3D',  # 深灰
      'bg': '#FDFDFD',         # 纸白
      'text': '#1A1A1A',       # 正文黑
      'grid': '#E5E5E5'        # 极淡网格
  }

  # 数据
  years = ['2019', '2020', '2021', '2022', '2023', '2024']
  values = [45, 52, 48, 61, 67, 72]

  # 绘图
  fig, ax = plt.subplots(figsize=(8, 5), facecolor=colors['bg'])
  ax.set_facecolor(colors['bg'])

  # 柱状图（数据蓝）
  bars = ax.bar(years, values, color=colors['primary'], width=0.6, edgecolor='none')

  # 最后一根柱子用 Economist 红强调
  bars[-1].set_color(colors['accent'])

  # 数据标签直接标注（不用图例）
  for bar, value in zip(bars, values):
      ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
              str(value), ha='center', va='bottom',
              fontsize=11, color=colors['text'], fontweight='bold')

  # 极淡网格线（仅水平）
  ax.yaxis.grid(True, color=colors['grid'], linewidth=0.5, alpha=0.5)
  ax.set_axisbelow(True)

  # 移除边框（仅保留底部）
  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)
  ax.spines['left'].set_visible(False)
  ax.spines['bottom'].set_color(colors['text'])
  ax.spines['bottom'].set_linewidth(0.8)

  # 标题（左对齐，Economist 风格）
  ax.set_title('年度增长趋势', loc='left', fontsize=14,
               color=colors['text'], fontweight='bold', pad=15)

  # 副标题
  ax.text(0, 1.02, '数据来源：Economist 风格模拟', transform=ax.transAxes,
          fontsize=9, color=colors['secondary'])

  ax.tick_params(colors=colors['text'], labelsize=10)
  ax.set_yticks([])  # 移除Y轴刻度（数据标签已标注）

  plt.tight_layout()
  plt.savefig('economist_chart.png', dpi=150, bbox_inches='tight', facecolor=colors['bg'])
  plt.close()
  ```
- **适用场景**: 经济数据分析、市场趋势报告、新闻数据可视化、research_report 场景
- **与 DLP 对接规则**: 映射到 `visual_dna.color_scheme` 的 Economist 配色（主色 `#006BA6` + 强调色 `#E3120B`）。当 `output_type == "research_report"` 且 `content_theme` 含"经济/金融/市场/数据"关键词时优先匹配此原子。与 DLP-economist（The Economist 排版）和 DLP-economist-chart（Economist 图表规范）直接对接。字体映射到 Milo Serif/Source Serif Pro 衬线栈，保持杂志级质感。
- **反 AI 廉价感要点**:
  - **对抗过度平滑**: 网格线必须极淡（opacity 0.5），AI 倾向于使用粗网格线，此处强制极淡
  - **对抗配色同质化**: Economist 红+数据蓝为标志性配色，禁止替换为 AI 常见的"蓝橙配色"
  - **对抗构图模板化**: 数据标签直接标注（不用图例），禁止 AI 常见的"右侧图例"
  - **对抗细节平均化**: 最后一根柱子用红色强调，禁止所有柱子等色排列

---

### VCA-DATA-002: FT 风格（Financial Times Style）

- **原子 ID**: VCA-DATA-002
- **风格描述**: FT 粉色背景 #FFF1E5，深蓝主色，简洁线条。核心视觉特征是"金融级数据可视化"——FT 标志性的粉色背景（#FFF1E5）是品牌辨识度核心，深蓝主色传递金融的严谨，线条简洁无装饰，传递金融新闻的权威与克制。
- **配色方案**:
  - 主色: `#0F5499`（FT 深蓝）
  - 辅色: `#990F3D`（FT 深红，强调色）
  - 强调色: `#00875A`（FT 绿，正向数据）
  - 背景色: `#FFF1E5`（FT 粉，标志性背景）
  - 文本色: `#262A33`
  - 网格线: `#E8D5C4`（粉色系网格）
- **生成代码模板**:
  ```python
  # Matplotlib FT 风格图表模板
  import matplotlib.pyplot as plt
  import numpy as np

  # 配色（FT 风格）
  colors = {
      'primary': '#0F5499',    # FT 深蓝
      'accent': '#990F3D',     # FT 深红
      'positive': '#00875A',   # FT 绿
      'bg': '#FFF1E5',         # FT 粉（标志性）
      'text': '#262A33',       # 正文深灰
      'grid': '#E8D5C4'        # 粉色系网格
  }

  # 数据
  quarters = ['Q1', 'Q2', 'Q3', 'Q4', 'Q1', 'Q2', 'Q3', 'Q4']
  revenue = [120, 135, 142, 158, 165, 178, 185, 201]

  # 绘图
  fig, ax = plt.subplots(figsize=(8, 5), facecolor=colors['bg'])
  ax.set_facecolor(colors['bg'])

  # 折线图（FT 深蓝，简洁线条）
  ax.plot(quarters, revenue, color=colors['primary'], linewidth=2.5,
          marker='o', markersize=6, markerfacecolor=colors['bg'],
          markeredgecolor=colors['primary'], markeredgewidth=2)

  # 数据标签
  for i, (q, r) in enumerate(zip(quarters, revenue)):
      ax.annotate(f'{r}', (i, r), textcoords="offset points",
                  xytext=(0, 10), ha='center', fontsize=9,
                  color=colors['text'])

  # 网格线（粉色系，极淡）
  ax.yaxis.grid(True, color=colors['grid'], linewidth=0.8, alpha=0.6)
  ax.set_axisbelow(True)

  # 移除边框
  for spine in ['top', 'right', 'left']:
      ax.spines[spine].set_visible(False)
  ax.spines['bottom'].set_color(colors['text'])
  ax.spines['bottom'].set_linewidth(0.8)

  # 标题（FT 风格，左对齐）
  ax.set_title('季度营收趋势', loc='left', fontsize=14,
               color=colors['text'], fontweight='bold', pad=15)
  ax.text(0, 1.02, 'Financial Times 风格 · 单位：百万美元',
          transform=ax.transAxes, fontsize=9, color=colors['text'])

  ax.tick_params(colors=colors['text'], labelsize=10)
  ax.set_yticks([])

  plt.tight_layout()
  plt.savefig('ft_chart.png', dpi=150, bbox_inches='tight', facecolor=colors['bg'])
  plt.close()
  ```
- **适用场景**: 金融数据分析、财报可视化、市场趋势报告、research_report 场景
- **与 DLP 对接规则**: 映射到 `visual_dna.color_scheme` 的 FT 配色（主色 `#0F5499` + 背景色 `#FFF1E5`）。当 `output_type == "research_report"` 且 `content_theme` 含"金融/财报/市场/股票"关键词时优先匹配此原子。与 DLP-economist-chart（Economist 图表规范）的金融数据基因部分兼容。字体映射到 Financier Display/Source Serif Pro 衬线栈，保持金融级质感。
- **反 AI 廉价感要点**:
  - **对抗过度平滑**: FT 粉色背景 `#FFF1E5` 为硬性约束，禁止替换为纯白背景
  - **对抗配色同质化**: FT 深蓝+粉色背景为标志性配色，禁止 AI 常见的"白底蓝线"
  - **对抗构图模板化**: 数据标签直接标注，禁止右侧图例
  - **对抗细节平均化**: 线条简洁无装饰（无填充区域、无阴影），禁止 AI 常见的"渐变填充"

---

### VCA-DATA-003: NYT 风格（New York Times Style）

- **原子 ID**: VCA-DATA-003
- **风格描述**: 深色背景，亮色数据，叙事驱动。核心视觉特征是"叙事级数据可视化"——NYT 数据新闻团队标志性的深色背景配亮色数据，强调数据的故事性而非数据本身，图表服务于叙事，每个数据点都有上下文。
- **配色方案**:
  - 主色: `#FFFFFF`（白色，主数据色）
  - 辅色: `#FF6B6B`（珊瑚红，强调数据）
  - 强调色: `#4ECDC4`（薄荷绿，对比数据）
  - 背景色: `#1A1A1A`（深黑背景）
  - 文本色: `#E0E0E0`
  - 网格线: `#3A3A3A`（深灰网格）
- **生成代码模板**:
  ```python
  # Matplotlib NYT 风格图表模板
  import matplotlib.pyplot as plt
  import numpy as np

  # 配色（NYT 风格）
  colors = {
      'primary': '#FFFFFF',    # 白色主数据
      'accent': '#FF6B6B',     # 珊瑚红强调
      'contrast': '#4ECDC4',   # 薄荷绿对比
      'bg': '#1A1A1A',         # 深黑背景
      'text': '#E0E0E0',       # 浅灰文字
      'grid': '#3A3A3A'        # 深灰网格
  }

  # 数据
  decades = ['1950s', '1960s', '1970s', '1980s', '1990s', '2000s', '2010s', '2020s']
  trend = [30, 35, 42, 48, 55, 62, 71, 85]
  highlight = [30, 35, 42, 48, 55, 62, 71, 95]  # 最后一项高亮

  # 绘图
  fig, ax = plt.subplots(figsize=(9, 5), facecolor=colors['bg'])
  ax.set_facecolor(colors['bg'])

  # 面积图（白色，半透明）
  ax.fill_between(decades, trend, color=colors['primary'], alpha=0.15)
  ax.plot(decades, trend, color=colors['primary'], linewidth=2)

  # 高亮最后一段（珊瑚红）
  ax.plot(decades[-2:], highlight[-2:], color=colors['accent'], linewidth=3)
  ax.fill_between(decades[-2:], highlight[-2:], color=colors['accent'], alpha=0.3)

  # 叙事标注
  ax.annotate('加速增长', xy=(7, 95), xytext=(5.5, 70),
              fontsize=11, color=colors['accent'],
              arrowprops=dict(arrowstyle='->', color=colors['accent'], lw=1.5))

  # 网格线（深灰，极淡）
  ax.yaxis.grid(True, color=colors['grid'], linewidth=0.5, alpha=0.5)
  ax.set_axisbelow(True)

  # 移除边框
  for spine in ax.spines.values():
      spine.set_visible(False)

  # 标题（NYT 风格，左对齐，大字）
  ax.set_title('十年趋势演变', loc='left', fontsize=16,
               color=colors['text'], fontweight='bold', pad=20)
  ax.text(0, 1.05, 'New York Times 风格 · 叙事驱动可视化',
          transform=ax.transAxes, fontsize=10, color=colors['text'], alpha=0.7)

  ax.tick_params(colors=colors['text'], labelsize=10)

  plt.tight_layout()
  plt.savefig('nyt_chart.png', dpi=150, bbox_inches='tight', facecolor=colors['bg'])
  plt.close()
  ```
- **适用场景**: 数据新闻、叙事型数据可视化、深度报道、wechat_article 场景
- **与 DLP 对接规则**: 映射到 `visual_dna.color_scheme` 的深色配色（背景色 `#1A1A1A` + 主色 `#FFFFFF`）。当 `output_type == "wechat_article"` 且 `content_theme` 含"数据/新闻/叙事/趋势"关键词时优先匹配此原子。与 DLP-newyorker（The New Yorker）的叙事基因兼容。字体映射到 Cheltenham/Source Serif Pro 衬线栈，保持叙事级质感。
- **反 AI 廉价感要点**:
  - **对抗过度平滑**: 深色背景+亮色数据为硬性约束，禁止 AI 常见的"白底浅色数据"
  - **对抗配色同质化**: 白色+珊瑚红+薄荷绿为标志性配色，禁止 AI 常见的"蓝紫渐变"
  - **对抗构图模板化**: 叙事标注（箭头+文字）为硬性约束，禁止纯数据无叙事
  - **对抗细节平均化**: 高亮最后一段数据，禁止所有数据点等色排列

---

### VCA-DATA-004: Pudding 风格（The Pudding Style）

- **原子 ID**: VCA-DATA-004
- **风格描述**: 活泼配色，交互式，创意可视化。核心视觉特征是"创意级数据可视化"——The Pudding 标志性的活泼配色（高饱和但不刺眼），非传统图表类型（气泡图/力导向图/自定义形状），强调可视化的创意性与趣味性，适合大众传播。
- **配色方案**:
  - 主色: `#FF6B6B`（珊瑚红，活泼主色）
  - 辅色: `#4ECDC4`（薄荷绿，活泼辅色）
  - 强调色: `#FFE66D`（明黄，活泼强调）
  - 背景色: `#FAFAFA`（浅灰白）
  - 文本色: `#1A1A1A`
  - 补充色: `#A06CD5`（紫罗兰）、`#6C5CE7`（靛蓝）
- **生成代码模板**:
  ```python
  # Matplotlib Pudding 风格气泡图模板
  import matplotlib.pyplot as plt
  import numpy as np

  # 配色（Pudding 风格，活泼但不刺眼）
  colors = {
      'primary': '#FF6B6B',    # 珊瑚红
      'secondary': '#4ECDC4',  # 薄荷绿
      'accent': '#FFE66D',     # 明黄
      'bg': '#FAFAFA',         # 浅灰白
      'text': '#1A1A1A',       # 正文黑
      'extra1': '#A06CD5',     # 紫罗兰
      'extra2': '#6C5CE7'      # 靛蓝
  }

  # 数据（气泡图）
  np.random.seed(42)
  categories = ['A', 'B', 'C', 'D', 'E', 'F']
  x = np.random.uniform(0.1, 0.9, len(categories))
  y = np.random.uniform(0.1, 0.9, len(categories))
  sizes = np.random.uniform(200, 1500, len(categories))
  color_list = [colors['primary'], colors['secondary'], colors['accent'],
                colors['extra1'], colors['extra2'], colors['primary']]

  # 绘图
  fig, ax = plt.subplots(figsize=(8, 6), facecolor=colors['bg'])
  ax.set_facecolor(colors['bg'])

  # 气泡图
  scatter = ax.scatter(x, y, s=sizes, c=color_list, alpha=0.7,
                       edgecolors='white', linewidth=2)

  # 数据标签（直接标注在气泡上）
  for i, cat in enumerate(categories):
      ax.text(x[i], y[i], cat, ha='center', va='center',
              fontsize=14, color='white', fontweight='bold')

  # 移除边框和刻度
  for spine in ax.spines.values():
      spine.set_visible(False)
  ax.set_xticks([])
  ax.set_yticks([])

  # 标题（Pudding 风格，活泼大字）
  ax.set_title('创意数据可视化', loc='left', fontsize=18,
               color=colors['text'], fontweight='bold', pad=20)
  ax.text(0, 1.02, 'The Pudding 风格 · 气泡大小代表数据量',
          transform=ax.transAxes, fontsize=10, color=colors['text'], alpha=0.7)

  plt.tight_layout()
  plt.savefig('pudding_chart.png', dpi=150, bbox_inches='tight', facecolor=colors['bg'])
  plt.close()
  ```
- **适用场景**: 创意数据可视化、大众传播图表、趣味数据文章、wechat_article 场景
- **与 DLP 对接规则**: 映射到 `visual_dna.color_scheme` 的活泼配色（多色板，突破五色板限制）。当 `output_type == "wechat_article"` 且 `target_audience == "youth"` 时优先匹配此原子。与 DLP-ted（TED 演讲幻灯片）的活泼基因兼容。字体映射到 Source Sans Pro/Inter 无衬线栈，传递活泼感。
- **反 AI 廉价感要点**:
  - **对抗过度平滑**: 气泡边缘添加白色描边（2px），避免 AI 常见的"无描边扁平气泡"
  - **对抗配色同质化**: 活泼多色（珊瑚红+薄荷绿+明黄+紫罗兰）为硬性约束，禁止 AI 常见的"蓝灰配色"
  - **对抗构图模板化**: 非传统图表类型（气泡图/力导向图），禁止 AI 常见的"标准柱状图/折线图"
  - **对抗细节平均化**: 气泡大小必须有 5:1 以上的对比比，禁止等大气泡排列

---

### VCA-DATA-005: Information is Beautiful 风格

- **原子 ID**: VCA-DATA-005
- **风格描述**: 高饱和配色，圆形/气泡图为主。核心视觉特征是"美学级数据可视化"——David McCandless 的 Information is Beautiful 标志性高饱和配色，以圆形/气泡图为主要图表类型，强调数据的美学呈现而非精确数值，适合信息图与海报。
- **配色方案**:
  - 主色: `#00A0B0`（青蓝，高饱和主色）
  - 辅色: `#6A4A3C`（棕色，高饱和辅色）
  - 强调色: `#CC333F`（红色，高饱和强调）
  - 背景色: `#EBEBEB`（浅灰背景）
  - 文本色: `#1A1A1A`
  - 补充色: `#F2D03D`（明黄）、`#46617D`（深蓝）、`#8FBF3F`（草绿）
- **生成代码模板**:
  ```python
  # Matplotlib Information is Beautiful 风格气泡图模板
  import matplotlib.pyplot as plt
  import numpy as np

  # 配色（Information is Beautiful 风格，高饱和）
  colors = {
      'primary': '#00A0B0',    # 青蓝
      'secondary': '#6A4A3C',  # 棕色
      'accent': '#CC333F',     # 红色
      'bg': '#EBEBEB',         # 浅灰
      'text': '#1A1A1A',       # 正文黑
      'extra1': '#F2D03D',     # 明黄
      'extra2': '#46617D',     # 深蓝
      'extra3': '#8FBF3F'      # 草绿
  }

  # 数据（同心圆气泡图）
  categories = ['类别A', '类别B', '类别C', '类别D', '类别E']
  values = [100, 75, 50, 30, 15]
  color_list = [colors['primary'], colors['accent'], colors['extra1'],
                colors['secondary'], colors['extra3']]

  # 绘图
  fig, ax = plt.subplots(figsize=(8, 6), facecolor=colors['bg'])
  ax.set_facecolor(colors['bg'])

  # 同心圆气泡（从大到小）
  max_size = max(values)
  for i, (cat, val, color) in enumerate(zip(categories, values, color_list)):
      size = (val / max_size) * 5000
      y_offset = -i * 1.5
      ax.scatter(0.5, 0.5 + y_offset * 0.05, s=size, c=color, alpha=0.8,
                 edgecolors='white', linewidth=2)
      ax.text(0.5, 0.5 + y_offset * 0.05, f'{cat}\n{val}', ha='center', va='center',
              fontsize=10, color='white', fontweight='bold')

  # 移除边框和刻度
  for spine in ax.spines.values():
      spine.set_visible(False)
  ax.set_xticks([])
  ax.set_yticks([])
  ax.set_xlim(0, 1)
  ax.set_ylim(0, 1)

  # 标题
  ax.set_title('信息美学可视化', loc='left', fontsize=16,
               color=colors['text'], fontweight='bold', pad=20)
  ax.text(0, 1.02, 'Information is Beautiful 风格 · 气泡大小代表数值',
          transform=ax.transAxes, fontsize=10, color=colors['text'], alpha=0.7)

  plt.tight_layout()
  plt.savefig('iib_chart.png', dpi=150, bbox_inches='tight', facecolor=colors['bg'])
  plt.close()
  ```
- **适用场景**: 信息图、数据海报、美学数据可视化、wechat_article 场景
- **与 DLP 对接规则**: 映射到 `visual_dna.color_scheme` 的高饱和配色（多色板）。当 `output_type == "wechat_article"` 且 `content_theme` 含"信息图/美学/海报/创意"关键词时优先匹配此原子。与 DLP-ted（TED 演讲幻灯片）和 DLP-pudding 的创意基因兼容。字体映射到 Source Sans Pro/Inter 无衬线栈，传递现代感。
- **反 AI 廉价感要点**:
  - **对抗过度平滑**: 高饱和配色为硬性约束，禁止 AI 常见的"低饱和柔和配色"
  - **对抗配色同质化**: 青蓝+棕色+红色+明黄为标志性配色，禁止 AI 常见的"蓝紫渐变"
  - **对抗构图模板化**: 圆形/气泡图为主要图表类型，禁止 AI 常见的"柱状图/折线图"
  - **对抗细节平均化**: 气泡大小必须有 5:1 以上的对比比，禁止等大排列

---

### VCA-DATA-006: Distill 风格

- **原子 ID**: VCA-DATA-006
- **风格描述**: 学术风格，极简，白底，精确数据。核心视觉特征是"学术级数据可视化"——Distill.pub 标志性的极简白底，精确的数据呈现，无装饰元素，强调数据的可读性与学术严谨性，适合机器学习/AI 论文的配图。
- **配色方案**:
  - 主色: `#4C55C4`（学术蓝，主数据色）
  - 辅色: `#E06C75`（学术红，对比数据）
  - 强调色: `#61AFEF`（浅蓝，辅助数据）
  - 背景色: `#FFFFFF`（纯白背景）
  - 文本色: `#282C34`
  - 网格线: `#F0F0F0`（极淡灰）
- **生成代码模板**:
  ```python
  # Matplotlib Distill 风格图表模板
  import matplotlib.pyplot as plt
  import numpy as np

  # 配色（Distill 风格，学术极简）
  colors = {
      'primary': '#4C55C4',    # 学术蓝
      'secondary': '#E06C75',  # 学术红
      'accent': '#61AFEF',     # 浅蓝
      'bg': '#FFFFFF',         # 纯白
      'text': '#282C34',       # 正文深灰
      'grid': '#F0F0F0'        # 极淡网格
  }

  # 数据
  epochs = np.arange(1, 21)
  train_loss = 2.5 * np.exp(-0.15 * epochs) + 0.1
  val_loss = 2.5 * np.exp(-0.12 * epochs) + 0.15

  # 绘图
  fig, ax = plt.subplots(figsize=(8, 5), facecolor=colors['bg'])
  ax.set_facecolor(colors['bg'])

  # 训练损失（学术蓝）
  ax.plot(epochs, train_loss, color=colors['primary'], linewidth=2,
          label='Training Loss', marker='o', markersize=4)

  # 验证损失（学术红）
  ax.plot(epochs, val_loss, color=colors['secondary'], linewidth=2,
          label='Validation Loss', marker='s', markersize=4)

  # 网格线（极淡）
  ax.grid(True, color=colors['grid'], linewidth=0.5, alpha=0.8)
  ax.set_axisbelow(True)

  # 边框（仅左下，极细）
  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)
  ax.spines['left'].set_color(colors['text'])
  ax.spines['left'].set_linewidth(0.5)
  ax.spines['bottom'].set_color(colors['text'])
  ax.spines['bottom'].set_linewidth(0.5)

  # 标题（Distill 风格，左对齐，学术字体）
  ax.set_title('模型训练曲线', loc='left', fontsize=13,
               color=colors['text'], fontweight='bold', pad=15)
  ax.text(0, 1.02, 'Distill 风格 · 学术级数据可视化',
          transform=ax.transAxes, fontsize=9, color=colors['text'], alpha=0.7)

  # 图例（底部，水平排列）
  ax.legend(loc='upper right', frameon=False, fontsize=10,
            labelcolor=colors['text'])

  ax.set_xlabel('Epoch', fontsize=11, color=colors['text'])
  ax.set_ylabel('Loss', fontsize=11, color=colors['text'])
  ax.tick_params(colors=colors['text'], labelsize=10)

  plt.tight_layout()
  plt.savefig('distill_chart.png', dpi=150, bbox_inches='tight', facecolor=colors['bg'])
  plt.close()
  ```
- **适用场景**: 学术论文配图、机器学习/AI 可视化、精确数据呈现、research_report 场景
- **与 DLP 对接规则**: 映射到 `visual_dna.color_scheme` 的学术配色（主色 `#4C55C4` + 背景色 `#FFFFFF`）。当 `output_type == "research_report"` 且 `target_audience == "academic"` 时优先匹配此原子。与 DLP-nature（Nature 正刊）和 DLP-science（Science 正刊）的学术基因兼容。字体映射到 Source Serif Pro/Latin Modern Roman 衬线栈，保持学术级质感。
- **反 AI 廉价感要点**:
  - **对抗过度平滑**: 极简白底+精确数据为硬性约束，禁止 AI 常见的"渐变背景/阴影装饰"
  - **对抗配色同质化**: 学术蓝+学术红为标志性配色，禁止 AI 常见的"蓝紫渐变"
  - **对抗构图模板化**: 图例在图表内部（右上角），禁止 AI 常见的"右侧图例占空间"
  - **对抗细节平均化**: 边框极细（0.5px），网格极淡（opacity 0.8），禁止 AI 常见的"粗边框/粗网格"

---

## 四、品牌视觉元素原子（VCA-BRAND）

> **融入来源**: algorithmic-art-skill — 极简几何、生成纹理
> **DLP 对接**: 每个品牌视觉元素原子映射到 `visual_dna.color_scheme` 的品牌色板，由 Taste-Skill 根据 `content_theme` 和 `brand_assets` 选择匹配的品牌视觉元素。

### VCA-BRAND-001: Logo 占位（Logo Placeholder）

- **原子 ID**: VCA-BRAND-001
- **风格描述**: 几何 Logo 占位符，圆形/方形/六边形。核心视觉特征是"极简几何占位"——当品牌 Logo 不可用时，使用极简几何形状作为占位符，避免空白或低质量占位图。几何形状（圆/方/六边形）配合品牌色，传递专业感。
- **配色方案**:
  - 主色: `#1A56DB`（品牌蓝，Logo 主色）
  - 辅色: `#0E9F6E`（品牌绿，Logo 辅色）
  - 强调色: `#E74694`（品牌粉，Logo 强调）
  - 背景色: `#F9FAFB`（浅灰背景）
  - 文本色: `#1F2937`
- **生成代码模板**:
  ```svg
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
    <!-- Logo 占位符：六边形几何 -->
    <rect width="200" height="200" fill="#F9FAFB"/>

    <!-- 六边形 Logo 占位 -->
    <polygon points="100,30 160,65 160,135 100,170 40,135 40,65"
             fill="none" stroke="#1A56DB" stroke-width="3"/>

    <!-- 内部几何（品牌色组合） -->
    <circle cx="100" cy="80" r="20" fill="#1A56DB"/>
    <rect x="80" y="105" width="40" height="40" fill="#0E9F6E" rx="4"/>
    <circle cx="100" cy="125" r="8" fill="#E74694"/>

    <!-- 品牌文字占位 -->
    <text x="100" y="190" font-family="Inter, sans-serif" font-size="10"
          fill="#1F2937" text-anchor="middle" font-weight="600">BRAND</text>
  </svg>
  ```
- **适用场景**: 品牌 Logo 不可用时的占位、品牌系统文档、设计规范文档
- **与 DLP 对接规则**: 映射到 `visual_dna.color_scheme` 的品牌配色（主色 `#1A56DB` + 辅色 `#0E9F6E`）。当 `brand_assets.logo` 为 null 时优先匹配此原子作为 Logo 占位符。与所有 DLP 兼容——占位符颜色从命中的 DLP 的 `color_palette.primary/secondary/accent` 提取。几何形状参数映射到 `visual_dna.grid_system` 的圆角系统——DLP 为 0px 圆角时使用方形/六边形，DLP 为 6px+ 圆角时使用圆形。
- **风格先锋不油腻要点**:
  - 几何形状限制 3 种（圆/方/六边形），禁止复杂路径
  - 线宽 ≤ 3px，避免"粗框油腻"
  - 配色限制 3 色（品牌主色+辅色+强调），禁止多色 Logo

---

### VCA-BRAND-002: 品牌色带（Brand Color Band）

- **原子 ID**: VCA-BRAND-002
- **风格描述**: 水平/垂直色带，用于页眉/页脚。核心视觉特征是"品牌色带"——使用品牌色组成的水平或垂直色带，作为页眉/页脚的品牌标识。色带宽度/高度遵循 4px 基准栅格，颜色从品牌色板提取。
- **配色方案**:
  - 主色: `#1A56DB`（品牌蓝，色带主色）
  - 辅色: `#0E9F6E`（品牌绿，色带辅色）
  - 强调色: `#E74694`（品牌粉，色带强调）
  - 背景色: `#FFFFFF`
  - 文本色: `#1F2937`
- **生成代码模板**:
  ```svg
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 40" width="800" height="40">
    <!-- 品牌色带：水平色带（页眉） -->
    <!-- 主色带（品牌蓝，占 60%） -->
    <rect x="0" y="0" width="480" height="40" fill="#1A56DB"/>
    <!-- 辅色带（品牌绿，占 25%） -->
    <rect x="480" y="0" width="200" height="40" fill="#0E9F6E"/>
    <!-- 强调色带（品牌粉，占 15%） -->
    <rect x="680" y="0" width="120" height="40" fill="#E74694"/>

    <!-- 品牌文字（白色，叠加在主色带上） -->
    <text x="20" y="25" font-family="Inter, sans-serif" font-size="14"
          fill="#FFFFFF" font-weight="600">BRAND NAME</text>
  </svg>
  ```
- **适用场景**: 页眉品牌标识、页脚品牌色带、文档品牌水印、所有 output_type 场景
- **与 DLP 对接规则**: 映射到 `visual_dna.color_scheme` 的品牌配色（主色+辅色+强调色）。色带宽度比例映射到品牌色的重要性——主色 60%、辅色 25%、强调色 15%。与所有 DLP 兼容——色带颜色从命中的 DLP 的 `color_palette.primary/secondary/accent` 提取。色带高度映射到 `visual_dna.grid_system` 的间距系统——页眉色带 40px（10×4px）、页脚色带 32px（8×4px）。
- **风格先锋不油腻要点**:
  - 色带高度 ≤ 40px，避免"厚重油腻"
  - 配色限制 3 色（主色+辅色+强调），禁止多色色带
  - 色带比例固定（60:25:15），禁止等宽色带

---

### VCA-BRAND-003: 品牌纹理（Brand Texture）

- **原子 ID**: VCA-BRAND-003
- **风格描述**: 重复几何图案，用于背景。核心视觉特征是"品牌纹理"——使用品牌色组成的重复几何图案（圆点/斜线/网格/波纹），作为背景纹理。纹理透明度 ≤ 0.1，避免喧宾夺主，仅提供品牌色的微妙存在感。
- **配色方案**:
  - 主色: `#1A56DB`（品牌蓝，纹理主色）
  - 辅色: `#0E9F6E`（品牌绿，纹理辅色）
  - 强调色: `#E74694`（品牌粉，纹理强调）
  - 背景色: `#FFFFFF`
  - 文本色: `#1F2937`
- **生成代码模板**:
  ```svg
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600">
    <!-- 品牌纹理：重复圆点图案 -->
    <defs>
      <!-- 圆点纹理 pattern -->
      <pattern id="brandDots" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
        <circle cx="10" cy="10" r="2" fill="#1A56DB" opacity="0.08"/>
      </pattern>
      <!-- 斜线纹理 pattern -->
      <pattern id="brandLines" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
        <line x1="0" y1="0" x2="0" y2="20" stroke="#0E9F6E" stroke-width="1" opacity="0.06"/>
      </pattern>
    </defs>

    <!-- 白色背景 -->
    <rect width="800" height="600" fill="#FFFFFF"/>

    <!-- 叠加圆点纹理（左半部分） -->
    <rect x="0" y="0" width="400" height="600" fill="url(#brandDots)"/>

    <!-- 叠加斜线纹理（右半部分） -->
    <rect x="400" y="0" width="400" height="600" fill="url(#brandLines)"/>

    <!-- 品牌文字 -->
    <text x="400" y="300" font-family="Inter, sans-serif" font-size="24"
          fill="#1F2937" text-anchor="middle" font-weight="600">BRAND TEXTURE</text>
  </svg>
  ```
- **适用场景**: 背景纹理、品牌水印、文档背景装饰、所有 output_type 场景
- **与 DLP 对接规则**: 映射到 `visual_dna.color_scheme` 的品牌配色（主色+辅色）。纹理透明度强制 ≤ 0.1，避免喧宾夺主。与所有 DLP 兼容——纹理颜色从命中的 DLP 的 `color_palette.primary/secondary` 提取。纹理间距映射到 `visual_dna.grid_system` 的间距系统——圆点间距 20px（5×4px）、斜线间距 20px（5×4px）。
- **风格先锋不油腻要点**:
  - 纹理透明度 ≤ 0.1，避免"喧宾夺主"
  - 几何图案限制 4 种（圆点/斜线/网格/波纹），禁止复杂图案
  - 配色限制 2 色（主色+辅色），禁止多色纹理

---

### VCA-BRAND-004: 品牌图标集（Brand Icon Set）

- **原子 ID**: VCA-BRAND-004
- **风格描述**: 统一线宽/风格的图标集。核心视觉特征是"品牌图标集"——统一线宽（1.5px）、统一风格（线性/填充/双色）、统一圆角（round 端点）的图标集，确保品牌视觉的一致性。图标基于 24×24px 网格，适配各种 UI 场景。
- **配色方案**:
  - 主色: `#1A56DB`（品牌蓝，图标主色）
  - 辅色: `#0E9F6E`（品牌绿，图标辅色）
  - 强调色: `#E74694`（品牌粉，图标强调）
  - 背景色: `#FFFFFF`
  - 文本色: `#1F2937`
- **生成代码模板**:
  ```svg
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 40" width="120" height="40">
    <!-- 品牌图标集：统一线宽 1.5px，round 端点 -->

    <!-- 图标1：设置齿轮（品牌蓝） -->
    <g transform="translate(0, 0)" stroke="#1A56DB" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="12" cy="12" r="3"/>
      <path d="M12 2 L12 5 M12 19 L12 22 M2 12 L5 12 M19 12 L22 12 M5 5 L7 7 M17 17 L19 19 M5 19 L7 17 M17 7 L19 5"/>
    </g>

    <!-- 图标2：心形（品牌绿） -->
    <g transform="translate(32, 0)" stroke="#0E9F6E" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 21 C 12 21, 4 13, 4 8 C 4 5, 6 3, 9 3 C 11 3, 12 5, 12 5 C 12 5, 13 3, 15 3 C 18 3, 20 5, 20 8 C 20 13, 12 21, 12 21 Z"/>
    </g>

    <!-- 图标3：星形（品牌粉） -->
    <g transform="translate(64, 0)" stroke="#E74694" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round">
      <polygon points="12,2 15,9 22,9 17,14 19,21 12,17 5,21 7,14 2,9 9,9"/>
    </g>

    <!-- 图标4：用户（品牌蓝） -->
    <g transform="translate(96, 0)" stroke="#1A56DB" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="12" cy="8" r="4"/>
      <path d="M4 22 C 4 17, 8 15, 12 15 C 16 15, 20 17, 20 22"/>
    </g>
  </svg>
  ```
- **适用场景**: UI 图标、品牌图标集、导航图标、所有 output_type 场景
- **与 DLP 对接规则**: 映射到 `visual_dna.color_scheme` 的品牌配色（主色+辅色+强调色）+ `visual_dna.line_style` 的线条规范（1.5px 线宽 + round 端点）。与所有 DLP 兼容——图标颜色从命中的 DLP 的 `color_palette.primary/secondary/accent` 提取。图标网格映射到 `visual_dna.grid_system` 的 4px 基准——24×24px 网格（6×4px）。
- **风格先锋不油腻要点**:
  - 线宽统一 1.5px，禁止混合线宽
  - 端点统一 round，禁止混合端点
  - 配色限制 3 色（主色+辅色+强调），禁止多色图标

---

## 五、融入内容来源标注

### 5.1 融入 techarticleimage-skill 的内容

| 融入能力 | 对应原子 | 融入说明 |
|---------|---------|---------|
| 25 种真实艺术流派风格（本库选取 10 个最核心的） | VCA-ART-001 至 VCA-ART-010 | 每个艺术流派原子锚定真实艺术家/作品（Dieter Rams/El Lissitzky/Müller-Brockmann/Ettore Sottsass/Walter Gropius/Chrysler Building/Le Corbusier/Boccioni/Hannah Höch/Carlos Cruz-Diez），配色来自代表性作品的实测色值 |
| 反 AI 廉价感机制 | VCA-ART-001 至 VCA-ART-010（反 AI 廉价感要点）+ VCA-DATA-001 至 VCA-DATA-006（反 AI 廉价感要点） | 每个艺术流派原子和数据可视风格原子标注"反 AI 廉价感要点"，从 4 个维度（过度平滑/配色同质化/构图模板化/细节平均化）对抗 AI 生成图片的常见问题 |
| 数据可视风格 | VCA-DATA-001 至 VCA-DATA-006 | 6 种真实数据可视化风格（Economist/FT/NYT/Pudding/Information is Beautiful/Distill），配色来自各媒体的公开版式规范 |

### 5.2 融入 algorithmic-art-skill 的内容

| 融入能力 | 对应原子 | 融入说明 |
|---------|---------|---------|
| 极简几何 | VCA-ART-001（极简主义）/ VCA-ART-005（包豪斯）/ VCA-ART-010（极简几何）/ VCA-GEN-006（几何分形）/ VCA-BRAND-001（Logo 占位） | 所有极简几何原子使用基本几何形（圆/三角/方/线），禁止复杂路径 |
| 生成纹理 | VCA-GEN-001（流场）/ VCA-GEN-004（Perlin 噪声）/ VCA-BRAND-003（品牌纹理） | 生成式纹理原子提供可执行的代码模板（SVG/Matplotlib），默认参数经过审美校准 |
| 高级渐变 | VCA-ART-010（极简几何）/ VCA-GEN-001（流场）/ VCA-GEN-003（Voronoi 图） | 高级渐变使用 HSL 色彩空间而非 RGB 线性渐变，避免"塑料感" |
| 生成式艺术能力 | VCA-GEN-001 至 VCA-GEN-006 | 6 种生成式艺术原子（流场/粒子系统/Voronoi 图/Perlin 噪声/L-system/几何分形），每个提供可执行的代码模板 |
| 风格先锋不油腻 | VCA-GEN-001 至 VCA-GEN-006（风格先锋不油腻要点）+ VCA-BRAND-001 至 VCA-BRAND-004（风格先锋不油腻要点） | 所有生成式艺术原子和品牌视觉元素原子遵循"克制装饰"原则，避免过度装饰 |

---

## 六、强制规则

1. **原子优先**: 所有渲染模块的视觉创意元素必须从本原子库选取原子，不得自行声明视觉风格参数。
2. **多轨实现**: 每个原子必须提供 SVG/Canvas/Matplotlib 之一或多个的可执行代码模板，确保跨引擎视觉一致性。
3. **DLP 对接**: 每个原子必须通过 `visual_dna.color_scheme` / `visual_dna.font_scheme` / `visual_dna.line_style` 字段与 DLP 对接，由 Taste-Skill 仲裁。
4. **反 AI 廉价感**: 艺术流派原子（VCA-ART）和数据可视风格原子（VCA-DATA）必须标注"反 AI 廉价感要点"，从 4 个维度对抗 AI 廉价感。
5. **风格先锋不油腻**: 生成式艺术原子（VCA-GEN）和品牌视觉元素原子（VCA-BRAND）必须遵循"克制装饰"原则，默认参数经过审美校准。
6. **配色可追溯**: 所有配色必须锚定真实艺术流派/媒体/品牌，禁止 AI 凭空生成的"安全配色"。
7. **融入来源标注**: 所有融入内容必须明确标注来源技能（techarticleimage-skill / algorithmic-art-skill）。
8. **原子不可覆盖**: 任何渲染模块不得绕过原子库使用硬编码视觉风格值，如需调整需通过 Taste-Skill 仲裁修改 `visual_dna`。

---

## 七、穷尽重试策略

### L1: 完整原子库可用
所有 26 个视觉创意原子均可正常选取，SVG/Canvas/Matplotlib 多轨实现完整。

### L2: 部分原子不可用
- 穷尽尝试使用同类别其他原子替代
- 记录缺失原子 ID，使用最接近的原子质量保持
- 标注为"部分原子质量保持"输出

### L3: 代码模板部分缺失
- 穷尽尝试使用可用代码模板（SVG 优先或 Matplotlib 优先）
- 缺失模板使用默认几何形状兜底（矩形+圆形+线条）
- 标注为"单轨质量保持"输出

### L4: 原子库完全不可用
- 穷尽尝试使用 `visual_dna.color_scheme` 的五色板生成基础几何
- 使用矩形+圆形+线条的基础组合
- 标注为"穷尽重试视觉"输出

### L5: 视觉系统完全不可用
- 仅输出纯文本内容
- 无视觉创意元素
- 标注为"穷尽重试输出"

---

> 知识来源: techarticleimage-skill（25 种艺术流派风格 + 反 AI 廉价感机制）、algorithmic-art-skill（生成式艺术 + 极简几何 + 高级渐变）、rendering-pipeline/visual-dna.md、rendering-pipeline/design-language-profiles/README.md

© 阿洋
