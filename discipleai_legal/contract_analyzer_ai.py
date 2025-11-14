"""
Contract Analyzer AI  
AI-powered contract analysis using GPT-4o  
"""

import os
import sys
import json
from typing import Dict, Optional
from datetime import datetime

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class ContractAnalyzerAI:
    """
    AI-powered Contract Analyzer  
    Uses GPT-4o-mini for intelligent contract analysis
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize AI analyzer"""
        self.version = "1.0.0"
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.analyses_count = 0

        if self.api_key and OPENAI_AVAILABLE:
            self.client = OpenAI(api_key=self.api_key)
            self.ai_enabled = True
            print(f"✅ Contract Analyzer AI v{self.version} initialized (AI-powered)")
        else:
            self.client = None
            self.ai_enabled = False
            print(f"✅ Contract Analyzer AI v{self.version} initialized (demo mode)")

    def analyze_contract(self, contract_text: str, metadata: Optional[Dict] = None) -> Dict:
        """
        Analyze a contract using AI + CGC CORE governance

        Args:
            contract_text: Full text of the contract
            metadata: Optional dict with filename, parties, etc.

        Returns:
            dict with analysis results + CGC governance
        """
        # Import CGC CORE
        try:
            sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
            from cgc_core.core_engine import get_cgc_core
            cgc = get_cgc_core()
            cgc_available = True
        except Exception as e:
            print(f"⚠️ CGC CORE not available: {e}")
            cgc = None
            cgc_available = False

        governance_input = {
            "action": "analyze_contract",
            "contract_text": contract_text[:1000],
            "metadata": metadata or {},
            "analysis_type": "legal_contract"
        }

        if cgc_available:
            print("🔄 Routing through CGC CORE governance...")
            governance_decision = cgc.execute_decision(
                module="discipleai_legal",
                action="analyze_contract",
                input_data=governance_input,
                context={"subsidiary": "DiscipleAI Legal™"}
            )

            if not governance_decision["decision"]["approved"]:
                return {
                    "success": False,
                    "error": "Analysis rejected by CGC CORE governance",
                    "governance_decision": governance_decision,
                    "reasoning": governance_decision["decision"]["reasoning"]
                }
        else:
            governance_decision = None

        # AI or demo analysis
        if not self.client:
            result = self._demo_analysis(contract_text, metadata)
        else:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": self._get_system_prompt()},
                        {"role": "user", "content": f"Analyze this contract:\n\n{contract_text[:15000]}"}
                    ],
                    temperature=0.3,
                    max_tokens=2000
                )
                ai_analysis = response.choices[0].message.content
                result = self._structure_analysis(contract_text, ai_analysis, metadata)
            except Exception as e:
                print(f"❌ AI analysis error: {e}")
                result = self._demo_analysis(contract_text, metadata)

        # Add CGC metadata
        if cgc_available and governance_decision:
            result["cgc_governance"] = {
                "enabled": True,
                "decision_id": governance_decision["decision_id"],
                "approved": governance_decision["decision"]["approved"],
                "confidence": governance_decision["decision"]["confidence"],
                "modules_executed": 6,
                "audit_hash": governance_decision["module_results"]["audit"]["block_hash"],
                "governance_time_ms": governance_decision["performance"]["total_time_ms"]
            }
            try:
                cgc.log_contract_analysis(
                    contract_id=result["analysis_id"],
                    result=result,
                    user_email=metadata.get("user_email", "unknown") if metadata else "unknown"
                )
            except Exception:
                pass
        else:
            result["cgc_governance"] = {
                "enabled": False,
                "reason": "CGC CORE not available"
            }

        self.analyses_count += 1
        return result

    def _get_system_prompt(self) -> str:
        """Get system prompt for AI"""
        return (
            "You are an expert legal contract analyst. Analyze contracts and provide:\n\n"
            "1. Contract Type & Parties\n"
            "2. Key Terms & Conditions\n"
            "3. Risk Assessment (HIGH/MEDIUM/LOW)\n"
            "4. Compliance Score (0-100)\n"
            "5. Critical Issues\n"
            "6. Recommendations\n\n"
            "Be concise and professional."
        )

    def _structure_analysis(self, contract_text: str, ai_analysis: str, metadata: Optional[Dict]) -> Dict:
        """Structure AI analysis into standard format"""
        return {
            "success": True,
            "analysis_id": f"AI-{self.analyses_count:06d}",
            "metadata": metadata or {},
            "contract_length": len(contract_text),
            "word_count": len(contract_text.split()),
            "ai_analysis": ai_analysis,
            "overall_risk": "MEDIUM",  # TODO: parse from ai_analysis
            "compliance_score": 85.0,  # TODO: parse from ai_analysis
            "timestamp": datetime.now().isoformat(),
            "ai_powered": True
        }

    def _demo_analysis(self, contract_text: str, metadata: Optional[Dict]) -> Dict:
        """Demo analysis when AI not available"""
        return {
            "success": True,
            "analysis_id": f"DEMO-{self.analyses_count:06d}",
            "metadata": metadata or {},
            "contract_length": len(contract_text),
            "word_count": len(contract_text.split()),
            "ai_analysis": (
                "# Contract Analysis (Demo Mode)\n\n"
                "## Overview\n"
                "This is a demo analysis. Enable OpenAI API key for full AI-powered analysis.\n\n"
                "## Key Findings\n"
                "- Contract type: General Agreement\n"
                "- Parties identified: Multiple parties detected\n"
                "- Risk Level: MEDIUM\n"
                "- Compliance Score: 85%\n\n"
                "## Recommendations\n"
                "1. Enable AI analysis for detailed insights\n"
                "2. Review contract clauses carefully\n"
                "3. Consider legal counsel for complex terms"
            ),
            "overall_risk": "MEDIUM",
            "compliance_score": 85.0,
            "timestamp": datetime.now().isoformat(),
            "ai_powered": False,
            "demo_mode": True
        }

    def get_stats(self) -> Dict:
        """Get analyzer stats"""
        return {
            "version": self.version,
            "analyses_count": self.analyses_count,
            "ai_enabled": self.ai_enabled,
            "status": "active"
        }


# Test block
if __name__ == "__main__":
    analyzer = ContractAnalyzerAI()

    test_contract = """
    EMPLOYMENT AGREEMENT

    This Agreement is made on January 15, 2025, between:
    - TechCorp Inc. ("Employer")
    - John Smith ("Employee")

    TERMS:
    1. Position: Software Engineer
    2. Salary: $120,000 per year
    3. Confidentiality required
    """

    result = analyzer.analyze_contract(test_contract, {"filename": "test.pdf"})
    print(json.dumps(result, indent=2, default=str))