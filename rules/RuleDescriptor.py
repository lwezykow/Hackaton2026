from dataclasses import dataclass

@dataclass
class RuleDescriptor:
    rule_id: str
    rule_category: str
    rule: str
    business_description: str
    is_mandatory: bool
    severity: int      # 1 or 2
    weight: float
    difficulty: int    # 1–3

