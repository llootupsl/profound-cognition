#!/usr/bin/env python3
# 作者：阿洋
"""capability-binding-check.py — 能力卡与任务绑定补全检查（D1.4.3/D7.4.x）

扫描 knowledge/external-capabilities/ 下所有能力卡，检查：
  1. 每个能力卡是否有 consumer_nodes / 消费节点 字段
  2. consumer_nodes 中的节点是否在 SKILL.md DAG 中存在
  3. 输出未绑定能力卡清单

同时检测 D7.4.1/D7.4.2/D7.4.3 字段（prerequisites/fallback_strategy/effect_metrics）的覆盖情况。

退出码:
  0 = 全部通过（未绑定卡为 WARNING，不阻塞）
  1 = 存在无效绑定（consumer_nodes 引用了不存在的 DAG 节点）

用法: python scripts/capability-binding-check.py
"""

import re
import sys
from pathlib import Path

# 跨平台 UTF-8 输出兼容
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

if sys.platform == "win32":
    import ctypes
    try:
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        ctypes.windll.kernel32.SetConsoleCP(65001)
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).parent.parent
CAPABILITIES_DIR = PROJECT_ROOT / "knowledge" / "external-capabilities"
ABILITY_CARDS_FILE = PROJECT_ROOT / "output" / "ability-cards.md"
SKILL_MD = PROJECT_ROOT / "SKILL.md"

# 非能力卡文件（索引/消费者文件，不需要 consumer_nodes）
NON_CAPABILITY_FILES = {
    "last30days-skill-consumer.md",
    "external-capabilities-index.md",
}


def parse_dag_nodes(skill_md_path):
    """从 SKILL.md 的 DAG 拓扑 YAML 块中解析全部 node_id。"""
    if not skill_md_path.exists():
        return set()

    content = skill_md_path.read_text(encoding="utf-8")
    yaml_blocks = re.findall(r'```yaml\n(.*?)```', content, re.DOTALL)

    node_ids = set()
    for block in yaml_blocks:
        if 'dag_topology' not in block:
            continue
        matches = re.findall(r'-\s*node_id:\s+"([^"]+)"', block)
        node_ids.update(matches)

    return node_ids


def parse_consumer_nodes(content):
    """从能力卡内容中解析 consumer_nodes / 消费节点字段。

    支持以下格式:
      1. ## 消费节点 下的列表项或表格
      2. ### 消费此卡片的 DAG 节点 下的列表项或表格
      3. ### 消费此卡片的领域引擎 下的列表项或表格
      4. consumer_nodes: YAML 字段
      5. consumer_nodes: [T01, T02] YAML 数组

    表格格式支持:
      | 节点 | 用途 |
      |------|------|
      | T02 | 文献检索 |
    """
    consumer_nodes = set()

    # 节点 ID 提取正则（支持 T01, T00b, TM02, I01 等）
    node_id_regex = r'\b(T\d+[a-z]?|TM\d+[a-z]?|I\d+|T_\w+|T\d+_output_guard|T\d+d_\w+)\b'

    # 格式 1 & 2 & 3: Markdown 标题下的列表项或表格
    # 允许标题后有空行（\n+），支持列表（- 开头）和表格（| 开头）两种格式
    patterns_md = [
        # 列表格式
        r'##\s*消费节点\s*\n+((?:-\s*.+\n)+)',
        r'###\s*消费此卡片的\s*DAG\s*节点\s*\n+((?:-\s*.+\n)+)',
        r'###\s*消费此卡片的领域引擎\s*\n+((?:-\s*.+\n)+)',
        # 表格格式
        r'##\s*消费节点\s*\n+((?:\|[^\n]*\|\s*\n)+)',
        r'###\s*消费此卡片的\s*DAG\s*节点\s*\n+((?:\|[^\n]*\|\s*\n)+)',
        r'###\s*消费此卡片的领域引擎\s*\n+((?:\|[^\n]*\|\s*\n)+)',
    ]
    for pattern in patterns_md:
        matches = re.findall(pattern, content)
        for match in matches:
            if '|' in match:
                # 表格格式：遍历每一行，提取节点 ID
                # 表头行（含"节点"）和分隔行（|---|）不会匹配节点 ID 正则，无需特殊处理
                for line in match.split('\n'):
                    line = line.strip()
                    if line.startswith('|'):
                        node_matches = re.findall(node_id_regex, line)
                        consumer_nodes.update(node_matches)
            else:
                # 列表格式：提取列表项中的节点 ID
                items = re.findall(r'-\s*(.+?)(?:\s*$|\s*#)', match, re.MULTILINE)
                for item in items:
                    item = item.strip()
                    node_matches = re.findall(node_id_regex, item)
                    consumer_nodes.update(node_matches)

    # 格式 3: consumer_nodes: YAML 字段
    yaml_match = re.search(r'consumer_nodes:\s*\n((?:\s+-\s+.+\n)+)', content)
    if yaml_match:
        items = re.findall(r'-\s*[\'"]?([^\'"\n]+)[\'"]?', yaml_match.group(1))
        for item in items:
            consumer_nodes.add(item.strip())

    # 格式 4: consumer_nodes: [T01, T02] YAML 数组
    array_match = re.search(r'consumer_nodes:\s*\[([^\]]+)\]', content)
    if array_match:
        items = re.findall(r'[\'"]?([^\'"\],]+)[\'"]?', array_match.group(1))
        for item in items:
            consumer_nodes.add(item.strip())

    # 也匹配 "supervisor protocol" 等非节点消费者（不算 DAG 节点）
    # 只保留看起来像节点 ID 的引用
    valid_node_pattern = re.compile(r'^(T\d+[a-z]?|TM\d+[a-z]?|I\d+|T_\w+)$')
    dag_consumer_nodes = {n for n in consumer_nodes if valid_node_pattern.match(n)}

    return dag_consumer_nodes, consumer_nodes


def check_field(content, field_names):
    """检查能力卡内容中是否包含指定字段。"""
    for name in field_names:
        if name in content:
            return True
    return False


def parse_ability_cards(ability_cards_path):
    """【A6.3-F1 / P1-1 修复，Wave 5】解析 output/ability-cards.md 中的 AC-XX 能力映射卡。

    返回:
      ac_cards: list[dict]，每个 dict 含 id (AC-XX) / name / category / description
      parse_errors: list[str]，解析错误（编号重复/格式错误等）
    """
    ac_cards = []
    parse_errors = []
    seen_ids = {}

    if not ability_cards_path.exists():
        parse_errors.append(f"能力映射卡文件不存在: {ability_cards_path}")
        return ac_cards, parse_errors

    content = ability_cards_path.read_text(encoding="utf-8")
    # 表格行格式: | AC-01 | 第一性原理 | 认知策略 | 从基本原理出发重构问题 |
    # 匹配: | AC-数字 | 名称 | 分类 | 描述 |
    table_row_re = re.compile(
        r'^\|\s*(AC-\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*$',
        re.MULTILINE
    )

    matches = table_row_re.findall(content)
    for ac_id, name, category, description in matches:
        # 跳过表头行（如"AC-XX"或"编号"）
        if ac_id.upper() == 'AC-XX' or name.strip() == '卡片名称':
            continue
        if ac_id in seen_ids:
            parse_errors.append(f"AC-XX 编号重复: {ac_id}（首次出现于 {seen_ids[ac_id]}）")
            continue
        seen_ids[ac_id] = name.strip()
        ac_cards.append({
            'id': ac_id,
            'name': name.strip(),
            'category': category.strip(),
            'description': description.strip(),
        })

    # 检查编号连续性（AC-01 至 AC-N）
    if ac_cards:
        numbers = sorted(int(re.match(r'AC-(\d+)', c['id']).group(1)) for c in ac_cards)
        expected = list(range(1, max(numbers) + 1))
        missing = set(expected) - set(numbers)
        if missing:
            parse_errors.append(
                f"AC-XX 编号不连续，缺失: {sorted(missing)}"
            )

    return ac_cards, parse_errors


def main():
    errors = []
    warnings = []

    # 解析 DAG 节点
    dag_nodes = parse_dag_nodes(SKILL_MD)
    if not dag_nodes:
        errors.append("无法从 SKILL.md 解析 DAG 节点")
        print("FAIL: 无法解析 DAG 节点")
        sys.exit(1)

    # 扫描能力卡
    if not CAPABILITIES_DIR.exists():
        errors.append("knowledge/external-capabilities/ 目录不存在")
        print("FAIL: 目录不存在")
        sys.exit(1)

    card_files = sorted(CAPABILITIES_DIR.glob("*.md"))
    # 过滤非能力卡文件
    card_files = [f for f in card_files if f.name not in NON_CAPABILITY_FILES]

    # 【A6.3-F1 / P1-1 修复，Wave 5】扫描 AC-XX 能力映射卡（output/ability-cards.md）
    ac_cards, ac_parse_errors = parse_ability_cards(ABILITY_CARDS_FILE)

    unbound_cards = []
    invalid_bindings = []
    missing_prereq = []
    missing_fallback = []
    missing_metrics = []

    for card_file in card_files:
        content = card_file.read_text(encoding="utf-8")
        card_name = card_file.stem

        # 检查 consumer_nodes
        dag_consumers, all_consumers = parse_consumer_nodes(content)

        # 检查是否存在消费节点/消费关系 section（即使内容为"暂无..."也视为已声明）
        has_consumer_section = bool(re.search(
            r'##\s*消费节点|###\s*消费此卡片的\s*DAG\s*节点|###\s*消费此卡片的领域引擎|##\s*消费关系',
            content
        ))

        if not dag_consumers and not all_consumers and not has_consumer_section:
            unbound_cards.append(card_name)
        elif dag_consumers:
            # 检查引用的节点是否在 DAG 中存在
            invalid_nodes = dag_consumers - dag_nodes
            if invalid_nodes:
                invalid_bindings.append((card_name, invalid_nodes))

        # 检查 D7.4.1 调用前置条件（"## 依赖" section 视为等价前置条件声明）
        if not check_field(content, ['调用前置条件', 'prerequisites', '## 依赖', '## 前置条件']):
            missing_prereq.append(card_name)

        # 检查 D7.4.2 失败回退策略
        if not check_field(content, ['失败回退', 'fallback_strategy', '穷尽重试策略', '穷尽重试替代路径']):
            missing_fallback.append(card_name)

        # 检查 D7.4.3 效果度量
        if not check_field(content, ['效果度量', 'effect_metrics']):
            missing_metrics.append(card_name)

    # 输出
    print("=" * 60)
    print("能力卡与任务绑定检查（D1.4.3/D7.4.x）")
    print("=" * 60)
    print(f"  DAG 节点数:              {len(dag_nodes)}")
    print(f"  基础能力卡数:            {len(card_files)}")
    print(f"  AC-XX 能力映射卡数:      {len(ac_cards)}")
    print(f"  总能力卡数（基础+映射）: {len(card_files) + len(ac_cards)}")
    print(f"  已绑定 consumer_nodes:   {len(card_files) - len(unbound_cards)}")
    print(f"  未绑定能力卡:            {len(unbound_cards)}")
    print(f"  无效绑定:                {len(invalid_bindings)}")
    print(f"  缺少 调用前置条件(D7.4.1): {len(missing_prereq)}")
    print(f"  缺少 失败回退(D7.4.2):    {len(missing_fallback)}")
    print(f"  缺少 效果度量(D7.4.3):    {len(missing_metrics)}")
    print(f"  AC-XX 解析错误:          {len(ac_parse_errors)}")

    if unbound_cards:
        print(f"\n--- 未绑定能力卡（WARNING, {len(unbound_cards)} 个）---")
        for card in unbound_cards[:20]:
            print(f"  ⚠ {card}")
        if len(unbound_cards) > 20:
            print(f"  ... 还有 {len(unbound_cards) - 20} 个")

    if invalid_bindings:
        print(f"\n--- 无效绑定（ERROR, {len(invalid_bindings)} 个）---")
        for card, invalid in invalid_bindings:
            print(f"  ✗ {card}: 引用了不存在的节点 {sorted(invalid)}")

    if missing_prereq:
        print(f"\n--- 缺少 调用前置条件 D7.4.1（{len(missing_prereq)} 个）---")
        for card in missing_prereq[:10]:
            print(f"  ℹ {card}")
        if len(missing_prereq) > 10:
            print(f"  ... 还有 {len(missing_prereq) - 10} 个")

    if missing_fallback:
        print(f"\n--- 缺少 失败回退 D7.4.2（{len(missing_fallback)} 个）---")
        for card in missing_fallback[:10]:
            print(f"  ℹ {card}")
        if len(missing_fallback) > 10:
            print(f"  ... 还有 {len(missing_fallback) - 10} 个")

    if missing_metrics:
        print(f"\n--- 缺少 效果度量 D7.4.3（{len(missing_metrics)} 个）---")
        for card in missing_metrics[:10]:
            print(f"  ℹ {card}")
        if len(missing_metrics) > 10:
            print(f"  ... 还有 {len(missing_metrics) - 10} 个")

    if ac_parse_errors:
        print(f"\n--- AC-XX 能力映射卡解析错误（ERROR, {len(ac_parse_errors)} 个）---")
        for err in ac_parse_errors:
            print(f"  ✗ {err}")

    # 退出码判定：无效绑定或 AC-XX 解析错误 → 退出码 1；未绑定 → 仅警告
    if invalid_bindings:
        print(f"\nFAIL: 检测到 {len(invalid_bindings)} 个无效绑定")
        sys.exit(1)

    if ac_parse_errors:
        print(f"\nFAIL: 检测到 {len(ac_parse_errors)} 个 AC-XX 解析错误")
        sys.exit(1)

    print(f"\nPASS (基础卡 {len(card_files)} + AC-XX 映射卡 {len(ac_cards)} = "
          f"总能力卡 {len(card_files) + len(ac_cards)}; "
          f"with {len(unbound_cards)} unbound warnings, "
          f"{len(missing_prereq)} missing prerequisites, "
          f"{len(missing_fallback)} missing fallback, "
          f"{len(missing_metrics)} missing metrics)")
    sys.exit(0)


if __name__ == "__main__":
    main()
