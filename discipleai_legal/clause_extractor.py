"""
Clause Extractor
AI-powered extraction and analysis of contract clauses
"""

from typing import Dict, List, Optional
from datetime import datetime
import json
import re


class ClauseExtractor:
    """
    Intelligent clause extraction and categorization
    Identifies and analyzes key contract provisions
    """
    
    def __init__(self):
        self.version = "1.0.0"
        self.extractions_performed = 0
        
        # Clause patterns and categories
        self.clause_categories = {
            'PARTIES': {
                'keywords': ['party', 'parties', 'between', 'hereinafter', 'referred to as'],
                'importance': 'CRITICAL'
            },
            'DEFINITIONS': {
                'keywords': ['means', 'defined as', 'shall mean', 'refers to', 'definition'],
                'importance': 'HIGH'
            },
            'PAYMENT': {
                'keywords': ['payment', 'fee', 'compensation', 'price', 'cost', 'invoice', 'remuneration'],
                'importance': 'CRITICAL'
            },
            'TERM': {
                'keywords': ['term', 'duration', 'period', 'commence', 'expiration', 'effective date'],
                'importance': 'CRITICAL'
            },
            'TERMINATION': {
                'keywords': ['termination', 'terminate', 'cancel', 'end', 'cessation'],
                'importance': 'CRITICAL'
            },
            'CONFIDENTIALITY': {
                'keywords': ['confidential', 'proprietary', 'non-disclosure', 'secret', 'private'],
                'importance': 'HIGH'
            },
            'INTELLECTUAL_PROPERTY': {
                'keywords': ['intellectual property', 'ip', 'copyright', 'trademark', 'patent', 'trade secret'],
                'importance': 'HIGH'
            },
            'LIABILITY': {
                'keywords': ['liability', 'indemnify', 'indemnification', 'hold harmless', 'damages'],
                'importance': 'CRITICAL'
            },
            'WARRANTY': {
                'keywords': ['warranty', 'warrants', 'guarantee', 'representation'],
                'importance': 'HIGH'
            },
            'DISPUTE_RESOLUTION': {
                'keywords': ['dispute', 'arbitration', 'mediation', 'litigation', 'jurisdiction'],
                'importance': 'HIGH'
            },
            'GOVERNING_LAW': {
                'keywords': ['governing law', 'applicable law', 'jurisdiction', 'venue'],
                'importance': 'HIGH'
            },
            'FORCE_MAJEURE': {
                'keywords': ['force majeure', 'act of god', 'unforeseeable', 'beyond control'],
                'importance': 'MEDIUM'
            },
            'ASSIGNMENT': {
                'keywords': ['assignment', 'assign', 'transfer', 'delegate'],
                'importance': 'MEDIUM'
            },
            'AMENDMENTS': {
                'keywords': ['amendment', 'modify', 'change', 'alteration', 'variation'],
                'importance': 'MEDIUM'
            },
            'NOTICES': {
                'keywords': ['notice', 'notification', 'notify', 'communication'],
                'importance': 'MEDIUM'
            },
            'NON_COMPETE': {
                'keywords': ['non-compete', 'non-competition', 'competitive', 'compete'],
                'importance': 'HIGH'
            },
            'NON_SOLICITATION': {
                'keywords': ['non-solicitation', 'solicit', 'hiring', 'employee'],
                'importance': 'MEDIUM'
            }
        }
        
        print(f"✅ Clause Extractor v{self.version} initialized")
        print(f"   Clause categories: {len(self.clause_categories)}")
    
    def extract_clauses(
        self,
        contract_text: str,
        extract_full_text: bool = True,
        categorize: bool = True
    ) -> Dict:
        """
        Extract and analyze contract clauses
        
        Args:
            contract_text: Full contract text
            extract_full_text: Whether to extract full clause text
            categorize: Whether to categorize clauses
            
        Returns:
            Extracted clauses with analysis
        """
        
        self.extractions_performed += 1
        
        # Split into sections
        sections = self._split_sections(contract_text)
        
        # Identify clauses
        clauses = []
        
        if categorize:
            for category, config in self.clause_categories.items():
                found = self._find_category_clauses(
                    contract_text,
                    category,
                    config,
                    extract_full_text
                )
                clauses.extend(found)
        
        # Extract monetary amounts
        amounts = self._extract_amounts(contract_text)
        
        # Extract dates
        dates = self._extract_dates(contract_text)
        
        # Extract parties
        parties = self._extract_parties(contract_text)
        
        # Analyze clause coverage
        coverage = self._analyze_coverage(clauses)
        
        # Missing critical clauses
        missing = self._identify_missing(clauses)
        
        return {
            'success': True,
            'extraction_id': f"EXTRACT-{self.extractions_performed:06d}",
            'total_clauses': len(clauses),
            'clauses': clauses,
            'parties': parties,
            'amounts': amounts,
            'dates': dates,
            'coverage': coverage,
            'missing_critical': missing,
            'timestamp': datetime.now().isoformat()
        }
    
    def _split_sections(self, text: str) -> List[str]:
        """Split contract into sections"""
        
        # Split by numbered sections or headers
        sections = []
        
        # Try numbered sections (1., 2., etc.)
        numbered = re.split(r'\n\s*\d+\.', text)
        if len(numbered) > 3:
            return numbered
        
        # Try lettered sections (A., B., etc.)
        lettered = re.split(r'\n\s*[A-Z]\.', text)
        if len(lettered) > 3:
            return lettered
        
        # Default: split by double newlines
        paragraphs = text.split('\n\n')
        return [p.strip() for p in paragraphs if p.strip()]
    
    def _find_category_clauses(
        self,
        text: str,
        category: str,
        config: Dict,
        extract_full: bool
    ) -> List[Dict]:
        """Find clauses for specific category"""
        
        clauses = []
        text_lower = text.lower()
        
        for keyword in config['keywords']:
            # Find occurrences
            pattern = re.compile(
                f'.{{0,50}}{re.escape(keyword)}.{{0,200}}',
                re.IGNORECASE | re.DOTALL
            )
            
            matches = pattern.findall(text)
            
            for match in matches[:1]:  # First occurrence per keyword
                clauses.append({
                    'category': category,
                    'importance': config['importance'],
                    'keyword': keyword,
                    'snippet': match.strip(),
                    'full_text': self._extract_full_clause(text, keyword) if extract_full else None
                })
        
        return clauses
    
    def _extract_full_clause(self, text: str, keyword: str) -> str:
        """Extract full clause text around keyword"""
        
        # Find the paragraph containing keyword
        paragraphs = text.split('\n\n')
        
        for para in paragraphs:
            if keyword.lower() in para.lower():
                return para.strip()
        
        return ""
    
    def _extract_amounts(self, text: str) -> List[Dict]:
        """Extract monetary amounts"""
        
        amounts = []
        
        # Pattern for dollar amounts
        pattern = r'\$[\d,]+(?:\.\d{2})?'
        matches = re.findall(pattern, text)
        
        for match in matches:
            # Get context
            idx = text.find(match)
            context = text[max(0, idx-50):min(len(text), idx+100)]
            
            amounts.append({
                'amount': match,
                'numeric': float(match.replace('$', '').replace(',', '')),
                'context': context.strip()
            })
        
        return amounts
    
    def _extract_dates(self, text: str) -> List[Dict]:
        """Extract dates"""
        
        dates = []
        
        # Multiple date patterns
        patterns = [
            r'\d{1,2}/\d{1,2}/\d{4}',
            r'\d{4}-\d{2}-\d{2}',
            r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # Get context
                idx = text.find(match)
                context = text[max(0, idx-50):min(len(text), idx+100)]
                
                dates.append({
                    'date': match,
                    'context': context.strip()
                })
        
        return dates
    
    def _extract_parties(self, text: str) -> List[str]:
        """Extract party names"""
        
        parties = []
        
        # Look for common party patterns
        patterns = [
            r'between\s+([A-Z][A-Za-z\s&,.]+?)\s+\("',
            r'party[:\s]+([A-Z][A-Za-z\s&,.]+)',
            r'"([A-Z][A-Za-z\s&,.]+?)"\s+\(hereinafter',
            r'([A-Z][A-Za-z\s]+(?:Inc|LLC|Ltd|Corp|Corporation))'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            parties.extend(matches)
        
        # Clean and deduplicate
        parties = [p.strip() for p in parties if len(p.strip()) > 3]
        parties = list(set(parties))[:10]
        
        return parties
    
    def _analyze_coverage(self, clauses: List[Dict]) -> Dict:
        """Analyze clause coverage"""
        
        # Count by importance
        critical = len([c for c in clauses if c['importance'] == 'CRITICAL'])
        high = len([c for c in clauses if c['importance'] == 'HIGH'])
        medium = len([c for c in clauses if c['importance'] == 'MEDIUM'])
        
        # Categories covered
        categories = set(c['category'] for c in clauses)
        
        total_categories = len(self.clause_categories)
        coverage_pct = (len(categories) / total_categories) * 100 if total_categories > 0 else 0
        
        return {
            'total_categories': total_categories,
            'categories_found': len(categories),
            'coverage_percentage': round(coverage_pct, 1),
            'by_importance': {
                'critical': critical,
                'high': high,
                'medium': medium
            }
        }
    
    def _identify_missing(self, clauses: List[Dict]) -> List[str]:
        """Identify missing critical clauses"""
        
        found_categories = set(c['category'] for c in clauses)
        
        missing = []
        for category, config in self.clause_categories.items():
            if config['importance'] == 'CRITICAL' and category not in found_categories:
                missing.append(category)
        
        return missing
    
    def get_stats(self) -> Dict:
        """Get extractor statistics"""
        return {
            'version': self.version,
            'extractions_performed': self.extractions_performed,
            'categories_available': len(self.clause_categories),
            'status': 'active'
        }


# Test
if __name__ == '__main__':
    print("\n" + "="*70)
    print("CLAUSE EXTRACTOR - Test")
    print("="*70 + "\n")
    
    extractor = ClauseExtractor()
    
    test_contract = """
    SERVICE AGREEMENT
    
    Between TechCorp Inc. and ClientCo LLC.
    
    1. PAYMENT: Client shall pay $50,000 annually.
    
    2. TERM: This agreement commences January 1, 2025 and continues for 12 months.
    
    3. TERMINATION: Either party may terminate with 30 days notice.
    
    4. CONFIDENTIALITY: All information shall remain confidential.
    
    5. GOVERNING LAW: This agreement is governed by California law.
    """
    
    result = extractor.extract_clauses(test_contract)
    
    print(json.dumps(result, indent=2, default=str))
    print("\n" + "="*70)