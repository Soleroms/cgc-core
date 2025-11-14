"""
Compliance Checker Module
DiscipleAI Legal™
"""

from typing import Dict, List


class ComplianceChecker:
    """
    Multi-framework compliance verification
    Supports: ISO 27001, GDPR, CCPA, SOC 2, HIPAA
    """
    
    FRAMEWORKS = {
        'ISO_27001': 'Information Security Management',
        'GDPR': 'EU General Data Protection Regulation',
        'CCPA': 'California Consumer Privacy Act',
        'LGPD': 'Brazil General Data Protection Law',
        'SOC2': 'Service Organization Control 2',
        'HIPAA': 'Health Insurance Portability and Accountability Act'
    }
    
    def __init__(self):
        self.checks_performed = 0
    
    def check_compliance(self, contract_text: str, frameworks: List[str] = None) -> Dict:
        """
        Check contract compliance against specified frameworks
        
        Args:
            contract_text: Contract text to analyze
            frameworks: List of framework codes (default: all)
            
        Returns:
            dict: Compliance results per framework
        """
        
        if frameworks is None:
            frameworks = list(self.FRAMEWORKS.keys())
        
        results = {}
        
        for framework in frameworks:
            if framework in self.FRAMEWORKS:
                results[framework] = self._check_framework(
                    contract_text, 
                    framework
                )
        
        self.checks_performed += 1
        
        return {
            'frameworks_checked': frameworks,
            'results': results,
            'overall_compliance': self._calculate_overall_score(results)
        }
    
    def _check_framework(self, text: str, framework: str) -> Dict:
        """Check compliance with specific framework"""
        
        # Framework-specific keywords
        keywords = self._get_framework_keywords(framework)
        
        # Count keyword matches
        matches = sum(1 for kw in keywords if kw.lower() in text.lower())
        score = min((matches / len(keywords)) * 100, 100)
        
        # Determine compliance level
        if score >= 80:
            level = 'COMPLIANT'
            risk = 'LOW'
        elif score >= 50:
            level = 'PARTIAL'
            risk = 'MEDIUM'
        else:
            level = 'NON_COMPLIANT'
            risk = 'HIGH'
        
        return {
            'framework': self.FRAMEWORKS[framework],
            'code': framework,
            'score': round(score, 1),
            'level': level,
            'risk': risk,
            'matches': matches,
            'total_checks': len(keywords)
        }
    
    def _get_framework_keywords(self, framework: str) -> List[str]:
        """Get keywords for framework checking"""
        
        keywords_map = {
            'ISO_27001': [
                'information security', 'confidentiality', 'integrity',
                'availability', 'access control', 'encryption', 
                'security policy', 'risk assessment'
            ],
            'GDPR': [
                'personal data', 'data subject', 'consent', 'privacy',
                'data protection', 'right to erasure', 'data breach',
                'data controller', 'data processor'
            ],
            'CCPA': [
                'personal information', 'consumer rights', 'opt-out',
                'california', 'sale of data', 'privacy notice'
            ],
            'LGPD': [
                'dados pessoais', 'titular', 'consentimento', 'lgpd',
                'personal data', 'brazil', 'data protection'
            ],
            'SOC2': [
                'security controls', 'availability', 'processing integrity',
                'confidentiality', 'privacy', 'audit', 'monitoring'
            ],
            'HIPAA': [
                'protected health information', 'phi', 'hipaa', 
                'healthcare', 'medical records', 'patient privacy',
                'business associate'
            ]
        }
        
        return keywords_map.get(framework, [])
    
    def _calculate_overall_score(self, results: Dict) -> Dict:
        """Calculate overall compliance score"""
        
        if not results:
            return {'score': 0, 'level': 'UNKNOWN'}
        
        scores = [r['score'] for r in results.values()]
        avg_score = sum(scores) / len(scores)
        
        if avg_score >= 80:
            level = 'STRONG'
        elif avg_score >= 60:
            level = 'ADEQUATE'
        elif avg_score >= 40:
            level = 'WEAK'
        else:
            level = 'POOR'
        
        return {
            'score': round(avg_score, 1),
            'level': level
        }


# Test
if __name__ == '__main__':
    checker = ComplianceChecker()
    
    sample = """
    This agreement includes provisions for data protection and privacy.
    All personal data will be handled in accordance with GDPR requirements.
    The parties agree to implement appropriate security controls and encryption.
    """
    
    result = checker.check_compliance(sample, ['GDPR', 'ISO_27001'])
    
    import json
    print(json.dumps(result, indent=2))