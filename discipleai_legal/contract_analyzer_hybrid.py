"""
Hybrid Contract Analyzer
Combines rule-based + AI analysis
DiscipleAI Legal™ - OlympusMont Systems LLC
"""

import json
from typing import Dict, Optional
from datetime import datetime

# Import both analyzers
from .contract_analyzer import ContractAnalyzer as RuleBasedAnalyzer
from .contract_analyzer_ai import AIContractAnalyzer


class HybridContractAnalyzer:
    """
    Combines rule-based and AI analysis for best results
    
    Strategy:
    1. Fast rule-based pre-analysis
    2. AI deep analysis for complex cases
    3. Merge results
    """
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """
        Initialize hybrid analyzer
        
        Args:
            openai_api_key: Optional OpenAI key. If None, falls back to rule-based only
        """
        # Always have rule-based
        self.rule_analyzer = RuleBasedAnalyzer()
        
        # Try to init AI analyzer
        try:
            self.ai_analyzer = AIContractAnalyzer(api_key=openai_api_key)
            self.ai_available = True
            print("✅ Hybrid Analyzer: AI + Rules enabled")
        except Exception as e:
            self.ai_analyzer = None
            self.ai_available = False
            print(f"⚠️ Hybrid Analyzer: Rules only (AI unavailable: {e})")
        
        self.analyses_performed = 0
    
    def analyze(
        self, 
        contract_text: str, 
        metadata: Optional[Dict] = None,
        use_ai: bool = True
    ) -> Dict:
        """
        Perform hybrid analysis
        
        Args:
            contract_text: Contract to analyze
            metadata: Optional metadata
            use_ai: Whether to use AI (default True if available)
            
        Returns:
            dict: Combined analysis results
        """
        
        if metadata is None:
            metadata = {}
        
        start_time = datetime.now()
        
        # PHASE 1: Rule-based analysis (always)
        print("📊 Running rule-based analysis...")
        rule_result = self.rule_analyzer.analyze_contract(
            contract_text=contract_text,
            contract_metadata=metadata
        )
        
        # Extract rule-based insights
        rule_analysis = rule_result.get('contract_analysis', {})
        risk_score = rule_analysis.get('risk_score', 0)
        
        # PHASE 2: AI analysis (if available and requested)
        ai_result = None
        if use_ai and self.ai_available and self.ai_analyzer:
            # Only use AI if:
            # - High risk detected by rules
            # - Complex contract (long)
            # - User explicitly requested
            
            should_use_ai = (
                risk_score >= 50 or
                len(contract_text) > 5000 or
                metadata.get('force_ai', False)
            )
            
            if should_use_ai:
                print("🤖 Running AI analysis...")
                try:
                    ai_result = self.ai_analyzer.analyze_contract(
                        contract_text=contract_text,
                        metadata=metadata
                    )
                except Exception as e:
                    print(f"⚠️ AI analysis failed: {e}")
                    ai_result = None
        
        # PHASE 3: Merge results
        merged = self._merge_results(
            rule_result=rule_result,
            ai_result=ai_result,
            contract_text=contract_text
        )
        
        # Add performance metrics
        elapsed = (datetime.now() - start_time).total_seconds()
        merged['performance'] = {
            'total_time_seconds': round(elapsed, 2),
            'rule_based_used': True,
            'ai_used': ai_result is not None,
            'analysis_mode': 'hybrid' if ai_result else 'rule_based'
        }
        
        self.analyses_performed += 1
        
        return merged
    
    def _merge_results(
        self, 
        rule_result: Dict, 
        ai_result: Optional[Dict],
        contract_text: str
    ) -> Dict:
        """
        Intelligently merge rule-based and AI results
        """
        
        # Start with rule-based as foundation
        merged = {
            'analysis_id': rule_result.get('analysis_id', f'HYB-{datetime.now().strftime("%Y%m%d%H%M%S")}'),
            'timestamp': datetime.now().isoformat(),
            'analyzer_type': 'hybrid',
            'powered_by': 'CGC CORE™ + DiscipleAI Legal™'
        }
        
        # Contract summary
        rule_analysis = rule_result.get('contract_analysis', {})
        merged['contract_summary'] = {
            'word_count': len(contract_text.split()),
            'char_count': len(contract_text),
            'estimated_pages': len(contract_text.split()) // 250,
            'total_clauses': rule_analysis.get('total_clauses_found', 0)
        }
        
        # If AI available, prefer AI insights
        if ai_result:
            merged['analysis_method'] = 'ai_enhanced'
            
            # AI compliance (more detailed)
            ai_compliance = ai_result.get('ai_analysis', {}).get('compliance', {})
            if ai_compliance:
                merged['compliance'] = ai_compliance
            else:
                # Fallback to rule-based
                merged['compliance'] = {
                    'flags': rule_result.get('compliance_flags', []),
                    'source': 'rule_based'
                }
            
            # AI risk assessment (more nuanced)
            merged['risk_assessment'] = {
                'overall_risk': ai_result.get('overall_risk', 'UNKNOWN'),
                'compliance_score': ai_result.get('compliance_score', 75),
                'ai_confidence': 'high',
                'rule_based_score': rule_analysis.get('risk_score', 0)
            }
            
            # AI extracted clauses
            ai_clauses = ai_result.get('ai_analysis', {}).get('clauses', {})
            if ai_clauses:
                merged['clauses'] = ai_clauses
            else:
                merged['clauses'] = rule_result.get('clauses', {})
            
            # AI recommendations
            ai_recs = ai_result.get('ai_analysis', {}).get('recommendations', [])
            if ai_recs:
                merged['recommendations'] = ai_recs
            else:
                merged['recommendations'] = rule_analysis.get('recommendations', [])
        
        else:
            # Rule-based only
            merged['analysis_method'] = 'rule_based'
            merged['compliance'] = {
                'flags': rule_result.get('compliance_flags', []),
                'source': 'rule_based'
            }
            merged['risk_assessment'] = {
                'overall_risk': rule_analysis.get('risk_level', 'UNKNOWN'),
                'risk_score': rule_analysis.get('risk_score', 0),
                'factors': rule_analysis.get('risk_factors', [])
            }
            merged['clauses'] = rule_result.get('clauses', {})
            merged['recommendations'] = rule_analysis.get('recommendations', [])
        
        # Always include both raw results for transparency
        merged['raw_results'] = {
            'rule_based': rule_result,
            'ai': ai_result
        }
        
        # Executive summary (prefer AI if available)
        if ai_result:
            merged['executive_summary'] = ai_result.get('ai_analysis', {}).get('summary', 
                rule_analysis.get('executive_summary', 'Analysis complete'))
        else:
            merged['executive_summary'] = rule_analysis.get('executive_summary', 'Analysis complete')
        
        return merged
    
    def get_status(self) -> Dict:
        """Get analyzer status"""
        return {
            'module': 'Hybrid Contract Analyzer',
            'version': '1.0.0',
            'powered_by': 'CGC CORE™',
            'capabilities': {
                'rule_based_analysis': True,
                'ai_analysis': self.ai_available,
                'clause_extraction': True,
                'risk_assessment': True,
                'compliance_checking': True,
                'multi_framework': True
            },
            'metrics': {
                'analyses_performed': self.analyses_performed,
                'ai_available': self.ai_available
            }
        }


# Test
if __name__ == '__main__':
    print("\n" + "="*60)
    print("HYBRID CONTRACT ANALYZER - Test Mode")
    print("="*60 + "\n")
    
    sample = """
    SERVICE AGREEMENT
    
    This Agreement is between Company A and Company B, effective January 1, 2025.
    
    1. CONFIDENTIALITY: Both parties agree to maintain confidentiality of proprietary information.
    
    2. LIABILITY: Liability shall not exceed $50,000 for any claims.
    
    3. TERMINATION: Either party may terminate with 30 days notice.
    
    4. GOVERNING LAW: This agreement is governed by Delaware law.
    
    5. DATA PROTECTION: Parties will comply with GDPR and CCPA requirements.
    """
    
    analyzer = HybridContractAnalyzer()
    
    result = analyzer.analyze(
        contract_text=sample,
        metadata={'type': 'Service Agreement', 'jurisdiction': 'Delaware'}
    )
    
    print(json.dumps(result, indent=2, default=str))
    print("\n" + "="*60)
    print(json.dumps(analyzer.get_status(), indent=2))
```
