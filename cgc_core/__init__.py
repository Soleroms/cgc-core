"""
CGC CORE™
Cognitive Governance Cycle - Complete Implementation
OlympusMont Systems LLC

The heart of all decision-making across subsidiaries
"""

__version__ = "2.1.4"
__core__ = "CGC CORE"
__company__ = "OlympusMont Systems LLC"

from .core_engine import CGCCoreEngine
from .pan_module import PerceptionAnalysisNode
from .ecm_module import EthicalCalibrationModule
from .pfm_module import PredictiveFeedbackMechanism
from .sda_module import SmartDataAdvisor
from .tco_module import TraceabilityOversight

__all__ = [
    "CGCCoreEngine",
    "PerceptionAnalysisNode",
    "EthicalCalibrationModule",
    "PredictiveFeedbackMechanism",
    "SmartDataAdvisor",
    "TraceabilityOversight"
]

print(f"✅ {__core__} v{__version__} initialized")
print("   Complete cognitive governance active")