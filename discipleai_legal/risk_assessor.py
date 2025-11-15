"""
Risk Assessor
Advanced risk analysis for contracts
"""

from typing import Dict, List, Optional
from datetime import datetime
import json
import re


class RiskAssessor:
    """
    Comprehensive risk assessment for legal contracts
    Financial, operational, reputational, and legal risk analysis
    """
    
    def __init__(self):
        self.version = "1.0.0"
        self.assessments_performed = 0
        
        # Risk indicators database
        self.risk_indicators = {
            'CRITICAL': {
                'unlimited liability': 10,
                'no indemnification': 9,
                'automatic renewal': 8,
                'unilateral termination': 8,
                'no warranty': 9,
                'as is': 8,
                'sole discretion': 7,
                'irrevocable': 8,
                'perpetual': 7,
                'non-refundable': 6
            },
            'HIGH': {
                'liquidated damages': 6,
                'penalty clause': 7,
                'without cause termination': 6,
                'non-compete': 5,
                'exclusive rights': 5,
                'assignment of ip': 6,
                'broad indemnification': 6,
                'unlimited duration': 5,
                'joint and several': 6,
                'personal guarantee': 7
            },
            'MEDIUM': {
                'governing law': 3,
                'arbitration': 2,
                'confidentiality': 2,
                'force majeure': 1,
                'change of control': 4,
                'audit rights': 3,
                'most favored nation': 4,
                'right of first refusal': 3,
                'non-solicitation': 3,
                'escrow': 2
            }
        }
        
        # Financial risk thresholds
        self.financial_thresholds = {
            'liability_cap': {
                'low': 1000000,
                'medium': 5000000,
                'high': 10000000
            },
            'contract_value': {
                'low': 100000,
                'medium': 500000,
                'high': 1000000
            }
        }
        
        print(f"✅ Risk Assessor v{self.version} initialized")
        print(f"   Risk indicators: {sum(len(v) for v in self.risk_indicators.values())}")
    
    def assess_risk(
        self,
        contract_text: str,
        contract_value: Optional[float] = None,
        contract_type: str = "general",
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Comprehensive risk assessment
        
        Args:
            contract_text: Full contract text
            contract_value: Total contract value in USD
            contract_type: Type of contract
            metadata: Additional context
            
        Returns:
            Complete risk assessment
        """
        
        self.assessments_performed += 1
        
        # Analyze different risk categories
        financial_risk = self._assess_financial_risk(contract_text, contract_value)
        legal_risk = self._assess_legal_risk(contract_text)
        operational_risk = self._assess_operational_risk(contract_text)
        reputational_risk = self._assess_reputational_risk(contract_text)
        
        # Identify specific risk clauses
        risk_clauses = self._identify_risk_clauses(contract_text)
        
        # Calculate overall risk score
        overall_score = self._calculate_overall_score(
            financial_risk,
            legal_risk,
            operational_risk,
            reputational_risk
        )
        
        # Determine risk level
        risk_level = self._determine_risk_level(overall_score)
        
        # Generate mitigation strategies
        mitigations = self._generate_mitigations(risk_clauses, risk_level)
        
        # Red flags
        red_flags = self._identify_red_flags(risk_clauses)
        
        return {
            'success': True,
            'assessment_id': f"RISK-{self.assessments_performed:06d}",
            'overall_risk_score': round(overall_score, 1),
            'overall_risk_level': risk_level,
            'risk_breakdown': {
                'financial': financial_risk,
                'legal': legal_risk,
                'operational': operational_risk,
                'reputational': reputational_risk
            },
            'risk_clauses': risk_clauses,
            'red_flags': red_flags,
            'mitigations': mitigations,
            'recommendation': self._get_recommendation(risk_level),
            'timestamp': datetime.now().isoformat()
        }
    
    def _assess_financial_risk(self, text: str, contract_value: Optional[float]) -> Dict:
        """Assess financial risk"""
        
        text_lower = text.lower()
        score = 0
        factors = []
        
        # Check for liability caps
        if 'unlimited liability' in text_lower or 'no cap' in text_lower:
            score += 30
            factors.append('Unlimited liability exposure')
        elif 'liability limited to' in text_lower or 'cap' in text_lower:
            score += 5
            factors.append('Liability capped')
        else:
            score += 15
            factors.append('Liability terms unclear')
        
        # Payment terms
        if 'non-refundable' in text_lower:
            score += 15
            factors.append('Non-refundable payments')
        
        if 'penalty' in text_lower or 'liquidated damages' in text_lower:
            score += 20
            factors.append('Financial penalties present')
        
        # Contract value risk
        if contract_value:
            if contract_value > self.financial_thresholds['contract_value']['high']:
                score += 20
                factors.append(f'High contract value: ${contract_value:,.0f}')
            elif contract_value > self.financial_thresholds['contract_value']['medium']:
                score += 10
                factors.append(f'Medium contract value: ${contract_value:,.0f}')
        
        # Currency risk
        if any(curr in text for curr in ['EUR', '€', 'GBP', '£', 'JPY', '¥']):
            score += 10
            factors.append('Foreign currency exposure')
        
        return {
            'score': min(score, 100),
            'level': self._score_to_level(score),
            'factors': factors
        }
    
    def _assess_legal_risk(self, text: str) -> Dict:
        """Assess legal risk"""
        
        text_lower = text.lower()
        score = 0
        factors = []
        
        # Jurisdiction
        if 'governing law' not in text_lower:
            score += 15
            factors.append('No governing law specified')
        elif any(foreign in text_lower for foreign in ['england', 'germany', 'china', 'singapore']):
            score += 20
            factors.append('Foreign jurisdiction')
        
        # Dispute resolution
        if 'arbitration' in text_lower:
            score += 5
            factors.append('Arbitration required')
        elif 'litigation' in text_lower or 'court' in text_lower:
            score += 10
            factors.append('Litigation pathway')
        else:
            score += 15
            factors.append('Dispute resolution unclear')
        
        # Indemnification
        if 'indemnify' in text_lower or 'hold harmless' in text_lower:
            if 'broad' in text_lower or 'unlimited' in text_lower:
                score += 25
                factors.append('Broad indemnification obligations')
            else:
                score += 10
                factors.append('Standard indemnification')
        
        # IP assignment
        if 'assign' in text_lower and 'intellectual property' in text_lower:
            score += 15
            factors.append('IP assignment required')
        
        # Non-compete
        if 'non-compete' in text_lower or 'non-competition' in text_lower:
            score += 15
            factors.append('Non-compete restrictions')
        
        return {
            'score': min(score, 100),
            'level': self._score_to_level(score),
            'factors': factors
        }
    
    def _assess_operational_risk(self, text: str) -> Dict:
        """Assess operational risk"""
        
        text_lower = text.lower()
        score = 0
        factors = []
        
        # Termination terms
        if 'without cause' in text_lower:
            score += 20
            factors.append('Termination without cause allowed')
        
        if 'immediate termination' in text_lower:
            score += 15
            factors.append('Immediate termination possible')
        
        # Performance obligations
        if 'service level' in text_lower or 'sla' in text_lower:
            score += 10
            factors.append('SLA commitments required')
        
        # Exclusivity
        if 'exclusive' in text_lower or 'solely' in text_lower:
            score += 15
            factors.append('Exclusivity obligations')
        
        # Change control
        if 'change of control' in text_lower:
            score += 10
            factors.append('Change of control provisions')
        
        # Renewal terms
        if 'automatic renewal' in text_lower or 'auto-renew' in text_lower:
            score += 15
            factors.append('Automatic renewal')
        
        return {
            'score': min(score, 100),
            'level': self._score_to_level(score),
            'factors': factors
        }
    
    def _assess_reputational_risk(self, text: str) -> Dict:
        """Assess reputational risk"""
        
        text_lower = text.lower()
        score = 0
        factors = []
        
        # Confidentiality
        if 'confidential' not in text_lower:
            score += 15
            factors.append('No confidentiality protections')
        
        # Non-disparagement
        if 'non-disparagement' in text_lower:
            score += 5
            factors.append('Non-disparagement clause present')
        
        # Publicity rights
        if 'publicity' in text_lower or 'marketing' in text_lower:
            if 'without consent' in text_lower:
                score += 20
                factors.append('Publicity without consent')
            else:
                score += 5
                factors.append('Publicity rights addressed')
        
        # Data handling
        if any(term in text_lower for term in ['personal data', 'pii', 'gdpr', 'privacy']):
            score += 10
            factors.append('Data privacy obligations')
        
        return {
            'score': min(score, 100),
            'level': self._score_to_level(score),
            'factors': factors
        }
    
    def _identify_risk_clauses(self, text: str) -> List[Dict]:
        """Identify specific risky clauses"""
        
        clauses = []
        text_lower = text.lower()
        
        for severity, indicators in self.risk_indicators.items():
            for indicator, risk_score in indicators.items():
                if indicator in text_lower:
                    # Find context
                    pattern = re.compile(f'.{{0,100}}{re.escape(indicator)}.{{0,100}}', re.IGNORECASE)
                    matches = pattern.findall(text)
                    
                    for match in matches[:1]:  # First occurrence
                        clauses.append({
                            'severity': severity,
                            'indicator': indicator,
                            'risk_score': risk_score,
                            'context': match.strip(),
                            'recommendation': self._get_clause_recommendation(indicator)
                        })
        
        # Sort by risk score
        clauses.sort(key=lambda x: x['risk_score'], reverse=True)
        
        return clauses[:10]  # Top 10 risks
    
    def _calculate_overall_score(self, financial, legal, operational, reputational) -> float:
        """Calculate weighted overall risk score"""
        
        # Weighted average
        weights = {
            'financial': 0.35,
            'legal': 0.30,
            'operational': 0.20,
            'reputational': 0.15
        }
        
        score = (
            financial['score'] * weights['financial'] +
            legal['score'] * weights['legal'] +
            operational['score'] * weights['operational'] +
            reputational['score'] * weights['reputational']
        )
        
        return score
    
    def _determine_risk_level(self, score: float) -> str:
        """Determine overall risk level"""
        
        if score >= 70:
            return 'CRITICAL'
        elif score >= 50:
            return 'HIGH'
        elif score >= 30:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _identify_red_flags(self, risk_clauses: List[Dict]) -> List[str]:
        """Identify critical red flags"""
        
        red_flags = []
        
        critical_clauses = [c for c in risk_clauses if c['severity'] == 'CRITICAL']
        
        for clause in critical_clauses[:5]:  # Top 5
            red_flags.append(
                f"⚠️ {clause['indicator'].upper()}: {clause['context'][:100]}..."
            )
        
        return red_flags
    
    def _generate_mitigations(self, risk_clauses: List[Dict], risk_level: str) -> List[str]:
        """Generate risk mitigation strategies"""
        
        mitigations = []
        
        if risk_level in ['CRITICAL', 'HIGH']:
            mitigations.append('🔴 URGENT: Legal review required before signing')
        
        # Top 3 risks
        for clause in risk_clauses[:3]:
            mitigations.append(clause['recommendation'])
        
        # General strategies
        if risk_level == 'CRITICAL':
            mitigations.append('Consider negotiating liability caps')
            mitigations.append('Add termination for convenience clause')
            mitigations.append('Request indemnification protections')
        
        return mitigations[:7]
    
    def _get_clause_recommendation(self, indicator: str) -> str:
        """Get recommendation for specific clause"""
        
        recommendations = {
            'unlimited liability': 'Negotiate liability cap (e.g., contract value or $1M)',
            'no indemnification': 'Request mutual indemnification provisions',
            'automatic renewal': 'Add notice period for non-renewal (60-90 days)',
            'unilateral termination': 'Request bilateral termination rights',
            'no warranty': 'Negotiate limited warranty period',
            'non-compete': 'Limit scope, duration, and geography',
            'exclusive rights': 'Add performance minimums or opt-out clause',
            'penalty clause': 'Convert to liquidated damages with reasonable cap'
        }
        
        return recommendations.get(
            indicator,
            f'Review and negotiate {indicator} terms'
        )
    
    def _get_recommendation(self, risk_level: str) -> str:
        """Get overall recommendation"""
        
        recommendations = {
            'CRITICAL': '🔴 DO NOT SIGN - Critical risks identified. Legal review mandatory.',
            'HIGH': '🟠 PROCEED WITH CAUTION - Significant risks. Negotiate key terms.',
            'MEDIUM': '🟡 ACCEPTABLE WITH REVIEW - Moderate risks. Review flagged items.',
            'LOW': '🟢 LOW RISK - Standard terms. Proceed with normal review.'
        }
        
        return recommendations.get(risk_level, 'Review recommended')
    
    def _score_to_level(self, score: float) -> str:
        """Convert score to risk level"""
        
        if score >= 70:
            return 'CRITICAL'
        elif score >= 50:
            return 'HIGH'
        elif score >= 30:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def get_stats(self) -> Dict:
        """Get assessor statistics"""
        return {
            'version': self.version,
            'assessments_performed': self.assessments_performed,
            'risk_indicators_tracked': sum(len(v) for v in self.risk_indicators.values()),
            'status': 'active'
        }


# Test
if __name__ == '__main__':
    print("\n" + "="*70)
    print("RISK ASSESSOR - Test")
    print("="*70 + "\n")
    
    assessor = RiskAssessor()
    
    test_contract = """
    SERVICE AGREEMENT
    
    This agreement includes unlimited liability and automatic renewal.
    No indemnification provided. Termination without cause allowed.
    Non-refundable fees. Penalty clauses apply.
    Governing law: England. Exclusive rights granted.
    """
    
    result = assessor.assess_risk(
        contract_text=test_contract,
        contract_value=500000,
        contract_type='service'
    )
    
    print(json.dumps(result, indent=2, default=str))
    print("\n" + "="*70)