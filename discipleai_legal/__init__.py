"""
DiscipleAI Legal™
Complete legal AI suite
"""

__version__ = "1.0.0"
__subsidiary__ = "DiscipleAI Legal"
__parent__ = "OlympusMont Systems LLC"

from .contract_analyzer_ai import ContractAnalyzerAI
from .compliance_checker import ComplianceChecker
from .risk_assessor import RiskAssessor
from .clause_extractor import ClauseExtractor
from .legal_research_engine import LegalResearchEngine

__all__ = [
    'ContractAnalyzerAI',
    'ComplianceChecker',
    'RiskAssessor',
    'ClauseExtractor',
    'LegalResearchEngine'
]

print(f"✅ {__subsidiary__} v{__version__} initialized")
print(f"   Complete legal AI suite loaded")