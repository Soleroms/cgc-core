"""
Contract Analyzer: Base contract analysis functionality
"""

from typing import Dict, List, Optional
from datetime import datetime
import re
import json


class ContractAnalyzer:
    """
    Base Contract Analyzer
    Provides contract parsing and basic analysis
    """

    def __init__(self):
        self.version = "1.0.0"
        self.analyses_count = 0

        print(f"✅ Contract Analyzer v{self.version} initialized")

    def analyze_contract(self, contract_text: str, metadata: Optional[Dict] = None) -> Dict:
        """
        Analyze a contract

        Args:
            contract_text: Full text of contract
            metadata: Optional metadata (filename, etc)

        Returns:
            Analysis results
        """

        self.analyses_count += 1

        result = {
            'success': True,
            'analysis_id': f"CA-{self.analyses_count:06d}",
            'metadata': metadata or {},
            'contract_length': len(contract_text),
            'word_count': len(contract_text.split()),
            'timestamp': datetime.now().isoformat()
        }

        result['parties'] = self._extract_parties(contract_text)
        result['dates'] = self._extract_dates(contract_text)
        result['amounts'] = self._extract_amounts(contract_text)
        result['clauses'] = self._identify_clauses(contract_text)
        result['risk_level'] = self._assess_risk(contract_text)

        return result

    def _extract_parties(self, text: str) -> List[str]:
        """Extract party names from contract"""

        parties = []

        patterns = [
            r'between\s+([A-Z][A-Za-z\s&,.]+?)\s+\("',
            r'party[:\s]+([A-Z][A-Za-z\s&,.]+)',
            r'"([A-Z][A-Za-z\s&,.]+?)"\s+\(hereinafter',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text)
            parties.extend(matches)

        parties = [p.strip() for p in parties if len(p.strip()) > 3]
        return list(set(parties))[:10]

    def _extract_dates(self, text: str) -> List[str]:
        """Extract dates from contract"""

        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{4}',
            r'\d{4}-\d{2}-\d{2}',
            r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}'
        ]

        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            dates.extend(matches)

        return list(set(dates))[:10]

    def _extract_amounts(self, text: str) -> List[str]:
        """Extract monetary amounts"""

        pattern = r'\$[\d,]+(?:\.\d{2})?'
        amounts = re.findall(pattern, text)

        return list(set(amounts))[:10]

    def _identify_clauses(self, text: str) -> List[Dict]:
        """Identify contract clauses"""

        clauses = []

        clause_keywords = {
            'confidentiality': ['confidential', 'non-disclosure', 'proprietary'],
            'termination': ['terminate', 'termination', 'cancel'],
            'liability': ['liable', 'liability', 'indemnify'],
            'payment': ['payment', 'compensation', 'fee'],
            'intellectual_property': ['intellectual property', 'copyright', 'patent'],
            'non_compete': ['non-compete', 'non-competition'],
            'dispute_resolution': ['arbitration', 'dispute', 'mediation'],
            'governing_law': ['governing law', 'jurisdiction']
        }

        text_lower = text.lower()

        for clause_type, keywords in clause_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    clauses.append({
                        'type': clause_type,
                        'keyword': keyword,
                        'present': True
                    })
                    break

        return clauses

    def _assess_risk(self, text: str) -> str:
        """Basic risk assessment"""

        text_lower = text.lower()

        high_risk_terms = [
            'unlimited liability',
            'no warranty',
            'as is',
            'automatic renewal',
            'sole discretion',
            'unilateral'
        ]

        medium_risk_terms = [
            'may terminate',
            'without cause',
            'non-refundable',
            'subject to change'
        ]

        high_risk_count = sum(1 for term in high_risk_terms if term in text_lower)
        medium_risk_count = sum(1 for term in medium_risk_terms if term in text_lower)

        if high_risk_count >= 2:
            return 'HIGH'
        elif high_risk_count >= 1 or medium_risk_count >= 3:
            return 'MEDIUM'
        else:
            return 'LOW'

    def get_stats(self) -> Dict:
        """Get analyzer statistics"""
        return {
            'version': self.version,
            'analyses_count': self.analyses_count,
            'status': 'active'
        }


# Test
if __name__ == '__main__':
    analyzer = ContractAnalyzer()

    test_contract = """
    AGREEMENT between TechCorp Inc. and John Smith
    Date: January 15, 2025
    Payment: $120,000 per year
    This agreement contains confidentiality and non-compete clauses.
    """

    result = analyzer.analyze_contract(test_contract)
    print(json.dumps(result, indent=2, default=str))