# contract_analyzer.py
"""
Contract Analyzer Module
DiscipleAI Legal™ - OlympusMont Systems LLC

Production-ready: improved clause extraction, party identification,
date extraction, risk scoring, compliance checks and safer governance call.
"""

import json
import re
import logging
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import sys

# OPTIONAL: maintain previous import behavior but safe-guard path insertion
_pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _pkg_root not in sys.path:
    sys.path.insert(0, _pkg_root)

# Try to import LegalCore; if not available, provide a stub for testing
try:
    from discipleai_legal.legal_core import LegalCore
except Exception:
    class LegalCore:
        def __init__(self, cfg=None):
            self.cfg = cfg
        def analyze_with_governance(self, action, legal_data, context):
            # simple echo stub for offline testing
            return {
                'status': 'ok',
                'decision': {
                    'approved': True,
                    'notes': 'stubbed LegalCore response',
                    'executive_summary': legal_data.get('executive_summary', '') if isinstance(legal_data, dict) else ''
                }
            }

# ----------------------
# Logger
# ----------------------
logger = logging.getLogger("contract-analyzer")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(logging.Formatter(
        '{"time":"%(asctime)s","level":"%(levelname)s","name":"%(name)s","message":"%(message)s"}'
    ))
    logger.addHandler(ch)

# ----------------------
# Analyzer
# ----------------------
class ContractAnalyzer:
    """
    Production-grade contract analyzer for US legal market
    Integrates with CGC Core for governance and compliance
    """

    CLAUSE_PATTERNS = {
        'termination': [
            r'\btermination\b',
            r'\bterminate\s+this\s+agreement\b',
            r'\beither\s+party\s+may\s+terminate\b',
            r'\bgrounds\s+for\s+termination\b',
            r'\bnotice\s+of\s+termination\b'
        ],
        'liability': [
            r'\blimitation\s+of\s+liability\b',
            r'\bliability\s+shall\s+not\s+exceed\b',
            r'\bin\s+no\s+event\s+shall\b.*\bliable\b',
            r'\bindemnif(?:y|ication)',
            r'\bconsequential\s+damages\b'
        ],
        'confidentiality': [
            r'\bconfidential\s+information\b',
            r'\bnon-?disclosure\b',
            r'\bproprietary\s+information\b',
            r'\btrade\s+secrets\b',
            r'\bconfidentiality\s+obligations\b'
        ],
        'intellectual_property': [
            r'\bintellectual\s+property\b',
            r'\bownership\s+of.*work\s+product\b',
            r'\b(patent|copyright|trademark)s?\b',
            r'\blicense\s+to\s+use\b',
            r'\bderivative\s+works\b'
        ],
        'dispute_resolution': [
            r'\barbitration\s+clause\b',
            r'\bdispute\s+resolution\b',
            r'\bgoverning\s+law\b',
            r'\bjurisdiction\s+and\s+venue\b',
            r'\bmediation\b'
        ],
        'non_compete': [
            r'\bnon-?compete\b',
            r'\bcovenant\s+not\s+to\s+compete\b',
            r'\brestrictive\s+covenant\b',
            r'\bsolicitation\s+of.*employees\b',
            r'\bcompetitive\s+business\b'
        ],
        'payment_terms': [
            r'\bpayment\s+terms\b',
            r'\bcompensation\s+structure\b',
            r'\bfees\s+and\s+expenses\b',
            r'\binvoicing\s+procedures\b',
            r'\blate\s+payment\s+penalties\b'
        ],
        'force_majeure': [
            r'\bforce\s+majeure\b',
            r'\bacts\s+of\s+god\b',
            r'\bcircumstances\s+beyond\s+the\s+control\b',
            r'\bnatural\s+disasters\b',
            r'\bpandemic\b'
        ]
    }

    HIGH_RISK_TERMS = [
        'unlimited liability',
        'perpetual obligation',
        'irrevocable',
        'automatic renewal',
        'unilateral modification',
        'waiver of jury trial',
        'forum selection',
        'liquidated damages',
        'personal guarantee',
        'joint and several liability'
    ]

    COMPLIANCE_KEYWORDS = {
        'GDPR': ['personal data', 'data subject', 'right to erasure', 'data controller'],
        'CCPA': ['california consumer', 'do not sell', 'personal information'],
        'HIPAA': ['protected health information', 'phi', 'covered entity', 'hipaa'],
        'SOX': ['financial reporting', 'internal controls', 'audit committee']
    }

    def __init__(self, cgc_config: Optional[Dict] = None):
        self.legal_core = LegalCore(cgc_config)
        self.total_contracts_analyzed = 0
        self.total_clauses_extracted = 0
        self.total_risks_identified = 0
        logger.info("Contract Analyzer initialized - US Legal Market")

    # ---------- Public ----------
    def analyze_contract(self, contract_text: str, contract_metadata: Optional[Dict] = None) -> Dict:
        if contract_metadata is None:
            contract_metadata = {}

        clauses = self._extract_clauses(contract_text)
        parties = self._identify_parties(contract_text)
        dates = self._extract_dates(contract_text)
        risk_assessment = self._assess_risk(contract_text, clauses)
        compliance_flags = self._check_compliance(contract_text)
        executive_summary = self._generate_executive_summary(contract_text, clauses, risk_assessment, compliance_flags)

        analysis_data = {
            'contract_text_length': len(contract_text),
            'contract_type': contract_metadata.get('type', 'Unknown'),
            'parties': parties,
            'dates': dates,
            'clauses': clauses,
            'risk_assessment': risk_assessment,
            'compliance_flags': compliance_flags,
            'executive_summary': executive_summary,
            'metadata': contract_metadata
        }

        # Safe call to governance layer
        try:
            result = self.legal_core.analyze_with_governance(
                action='analyze_contract',
                legal_data=analysis_data,
                context={
                    'analysis_type': 'full_contract_analysis',
                    'jurisdiction': contract_metadata.get('jurisdiction', 'USA'),
                    'market': 'legal_tech'
                }
            )
            if not isinstance(result, dict):
                logger.warning("LegalCore returned non-dict result; wrapping")
                result = {'status': 'unknown', 'decision': {'notes': str(result)}}
        except Exception as e:
            logger.exception("LegalCore integration failed; returning local analysis")
            result = {'status': 'error', 'decision': {'approved': False, 'notes': f'LegalCore error: {e}'}}

        # Update metrics
        self.total_contracts_analyzed += 1
        self.total_clauses_extracted += sum(len(v) for v in clauses.values())
        self.total_risks_identified += len(risk_assessment.get('high_risk_items', []))

        # Attach analysis metadata
        result.setdefault('contract_analysis', {})
        result['contract_analysis'].update({
       
	    'analyzed_at': datetime.now(timezone.utc).isoformat(),
            'analyzer_version': '1.1.0',
            'total_clauses_found': sum(len(v) for v in clauses.values()),
            'risk_score': risk_assessment.get('overall_risk_score', 0),
            'compliance_issues': len(compliance_flags),
            'recommendation': self._generate_recommendation(risk_assessment)
        })

# ensure executive summary and clauses are present in contract_analysis for downstream callers
result.setdefault('contract_analysis', {})
result['contract_analysis'].setdefault('executive_summary', analysis_data.get('executive_summary', ''))
result['contract_analysis'].setdefault('clauses', analysis_data.get('clauses', {}))

        return result

    # ---------- Helpers ----------
    def _split_sentences_with_spans(self, text: str) -> List[Tuple[int, int, str]]:
        """
        Returns list of (start_index, end_index, sentence_text).
        Keeps original spans to map regex matches to sentences accurately.
        """
        sentences = []
        for m in re.finditer(r'[^.!?]+[.!?]?', text, re.DOTALL):
            s = m.group(0).strip()
            if s:
                sentences.append((m.start(), m.end(), s))
        return sentences

    def _extract_clauses(self, text: str) -> Dict[str, List[Dict]]:
        """Extract clauses robustly using compiled regexes and sentence spans."""
        clauses = defaultdict(list)
        sentences = self._split_sentences_with_spans(text)
        text_lower = text.lower()

        for clause_type, patterns in self.CLAUSE_PATTERNS.items():
            for pat in patterns:
                try:
                    regex = re.compile(pat, re.IGNORECASE)
                except re.error:
                    continue
                for m in regex.finditer(text):
                    start_pos = m.start()
                    # map to sentence by comparing spans
                    matched_sentence = None
                    for s_start, s_end, s_text in sentences:
                        if s_start <= start_pos < s_end:
                            matched_sentence = s_text
                            sent_span = (s_start, s_end)
                            break
                    if matched_sentence is None:
                        # fallback: take a substring around match
                        s_start = max(0, start_pos - 120)
                        s_end = min(len(text), m.end() + 120)
                        matched_sentence = text[s_start:s_end].strip()
                        sent_span = (s_start, s_end)

                    clauses[clause_type].append({
                        'text': matched_sentence,
                        'position': start_pos,
                        'pattern_matched': pat,
                        'confidence': 0.85
                    })

        # Deduplicate by text + clause_type
        for k, v in list(clauses.items()):
            seen = set()
            unique = []
            for item in v:
                key = (item['text'].strip(), item['pattern_matched'])
                if key not in seen:
                    seen.add(key)
                    unique.append(item)
            clauses[k] = unique

        return dict(clauses)

    def _identify_parties(self, text: str) -> List[str]:
        """Identify contract parties using heuristic patterns and return top matches."""
        parties = []
        # more conservative patterns; capture groups specific
        patterns = [
            r'\bbetween\s+([A-Z][A-Za-z0-9\.\,&\s\-]{2,200}?)\s+(?:and|&)\s+([A-Z][A-Za-z0-9\.\,&\s\-]{2,200}?)\b',
            r'\b([A-Z][A-Za-z0-9\.\,&\s\-]{2,200}?)\s*\(\s*"(?:Disclosing|Receiving|Party)"\s*\)',
            r'\b([A-Z][A-Za-z0-9\.\,&\s\-]{2,200}?)\s+(?:Inc|LLC|Corporation|Corp|Ltd|Co)\b',
            r'\bhereinafter\s+referred\s+to\s+as\s+"([^"]+)"'
        ]

        for pat in patterns:
            try:
                for m in re.finditer(pat, text, re.IGNORECASE | re.MULTILINE):
                    groups = m.groups()
                    for g in groups:
                        if not g:
                            continue
                        party = g.strip().strip('",')
                        if len(party) > 2 and party not in parties:
                            parties.append(party)
            except re.error:
                continue

        # fallback: find simple "Party" lines
        for m in re.finditer(r'^(.*Inc\.|.*LLC|.*Corporation).*$', text, re.MULTILINE):
            cand = m.group(0).strip()
            if len(cand) > 3 and cand not in parties:
                parties.append(cand)

        return parties[:10]

    def _extract_dates(self, text: str) -> Dict[str, List[str]]:
        """Extract dates (strings) with simple normalization (no external libs)."""
        dates = {'effective_dates': [], 'termination_dates': [], 'renewal_dates': [], 'other_dates': []}

        # standardized date patterns
        patterns = [
            r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',  # 01/15/2025
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
            r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b'
        ]
        for p in patterns:
            for m in re.findall(p, text, flags=re.IGNORECASE):
                dates['other_dates'].append(m.strip())

        # context-specific
        for m in re.findall(r'\beffective\s+date[:\s]+([^\n\.]{3,120})', text, flags=re.IGNORECASE):
            dates['effective_dates'].append(m.strip())
        for m in re.findall(r'\bterminat(?:ion|e)\s+date[:\s]+([^\n\.]{3,120})', text, flags=re.IGNORECASE):
            dates['termination_dates'].append(m.strip())
        for m in re.findall(r'\brenewal\s+date[:\s]+([^\n\.]{3,120})', text, flags=re.IGNORECASE):
            dates['renewal_dates'].append(m.strip())

        # deduplicate
        for k in dates:
            dates[k] = list(dict.fromkeys(dates[k]))
        return dates

    def _assess_risk(self, text: str, clauses: Dict) -> Dict:
        """
        Assess contract risk level.
        Returns structured risk object.
        """
        score = 0
        risk_factors = []
        high_risk_items = []
        t = text.lower()

        # high risk terms
        for term in self.HIGH_RISK_TERMS:
            if term in t:
                score += 10
                high_risk_items.append({'term': term, 'severity': 'HIGH', 'recommendation': f'Review {term}'})

        # clause-based heuristics
        if 'liability' in clauses:
            lc = len(clauses['liability'])
            if lc == 0:
                score += 15
                risk_factors.append('No liability limitation found')
            elif lc > 3:
                score += 5
                risk_factors.append('Multiple liability clauses - review for conflicts')
        else:
            score += 15
            risk_factors.append('No liability limitation found')

        if 'termination' not in clauses or len(clauses.get('termination', [])) == 0:
            score += 20
            risk_factors.append('No clear termination clause identified')

        if 'dispute_resolution' not in clauses or len(clauses.get('dispute_resolution', [])) == 0:
            score += 10
            risk_factors.append('No dispute resolution mechanism specified')

        one_sided_patterns = ['unilateral right', 'sole discretion', 'without notice', 'at any time without cause', 'non-refundable']
        for p in one_sided_patterns:
            if p in t:
                score += 5
                risk_factors.append(f'Potentially one-sided term: {p}')

        score = min(max(score, 0), 100)

        if score >= 70:
            level = 'CRITICAL'
        elif score >= 50:
            level = 'HIGH'
        elif score >= 30:
            level = 'MEDIUM'
        else:
            level = 'LOW'

        return {
            'overall_risk_score': score,
            'risk_level': level,
            'risk_factors': risk_factors,
            'high_risk_items': high_risk_items,
            'clauses_missing': self._identify_missing_clauses(clauses),
            'recommendations': self._generate_risk_recommendations(score, risk_factors)
        }

    def _identify_missing_clauses(self, clauses: Dict) -> List[str]:
        critical_clauses = ['termination', 'liability', 'confidentiality', 'dispute_resolution', 'payment_terms']
        missing = [c for c in critical_clauses if not clauses.get(c)]
        return missing

    def _generate_risk_recommendations(self, risk_score: int, risk_factors: List[str]) -> List[str]:
        recs = []
        if risk_score >= 70:
            recs.extend(['URGENT: Seek legal counsel before signing', 'Consider significant amendments to reduce risk'])
        elif risk_score >= 50:
            recs.extend(['Legal review strongly recommended', 'Negotiate key terms to reduce exposure'])
        elif risk_score >= 30:
            recs.extend(['Standard legal review recommended', 'Minor modifications may be beneficial'])
        else:
            recs.append('Low risk - standard review procedures apply')

        # specific
        if any('No liability limitation' in f for f in risk_factors):
            recs.append('ADD: Liability limitation clause (cap damages)')
        if any('termination' in f.lower() for f in risk_factors):
            recs.append('ADD: Clear termination provisions with notice periods')
        if any('dispute' in f.lower() for f in risk_factors):
            recs.append('ADD: Arbitration/mediation clause to avoid litigation')

        return recs

    def _check_compliance(self, text: str) -> List[Dict]:
        flags = []
        t = text.lower()
        for reg, keywords in self.COMPLIANCE_KEYWORDS.items():
            found = [k for k in keywords if k.lower() in t]
            if found:
                flags.append({
                    'regulation': reg,
                    'detected': True,
                    'keywords_found': found,
                    'recommendation': f'Ensure {reg} compliance requirements are met',
                    'requires_review': True
                })
        return flags

    def _generate_executive_summary(self, text: str, clauses: Dict, risk_assessment: Dict, compliance_flags: List[Dict]) -> str:
        word_count = len(text.split())
        clause_count = sum(len(v) for v in clauses.values())
        parts = [
            f"CONTRACT OVERVIEW: {word_count:,} words analyzed, {clause_count} key clauses identified.",
            f"RISK ASSESSMENT: {risk_assessment['risk_level']} (Score: {risk_assessment['overall_risk_score']}/100)."
        ]
        if risk_assessment.get('risk_factors'):
            parts.append("Primary concerns: " + ", ".join(risk_assessment['risk_factors'][:3]) + ".")
        if compliance_flags:
            regs = ", ".join(f['regulation'] for f in compliance_flags)
            parts.append(f"COMPLIANCE: References to {regs} detected. Legal review required.")
        if risk_assessment['overall_risk_score'] >= 50:
            parts.append("RECOMMENDATION: Do not execute without legal counsel review and approval.")
        else:
            parts.append("RECOMMENDATION: Proceed with standard review procedures.")
        return " ".join(parts)

    def _generate_recommendation(self, risk_assessment: Dict) -> str:
        score = risk_assessment.get('overall_risk_score', 0)
        if score >= 70:
            return "DO NOT SIGN - Critical risks identified"
        elif score >= 50:
            return "CAUTION - Negotiate key terms before signing"
        elif score >= 30:
            return "REVIEW - Minor modifications recommended"
        else:
            return "ACCEPTABLE - Standard risk level"

    def get_analyzer_status(self) -> Dict:
        return {
            'module': 'Contract Analyzer',
            'version': '1.1.0',
            'status': 'active',
            'market': 'US Legal',
            'metrics': {
                'total_contracts_analyzed': self.total_contracts_analyzed,
                'total_clauses_extracted': self.total_clauses_extracted,
                'total_risks_identified': self.total_risks_identified
            },
            'capabilities': {
                'clause_extraction': True,
                'risk_assessment': True,
                'compliance_checking': True,
                'party_identification': True,
                'date_extraction': True
            }
        }



if __name__ == '__main__':

    logger.info("CONTRACT ANALYZER - Test Mode (US Legal Market)")

    sample_contract = """
    NON-DISCLOSURE AGREEMENT

    This Non-Disclosure Agreement ("Agreement") is entered into as of January 15, 2025,
    between TechCorp Inc., a Delaware corporation ("Disclosing Party"), and
    DataSystems LLC, a California limited liability company ("Receiving Party").

    1. CONFIDENTIAL INFORMATION
    The Disclosing Party agrees to disclose certain confidential and proprietary information
    to the Receiving Party. Confidential Information includes trade secrets, business plans,
    customer data, and technical specifications.

    2. OBLIGATIONS OF RECEIVING PARTY
    The Receiving Party shall maintain strict confidentiality and shall not disclose
    Confidential Information to any third party without prior written consent.

    3. TERM AND TERMINATION
    This Agreement shall remain in effect for a period of three (3) years from the
    effective date. Either party may terminate this Agreement upon thirty (30) days
    written notice.

    4. LIMITATION OF LIABILITY
    In no event shall either party be liable for consequential damages or damages
    exceeding $100,000 in the aggregate.

    5. DISPUTE RESOLUTION
    Any disputes arising under this Agreement shall be resolved through binding
    arbitration in accordance with the rules of the American Arbitration Association.
    The arbitration shall take place in New York, New York.

    6. GOVERNING LAW
    This Agreement shall be governed by the laws of the State of New York,
    without regard to conflict of law principles.

    7. AUTOMATIC RENEWAL
    Unless terminated, this Agreement will automatically renew for successive
    one-year periods.
    """

    analyzer = ContractAnalyzer()

    # Run analysis safely and capture exceptions
    try:
        result = analyzer.analyze_contract(
            sample_contract,
            contract_metadata={'type': 'NDA', 'jurisdiction': 'New York', 'date': '2025-01-15'}
        )
    except Exception as e:
        logger.exception("Analyze_contract raised an exception")
        raise

    import json

    # Ensure contract_analysis exists and has expected structure
    contract_analysis = result.get('contract_analysis', {})
    # Provide fallback values if anything is missing
    risk_score = contract_analysis.get('risk_score', result.get('risk_assessment', {}).get('overall_risk_score', 0))
    recommendation = contract_analysis.get('recommendation', result.get('decision', {}).get('recommendation', analyzer._generate_recommendation({'overall_risk_score': risk_score})))
    total_clauses = contract_analysis.get('total_clauses_found', analyzer.total_clauses_extracted)
    compliance_issues = contract_analysis.get('compliance_issues', len(result.get('compliance_flags', [])))

    print("\n📊 ANALYSIS RESULTS:\n")
    print(f"Risk Score: {risk_score}")
    print(f"Recommendation: {recommendation}")
    print(f"Clauses Found: {total_clauses}")
    print(f"Compliance Issues: {compliance_issues}\n")

    print("📋 Executive Summary:\n")
    # Prefer the executive summary coming from contract_analysis; if absent, generate locally with safe inputs
    exec_summary = contract_analysis.get('executive_summary')
    if not exec_summary:
        # attempt to use clauses from the analysis_data if available
        clauses_for_summary = result.get('clauses') or result.get('contract_analysis', {}).get('clauses') or {}
        # ensure clauses_for_summary is a dict
        if not isinstance(clauses_for_summary, dict):
            clauses_for_summary = {}
        # produce a safe executive summary
        exec_summary = analyzer._generate_executive_summary(sample_contract, clauses_for_summary, {'risk_level': 'UNKNOWN', 'overall_risk_score': risk_score, 'risk_factors': []}, result.get('compliance_flags', []))

    print(exec_summary + "\n")

    print("✅ Test completed successfully\n")
    # Update analyzed_at to timezone-aware UTC
    contract_analysis['analyzed_at'] = datetime.now(timezone.utc).isoformat()
    print(f"\n{json.dumps(analyzer.get_analyzer_status(), indent=2)}")
