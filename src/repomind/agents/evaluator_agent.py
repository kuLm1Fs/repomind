import re
from dataclasses import dataclass

FILE_PATTERN = re.compile(r"[\w./-]+\.(py|java|go|js|ts|md|yml|yaml)")
EVIDENCE_PATTERN = re.compile(r"[\w./-]+\.(py|java|go|js|ts|md|yml|yaml):\d+(-\d+)?")

@dataclass
class EvaluationResult:
    passed : bool
    reasons : list[str]

def evaluate_answer(answer: str) -> EvaluationResult:
    reasons: list[str] = []

    if "涉及文件" not in answer:
        reasons.append("missing involved files section")

    if "实现流程" not in answer:
        reasons.append("missing implementation flow section")
    
    if "证据" not in answer:
        reasons.append("missing evidence section")

    if not FILE_PATTERN.search(answer):
        reasons.append("missing concrete file reference")

    if not EVIDENCE_PATTERN.search(answer):
        reasons.append("missing line evidence")

    insufficient_markers = ["上下文不足", "无法判断", "没有找到", "不清楚"]
    if any(marker in answer for marker in insufficient_markers):
        reasons.append("answer says context is insufficient")

    return EvaluationResult(
        passed=not reasons,
        reasons=reasons,
    )