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
        'financial': 'Financial/Monetary Risk',
        'liability': 'Legal Liability Risk',
        'compliance': 'Regulatory Compliance Risk',
        'operational': 'Operational Risk',
        'reputational': 'Reputational Risk'
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
        
        # Financial risks
        financial = self._assess_financial_risk(contract_text)
        if financial['risk_level'] != 'LOW':
            risks.append(financial)
        
        # Liability risks
        liability = self._assess_liability_risk(contract_text)
        if liability['risk_level'] != 'LOW':
            risks.append(liability)
        
        # Compliance risks
        compliance = self._assess_compliance_risk(contract_text)
        if compliance['risk_level'] != 'LOW':
            risks.append(compliance)
        
        # Calculate overall risk
        overall = self._calculate_overall_risk(risks)
        
        self.assessments_performed += 1
        
        return {
            'assessment_id': f'RISK-{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'timestamp': datetime.now().isoformat(),
            'risks_identified': len(risks),
            'risks': risks,
            'overall_risk': overall,
            'recommendations': self._generate_recommendations(risks)
        }
    
    def _assess_financial_risk(self, text: str) -> Dict:
        """Assess financial/monetary risks"""
        
        high_risk_terms = ['unlimited liability', 'no cap', 'no limit']
        medium_risk_terms = ['indemnification', 'damages', 'penalty']
        
        high_count = sum(1 for term in high_risk_terms if term in text.lower())
        medium_count = sum(1 for term in medium_risk_terms if term in text.lower())
        
        if high_count > 0:
            level = 'HIGH'
            severity = 8
        elif medium_count >= 2:
            level = 'MEDIUM'
            severity = 5
        else:
            level = 'LOW'
            severity = 2
        
        return {
            'category': 'financial',
            'description': self.RISK_CATEGORIES['financial'],
            'risk_level': level,
            'severity': severity,
            'findings': f'Found {high_count} high-risk and {medium_count} medium-risk terms',
            'mitigation': 'Cap liability amounts and define clear limits'
        }
    
    def _assess_liability_risk(self, text: str) -> Dict:
        """Assess legal liability risks"""
        
        risk_terms = [
            'gross negligence', 'willful misconduct', 'consequential damages',
            'indirect damages', 'punitive damages'
        ]
        
        count = sum(1 for term in risk_terms if term in text.lower())
        
        if count >= 3:
            level = 'HIGH'
            severity = 7
        elif count >= 1:
            level = 'MEDIUM'
            severity = 4
        else:
            level = 'LOW'
            severity = 2
        
        return {
            'category': 'liability',
            'description': self.RISK_CATEGORIES['liability'],
            'risk_level': level,
            'severity': severity,
            'findings': f'Identified {count} liability-related clauses',
            'mitigation': 'Add limitation of liability clauses'
        }
    
    def _assess_compliance_risk(self, text: str) -> Dict:
        """Assess regulatory compliance risks"""
        
        compliance_terms = ['gdpr', 'ccpa', 'hipaa', 'sox', 'compliance']
        count = sum(1 for term in compliance_terms if term in text.lower())
        
        if count == 0:
            level = 'HIGH'
            severity = 9
        elif count < 2:
            level = 'MEDIUM'
            severity = 5
        else:
            level = 'LOW'
            severity = 2
        
        return {
            'category': 'compliance',
            'description': self.RISK_CATEGORIES['compliance'],
            'risk_level': level,
            'severity': severity,
            'findings': f'Compliance terms mentioned: {count}',
            'mitigation': 'Add explicit compliance requirements and audit rights'
        }
    
    def _calculate_overall_risk(self, risks: List[Dict]) -> Dict:
        """Calculate overall risk score"""
        
        if not risks:
            return {'level': 'LOW', 'score': 0}
        
        # Calculate weighted average severity
        total_severity = sum(r['severity'] for r in risks)
        avg_severity = total_severity / len(risks)
        
        # Determine overall level
        if avg_severity >= 7:
            level = 'HIGH'
        elif avg_severity >= 4:
            level = 'MEDIUM'
        else:
            level = 'LOW'
        
        return {
            'level': level,
            'score': round(avg_severity, 1),
            'high_risks': sum(1 for r in risks if r['risk_level'] == 'HIGH'),
            'medium_risks': sum(1 for r in risks if r['risk_level'] == 'MEDIUM'),
            'low_risks': sum(1 for r in risks if r['risk_level'] == 'LOW')
        }
    
    def _generate_recommendations(self, risks: List[Dict]) -> List[str]:
        """Generate actionable recommendations"""
        
        recommendations = []
        
        for risk in risks:
            if risk['risk_level'] in ['HIGH', 'MEDIUM']:
                recommendations.append(
                    f"{risk['category'].upper()}: {risk['mitigation']}"
                )
        
        if not recommendations:
            recommendations.append("Contract appears well-structured. Continue monitoring.")
        
        return recommendations


# Test
if __name__ == '__main__':
    assessor = RiskAssessor()
    
    sample = """
    The company shall indemnify and hold harmless the other party from
    all damages, including consequential damages and punitive damages.
    There is no limitation on liability amounts.
    """
    
    result = assessor.assess_risks(sample)
    
    import json
    print(json.dumps(result, indent=2))
```

