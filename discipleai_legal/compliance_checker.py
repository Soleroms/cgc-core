"""
Compliance Checker
Verifies contract compliance with regulations and standards
"""

from typing import Dict, List, Optional
from datetime import datetime
import json


class ComplianceChecker:
    """
    Compliance verification against legal standards
    GDPR, HIPAA, SOX, Employment Law, etc.
    """
    
    def __init__(self):
        self.version = "1.0.0"
        self.checks_performed = 0
        
        # Compliance frameworks
        self.frameworks = {
            'GDPR': {
                'name': 'General Data Protection Regulation',
                'region': 'EU',
                'requirements': [
                    'data processing consent',
                    'right to erasure',
                    'data portability',
                    'privacy by design',
                    'data breach notification'
                ]
            },
            'HIPAA': {
                'name': 'Health Insurance Portability and Accountability Act',
                'region': 'US',
                'requirements': [
                    'PHI protection',
                    'minimum necessary standard',
                    'patient rights',
                    'security safeguards',
                    'breach notification'
                ]
            },
            'SOX': {
                'name': 'Sarbanes-Oxley Act',
                'region': 'US',
                'requirements': [
                    'financial disclosure',
                    'internal controls',
                    'audit independence',
                    'criminal penalties',
                    'whistleblower protection'
                ]
            },
            'EMPLOYMENT_LAW': {
                'name': 'US Employment Law',
                'region': 'US',
                'requirements': [
                    'at-will employment disclosure',
                    'equal employment opportunity',
                    'wage and hour compliance',
                    'workplace safety',
                    'anti-discrimination'
                ]
            },
            'CCPA': {
                'name': 'California Consumer Privacy Act',
                'region': 'California',
                'requirements': [
                    'disclosure of data collection',
                    'right to opt-out',
                    'right to deletion',
                    'non-discrimination',
                    'data security'
                ]
            }
        }
        
        print(f"✅ Compliance Checker v{self.version} initialized")
        print(f"   Frameworks loaded: {len(self.frameworks)}")
    
    def check_compliance(
        self,
        contract_text: str,
        contract_type: str = "general",
        jurisdiction: str = "US",
        industry: Optional[str] = None
    ) -> Dict:
        """
        Check contract compliance
        
        Args:
            contract_text: Full contract text
            contract_type: Type of contract
            jurisdiction: Legal jurisdiction
            industry: Industry sector
            
        Returns:
            Compliance assessment
        """
        
        self.checks_performed += 1
        
        # Determine applicable frameworks
        applicable = self._determine_frameworks(
            contract_type, jurisdiction, industry
        )
        
        # Check each framework
        results = {}
        for framework_id in applicable:
            results[framework_id] = self._check_framework(
                contract_text,
                framework_id
            )
        
        # Calculate overall score
        overall_score = self._calculate_score(results)
        
        # Identify violations
        violations = self._identify_violations(results)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(violations)
        
        return {
            'success': True,
            'check_id': f"COMP-{self.checks_performed:06d}",
            'overall_score': round(overall_score, 1),
            'compliance_level': self._get_level(overall_score),
            'applicable_frameworks': applicable,
            'framework_results': results,
            'violations': violations,
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        }
    
    def _determine_frameworks(
        self,
        contract_type: str,
        jurisdiction: str,
        industry: Optional[str]
    ) -> List[str]:
        """Determine which frameworks apply"""
        
        applicable = []
        
        # Employment contracts
        if 'employment' in contract_type.lower():
            applicable.append('EMPLOYMENT_LAW')
        
        # Healthcare
        if industry and 'health' in industry.lower():
            applicable.append('HIPAA')
        
        # Financial
        if industry and any(x in industry.lower() for x in ['finance', 'banking', 'investment']):
            applicable.append('SOX')
        
        # EU jurisdiction
        if jurisdiction.upper() in ['EU', 'UK', 'EUROPE']:
            applicable.append('GDPR')
        
        # California
        if jurisdiction.upper() in ['CA', 'CALIFORNIA']:
            applicable.append('CCPA')
        
        # Default to GDPR for data processing
        if not applicable and 'data' in contract_type.lower():
            applicable.append('GDPR')
        
        return applicable if applicable else ['EMPLOYMENT_LAW']
    
    def _check_framework(self, text: str, framework_id: str) -> Dict:
        """Check compliance with specific framework"""
        
        framework = self.frameworks[framework_id]
        requirements = framework['requirements']
        
        text_lower = text.lower()
        
        met = []
        missing = []
        
        for req in requirements:
            # Simple keyword matching (in production, use NLP)
            keywords = req.lower().split()
            if any(kw in text_lower for kw in keywords):
                met.append(req)
            else:
                missing.append(req)
        
        compliance_rate = len(met) / len(requirements) if requirements else 0
        
        return {
            'framework': framework['name'],
            'region': framework['region'],
            'requirements_total': len(requirements),
            'requirements_met': len(met),
            'requirements_missing': len(missing),
            'compliance_rate': round(compliance_rate * 100, 1),
            'met': met,
            'missing': missing,
            'status': 'COMPLIANT' if compliance_rate >= 0.8 else 'NON_COMPLIANT'
        }
    
    def _calculate_score(self, results: Dict) -> float:
        """Calculate overall compliance score"""
        
        if not results:
            return 0.0
        
        scores = [r['compliance_rate'] for r in results.values()]
        return sum(scores) / len(scores)
    
    def _identify_violations(self, results: Dict) -> List[Dict]:
        """Identify compliance violations"""
        
        violations = []
        
        for framework_id, result in results.items():
            if result['requirements_missing']:
                for missing in result['requirements_missing']:
                    violations.append({
                        'framework': result['framework'],
                        'severity': 'HIGH' if result['compliance_rate'] < 50 else 'MEDIUM',
                        'requirement': missing,
                        'description': f"Missing requirement: {missing}"
                    })
        
        return violations
    
    def _generate_recommendations(self, violations: List[Dict]) -> List[str]:
        """Generate compliance recommendations"""
        
        if not violations:
            return ['Contract appears compliant with applicable frameworks']
        
        recommendations = []
        
        # Group by framework
        by_framework = {}
        for v in violations:
            fw = v['framework']
            if fw not in by_framework:
                by_framework[fw] = []
            by_framework[fw].append(v['requirement'])
        
        for framework, reqs in by_framework.items():
            recommendations.append(
                f"Add {framework} requirements: {', '.join(reqs[:3])}"
            )
        
        # Severity-based
        high_severity = [v for v in violations if v['severity'] == 'HIGH']
        if high_severity:
            recommendations.insert(0, 
                f"URGENT: Address {len(high_severity)} high-severity compliance gaps"
            )
        
        return recommendations[:5]  # Top 5
    
    def _get_level(self, score: float) -> str:
        """Get compliance level"""
        
        if score >= 90:
            return 'EXCELLENT'
        elif score >= 80:
            return 'GOOD'
        elif score >= 70:
            return 'ACCEPTABLE'
        elif score >= 60:
            return 'NEEDS_IMPROVEMENT'
        else:
            return 'NON_COMPLIANT'
    
    def get_stats(self) -> Dict:
        """Get checker statistics"""
        return {
            'version': self.version,
            'checks_performed': self.checks_performed,
            'frameworks_available': len(self.frameworks),
            'status': 'active'
        }


# Test
if __name__ == '__main__':
    print("\n" + "="*70)
    print("COMPLIANCE CHECKER - Test")
    print("="*70 + "\n")
    
    checker = ComplianceChecker()
    
    test_contract = """
    EMPLOYMENT AGREEMENT
    
    This agreement complies with equal employment opportunity laws.
    Wage and hour compliance is maintained.
    At-will employment disclosure included.
    Workplace safety standards enforced.
    """
    
    result = checker.check_compliance(
        contract_text=test_contract,
        contract_type='employment',
        jurisdiction='US'
    )
    
    print(json.dumps(result, indent=2))