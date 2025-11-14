"""
DiscipleAI Legal™
OlympusMont Systems LLC

AI-Powered Legal Analysis with Ethical Governance
Subsidiary #1 of OlympusMont Systems
"""

__version__ = "1.0.0"
__subsidiary__ = "DiscipleAI Legal"
__parent__ = "OlympusMont Systems LLC"

from .legal_core import LegalCore
from .contract_analyzer import ContractAnalyzer
from .compliance_checker import ComplianceChecker
from .risk_assessor import RiskAssessor

__all__ = [
    'LegalCore',
    'ContractAnalyzer', 
    'ComplianceChecker',
    'RiskAssessor'
]

print(f"✅ {__subsidiary__} v{__version__} initialized")