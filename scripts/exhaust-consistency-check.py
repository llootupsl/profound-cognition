#!/usr/bin/env python3
# 作者：阿洋
"""exhaust-consistency-check.py — EXHAUST 一致性扫描脚本

扫描全项目所有 .md/.yml/.yaml/.json/.py 文件，检测违反 EXHAUST 模式四大铁律的
禁用措辞（降级、DEGRADED、fallback、硬终止、终止研究、max_rounds、轮数上限、
最多N次、递归上限、[ESTIMATED] 独立 token 等）。

允许的正面表述（不视为违规）：
  - 不设上限 / 不终止 / 无上限 / 无限制 / 不作为硬终止条件
  - 不丢弃 / 不跳过 / 不降级（否定形式是允许的）

排除禁止清单引用（这些是规则定义本身，必须允许）：
  - SKILL.md 中"EXHAUST 一致性审计规则"节（禁止内容 / 允许内容 / 审计流程）
  - test-prompts.json 中 forbidden_terms 数组

[ESTIMATED] 特殊处理：作为独立 token 检测；当其后紧跟"（已禁止...）"等
标注说明时（即引用规则并标注其已禁止），不视为违规。

v6.0 tok 字段变更（spec Stage 0 Task 0.6）：
  - tasks/ 目录下任务文件的 `tok` 字段已重命名为 `suggested_tok`，语义从
    "硬性预算"变更为"建议预算（非硬性上限）"。
  - 本脚本不将 `tok`/`suggested_tok` 字段视为硬性预算违规。token 预算仅用于
    资源预估与调度参考，不构成 EXHAUST 模式下的终止条件。
  - `suggested_tok` 已加入 ALLOWED_PHRASES，确保含此字段的行不被误报。

用法: python scripts/exhaust-consistency-check.py
退出码: 0=无违规, 1=有违规
"""

import os
import re
import sys
from pathlib import Path

# 跨平台 UTF-8 输出兼容（修复 Windows GBK 编码崩溃）
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Windows 控制台 UTF-8 代码页设置（修复 PowerShell 管道中文乱码）
if sys.platform == "win32":
    import ctypes
    try:
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        ctypes.windll.kernel32.SetConsoleCP(65001)
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).parent.parent

# 扫描的文件扩展名
SCAN_EXTENSIONS = {".md", ".yml", ".yaml", ".json", ".py"}

# 排除的目录（不扫描）
EXCLUDE_DIRS = {
    ".git",
    ".github",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "build",
    "dist",
}

# 排除的文件路径（禁止清单引用所在文件中的特定区域）
# SKILL.md 中"EXHAUST 一致性审计规则"节
SKILL_MD = PROJECT_ROOT / "SKILL.md"
TEST_PROMPTS_JSON = PROJECT_ROOT / "test-prompts.json"

# 禁止措辞模式（正则）
# 注意：顺序重要——更具体的模式优先
FORBIDDEN_PATTERNS = [
    # 降级策略类
    (re.compile(r"降级"), "降级"),
    (re.compile(r"DEGRADED"), "DEGRADED"),
    (re.compile(r"fallback", re.IGNORECASE), "fallback"),
    (re.compile(r"回退"), "回退"),  # P0-3 修复：新增中文"回退"模式扫描
    # 硬终止类
    (re.compile(r"硬终止"), "硬终止"),
    (re.compile(r"终止研究"), "终止研究"),
    # 轮数上限类
    (re.compile(r"max_rounds"), "max_rounds"),
    (re.compile(r"轮数上限"), "轮数上限"),
    (re.compile(r"最多\d+次"), "最多N次"),
    (re.compile(r"递归上限"), "递归上限"),
]

# 允许的正面表述（出现这些时，禁止措辞不算违规）
# 这些是否定形式或正面声明，本身允许
ALLOWED_PHRASES = [
    "不设上限",
    "不终止",
    "无上限",
    "无限制",
    "不作为硬终止条件",
    "不丢弃",
    "不跳过",
    "不降级",
    "不降低质量标准",
    "不降低",
    "不牺牲",
    "不截断",
    "不压缩",
    "不简化",
    "不缩减",
    "不删除",
    "不跳过任何",
    "不丢弃任何",
    # v6.0: suggested_tok 是建议预算字段，非硬性上限，不视为 EXHAUST 违规
    "suggested_tok",
    # 穷尽重试是 EXHAUST 模式的正面行为（穷尽尝试所有替代路径）
    "穷尽重试",
    # v6.0.1: "missing fallback" 是 supervisor-check-tests.py 输出中的检查项名称
    # （指"缺少 fallback 字段"），非 EXHAUST 禁用的"降级策略 fallback"含义。
    # 引用此输出的文档行不应被误报为违规。详见 Audit-6 Wave 1 收尾修复。
    "missing fallback",
    # v6.0.1 P0-3: MAPIE 不可用时的"回退到固定置信度 0.8"是 T13 的标注约束机制
    # （非 EXHAUST 模式的"降级策略"含义），合法 fallback 声明不应被新增的"回退"
    # 模式扫描误报为违规。详见 Audit-6 Wave 5 P0-2 修复。
    "回退到固定置信度",
    # v6.0.1 P0-2: 修复后新增的正面表述，明确声明不设置 MEDIUM 上限、不降低
    # EXHAUST 深度要求、confidence_rating 不可全部为 HIGH 是标注约束而非深度上限。
    "不设置 MEDIUM 上限",
    "不降低 EXHAUST 深度要求",
    "标注约束，非深度上限",
    "标注约束",
    # v6.0.1 P0-3: "返回退出"是编程术语（return exit code），
    # 正则 r"回退" 会误匹配 "返回退出码" 中的 "回退" 子串（中文分词问题）。
    # 包含 "返回退出" 的行应豁免。详见 Audit-6 Wave 5 P0-3 修复。
    "返回退出",
    # v6.0.1 Wave 6: "降级检测" 是审计维度的合法术语（检测是否存在降级行为），
    # 不是使用降级策略。豁免包含此词的行（如 audit-6-summary-check.py L62
    # DIMENSIONS["A6.4"] = "隐式降级检测"）。详见 Audit-6 Wave 6 CI 复跑修复。
    "降级检测",
]

# 否定前缀词（出现在禁止措辞前面时，表示"不要有这个"，是正面表述）
# 检查禁止措辞前 N 个字符内是否包含这些词
NEGATION_PREFIXES = [
    # 单字否定
    "不",
    "无",
    "非",
    "未",
    # 双字否定
    "勿",
    "莫",
    "绝不",
    "切勿",
    "不要",
    "不会",
    "不能",
    "不得",
    "不应",
    "不可",
    "而非",
    # 多字否定/移除类
    "已移除",
    "已禁止",
    "已删除",
    "已替换",
    "已废弃",
    "已弃用",
    "禁止",
    "避免",
    "消除",
    "移除",
    "删除",
    "替换",
    "改为",
    "不存在",
    "不设",
    "不作为",
    "不视为",
    "不做",
    "不是",
    "没有",
    "无需",
    "而非",
    "而不是",
    # 标记符号
    "❌",
    "✗",
    "已禁止",
]

# 否定后缀词（出现在禁止措辞后面时，表示该措辞已被标注为禁止/移除）
NEGATION_SUFFIXES = [
    "已移除",
    "已禁止",
    "已删除",
    "已替换",
    "已废弃",
    "已弃用",
    "（已禁止",
    "(已禁止",
    "（已移除",
    "(已移除",
    "（禁止",
    "(禁止",
    "（不允许",
    "(不允许",
    "（不可使用",
    "(不可使用",
]


def is_in_skill_md_audit_section(file_path, line_number):
    """检查行是否在 SKILL.md 的 EXHAUST 一致性审计规则节内。

    该节从 "## EXHAUST 一致性审计规则" 开始，到下一个 "---" 分隔线或文件末尾结束。
    """
    if not SKILL_MD.exists():
        return False
    try:
        content = SKILL_MD.read_text(encoding="utf-8")
    except Exception:
        return False

    lines = content.split("\n")
    in_section = False
    section_start = -1
    section_end = len(lines)

    for i, line in enumerate(lines, start=1):
        if "## EXHAUST 一致性审计规则" in line:
            in_section = True
            section_start = i
            continue
        if in_section:
            # 节结束于下一个 "---" 分隔线（一级分隔）或下一个 "## " 标题
            if line.strip() == "---" and i > section_start + 1:
                section_end = i
                break
            if line.startswith("## ") and i > section_start:
                section_end = i - 1
                break

    return section_start <= line_number <= section_end


def is_in_test_prompts_forbidden_terms(file_path, line_number):
    """检查行是否在 test-prompts.json 的 forbidden_terms 数组内。"""
    if file_path != TEST_PROMPTS_JSON:
        return False
    if not TEST_PROMPTS_JSON.exists():
        return False

    try:
        content = TEST_PROMPTS_JSON.read_text(encoding="utf-8")
    except Exception:
        return False

    lines = content.split("\n")
    in_array = False
    array_start = -1
    array_end = len(lines)

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if '"forbidden_terms"' in stripped:
            # 查找数组开始
            if "[" in stripped:
                in_array = True
                array_start = i
                if "]" in stripped:
                    array_end = i
                    break
                continue
        if in_array:
            if "]" in stripped:
                array_end = i
                break

    return array_start <= line_number <= array_end


def is_in_exclude_context(file_path, line_number, line_content):
    """检查是否处于应排除的上下文中（禁止清单引用区域）。"""
    # SKILL.md 审计规则节
    if file_path.resolve() == SKILL_MD.resolve():
        if is_in_skill_md_audit_section(file_path, line_number):
            return True

    # test-prompts.json forbidden_terms 数组
    if file_path.resolve() == TEST_PROMPTS_JSON.resolve():
        if is_in_test_prompts_forbidden_terms(file_path, line_number):
            return True

    # v6.0.1 P0-3: 目录级豁免已移至 scan_file 函数开头（文件级豁免），
    # 避免逐行调用 file_path.resolve() 导致性能问题。

    return False


def is_allowed_context(line_content, term, term_pos):
    """检查禁止措辞是否处于允许的上下文中（否定形式或正面表述）。

    判定逻辑：
    1. 检查禁止措辞前 20 个字符内是否有否定前缀词（如"不""无""禁止""已移除"等）
    2. 检查禁止措辞后 15 个字符内是否有否定后缀词（如"已移除""已禁止"等）
    3. 检查同行是否包含允许的正面表述
    4. 检查禁止措辞是否在引号内且同行有否定词（如 '"降级"' 在 '无"降级"' 中）
    5. 检查是否在引号内引用（被引号包围的禁止词是引用而非使用）
    6. 检查是否在规则定义上下文中（"若存在XX → 视为错误"模式）
    7. 检查是否在历史变更说明中（"移除XX""XX→YY"模式）
    """
    # 0. 检查是否为 CSS 字体回退上下文（font fallback）
    # 当 "fallback" 出现在 CSS/排版上下文中时，不视为 EXHAUST 模式违规
    CSS_FONT_KEYWORDS = [
        "font-family", "font_stack", "字体栈", "字体 fallback",
        "中文 fallback", "Fallback 策略", "Fallback 策略",
        "serif", "sans-serif", "SimSun", "SimHei", "宋体", "黑体",
        "Source Serif", "Milo Serif", "Crimson Text", "EB Garamond",
        "Adobe Caslon", "Computer Modern", "Times New Roman",
        "Arial", "Helvetica", "Whitman", "Sohne", "Camphor", "GT America",
        "Noto Serif", "Source Han", "PingFang", "Microsoft YaHei",
        "font-family", "CSS font-family",
        # 扩展：中文排版术语与常见字体名
        "衬线", "无衬线", "等宽", "monospace",
        "Georgia", "TED Serif", "Songti", "Maison Neue",
        "Courier", "字形", "字重", "字体兜底", "跨平台",
        # 扩展：Inter 字体与 UI 文档场景（R2-01 例外）
        "Inter", "fallback 字体", "宿主应用字体", "ui_documentation",
    ]
    # 检查整行是否包含 CSS/排版关键词
    for keyword in CSS_FONT_KEYWORDS:
        if keyword in line_content:
            return True

    # 0.1 检查是否为 CHANGELOG.md 中的历史变更描述
    # CHANGELOG.md 中引用禁用措辞是描述历史修复，不是使用
    CHANGELOG_HISTORY_MARKERS = [
        "EXHAUST 模式违规措辞清理",
        "max_rounds 重命名为",
        "max_rounds: null",
        "rounds_policy: no_limit",
        "清理",
        "重命名",
    ]
    for marker in CHANGELOG_HISTORY_MARKERS:
        if marker in line_content:
            return True

    # 0.2 检查是否为渲染格式适配链上下文（R2-01）
    # 渲染上下文中的 "fallback" 属于格式适配链（format adaptation chain），
    # 不视为 EXHAUST 模式违规——格式变化但内容完整保留 = 允许
    RENDERING_FORMAT_KEYWORDS = [
        "格式适配链", "format adaptation chain", "渲染工具",
        "rendering-tech-stack", "Typst", "WeasyPrint", "Pandoc",
        "Reveal.js", "Slidev", "Marp", "HTML", "Markdown",
        "渲染链", "渲染上下文", "排版引擎", "输出格式",
        "穷尽尝试渲染", "穷尽尝试层", "穷尽重试链",
        "PDF 渲染", "跨格式转换", "排版",
    ]
    for keyword in RENDERING_FORMAT_KEYWORDS:
        if keyword in line_content:
            return True

    # 0.3 检查是否为证据等级降级上下文（evidence level degradation）
    # 证据等级 L0-L3 的升级/降级是域概念，不是 EXHAUST 模式违规
    # 适用文件：evidence-standard-protocol.md, evidence-standards.md,
    #           academic-compliance-protocol.md, TC-102-DeepEval.md,
    #           PaperQA2.md, TM02_causal_verification.md
    EVIDENCE_LEVEL_KEYWORDS = [
        "证据等级", "证据强度", "L0", "L1", "L2", "L3",
        "时效性降级", "地域性降级", "利益相关方降级",
        "时效性", "地域性", "利益相关方",
        "置信度", "degradation_note", "处方",
        "升级/降级", "升级与降级", "降级规则", "降级幅度",
        "降级因素", "降级触发", "降级说明",
        "Gate-终", "C 级", "C级",
        "证据等级动态治理", "验证失败降级", "冲突降级",
        "降级决策树", "降级计算", "降级条件",
        "时效降级", "地域降级",
        "地域适用性", "跨地域", "地域适配性",
        "必要时降级",
    ]
    for keyword in EVIDENCE_LEVEL_KEYWORDS:
        if keyword in line_content:
            return True

    # 0.4 检查是否为 LangGraph 递归上限上下文
    # LangGraph 框架的 recursion_limit 是引擎参数，不是 EXHAUST 模式违规
    # 适用文件：execution-protocol.md, TC-100-LangGraph.md, cycle-detection-check.py
    LANGGRAPH_KEYWORDS = [
        "LangGraph", "recursion_limit", "cycle-detection",
        "循环检测", "状态指纹", "DAG", "Kahn",
        "RecursionError", "图的最大执行步数",
        "R9-05", "条件边",
        "执行时设置", "留足余量", "58 节点",
    ]
    for keyword in LANGGRAPH_KEYWORDS:
        if keyword in line_content:
            return True

    # 0.5 检查是否为能力卡回退路径上下文
    # MC-*/TC-* 能力卡中"降级到 LLM 内建能力"是域概念
    # 适用文件：knowledge/external-capabilities/MC-*.md, TC-*.md
    CAPABILITY_FALLBACK_KEYWORDS = [
        "回退路径", "LLM 内建", "INTERNAL_REASONING",
        "能力卡", "MC-", "TC-",
        "LLM_INTERNAL_REASONING",
    ]
    for keyword in CAPABILITY_FALLBACK_KEYWORDS:
        if keyword in line_content:
            return True

    # 0.6 检查是否为脚本字段名上下文
    # fallback_strategy, fallback_recommendation 等是变量名/字段名
    # 适用文件：capability-binding-check.py, kg-availability-check.py,
    #           lightrag-adapter.md, config.yaml, T19_check.yml,
    #           supervisor-check-tests.py, T08-T13 任务文件
    SCRIPT_FIELD_KEYWORDS = [
        "fallback_strategy", "fallback_recommendation",
        "missing_fallback", "final_fallback",
        "fallback_count", "fallback_annotation",
        "fallback_reason", "L6_VECTOR_FALLBACK",
        "calibration_fallback", "severity",
        "LIGHT_RAG", "LIGHT_RAG_NAIVE_FALLBACK",
        "LIGHT_RAG_LOCAL_FALLBACK", "LIGHT_RAG_HYBRID_FALLBACK",
        "NO_MAPIE_CALIB", "CALIB_SMALL",
        "mapie_calibration", "calibration_check",
    ]
    for keyword in SCRIPT_FIELD_KEYWORDS:
        if keyword in line_content:
            return True

    # 0.7 检查是否为任务文件状态字段上下文
    # success|failed|timeout|fallback 是状态枚举
    # 适用文件：tasks/T08-T13, T19, TM02
    TASK_STATUS_KEYWORDS = [
        "success|failed|timeout|fallback",
        "回退到", "naive 查询", "hybrid 查询", "local 查询",
        "LightRAG", "回退标注",
        "complexity_score", "COMPLEXITY_SCORE_MISSING",
    ]
    for keyword in TASK_STATUS_KEYWORDS:
        if keyword in line_content:
            return True

    # 0.8 检查是否为插件错误处理上下文
    # 插件安装失败时的回退策略是错误处理，不是研究质量降级
    # 适用文件：llmlingua-compressor.md
    PLUGIN_ERROR_HANDLING_KEYWORDS = [
        "安装失败", "规则驱动", "环境不可用",
        "python-pptx 不可用", "浏览器环境不可用",
    ]
    for keyword in PLUGIN_ERROR_HANDLING_KEYWORDS:
        if keyword in line_content:
            return True

    # 0.9 检查是否为 Gate 失败回退机制上下文
    # Gate 失败精准回退（R7-05）是 supervisor_protocol.md 的合法错误处理机制，
    # 不视为 EXHAUST 模式违规。
    # 适用文件：supervisor_protocol.md, execution-protocol.md,
    #           append-protocol-test-cases.py, capability-binding-check.py,
    #           kg-availability-check.py, version-diff-tool.py,
    #           tasks/T01d, T20a, T21, TM06b,
    #           lightrag-adapter.md, dlp-retriever.md, capability-version-sync.md
    GATE_ROLLBACK_KEYWORDS = [
        # Gate 失败回退机制
        "Gate 失败回退", "Gate 失败精准回退", "精准回退",
        "Gate-α", "Gate-β", "Gate-γ", "Gate 检查项失败",
        "R7-05",
        # rollback 字段名
        "rollback", "rollback_id", "rollback_nodes",
        "rollback_scope", "rollback_strategy",
        # 回退机制术语
        "回退节点", "回退列表", "回退范围", "回退策略",
        "回退日志", "回退执行流程", "回退规则", "回退唯一标识",
        "回退行为", "回退动作", "回退声明", "回退链",
        "回退层级", "失败回退策略", "失败回退",
        # 任务文件中的合法回退流程
        "HKR 误判回退", "误判回退",
        "回退执行", "回退补齐", "回退至对应节点",
        "可回退", "可追溯、可回退",
        "检索回退策略", "检索回退",
        "推荐回退层级",
        "blocking 优先",
        # v6.0.1 P0-3 补充：supervisor_protocol.md 中的合法回退描述
        "仅回退", "全量回退", "回退这些",
        # v6.0.1 P0-3 补充：dlp-retriever.md 中的格式适配链回退表
        "回退表",
    ]
    for keyword in GATE_ROLLBACK_KEYWORDS:
        if keyword in line_content:
            return True

    # 1. 检查否定前缀：禁止措辞前 20 个字符内是否有否定词
    prefix_start = max(0, term_pos - 20)
    prefix = line_content[prefix_start:term_pos]
    for neg in NEGATION_PREFIXES:
        if neg in prefix:
            return True

    # 2. 检查否定后缀：禁止措辞后 15 个字符内是否有标注词
    suffix_end = min(len(line_content), term_pos + len(term) + 15)
    suffix = line_content[term_pos:suffix_end]
    for neg in NEGATION_SUFFIXES:
        if neg in suffix:
            return True

    # 3. 检查同行是否包含允许的正面表述
    for allowed in ALLOWED_PHRASES:
        if allowed in line_content:
            return True

    # 4. 检查同行是否包含其他否定词（即使不在前缀位置）
    # 例如 "全程无'降级''DEGRADED'" 中，"无" 不在 "降级" 前 20 字符内
    # 但同行有 "无" 字，表示是正面表述
    line_negation_markers = [
        "无", "不", "禁止", "而非", "而不是", "已移除", "已禁止",
        "不存在", "不设", "不做", "没有", "❌", "✗",
    ]
    for marker in line_negation_markers:
        if marker in line_content:
            return True

    # 5. 检查是否在引号内引用（被引号包围的禁止词是引用而非使用）
    # 例如："硬终止"、"降级"、`max_rounds_guard`
    # 检查禁止措辞前后是否紧邻引号
    if term_pos > 0:
        prev_char = line_content[term_pos - 1]
        # 中文引号、英文引号、反引号
        if prev_char in ('"', '"', '"', "'", "`", "「", "『"):
            # 检查后面是否也有引号闭合
            after_pos = term_pos + len(term)
            if after_pos < len(line_content):
                next_char = line_content[after_pos]
                if next_char in ('"', '"', '"', "'", "`", "」", "』"):
                    return True

    # 6. 检查是否在规则定义上下文中（"若存在XX → 视为错误"模式）
    # 例如：若其他协议文件中存在轮数上限 → 视为错误
    rule_def_patterns = [
        "若存在", "若其他", "视为错误", "视为违规", "应当移除",
        "应当删除", "应当替换", "应视为", "删除上限", "删除该参数",
        "替换为", "删除回退", "→ 视为",
    ]
    for pattern in rule_def_patterns:
        if pattern in line_content:
            return True

    # 7. 检查是否在历史变更说明中（"移除XX""XX→YY"模式）
    # 例如：移除 context-budget-protocol 中"硬终止"
    # 例如："硬终止"→"强制落盘"
    history_patterns = [
        "移除", "修复", "→", "改为", "替换为", "原", "旧",
        "已改为", "已替换", "已修复", "已移除",
    ]
    for pattern in history_patterns:
        if pattern in line_content:
            return True

    return False


def check_estimated_token(line_content):
    """检测 [ESTIMATED] 作为独立 token 的使用。

    特殊处理：当 [ESTIMATED] 后紧跟"（已禁止...）"等标注说明时，
    视为引用规则并标注其已禁止，不视为违规。

    返回: (违规位置起始索引, 违规描述) 或 None
    """
    # 匹配 [ESTIMATED] 后跟 "（已禁止" 或 "(已禁止" 或 "（禁止" 或 "(禁止" 的标注形式
    # 这种是引用规则并标注已禁止，允许
    annotated_pattern = re.compile(
        r"\[ESTIMATED\]\s*[（(]\s*(?:已\s*禁止|禁止|不允许|不可使用)"
    )
    annotated_matches = list(annotated_pattern.finditer(line_content))
    annotated_spans = [m.span() for m in annotated_matches]

    # 匹配所有 [ESTIMATED] 出现
    token_pattern = re.compile(r"\[ESTIMATED\]")
    for m in token_pattern.finditer(line_content):
        start, end = m.span()
        # 检查是否处于标注形式中
        is_annotated = False
        for ann_start, ann_end in annotated_spans:
            if ann_start <= start < ann_end:
                is_annotated = True
                break
        if not is_annotated:
            # 检查是否处于允许的上下文中（与禁止措辞同样的判定逻辑）
            if is_allowed_context(line_content, "[ESTIMATED]", start):
                continue
            return (start, "[ESTIMATED]")
    return None


# ============================================================================
# 字数声明一致性检测（spec v6 Task 6）
# 真相源：SKILL.md §0.1
#   - research_report 总字数门槛：≥100000 字
#   - wechat_article  总字数门槛：≥3000 字
#   - course_material 总字数门槛：≥50000 字
# ============================================================================

# 产品类型 -> (中文名, 英文名, 应为字数)
WORD_COUNT_THRESHOLDS = {
    "research_report": ("研究报告", "research_report", 100000),
    "wechat_article":  ("公众号文章", "wechat_article", 3000),
    "course_material": ("课程材料", "course_material", 50000),
}

# 字数声明一致性检测的排除上下文标记
# 出现这些标记的行不视为字数违规（它们是部分级地板、技术参数等）
# 依据 SKILL.md §0.1 C 节定义的部分字数地板与其他技术性数值
WORD_COUNT_EXCLUDE_MARKERS = [
    "§",              # 部分级字数地板（§1/§3/§4/§5/§6/§7/§8 各部分地板）
    "章节集群",        # T20a 分批落盘大小上下文
    "约8000-22000",   # 章节集群字数范围（T20a）
    "timeout",        # 技术参数（如 qdrant-adapter.md 中 timeout: 15000 ms）
    "token",          # 上下文 token 数预算（如 nrsf-protocol.md 中 token 数 ≥ 8000）
    "T09",            # T09 认知推理字数（T20a 渲染表中的部分字数 ≥3000字）
    # 审计报告与 CHANGELOG 中的修复历史记录标记（引用旧值作为"修复前"描述，合法）
    "修复前",
    "修复后",
    "矛盾",
    "严重错误",
    "旧值",
    "从 `",
    "为 `",
]


def _is_word_count_excluded(line_content):
    """检查行是否处于字数检测的排除上下文中。

    命中任一排除标记即返回 True。排除标记覆盖：
    - 部分级字数地板（§1/§3/§4 ≥8000, §5 ≥30000, §6 ≥12000, §7/§8 ≥6000）
    - 章节集群字数（约8000-22000字）
    - 技术参数（timeout: 15000）
    - 上下文 token 数（token 数 ≥ 8000）
    - T09 认知推理字数（T09 认知推理 ... ≥3000字）
    """
    line_lower = line_content.lower()
    for marker in WORD_COUNT_EXCLUDE_MARKERS:
        if marker.lower() in line_lower:
            return True
    return False


def check_word_count_consistency(file_path, content, violations):
    """检测字数声明一致性违规（spec v6 Task 6）。

    基于 SKILL.md §0.1 真相源检测三种产品类型的总字数门槛：
      - research_report: ≥100000 字
      - wechat_article:  ≥3000 字
      - course_material: ≥50000 字

    检测模式（中英文均覆盖）：
      - 研究报告 / research_report  后跟 [≥>=] N 字?
      - 公众号文章 / wechat_article  后跟 [≥>=] N 字?
      - 课程材料 / course_material   后跟 [≥>=] N 字?

    排除规则（不视为违规）：
      - 部分级字数地板（§1/§3/§4 ≥8000, §5 ≥30000, §6 ≥12000, §7/§8 ≥6000）
      - 章节集群字数（约8000-22000字）
      - 技术参数（timeout: 15000）
      - 上下文 token 数（token 数 ≥ 8000）
      - T09 认知推理字数（T09 认知推理 ... ≥3000字）

    违规将追加到 violations 列表，格式为 4 元组：
      (line_num, "WORD_COUNT_VIOLATION", line_content, {
          "description": str, "current": int, "expected": int
      })
    """
    lines = content.split("\n")

    # 为每种产品类型构建中英文检测正则
    patterns = []
    for product_type, (cn_name, en_name, expected) in WORD_COUNT_THRESHOLDS.items():
        # 中文模式：研究报告 [≥>=] N 字?
        cn_pattern = re.compile(
            rf"{re.escape(cn_name)}\s*[≥>]=?\s*(\d+)\s*字?"
        )
        patterns.append((cn_pattern, cn_name, product_type, expected))
        # 英文模式：research_report [≥>=] N 字?
        en_pattern = re.compile(
            rf"{re.escape(en_name)}\s*[≥>]=?\s*(\d+)\s*字?"
        )
        patterns.append((en_pattern, en_name, product_type, expected))

    for line_idx, line in enumerate(lines, start=1):
        # 排除上下文检查（部分级地板、技术参数等）
        if _is_word_count_excluded(line):
            continue

        for pattern, name, product_type, expected in patterns:
            for m in pattern.finditer(line):
                current_str = m.group(1)
                try:
                    current = int(current_str)
                except ValueError:
                    continue

                # 数值与真相源不一致即违规
                if current != expected:
                    description = f"{name}总字数门槛不一致"
                    violations.append((
                        line_idx,
                        "WORD_COUNT_VIOLATION",
                        line.rstrip(),
                        {
                            "description": description,
                            "current": current,
                            "expected": expected,
                        }
                    ))


def scan_file(file_path):
    """扫描单个文件，返回违规列表。

    返回: [(line_number, term, line_content, extra?), ...]
      - 禁止措辞 / [ESTIMATED] 违规：3 元组 (line_no, term, line_content)
      - 字数一致性违规：4 元组 (line_no, "WORD_COUNT_VIOLATION", line_content, {
            "description": str, "current": int, "expected": int
        })
    """
    violations = []

    # v6.0.1 P0-3: 文件级目录豁免（性能优化）
    # 如果文件在豁免目录中，直接返回空违规列表，避免逐行调用 file_path.resolve()
    try:
        rel_path = file_path.resolve().relative_to(PROJECT_ROOT.resolve())
        parts = rel_path.parts
        if len(parts) >= 2:
            if (parts[0] == "docs" and parts[1] in ("audit-logs", "version_history")):
                return violations
            if (parts[0] == "knowledge" and parts[1] == "external-capabilities"):
                return violations
        if file_path.name == "CHANGELOG.md":
            return violations
    except ValueError:
        pass

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        # 编码错误等，跳过该文件
        return violations

    lines = content.split("\n")

    # v6.0.1 P0-3: 性能优化——只对 SKILL.md 和 test-prompts.json 逐行检查排除上下文
    # 其他文件不需要逐行检查 is_in_exclude_context（resolve() 调用很慢）
    need_exclude_check = False
    if file_path.name in ("SKILL.md", "test-prompts.json"):
        try:
            resolved_fp = file_path.resolve()
            if resolved_fp == SKILL_MD.resolve() or resolved_fp == TEST_PROMPTS_JSON.resolve():
                need_exclude_check = True
        except Exception:
            pass

    for line_idx, line in enumerate(lines, start=1):
        # 检查是否在排除上下文中（仅对 SKILL.md / test-prompts.json）
        if need_exclude_check:
            in_exclude = is_in_exclude_context(file_path, line_idx, line)
            if in_exclude:
                continue

        # 检查每个禁止措辞模式
        for pattern, term_name in FORBIDDEN_PATTERNS:
            for m in pattern.finditer(line):
                term_pos = m.start()
                # 检查是否处于允许的上下文（否定形式等）
                if is_allowed_context(line, term_name, term_pos):
                    continue
                # 检查是否在引用禁止清单的上下文中
                # （例如 README 中描述"移除了硬终止"这种历史说明）
                # 这种情况由具体上下文判断，这里依赖 is_in_exclude_context
                violations.append((line_idx, term_name, line.rstrip()))

        # 检查 [ESTIMATED] 独立 token
        est_result = check_estimated_token(line)
        if est_result is not None:
            pos, term_name = est_result
            violations.append((line_idx, term_name, line.rstrip()))

    # 检查字数声明一致性（spec v6 Task 6）
    # 注意：字数检测独立于上面的逐行排除上下文，因为它有自己的排除规则
    check_word_count_consistency(file_path, content, violations)

    return violations


# ============================================================================
# execution_params 字段一致性检测（spec v6.0 Stage 1 Task 1.2, R2-05）
# 防深度缩水：每个任务文件的 output_schema 必须包含 execution_params 字段
# ============================================================================

TASKS_DIR = PROJECT_ROOT / "tasks"


def check_execution_params_in_tasks():
    """扫描 tasks/ 目录下所有任务文件，检测 output_schema 中是否包含 execution_params 字段。

    缺失 execution_params 字段的任务文件将被报告为违规（深度缩水风险）。

    返回: [(rel_path, violation_description), ...]
    """
    violations = []

    if not TASKS_DIR.exists():
        return violations

    task_files = sorted(TASKS_DIR.glob("*.md"))
    for task_file in task_files:
        try:
            content = task_file.read_text(encoding="utf-8")
        except Exception:
            continue

        # 检查文件中是否包含 execution_params 字段定义
        if "execution_params" not in content:
            try:
                rel_path = task_file.relative_to(PROJECT_ROOT)
            except ValueError:
                rel_path = task_file
            violations.append((
                rel_path,
                "output_schema 中缺失 execution_params 字段（R2-05 防深度缩水）"
            ))

    return violations


def should_scan_file(file_path):
    """判断文件是否应被扫描。"""
    # 检查扩展名
    if file_path.suffix.lower() not in SCAN_EXTENSIONS:
        return False

    # 检查是否在排除目录中
    try:
        rel = file_path.relative_to(PROJECT_ROOT)
    except ValueError:
        return False

    parts = rel.parts
    for part in parts:
        if part in EXCLUDE_DIRS:
            return False

    # 排除本脚本自身
    if file_path.name == "exhaust-consistency-check.py" and "scripts" in parts:
        return False

    return True


def collect_files():
    """收集所有需要扫描的文件。"""
    files = []
    for root, dirs, filenames in os.walk(PROJECT_ROOT):
        # 过滤排除目录
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for filename in filenames:
            file_path = Path(root) / filename
            if should_scan_file(file_path):
                files.append(file_path)
    return files


def main():
    print("=" * 60)
    print("Profound Cognition — EXHAUST 一致性扫描")
    print("=" * 60)

    if not PROJECT_ROOT.exists():
        print(f"[ERROR] 项目根目录不存在: {PROJECT_ROOT}")
        sys.exit(2)

    files = collect_files()
    print(f"\n[扫描] 共发现 {len(files)} 个待扫描文件")

    all_violations = []
    files_with_violations = 0
    word_count_violation_count = 0

    for file_path in files:
        try:
            rel_path = file_path.relative_to(PROJECT_ROOT)
        except ValueError:
            rel_path = file_path

        violations = scan_file(file_path)
        if violations:
            files_with_violations += 1
            all_violations.append((rel_path, violations))
            # 统计字数一致性违规数
            for v in violations:
                if len(v) >= 4 and v[1] == "WORD_COUNT_VIOLATION":
                    word_count_violation_count += 1

    # execution_params 字段一致性检测（spec v6.0 Stage 1 Task 1.2, R2-05）
    exec_params_violations = check_execution_params_in_tasks()
    exec_params_violation_count = len(exec_params_violations)

    print(f"\n[结果] 扫描完成")
    print(f"  扫描文件数: {len(files)}")
    print(f"  违规文件数: {files_with_violations}")
    total_violations = sum(len(v) for _, v in all_violations)
    print(f"  违规总数: {total_violations}")
    print(f"  其中字数一致性违规: {word_count_violation_count}")
    print(f"  其中 execution_params 缺失违规: {exec_params_violation_count}")

    has_violations = bool(all_violations) or bool(exec_params_violations)

    if all_violations:
        print("\n" + "-" * 60)
        print("违规详情:")
        print("-" * 60)
        for rel_path, violations in all_violations:
            print(f"\n📄 {rel_path}")
            for v in violations:
                # 兼容 3 元组（禁止措辞）和 4 元组（字数一致性）
                if len(v) >= 4 and v[1] == "WORD_COUNT_VIOLATION":
                    line_no, term, line_content, extra = v
                    display_line = line_content.strip()
                    if len(display_line) > 120:
                        display_line = display_line[:117] + "..."
                    print(
                        f"  L{line_no} [{term}]: {display_line} "
                        f"(当前值: {extra['current']}, 应为: {extra['expected']})"
                    )
                else:
                    line_no, term, line_content = v[0], v[1], v[2]
                    display_line = line_content.strip()
                    if len(display_line) > 120:
                        display_line = display_line[:117] + "..."
                    print(f"  L{line_no} [{term}]: {display_line}")

    if exec_params_violations:
        if not all_violations:
            print("\n" + "-" * 60)
            print("违规详情:")
            print("-" * 60)
        print("\n📄 execution_params 字段缺失（R2-05 防深度缩水）:")
        for rel_path, desc in exec_params_violations:
            print(f"  {rel_path}: {desc}")

    total_with_exec = total_violations + exec_params_violation_count
    if has_violations:
        print("\n" + "=" * 60)
        print(f"❌ 扫描未通过: {total_with_exec} 处违规")
        print("=" * 60)
        sys.exit(1)
    else:
        print("\n" + "=" * 60)
        print("✅ 扫描通过: 无违规")
        print("=" * 60)
        sys.exit(0)


if __name__ == "__main__":
    main()
