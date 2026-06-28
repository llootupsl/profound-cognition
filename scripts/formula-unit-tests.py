#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Profound Cognition — 公式引擎单元测试 (D4.4.4)

测试范围：4 个非线性公式的正常/边界/异常输入
- FE-001: Softmax 动态注意力加权（含数值稳定版本 D4.4.2）
- FE-002: Logistic 胜负判定函数（含参数校准机制 D4.4.1）
- FE-003: 指数边际收益衰减模型（含场景化 ε D4.4.3）
- FE-004: Sigmoid 置信度校准函数

运行方式：python scripts/formula-unit-tests.py
退出码：0 全部通过 / 1 存在失败

作者：阿洋
版本：1.0.0
"""

import unittest
import math
import sys
from typing import List, Optional, Tuple

# 跨平台 UTF-8 输出兼容（修复 Windows GBK 编码崩溃）
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


# =============================================================================
# FE-001: Softmax 动态注意力加权（数值稳定版本 D4.4.2）
# =============================================================================

def softmax_stable(scores: List[float], temperature: float = 1.0) -> List[float]:
    """
    数值稳定的 Softmax 实现（D4.4.2 — 减最大值后 exp）
    """
    if not scores:
        return []
    if temperature <= 0:
        # 异常处理：温度 T → 0 时退化为 argmax
        max_val = max(scores)
        max_idx = scores.index(max_val)
        return [1.0 if i == max_idx else 0.0 for i in range(len(scores))]

    # 温度缩放
    scaled = [s / temperature for s in scores]
    # 减最大值（数值稳定关键步骤）
    max_val = max(scaled)
    shifted = [s - max_val for s in scaled]
    # 计算 exp（所有值 <= 0，不会溢出）
    exps = [math.exp(s) for s in shifted]
    # 归一化
    total = sum(exps)
    if total == 0:
        # 所有 s_i = 0 时等权
        n = len(scores)
        return [1.0 / n] * n
    return [e / total for e in exps]


def softmax_naive(scores: List[float], temperature: float = 1.0) -> List[float]:
    """
    原始（非稳定）Softmax 实现，用于对比测试
    """
    if not scores:
        return []
    scaled = [s / temperature for s in scores]
    exps = [math.exp(s) for s in scaled]
    total = sum(exps)
    return [e / total for e in exps]


class TestSoftmax(unittest.TestCase):
    """FE-001 Softmax 动态注意力加权测试"""

    # --- 正常输入 ---
    def test_normal_input(self):
        """正常输入：[1, 2, 3] 权重和为 1"""
        weights = softmax_stable([1.0, 2.0, 3.0])
        self.assertAlmostEqual(sum(weights), 1.0, places=10)
        # 第三个元素最大，权重应最高
        self.assertGreater(weights[2], weights[1])
        self.assertGreater(weights[1], weights[0])

    def test_normal_with_temperature(self):
        """正常输入：温度参数 T=2.0 使分布更均匀"""
        weights_t1 = softmax_stable([1.0, 2.0, 3.0], temperature=1.0)
        weights_t2 = softmax_stable([1.0, 2.0, 3.0], temperature=2.0)
        # T 越大，分布越均匀 → 最大权重应降低
        self.assertLess(max(weights_t2), max(weights_t1))

    def test_normal_monotonicity(self):
        """正常输入：得分越高权重越大（单调性）"""
        weights = softmax_stable([5.0, 3.0, 8.0, 1.0])
        # 8.0 对应的权重应最大
        self.assertEqual(weights.index(max(weights)), 2)
        # 1.0 对应的权重应最小
        self.assertEqual(weights.index(min(weights)), 3)

    # --- 边界输入 ---
    def test_boundary_all_equal(self):
        """边界输入：所有得分相等 → 等权分布"""
        weights = softmax_stable([5.0, 5.0, 5.0, 5.0])
        for w in weights:
            self.assertAlmostEqual(w, 0.25, places=10)

    def test_boundary_all_zero(self):
        """边界输入：所有得分为 0 → 等权分布"""
        weights = softmax_stable([0.0, 0.0, 0.0])
        for w in weights:
            self.assertAlmostEqual(w, 1.0 / 3, places=10)

    def test_boundary_single_element(self):
        """边界输入：单个元素 → 权重为 1.0"""
        weights = softmax_stable([7.0])
        self.assertEqual(len(weights), 1)
        self.assertAlmostEqual(weights[0], 1.0, places=10)

    def test_boundary_max_range(self):
        """边界输入：得分在 [0, 10] 范围边界"""
        weights = softmax_stable([0.0, 10.0])
        self.assertAlmostEqual(sum(weights), 1.0, places=10)
        self.assertGreater(weights[1], weights[0])

    # --- 异常输入 ---
    def test_abnormal_extreme_values(self):
        """异常输入：极端大值（D4.4.2 数值稳定验证）"""
        # 原始实现会溢出，稳定实现应正常工作
        weights = softmax_stable([1000.0, 1001.0, 1002.0])
        self.assertAlmostEqual(sum(weights), 1.0, places=10)
        # 与小范围等价输入结果一致
        weights_small = softmax_stable([0.0, 1.0, 2.0])
        for w_large, w_small in zip(weights, weights_small):
            self.assertAlmostEqual(w_large, w_small, places=10)

    def test_abnormal_zero_temperature(self):
        """异常输入：温度 T → 0 退化为 argmax"""
        weights = softmax_stable([1.0, 5.0, 3.0], temperature=0.0)
        # 应退化为 argmax（第二个元素）
        self.assertEqual(weights[1], 1.0)
        self.assertEqual(weights[0], 0.0)
        self.assertEqual(weights[2], 0.0)

    def test_abnormal_empty_input(self):
        """异常输入：空列表"""
        weights = softmax_stable([])
        self.assertEqual(weights, [])

    def test_stable_equals_naive_normal(self):
        """稳定版与原始版在正常输入下结果一致"""
        test_cases = [
            [1.0, 2.0, 3.0],
            [0.5, 0.5, 0.5],
            [0.0, 10.0],
            [3.0],
        ]
        for scores in test_cases:
            stable = softmax_stable(scores)
            naive = softmax_naive(scores)
            for s, n in zip(stable, naive):
                self.assertAlmostEqual(s, n, places=10)


# =============================================================================
# FE-002: Logistic 胜负判定函数（含参数校准机制 D4.4.1）
# =============================================================================

def logistic_adjudication(A: float, D: float) -> float:
    """
    Logistic 胜负判定：P(win) = 1 / (1 + exp(-(A - D)))
    A: 攻击强度 [0, 10]
    D: 辩护强度 [0, 10]
    返回：P(win) [0, 1]
    """
    diff = A - D
    # 异常处理：极端差值 clamp
    if abs(diff) > 20:
        return 0.99 if diff > 0 else 0.01
    try:
        return 1.0 / (1.0 + math.exp(-diff))
    except OverflowError:
        return 0.99 if diff > 0 else 0.01


def classify_p_win(p_win: float,
                   threshold_high: float = 0.7,
                   threshold_low: float = 0.3) -> str:
    """分类 P(win) 结果"""
    if p_win > threshold_high:
        return "attack_succeeded"
    elif p_win < threshold_low:
        return "attack_failed"
    else:
        return "balanced"


def calibrate_logistic_thresholds(history: List[dict]) -> dict:
    """
    参数校准机制（D4.4.1 — 基于历史数据动态调整阈值）
    history: [{p_win, actual_verdict}, ...]
    """
    if len(history) < 30:
        return {"threshold_high": 0.7, "threshold_low": 0.3,
                "calibration_triggered": False}

    # 计算当前阈值准确率
    correct = sum(1 for r in history
                  if classify_p_win(r["p_win"]) == r["actual_verdict"])
    accuracy = correct / len(history)

    if accuracy >= 0.75:
        return {"threshold_high": 0.7, "threshold_low": 0.3,
                "calibration_triggered": False}

    # 网格搜索最优阈值
    best_acc = 0
    best_th = {"threshold_high": 0.7, "threshold_low": 0.3}
    th = 0.6
    while th <= 0.8:
        tl = 0.2
        while tl <= 0.4:
            if tl < th:
                correct = sum(1 for r in history
                              if classify_p_win(r["p_win"], th, tl) == r["actual_verdict"])
                acc = correct / len(history)
                if acc > best_acc:
                    best_acc = acc
                    best_th = {"threshold_high": th, "threshold_low": tl}
            tl += 0.01
        th += 0.01

    # clamp
    best_th["threshold_high"] = max(0.6, min(0.8, best_th["threshold_high"]))
    best_th["threshold_low"] = max(0.2, min(0.4, best_th["threshold_low"]))
    best_th["calibration_triggered"] = True
    return best_th


class TestLogistic(unittest.TestCase):
    """FE-002 Logistic 胜负判定函数测试"""

    # --- 正常输入 ---
    def test_normal_attack_succeeds(self):
        """正常输入：A=8, D=3 → 攻击成功"""
        p = logistic_adjudication(8.0, 3.0)
        self.assertGreater(p, 0.7)
        self.assertEqual(classify_p_win(p), "attack_succeeded")

    def test_normal_attack_fails(self):
        """正常输入：A=2, D=8 → 攻击失败"""
        p = logistic_adjudication(2.0, 8.0)
        self.assertLess(p, 0.3)
        self.assertEqual(classify_p_win(p), "attack_failed")

    def test_normal_balanced(self):
        """正常输入：A=5, D=5 → 攻防均衡"""
        p = logistic_adjudication(5.0, 5.0)
        self.assertAlmostEqual(p, 0.5, places=10)
        self.assertEqual(classify_p_win(p), "balanced")

    def test_normal_range(self):
        """正常输入：P(win) 始终在 [0, 1]"""
        for a in range(0, 11):
            for d in range(0, 11):
                p = logistic_adjudication(float(a), float(d))
                self.assertGreaterEqual(p, 0.0)
                self.assertLessEqual(p, 1.0)

    # --- 边界输入 ---
    def test_boundary_max_attack(self):
        """边界输入：A=10, D=0 → P(win) 接近 1"""
        p = logistic_adjudication(10.0, 0.0)
        self.assertGreater(p, 0.99)

    def test_boundary_max_defense(self):
        """边界输入：A=0, D=10 → P(win) 接近 0"""
        p = logistic_adjudication(0.0, 10.0)
        self.assertLess(p, 0.01)

    def test_boundary_equal(self):
        """边界输入：A=D → P(win) = 0.5"""
        for val in [0.0, 1.0, 5.0, 10.0]:
            p = logistic_adjudication(val, val)
            self.assertAlmostEqual(p, 0.5, places=10)

    # --- 异常输入 ---
    def test_abnormal_extreme_diff(self):
        """异常输入：|A-D| > 20 → clamp 到 [0.01, 0.99]"""
        p = logistic_adjudication(100.0, 0.0)
        self.assertAlmostEqual(p, 0.99, places=10)
        p = logistic_adjudication(0.0, 100.0)
        self.assertAlmostEqual(p, 0.01, places=10)

    def test_abnormal_negative_input(self):
        """异常输入：负值（异常但可计算）"""
        # 负值不在设计范围但数学上可计算
        p = logistic_adjudication(-1.0, -2.0)
        self.assertGreater(p, 0.5)  # A > D 仍成立

    # --- 参数校准机制（D4.4.1）---
    def test_calibration_insufficient_samples(self):
        """校准测试：样本不足 30 时不触发校准"""
        history = [{"p_win": 0.8, "actual_verdict": "attack_succeeded"}] * 20
        result = calibrate_logistic_thresholds(history)
        self.assertFalse(result["calibration_triggered"])
        self.assertEqual(result["threshold_high"], 0.7)
        self.assertEqual(result["threshold_low"], 0.3)

    def test_calibration_sufficient_accuracy(self):
        """校准测试：准确率达标时不触发校准"""
        # 构造 30 条准确率 >= 0.75 的历史数据
        history = []
        for i in range(23):
            history.append({"p_win": 0.8, "actual_verdict": "attack_succeeded"})
        for i in range(7):
            history.append({"p_win": 0.8, "actual_verdict": "balanced"})
        result = calibrate_logistic_thresholds(history)
        self.assertFalse(result["calibration_triggered"])

    def test_calibration_triggered_low_accuracy(self):
        """校准测试：准确率不达标时触发校准"""
        # 构造 30 条准确率低的历史数据
        history = []
        for i in range(20):
            history.append({"p_win": 0.8, "actual_verdict": "attack_failed"})
        for i in range(10):
            history.append({"p_win": 0.2, "actual_verdict": "attack_succeeded"})
        result = calibrate_logistic_thresholds(history)
        self.assertTrue(result["calibration_triggered"])
        # 校准后阈值在 clamp 范围内
        self.assertGreaterEqual(result["threshold_high"], 0.6)
        self.assertLessEqual(result["threshold_high"], 0.8)
        self.assertGreaterEqual(result["threshold_low"], 0.2)
        self.assertLessEqual(result["threshold_low"], 0.4)


# =============================================================================
# FE-003: 指数边际收益衰减模型（含场景化 ε D4.4.3）
# =============================================================================

def info_decay(t: float, alpha: float = 1.0, lam: float = 0.3) -> float:
    """
    ΔInfo(t) = α · exp(-λt)
    t: 迭代轮次
    alpha: 初始信息增益率（默认 1.0）
    lam: 衰减系数（默认 0.3）
    """
    if alpha is None:
        alpha = 1.0
    if lam is None:
        lam = 0.3
    return alpha * math.exp(-lam * t)


def select_epsilon(output_type: str,
                   research_depth_label: Optional[str] = None) -> float:
    """
    场景化 ε 选择（D4.4.3）
    """
    if output_type == "research_report":
        if research_depth_label == "commercial_brief":
            return 0.05
        return 0.01
    elif output_type in ["wechat_article", "course_material"]:
        return 0.05
    else:
        return 0.05


def should_terminate(t: float, epsilon: float = 0.05,
                     alpha: float = 1.0, lam: float = 0.3) -> bool:
    """判断是否应终止迭代"""
    return info_decay(t, alpha, lam) < epsilon


class TestInfoDecay(unittest.TestCase):
    """FE-003 指数边际收益衰减模型测试"""

    # --- 正常输入 ---
    def test_normal_decay(self):
        """正常输入：t=1 → ΔInfo ≈ 0.74"""
        delta = info_decay(1.0)
        self.assertAlmostEqual(delta, math.exp(-0.3), places=5)
        self.assertGreater(delta, 0.7)
        self.assertLess(delta, 0.8)

    def test_normal_monotonic_decrease(self):
        """正常输入：ΔInfo(t) 单调递减"""
        values = [info_decay(t) for t in range(0, 10)]
        for i in range(len(values) - 1):
            self.assertGreaterEqual(values[i], values[i + 1])

    def test_normal_custom_params(self):
        """正常输入：自定义 α 和 λ"""
        delta = info_decay(2.0, alpha=2.0, lam=0.5)
        expected = 2.0 * math.exp(-0.5 * 2.0)
        self.assertAlmostEqual(delta, expected, places=10)

    # --- 边界输入 ---
    def test_boundary_t_zero(self):
        """边界输入：t=0 → ΔInfo = α"""
        delta = info_decay(0.0)
        self.assertAlmostEqual(delta, 1.0, places=10)
        delta = info_decay(0.0, alpha=2.0)
        self.assertAlmostEqual(delta, 2.0, places=10)

    def test_boundary_large_t(self):
        """边界输入：t 很大 → ΔInfo → 0"""
        delta = info_decay(100.0)
        self.assertLess(delta, 1e-10)

    def test_boundary_epsilon_threshold(self):
        """边界输入：刚好达到 ε 阈值"""
        # ΔInfo(t) = exp(-0.3t) = 0.05 → t = -ln(0.05)/0.3 ≈ 9.96
        t_threshold = -math.log(0.05) / 0.3
        delta = info_decay(t_threshold)
        self.assertAlmostEqual(delta, 0.05, places=5)

    # --- 异常输入 ---
    def test_abnormal_none_params(self):
        """异常输入：α/λ 为 None → 使用默认值"""
        delta = info_decay(1.0, alpha=None, lam=None)
        expected = 1.0 * math.exp(-0.3 * 1.0)
        self.assertAlmostEqual(delta, expected, places=10)

    def test_abnormal_negative_t(self):
        """异常输入：负 t（数学上可计算但无意义）"""
        delta = info_decay(-1.0)
        self.assertGreater(delta, 1.0)  # exp(0.3) > 1

    # --- 场景化 ε（D4.4.3）---
    def test_epsilon_academic(self):
        """场景化 ε：学术场景 ε=0.01"""
        eps = select_epsilon("research_report")
        self.assertEqual(eps, 0.01)

    def test_epsilon_commercial(self):
        """场景化 ε：商业场景 ε=0.05"""
        eps = select_epsilon("wechat_article")
        self.assertEqual(eps, 0.05)
        eps = select_epsilon("course_material")
        self.assertEqual(eps, 0.05)

    def test_epsilon_commercial_brief(self):
        """场景化 ε：research_report 但标注商业简报 → ε=0.05"""
        eps = select_epsilon("research_report", research_depth_label="commercial_brief")
        self.assertEqual(eps, 0.05)

    def test_epsilon_default(self):
        """场景化 ε：未知类型 → 默认 ε=0.05"""
        eps = select_epsilon("unknown_type")
        self.assertEqual(eps, 0.05)

    def test_terminate_academic_vs_commercial(self):
        """场景化 ε：学术场景需要更多轮才终止"""
        # 学术 ε=0.01 → 终止轮次更晚
        t_academic = 0
        while not should_terminate(t_academic, epsilon=0.01):
            t_academic += 0.1
        # 商业 ε=0.05 → 终止轮次更早
        t_commercial = 0
        while not should_terminate(t_commercial, epsilon=0.05):
            t_commercial += 0.1
        self.assertGreater(t_academic, t_commercial)


# =============================================================================
# FE-004: Sigmoid 置信度校准函数
# =============================================================================

def sigmoid_calibration(x: float, k: float = 10.0, mu: float = 0.5) -> float:
    """
    CalibratedConf(x) = 1 / (1 + exp(-k(x - μ)))
    x: 原始线性得分 [0, 1]
    k: 陡峭度（默认 10）
    mu: 中点偏移（默认 0.5）
    """
    if k is None:
        k = 10.0
    if mu is None:
        mu = 0.5
    # 异常处理：x 超出 [0, 1] → min-max 归一化
    if x < 0 or x > 1:
        x = max(0.0, min(1.0, x))
    try:
        return 1.0 / (1.0 + math.exp(-k * (x - mu)))
    except OverflowError:
        return 1.0 if (x - mu) > 0 else 0.0


class TestSigmoid(unittest.TestCase):
    """FE-004 Sigmoid 置信度校准函数测试"""

    # --- 正常输入 ---
    def test_normal_midpoint(self):
        """正常输入：x=0.5 → CalibratedConf = 0.5"""
        conf = sigmoid_calibration(0.5)
        self.assertAlmostEqual(conf, 0.5, places=10)

    def test_normal_high_confidence(self):
        """正常输入：x=0.9 → 高置信度"""
        conf = sigmoid_calibration(0.9)
        self.assertGreater(conf, 0.9)

    def test_normal_low_confidence(self):
        """正常输入：x=0.1 → 低置信度"""
        conf = sigmoid_calibration(0.1)
        self.assertLess(conf, 0.1)

    def test_normal_range(self):
        """正常输入：CalibratedConf 始终在 [0, 1]"""
        for i in range(101):
            x = i / 100.0
            conf = sigmoid_calibration(x)
            self.assertGreaterEqual(conf, 0.0)
            self.assertLessEqual(conf, 1.0)

    # --- 边界输入 ---
    def test_boundary_x_zero(self):
        """边界输入：x=0 → 接近 0"""
        conf = sigmoid_calibration(0.0)
        self.assertLess(conf, 0.01)

    def test_boundary_x_one(self):
        """边界输入：x=1 → 接近 1"""
        conf = sigmoid_calibration(1.0)
        self.assertGreater(conf, 0.99)

    def test_boundary_custom_k(self):
        """边界输入：自定义 k 参数"""
        # k 越大，sigmoid 越陡
        conf_low_k = sigmoid_calibration(0.6, k=1.0)
        conf_high_k = sigmoid_calibration(0.6, k=20.0)
        self.assertLess(conf_low_k, conf_high_k)

    def test_boundary_custom_mu(self):
        """边界输入：自定义 μ 参数"""
        conf = sigmoid_calibration(0.7, mu=0.7)
        self.assertAlmostEqual(conf, 0.5, places=10)

    # --- 异常输入 ---
    def test_abnormal_x_out_of_range(self):
        """异常输入：x 超出 [0, 1] → 归一化"""
        conf_neg = sigmoid_calibration(-1.0)
        self.assertAlmostEqual(conf_neg, sigmoid_calibration(0.0), places=10)
        conf_large = sigmoid_calibration(2.0)
        self.assertAlmostEqual(conf_large, sigmoid_calibration(1.0), places=10)

    def test_abnormal_none_params(self):
        """异常输入：k/μ 为 None → 使用默认值"""
        conf = sigmoid_calibration(0.5, k=None, mu=None)
        self.assertAlmostEqual(conf, 0.5, places=10)

    def test_abnormal_extreme_k(self):
        """异常输入：k 极大 → 接近阶跃函数"""
        conf = sigmoid_calibration(0.6, k=1000.0)
        self.assertGreater(conf, 0.99)
        conf = sigmoid_calibration(0.4, k=1000.0)
        self.assertLess(conf, 0.01)


# =============================================================================
# 主入口
# =============================================================================

if __name__ == "__main__":
    # 运行所有测试
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestSoftmax))
    suite.addTests(loader.loadTestsFromTestCase(TestLogistic))
    suite.addTests(loader.loadTestsFromTestCase(TestInfoDecay))
    suite.addTests(loader.loadTestsFromTestCase(TestSigmoid))

    # 运行并输出结果
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 退出码
    sys.exit(0 if result.wasSuccessful() else 1)
