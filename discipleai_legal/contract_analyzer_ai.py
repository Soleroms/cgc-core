"""
DiscipleAI Legal™ - AI Contract Analyzer
OlympusMont Systems LLC
Uses GPT-4o for intelligent contract analysis
"""

import os
import json
from datetime import datetime
import hashlib

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: OpenAI not installed. Install with: pip install openai")


class AIContractAnalyzer:
    """AI-powered contract analyzer using GPT-4o"""
    
    def __init__(self, api_key=None):
        """
        Initialize the analyzer
        
        Args:
            api_key: OpenAI API key. If None, reads from OPENAI_API_KEY env var
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            print("WARNING: No OpenAI API key provided. Set OPENAI_API_KEY env var.")
            self.client = None
        elif not OPENAI_AVAILABLE:
            print("ERROR: OpenAI package not installed")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)
            print("✅ AI Analyzer ready with GPT-4o-mini")
    
    def analyze_contract(self, contract_text, metadata=None):
        """
        Analyze a contract using GPT-4o
        
        Args:
            contract_text: Full text of the contract
            metadata: Optional dict with filename, parties, etc.
            
        Returns:
            dict with analysis results
        """
        if not self.client:
            return self._demo_analysis(contract_text, metadata)
        
        try:
            # Call GPT-4o-mini for analysis
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # ✅ MODELO CORRECTO
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": f"Analyze this contract:\n\n{contract_text[:15000]}"
                    }
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            ai_analysis = response.choices[0].message.content
            
            # Parse AI response and structure results
            return self._structure_analysis(
                contract_text, 
                ai_analysis, 
                metadata
            )
            
        except Exception as e:
            print(f"❌ AI analysis error: {e}")
            return self._demo_analysis(contract_text, metadata)
    
    def _get_system_prompt(self):
        """System prompt for GPT-4o"""
        return """You are an expert legal AI assistant specializing in contract analysis for the US market.

Analyze the contract and provide:

1. KEY CLAUSES: Extract and categorize critical clauses:
   - Term & Termination
   - Indemnification
   - Governing Law
   - Limitation of Liability
   - Assignment
   - Confidentiality
   - Payment Terms
   - Dispute Resolution

2. COMPLIANCE CHECK: Assess compliance with these frameworks:
   - ISO 27001 (Information Security)
   - GDPR/CCPA/LGPD (Data Privacy)
   - SOC 2 Type II (Security Controls)
   - Legal Ethics (Attorney-Client Privilege)
   - Data Sovereignty

3. RISK ASSESSMENT: Identify risks (HIGH/MEDIUM/LOW) for each area

4. RECOMMENDATIONS: Provide actionable improvements

Format your response as JSON with this structure:
{
  "summary": "Brief executive summary",
  "clauses": {
    "termination": {"found": true, "details": "..."},
    "liability": {"found": true, "details": "..."}
  },
  "compliance": {
    "ISO_27001": {"score": 85, "risk_level": "LOW"},
    "GDPR": {"score": 70, "risk_level": "MEDIUM"}
  },
  "risks": [
    {"level": "HIGH", "description": "...", "recommendation": "..."}
  ],
  "recommendations": ["Add X clause", "Modify Y section"]
}"""
    
    def _structure_analysis(self, contract_text, ai_response, metadata):
        """Structure the AI response into standard format"""
        
        # Generate audit hash
        audit_hash = hashlib.sha256(
            (contract_text + str(datetime.now())).encode()
        ).hexdigest()[:16]
        
        # Try to parse AI response as JSON
        try:
            parsed = json.loads(ai_response)
        except:
            # If not JSON, create structured response
            parsed = {
                "summary": ai_response[:500],
                "analysis": ai_response,
                "parsed": False
            }
        
        # Calculate scores
        word_count = len(contract_text.split())
        compliance_score = self._calculate_compliance_score(parsed)
        risk_level = self._determine_risk_level(parsed)
        
        return {
            "analysis_id": f"AI-{audit_hash}",
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
            "contract_summary": {
                "word_count": word_count,
                "char_count": len(contract_text),
                "estimated_pages": word_count // 250
            },
            "ai_analysis": parsed,
            "compliance_score": compliance_score,
            "overall_risk": risk_level,
            "audit_hash": f"0x{audit_hash}",
            "powered_by": "CGC CORE AI™ via GPT-4o-mini",
            "model_used": "gpt-4o-mini"
        }
    
    def _calculate_compliance_score(self, analysis):
        """Calculate overall compliance score from analysis"""
        if "compliance" in analysis:
            scores = []
            for framework, data in analysis.get("compliance", {}).items():
                if isinstance(data, dict) and "score" in data:
                    scores.append(data["score"])
            return sum(scores) / len(scores) if scores else 75
        return 75
    
    def _determine_risk_level(self, analysis):
        """Determine overall risk level"""
        if "risks" in analysis:
            risks = analysis.get("risks", [])
            high_risks = [r for r in risks if isinstance(r, dict) and r.get("level") == "HIGH"]
            if len(high_risks) >= 2:
                return "HIGH"
            elif len(high_risks) == 1:
                return "MEDIUM"
        return "LOW"
    
    def _demo_analysis(self, contract_text, metadata):
        """Fallback demo analysis without AI"""
        audit_hash = hashlib.sha256(
            (contract_text + str(datetime.now())).encode()
        ).hexdigest()[:16]
        
        return {
            "analysis_id": f"DEMO-{audit_hash}",
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
            "contract_summary": {
                "word_count": len(contract_text.split()),
                "char_count": len(contract_text),
                "estimated_pages": len(contract_text.split()) // 250
            },
            "demo_mode": True,
            "message": "OpenAI API not configured. This is a demo response.",
            "note": "Set OPENAI_API_KEY environment variable to enable AI analysis",
            "audit_hash": f"0x{audit_hash}"
        }


# Test function
if __name__ == "__main__":
    # Test with sample contract
    sample_contract = """
    SERVICE AGREEMENT
    
    This Service Agreement ("Agreement") is entered into as of January 1, 2025,
    by and between Company A ("Provider") and Company B ("Client").
    
    1. TERM: This Agreement shall commence on the date first written above and 
    continue for a period of one (1) year, with automatic renewal unless terminated
    with 30 days notice.
    
    2. CONFIDENTIALITY: Each party agrees to maintain confidentiality of all
    proprietary information disclosed during the term of this Agreement.
    The confidentiality obligations shall survive termination for 5 years.
    
    3. LIMITATION OF LIABILITY: In no event shall either party be liable for
    any indirect, incidental, or consequential damages. Total liability shall not
    exceed $100,000 in aggregate.
    
    4. DATA PROTECTION: Provider agrees to comply with all applicable data protection
    laws including GDPR and CCPA. Personal data will be processed according to
    applicable privacy regulations.
    
    5. GOVERNING LAW: This Agreement shall be governed by the laws of Delaware,
    without regard to conflict of law principles.
    
    6. DISPUTE RESOLUTION: Any disputes shall be resolved through binding arbitration
    in accordance with the rules of the American Arbitration Association.
    """
    
    print("\n" + "="*60)
    print("AI CONTRACT ANALYZER - Test Mode")
    print("="*60 + "\n")
    
    analyzer = AIContractAnalyzer()
    result = analyzer.analyze_contract(sample_contract)
    
    print(json.dumps(result, indent=2))
    
    print("\n" + "="*60)
    print("✅ Test completed")
    print("="*60 + "\n")