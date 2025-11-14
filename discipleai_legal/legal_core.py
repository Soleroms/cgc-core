"""
Legal Core Module
DiscipleAI Legal™ - Main Engine
"""

import sys
import os
from datetime import datetime
from typing import Dict, List, Optional

# Add cgc_core to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'cgc_core')))

try:
    from cgc_core_integration import create_cgc_core
    CGC_AVAILABLE = True
except ImportError:
    CGC_AVAILABLE = False
    print("⚠️ CGC Core not available - running in standalone mode")


class LegalCore:
    """
    Core engine for DiscipleAI Legal
    Integrates with CGC Core for governance
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize Legal Core with CGC governance"""
        
        self.subsidiary_name = "DiscipleAI Legal"
        self.version = "1.0.0"
        self.parent_company = "OlympusMont Systems LLC"
        
        # CGC Core configuration
        if config is None:
            config = {
                'confidence_threshold': 0.90,  # High confidence for legal
                'ethical_threshold': 0.85,     # High ethics for legal
                'strict_ethical_mode': True,
                'enable_auto_execution': False
            }
        
        # Initialize CGC Core
        if CGC_AVAILABLE:
            self.cgc = create_cgc_core(config)
            print(f"✅ CGC Core governance active")
        else:
            self.cgc = None
            print(f"⚠️ Running without CGC governance")
        
        # Metrics
        self.total_analyses = 0
        self.total_contracts = 0
        self.total_violations = 0
        self.start_time = datetime.now()
        
        print(f"✅ {self.subsidiary_name} v{self.version} initialized")
    
    def analyze_with_governance(
        self, 
        action: str, 
        legal_data: Dict, 
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Execute legal analysis with CGC Core governance
        
        Args:
            action: Legal action to perform
            legal_data: Legal document/data to analyze
            context: Additional context
            
        Returns:
            dict: Analysis result with governance metadata
        """
        
        if context is None:
            context = {}
        
        # Add legal context
        context.update({
            'subsidiary': self.subsidiary_name,
            'parent': self.parent_company,
            'version': self.version,
            'timestamp': datetime.now().isoformat(),
            'analysis_type': 'legal'
        })
        
        # If CGC available, use governance
        if self.cgc:
            result = self.cgc.execute_decision(
                module='discipleai_legal',
                action=action,
                input_data=legal_data,
                context=context
            )
        else:
            # Standalone mode
            result = {
                'decision': {
                    'approved': True,
                    'confidence': 0.80,
                    'decision': 'APPROVED',
                    'reasoning': 'Standalone mode - no governance'
                },
                'analysis': self._perform_analysis(action, legal_data),
                'metadata': context
            }
        
        self.total_analyses += 1
        return result
    
    def _perform_analysis(self, action: str, legal_data: Dict) -> Dict:
    """
    Perform actual legal analysis with AI
    """
    
    # Try to use AI analyzer if available
    try:
        from .contract_analyzer_ai import AIContractAnalyzer
        
        analyzer = AIContractAnalyzer()
        
        # Extract contract text if present
        contract_text = legal_data.get('contract_text', '')
        
        if contract_text:
            result = analyzer.analyze_contract(
                contract_text=contract_text,
                metadata=legal_data.get('metadata', {})
            )
            return {
                'action': action,
                'status': 'analyzed',
                'ai_powered': True,
                'analysis': result
            }
    
    except Exception as e:
        print(f"⚠️ AI analysis failed: {e}")
    
    # Fallback to basic analysis
    return {
        'action': action,
        'status': 'analyzed',
        'ai_powered': False,
        'findings': ['Basic analysis only - AI not available'],
        'recommendations': ['Enable OpenAI API for advanced analysis']
    }    
    def get_status(self) -> Dict:
        """Get subsidiary status"""
        
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        return {
            'subsidiary': self.subsidiary_name,
            'parent': self.parent_company,
            'version': self.version,
            'status': 'active',
            'cgc_governance': CGC_AVAILABLE,
            'metrics': {
                'total_analyses': self.total_analyses,
                'total_contracts': self.total_contracts,
                'total_violations': self.total_violations,
                'uptime_seconds': uptime
            },
            'modules': {
                'contract_analyzer': True,
                'compliance_checker': True,
                'risk_assessor': True,
                'clause_extractor': True
            }
        }


# Test function
if __name__ == '__main__':
    print("\n" + "="*60)
    print("DiscipleAI Legal™ - Test Mode")
    print("="*60 + "\n")
    
    # Initialize
    legal = LegalCore()
    
    # Test analysis
    test_contract = {
        'type': 'NDA',
        'parties': ['Company A', 'Company B'],
        'clauses': 12,
        'jurisdiction': 'USA'
    }
    
    result = legal.analyze_with_governance(
        action='analyze_contract',
        legal_data=test_contract,
        context={'test': True}
    )
    
    print("\n📊 Analysis Result:")
    import json
    print(json.dumps(result, indent=2, default=str))
    
    print("\n📈 Status:")
    print(json.dumps(legal.get_status(), indent=2))