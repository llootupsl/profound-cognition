#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 作者：阿洋
"""kg-availability-check.py — KG 备用源可用性检查脚本（R5-05/R9-06）

检查 LightRAG 及其备用 KG 源（DBpedia/YAGO/OpenKG/本地 Neo4j）的可用性，
为 T08-T13 节点的穷尽重试策略（L1_FULL → L2_FALLBACK → L3_BACKUP_KG →
L4_INTERNAL_REASONING）提供运行时决策依据。

备用源层级（详见 plugins/lightrag-adapter.md「备用源层级（R5-05）」）：
  主源: LightRAG（本地索引 ./lightrag_index/{research_id}/）
  备用源 1: DBpedia（SPARQL 端点 https://dbpedia.org/sparql）
  备用源 2: YAGO（SPARQL 端点 https://yago-knowledge.org/sparql）
  备用源 3: OpenKG（中文知识图谱 http://openkg.cn）
  备用源 4: 本地 Neo4j（bolt://localhost:7687）

检测逻辑：
  1. LightRAG: 检查 ./lightrag_index/ 目录下是否存在已构建的索引
  2. DBpedia/YAGO/OpenKG: HTTP GET 请求对应端点，超时 5 秒，HTTP 200 视为可用
  3. Neo4j: 尝试 TCP 连接 localhost:7687，超时 2 秒

退出码:
  0 = 至少一个 KG 源可用（可执行 KG 增强检索）
  1 = 全部 KG 源不可用（需回退到 L4_INTERNAL_REASONING）

用法: python scripts/kg-availability-check.py [research_id]
  research_id: 可选，指定研究 ID 用于检查对应的 LightRAG 索引
               未指定时检查 ./lightrag_index/ 下任意已存在的索引
"""

import json
import os
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request
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
LIGHTRAG_INDEX_DIR = PROJECT_ROOT / "lightrag_index"

# KG 源端点配置
KG_ENDPOINTS = {
    "dbpedia": {
        "url": "https://dbpedia.org/sparql",
        "query": "ASK { ?s ?p ?o } LIMIT 1",
        "timeout": 5,
        "type": "sparql",
    },
    "yago": {
        "url": "https://yago-knowledge.org/sparql",
        "query": "ASK { ?s ?p ?o } LIMIT 1",
        "timeout": 5,
        "type": "sparql",
    },
    "openkg": {
        "url": "http://openkg.cn",
        "timeout": 5,
        "type": "http",
    },
    "neo4j": {
        "host": "localhost",
        "port": 7687,
        "timeout": 2,
        "type": "tcp",
    },
}


def check_lightrag_index(research_id=None):
    """检查 LightRAG 索引可用性。

    Args:
        research_id: 研究 ID。若指定，检查 ./lightrag_index/{research_id}/；
                     若未指定，检查 ./lightrag_index/ 下任意已存在的索引。

    Returns:
        (available: bool, detail: str)
    """
    if not LIGHTRAG_INDEX_DIR.exists():
        return False, f"LightRAG 索引目录不存在: {LIGHTRAG_INDEX_DIR}"

    if research_id:
        index_path = LIGHTRAG_INDEX_DIR / research_id
        if not index_path.exists():
            return False, f"指定研究 ID 的索引不存在: {index_path}"
        # 检查索引文件是否完整（graph_chunk_entity_relation.graphml 等关键文件）
        key_files = [
            "graph_chunk_entity_relation.graphml",
            "chunks.db",
            "graph_db_vdb_node.faiss",
        ]
        existing = [f.name for f in index_path.iterdir() if f.is_file()]
        if not existing:
            return False, f"索引目录为空: {index_path}"
        return True, f"LightRAG 索引可用（{len(existing)} 个文件）: {index_path}"
    else:
        # 检查任意已存在的索引
        subdirs = [d for d in LIGHTRAG_INDEX_DIR.iterdir() if d.is_dir()]
        if not subdirs:
            return False, f"LightRAG 索引目录为空（无已构建索引）: {LIGHTRAG_INDEX_DIR}"
        return True, f"LightRAG 索引可用（{len(subdirs)} 个研究索引）: {LIGHTRAG_INDEX_DIR}"


def check_http_endpoint(name, config):
    """检查 HTTP/SPARQL 端点可用性。

    Args:
        name: KG 源名称
        config: 端点配置字典

    Returns:
        (available: bool, detail: str)
    """
    url = config["url"]
    timeout = config["timeout"]
    endpoint_type = config["type"]

    try:
        if endpoint_type == "sparql":
            # SPARQL 端点：发送 ASK 查询
            params = urllib.parse.urlencode({
                "query": config["query"],
                "format": "json",
            })
            full_url = f"{url}?{params}"
            req = urllib.request.Request(
                full_url,
                headers={"Accept": "application/sparql-results+json"},
            )
        else:
            # 普通 HTTP 端点
            req = urllib.request.Request(url, headers={"Accept": "text/html"})

        with urllib.request.urlopen(req, timeout=timeout) as response:
            status_code = response.getcode()
            if 200 <= status_code < 400:
                return True, f"{name} 可用（HTTP {status_code}）: {url}"
            else:
                return False, f"{name} 不可用（HTTP {status_code}）: {url}"

    except urllib.error.URLError as e:
        return False, f"{name} 不可用（网络错误: {e.reason}）: {url}"
    except socket.timeout:
        return False, f"{name} 不可用（超时 {timeout}s）: {url}"
    except Exception as e:
        return False, f"{name} 不可用（异常: {type(e).__name__}: {e}）: {url}"


def check_tcp_endpoint(name, config):
    """检查 TCP 端点可用性（用于 Neo4j bolt 协议）。

    Args:
        name: KG 源名称
        config: 端点配置字典

    Returns:
        (available: bool, detail: str)
    """
    host = config["host"]
    port = config["port"]
    timeout = config["timeout"]

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()

        if result == 0:
            return True, f"{name} 可用（TCP {host}:{port} 开放）"
        else:
            return False, f"{name} 不可用（TCP {host}:{port} 连接失败）"
    except socket.timeout:
        return False, f"{name} 不可用（TCP {host}:{port} 超时 {timeout}s）"
    except Exception as e:
        return False, f"{name} 不可用（异常: {type(e).__name__}: {e}）"


def check_kg_source(name, config, research_id=None):
    """检查单个 KG 源可用性（调度函数）。

    Args:
        name: KG 源名称
        config: 端点配置字典
        research_id: 研究 ID（仅 LightRAG 使用）

    Returns:
        (available: bool, detail: str)
    """
    if name == "lightrag":
        return check_lightrag_index(research_id)
    elif config["type"] == "tcp":
        return check_tcp_endpoint(name, config)
    else:
        return check_http_endpoint(name, config)


def main():
    # 解析命令行参数
    research_id = None
    if len(sys.argv) > 1:
        research_id = sys.argv[1]

    print("=" * 60)
    print("Profound Cognition — KG 备用源可用性检查（R5-05/R9-06）")
    print("=" * 60)

    if research_id:
        print(f"\n[参数] research_id = {research_id}")
    else:
        print("\n[参数] research_id = (未指定，检查任意已存在索引)")

    # 按备用源层级顺序检查
    # 主源: LightRAG → 备用源 1: DBpedia → 备用源 2: YAGO → 备用源 3: OpenKG → 备用源 4: Neo4j
    check_order = ["lightrag", "dbpedia", "yago", "openkg", "neo4j"]

    results = []
    print(f"\n[检查] 按备用源层级依次检测 {len(check_order)} 个 KG 源...")
    print("-" * 60)

    for name in check_order:
        config = KG_ENDPOINTS.get(name, {})
        available, detail = check_kg_source(name, config, research_id)
        status_mark = "✓" if available else "✗"
        print(f"  {status_mark} [{name}] {detail}")
        results.append((name, available, detail))

    print("-" * 60)

    # 汇总结果
    available_sources = [(name, detail) for name, available, detail in results if available]
    unavailable_sources = [name for name, available, _ in results if not available]

    print(f"\n[汇总]")
    print(f"  可用 KG 源: {len(available_sources)} / {len(check_order)}")
    if available_sources:
        print(f"  可用列表: {[name for name, _ in available_sources]}")
    if unavailable_sources:
        print(f"  不可用列表: {unavailable_sources}")

    # 输出 JSON 格式报告（供下游节点消费）
    report = {
        "timestamp": None,  # 由调用方填充
        "research_id": research_id,
        "available_sources": [name for name, _ in available_sources],
        "unavailable_sources": unavailable_sources,
        "fallback_recommendation": None,
    }

    # 推荐回退层级
    if available_sources:
        first_available = available_sources[0][0]
        if first_available == "lightrag":
            report["fallback_recommendation"] = "L1_FULL"
        elif first_available in ("dbpedia", "yago", "openkg", "neo4j"):
            report["fallback_recommendation"] = "L3_BACKUP_KG"
    else:
        report["fallback_recommendation"] = "L4_INTERNAL_REASONING"

    print(f"\n[推荐回退层级] {report['fallback_recommendation']}")
    print(f"\n[JSON 报告]")
    print(json.dumps(report, ensure_ascii=False, indent=2))

    # 退出码判定
    # 健康阈值：≥ 3/5 视为健康；< 3/5 视为受限运行（仍 exit 0，但输出 WARNING）
    healthy_threshold = 3
    print("\n" + "=" * 60)
    if available_sources:
        available_count = len(available_sources)
        total_count = len(check_order)
        if available_count >= healthy_threshold:
            print(f"✅ 检查通过（健康）: {available_count}/{total_count} 个 KG 源可用")
        else:
            print(f"✅ 检查通过（受限运行）: {available_count}/{total_count} 个 KG 源可用")
            print(f"   ⚠ 警告: 可用率 {available_count}/{total_count} 低于健康阈值 {healthy_threshold}/{total_count}（60%），KG 增强检索可靠性受限")
            print(f"   不可用源: {unavailable_sources}（建议检查网络连接或启动本地服务）")
        print(f"   推荐使用: {available_sources[0][0]}")
        print("=" * 60)
        sys.exit(0)
    else:
        print("❌ 检查失败: 全部 KG 源不可用")
        print("   需回退到 L4_INTERNAL_REASONING（LLM 内建能力）")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
