"""
Risk Assessor Module  
DiscipleAI Legal™  
"""

from typing import Dict, List
from datetime import datetime


class RiskAssessor:
    """
    Automated risk assessment for legal documents
    """

    RISK_CATEGORIES = {
        "financial": "Financial/Monetary Risk",
        "liability": "Legal Liability Risk",
        "compliance": "Regulatory Compliance Risk",
        "operational": "Operational Risk",
        "reputational": "Reputational Risk"
    }

    def __init__(self):
        self.assessments_performed = 0

    def assess_risks(self, contract_text: str, metadata: Dict = None) -> Dict:
        """
        Assess risks in contract

        Args:
            contract_text: Contract to analyze
            metadata: Additional context

        Returns:
            dict: Risk assessment results
        """
        risks = []

        # Financial risk
        financial = self._assess_financial_risk(contract_text)
        if financial["risk_level"] != "LOW":
            risks.append(financial)

        # Liability risk
        liability = self._assess_liability_risk(contract_text)
        if liability["risk_level"] != "LOW":
            risks.append(liability)

        # Compliance risk
        compliance = self._assess_compliance_risk(contract_text)
        if compliance["risk_level"] != "LOW":
            risks.append(compliance)

        # Overall risk
        overall = self._calculate_overall_risk(risks)
        self.assessments_performed += 1

        return {
            "assessment_id": f"RISK-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "risks_identified": len(risks),
            "risks": risks,
            "overall_risk": overall,
            "recommendations": self._generate_recommendations(risks)
        }

    def _assess_financial_risk(self, text: str) -> Dict:
        """Assess financial/monetary risks"""
        high_terms = ["unlimited liability", "no cap", "no limit"]
        medium_terms = ["indemnification", "damages", "penalty"]

        high_count = sum(term in text.lower() for term in high_terms)
        medium_count = sum(term in text.lower() for term in medium_terms)

        if high_count > 0:
            level, severity = "HIGH", 8
        elif medium_count >= 2:
            level, severity = "MEDIUM", 5
        else:
            level, severity = "LOW", 2

        return {
            "category": "financial",
            "description": self.RISK_CATEGORIES["financial"],
            "risk_level": level,
            "severity": severity,
            "findings": f"Found {high_count} high-risk and {medium_count} medium-risk terms",
            "mitigation": "Cap liability amounts and define clear limits"
        }

    def _assess_liability_risk(self, text: str) -> Dict:
        """Assess legal liability risks"""
        terms = [
            "gross negligence", "willful misconduct", "consequential damages",
            "indirect damages", "punitive damages"
        ]
        count = sum(term in text.lower() for term in terms)

        if count >= 3:
            level, severity = "HIGH", 7
        elif count >= 1:
            level, severity = "MEDIUM", 4
        else:
            level, severity = "LOW", 2

        return {
            "category": "liability",
            "description": self.RISK_CATEGORIES["liability"],
            "risk_level": level,
            "severity": severity,
            "findings": f"Identified {count} liability-related clauses",
            "mitigation": "Add limitation of liability clauses"
        }

    def _assess_compliance_risk(self, text: str) -> Dict:
        """Assess regulatory compliance risks"""
        terms = ["gdpr", "ccpa", "hipaa", "sox", "compliance"]
        count = sum(term in text.lower() for term in terms)

        if count == 0:
            level, severity = "HIGH", 9
        elif count < 2:
            level, severity = "MEDIUM", 5
        else:
            level, severity = "LOW", 2

        return {
            "category": "compliance",
            "description": self.RISK_CATEGORIES["compliance"],
            "risk_level": level,
            "severity": severity,
            "findings": f"Compliance terms mentioned: {count}",
            "mitigation": "Add explicit compliance requirements and audit rights"
        }

    def _calculate_overall_risk(self, risks: List[Dict]) -> Dict:
        """Calculate overall risk score"""
        if not risks:
            return {"level": "LOW", "score": 0}

        total = sum(r["severity"] for r in risks)
        avg = total / len(risks)

        if avg >= 7:
            level = "HIGH"
        elif avg >= 4:
            level = "MEDIUM"
        else:
            level = "LOW"

        return {
            "level": level,
            "score": round(avg, 1),
            "high_risks": sum(r["risk_level"] == "HIGH" for r in risks),
            "medium_risks": sum(r["risk_level"] == "MEDIUM" for r in risks),
            "low_risks": sum(r["risk_level"] == "LOW" for r in risks)
        }

    def _generate_recommendations(self, risks: List[Dict]) -> List[str]:
        """Generate actionable recommendations"""
        recs = [
            f"{r['category'].upper()}: {r['mitigation']}"
            for r in risks if r["risk_level"] in ["HIGH", "MEDIUM"]
        ]
        return recs or ["Contract appears well-structured. Continue monitoring."]


# Test block
if __name__ == "__main__":
    assessor = RiskAssessor()

    sample_contract = """
    The company shall indemnify and hold harmless the other party from
    all damages, including consequential damages and punitive damages.
    There is no limitation on liability amounts.
    """

    result = assessor.assess_risks(sample_contract)

    import json
    print(json.dumps(result, indent=2))