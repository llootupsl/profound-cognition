> **作者**: 阿洋

# AI 配图生成 API 调用规范

> **模块标识**: `output/illustration-generator`
> **职责**: 通过 AI 图像生成 API 为研究报告和演示文稿生成匹配的配图，支持多种图像模型和后端。穷尽尝试所有可用图像模型
> **依赖**: `output/aesthetic-enhancer`
> **CLI 命令**: 无（API 调用，非 CLI）

---

## 一、模型优先级策略

### 1.1 优先级链

```
优先级 1: Flux.1 Dev (最高质量，BFL API)
  ↓ 不可用时
优先级 2: Stable Diffusion API (Stability AI 或自部署)
  ↓ 不可用时
优先级 3: 文字描述占位 (Markdown 内嵌 SVG/CSS 占位图)
```

### 1.2 穷尽重试决策流程

```
输入: 配图请求
 ↓
检测 Flux.1 Dev API Key 是否配置？
 ├─ 是 → 尝试调用 Flux.1 Dev
 │   ├─ 成功 → 返回图片
 │   └─ 失败 → 记录错误 → 穷尽重试
 └─ 否 → 穷尽重试
 ↓
检测 Stable Diffusion API Key 是否配置？
 ├─ 是 → 尝试调用 Stable Diffusion
 │   ├─ 成功 → 返回图片
 │   └─ 失败 → 记录错误 → 穷尽重试
 └─ 否 → 穷尽重试
 ↓
生成文字描述占位
```

---

## 二、Flux.1 Dev API 调用模板

### 2.1 BFL API 端点

```python
import requests
import os

BFL_API_KEY = os.environ.get("BFL_API_KEY")
BFL_API_URL = "https://api.bfl.ml/v1/flux-dev"

def generate_with_flux(prompt: str, width: int = 1024, height: int = 768) -> dict:
    headers = {
        "Content-Type": "application/json",
        "X-Key": BFL_API_KEY,
    }
    payload = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "steps": 28,
        "guidance": 3.5,
        "prompt_upsampling": True,
        "safety_tolerance": 2,
        "interval": 2,
        "output_format": "jpeg",
        "seed": None,  # 随机
    }
    resp = requests.post(BFL_API_URL, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()

# 轮询获取结果
result = generate_with_flux("A professional abstract illustration for a research report about AI")
task_id = result["id"]

# 获取结果（需要轮询）
result_url = f"https://api.bfl.ml/v1/get_result?id={task_id}"
while True:
    r = requests.get(result_url, headers={"X-Key": BFL_API_KEY})
    data = r.json()
    if data["status"] == "Ready":
        image_url = data["result"]["sample"]
        break
    elif data["status"] == "Failed":
        raise Exception(f"Generation failed: {data}")
    time.sleep(2)
```

### 2.2 Flux.1 Dev 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `prompt` | string | 必填 | 正向提示词，最长 5000 字符 |
| `width` | int | 1024 | 宽度（64 的倍数，256-1440） |
| `height` | int | 768 | 高度（64 的倍数，256-1440） |
| `steps` | int | 28 | 推理步数（15-50） |
| `guidance` | float | 3.5 | 提示词引导强度（1.5-5.0） |
| `seed` | int | 随机 | 随机种子 |
| `prompt_upsampling` | bool | true | 是否启用提示词增强 |
| `output_format` | string | jpeg | 输出格式（jpeg/png） |

### 2.3 批量生成

```python
async def batch_generate_flux(requests_list: list[dict]) -> list[dict]:
    async def single(prompt, width, height):
        result = await generate_with_flux_async(prompt, width, height)
        return {"prompt": prompt, "url": result["sample"], "status": "ok"}

    tasks = [single(r["prompt"], r.get("width", 1024), r.get("height", 768))
             for r in requests_list]
    return await asyncio.gather(*tasks, return_exceptions=True)
```

---

## 三、Stable Diffusion API 调用模板

### 3.1 Stability AI 托管 API

```python
import requests
import base64
import os

STABILITY_KEY = os.environ.get("STABILITY_API_KEY")

def generate_with_stability(prompt: str, width: int = 1024, height: int = 768) -> bytes:
    resp = requests.post(
        "https://api.stability.ai/v2beta/stable-image/generate/sd3",
        headers={
            "Authorization": f"Bearer {STABILITY_KEY}",
            "Accept": "image/*",
        },
        files={"none": ""},
        data={
            "prompt": prompt,
            "negative_prompt": "low quality, blurry, watermark, text, signature",
            "output_format": "png",
            "aspect_ratio": f"{width}:{height}",
            "model": "sd3.5-large",
            "seed": 0,  # 0 为随机
            "mode": "text-to-image",
        },
    )
    resp.raise_for_status()
    return resp.content

# 保存图片
image_bytes = generate_with_stability(
    "A professional abstract illustration for a research report",
    width=16, height=9
)
with open("illustration.png", "wb") as f:
    f.write(image_bytes)
```

### 3.2 自部署 Stable Diffusion WebUI API

```python
import requests
import base64

SD_WEBUI_URL = "http://localhost:7860"

def generate_with_webui(prompt: str, negative_prompt: str = "",
                        width: int = 1024, height: int = 768,
                        steps: int = 25, cfg_scale: int = 7) -> str:
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "width": width,
        "height": height,
        "steps": steps,
        "cfg_scale": cfg_scale,
        "sampler_name": "DPM++ 2M Karras",
        "batch_size": 1,
    }
    resp = requests.post(f"{SD_WEBUI_URL}/sdapi/v1/txt2img", json=payload)
    resp.raise_for_status()
    data = resp.json()
    image_b64 = data["images"][0]
    return f"data:image/png;base64,{image_b64}"
```

### 3.3 自部署 ComfyUI API

```python
import requests
import json
import uuid

COMFYUI_URL = "http://localhost:8188"

def queue_prompt(prompt_workflow: dict) -> str:
    client_id = str(uuid.uuid4())
    resp = requests.post(f"{COMFYUI_URL}/prompt", json={
        "prompt": prompt_workflow,
        "client_id": client_id,
    })
    return resp.json()["prompt_id"], client_id

def get_image(prompt_id: str, client_id: str, output_node_id: str) -> bytes:
    ws_url = f"ws://localhost:8188/ws?clientId={client_id}"
    # WebSocket 监听执行完成...
    resp = requests.get(f"{COMFYUI_URL}/view", params={
        "filename": f"{output_node_id}_00001_.png",
        "type": "output",
    })
    return resp.content
```

### 3.4 Stable Diffusion 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `prompt` | string | 必填 | 正向提示词 |
| `negative_prompt` | string | "" | 负向提示词（排除的内容） |
| `width` | int | 1024 | 宽度（64 的倍数） |
| `height` | int | 768 | 高度（64 的倍数） |
| `steps` | int | 25 | 采样步数（20-50） |
| `cfg_scale` | float | 7 | 提示词引导强度（1-20） |
| `sampler` | string | DPM++ 2M Karras | 采样器 |
| `seed` | int | -1 | 随机种子（-1 随机） |

---

## 四、提示词工程指南

### 4.1 提示词结构模板

```
[质量前缀], [主体描述], [风格描述], [背景/环境], [光照/氛围], [技术要求], [排除项]
```

### 4.2 按场景的分类模板

#### 配图提示词模板

配图类型由内容语义自动决定，不预设分类。任何内容段落均可触发任意类型的视觉表达。

```
提示词模板（通用）：
[质量前缀], [主体描述], [风格描述], [背景/环境], [光照/氛围], [技术要求], [排除项]

质量前缀：A professional illustration for a research report about [主题]
风格描述：abstract geometric composition / flat vector illustration / infographic style / atmospheric scene（由内容语义自动选择）
配色：[主色系] color palette（从 visual_dna 读取）
背景：clean white background, soft gradient accents
技术要求：high quality, 8k, professional academic illustration
宽高比：--ar 16:9 或 --ar 4:3（由内容语义自动选择）

负向提示词（SD）：
text, watermark, busy, cluttered, low quality, blurry, photorealistic faces, signatures
```

### 4.3 风格关键词库

| 类别 | 关键词 |
|------|--------|
| 学术风格 | academic illustration, clean, professional, scholarly, structured |
| 极简风格 | minimalist, flat design, geometric, simple, zen, bauhaus |
| 科技风格 | futuristic, holographic, wireframe, digital, cyber, data flow |
| 自然风格 | organic, botanical, watercolor, earthy, natural texture, soft |
| 商务风格 | corporate, sleek, professional, glassmorphism, refined |
| 创意风格 | artistic, abstract expressionism, dreamlike, surreal, vibrant |

### 4.4 尺寸规范

| 用途 | 宽高比 | 推荐分辨率 |
|------|--------|-----------|
| 研究报告封面 | 16:9 | 1440×810 |
| 研究报告内页配图 | 4:3 | 1024×768 |
| 幻灯片封面 | 16:9 | 1920×1080 |
| 幻灯片内配图 | 4:3 | 1024×768 |
| 公众号封面 | 2.35:1 | 900×383 |
| 公众号内配图 | 16:9 | 1080×608 |
| 社交媒体卡片 | 1.91:1 | 1200×628 |
| 图标/装饰 | 1:1 | 512×512 |

---

## 五、图片格式与嵌入方式

### 5.1 输出格式选择

| 格式 | 适用场景 | 特点 |
|------|----------|------|
| PNG | 图表、Logo、插图 | 无损、支持透明、文件较大 |
| JPEG | 照片、封面、场景 | 有损、文件小、不支持透明 |
| WebP | Web 嵌入、公众号 | 有损/无损均可、文件最小 |
| SVG | 图标、简单插图 | 矢量、无限缩放、不可 AI 直接生成 |

### 5.2 嵌入方式

#### Markdown 文档嵌入

```markdown
<!-- 本地文件 -->
![配图说明](./illustrations/cover.png)

<!-- Base64 内联（小图） -->
![配图说明](data:image/png;base64,iVBORw0KGgo...)

<!-- 远程 URL -->
![配图说明](https://cdn.example.com/illustrations/cover.png)
```

#### WeasyPrint 文档嵌入

```html
<figure>
  <img src="./illustrations/cover.png" alt="配图说明" style="width:100%">
  <figcaption>图 1：配图说明</figcaption>
</figure>
```

#### Marp 嵌入

```markdown
![配图说明](./illustrations/cover.png)
```

#### HTML/Web 嵌入

```html
<picture>
  <source srcset="./illustrations/diagram.webp" type="image/webp">
  <source srcset="./illustrations/diagram.jpg" type="image/jpeg">
  <img src="./illustrations/diagram.png"
       alt="配图说明"
       width="800"
       height="600"
       loading="lazy">
</picture>

<figcaption>图 1：配图说明</figcaption>
```

---

## 六、质量检查清单

### 6.1 生成前检查

- [ ] 提示词包含质量前缀
- [ ] 提示词包含风格描述
- [ ] 提示词指定了宽高比
- [ ] 负向提示词已配置（SD 专属）
- [ ] API Key 已配置且有效
- [ ] 输出格式与目标用途匹配

### 6.2 生成后检查

- [ ] 图片分辨率满足最低要求（>= 150 DPI 等效）
- [ ] 图片文件大小合理（< 2MB 单张）
- [ ] 无扭曲、畸形或明显 AI 伪影
- [ ] 色彩与文档主题协调
- [ ] 无可见水印或签名
- [ ] 无具名人物面部（隐私合规）
- [ ] Alt 文本已配置

### 6.3 风格一致性检查

- [ ] 同一文档内所有配图风格统一
- [ ] 色调与文档主题色板一致
- [ ] 宽高比合理，无拉伸变形

---

## 穷尽尝试输出规范

当所有 AI 图像生成 API 均不可用时，穷尽尝试 **文字描述的占位表示**，确保文档结构完整可交付。

### 穷尽尝试触发条件

1. Flux.1 Dev API Key 未配置或额度耗尽
2. Stable Diffusion API Key 未配置或不可用
3. 所有 API 调用均失败（网络错误、超时）
4. 目标环境明确要求无 AI 生成图片

### 文字描述占位模板

#### SVG 占位图（推荐首选穷尽尝试）

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="450"
     viewBox="0 0 800 450">
  <rect width="800" height="450" fill="#F0F4F8" rx="8"/>
  <rect x="50" y="50" width="700" height="350" fill="#E2E8F0" rx="4"
        stroke="#CBD5E0" stroke-width="1" stroke-dasharray="8,4"/>
  <text x="400" y="200" text-anchor="middle" font-family="sans-serif"
        font-size="16" fill="#718096">
    配图：[图片描述]
  </text>
  <text x="400" y="235" text-anchor="middle" font-family="sans-serif"
        font-size="12" fill="#A0AEC0">
    分辨率：800×450 | 风格：[风格描述] | 色调：[色调描述]
  </text>
  <text x="400" y="260" text-anchor="middle" font-family="sans-serif"
        font-size="11" fill="#CBD5E0">
    [图片由 AI 生成，当前环境未配置图像模型]
  </text>
</svg>
```

#### Markdown 占位块

```markdown
> 🖼 **配图占位**：`[图片描述]`
>
> - **用途**：配图（类型由内容语义自动决定）
> - **推荐尺寸**：1024×768 (4:3)
> - **风格**：学术极简 / 科技抽象 / 自然氛围
> - **色调**：蓝灰 / 暖色 / 单色系
> - **提示词**：`[生成使用的提示词]`
>
> ⚠ 当前环境未配置 AI 图像模型，此配图需手动生成或替换。
```

### 穷尽尝试质量要求

- 占位图保留完整的尺寸和布局信息
- 提供可复用的 AI 生成提示词
- 明确标注"需要生成"状态
- 占位图不影响文档排版和阅读
- SVG 占位图使用内联样式，无外部依赖
- 颜色使用文档主题色系，保持视觉和谐


---
© 阿洋

---

## 渲染管道调用声明

> **声明**: 本模块（illustration-generator）为渲染管道（`rendering-pipeline/`）的原子化能力组件，挂载于 html-ppt-skill 容器底座之上。
> **调用入口**: 渲染管道启动时，通过 `rendering-pipeline/ARCHITECTURE.md` 路由到本模块。
> **依赖关系**:
> - 上游: `rendering-pipeline/visual-dna.md`（读取配色方案、字体方案、线条质感）
> - 上游: `rendering-pipeline/semantic-auto-detect.md`（接收配图类型标注）
> - 上游: `rendering-pipeline/layout-grid.md`（遵循栅格系统、页面尺寸、边距规范）
> - 上游: `rendering-pipeline/motion-semantic-match.md`（如需要动效，遵循语义匹配规则）
> - 同级: `output/aesthetic-enhancer.md`（美学增强协同）
> **强制规则**: 本模块生成的任何视觉元素必须严格遵循 `visual_dna` 中的配色/字体/间距/线条参数，不得使用硬编码值。