from dataclasses import dataclass

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

    return EvaluationResult(
        passed=not reasons,
        reasons=reasons,
    )