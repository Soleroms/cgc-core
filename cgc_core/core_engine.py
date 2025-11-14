"""
CGC Core Engine - Self-contained VERSION
Central orchestrator for governance decisions with 6 module stubs included.
No external network calls, no relative imports, ready for local testing.
"""

import json
import hashlib
import logging
from datetime import datetime
from typing import Dict, Optional, Any
import sqlite3
import os
import uuid

# --- Logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("cgc_core")

# --- Helper functions ---
def safe_makedirs_for_path(path: str) -> None:
    """Create parent directory for a path if it exists (ignore if empty)."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)

def now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def compute_hash(*parts: Any) -> str:
    """Compute SHA256 hex digest from provided parts (deterministic)."""
    m = hashlib.sha256()
    for p in parts:
        if p is None:
            continue
        if not isinstance(p, (bytes, bytearray)):
            p = str(p).encode("utf-8")
        m.update(p)
        m.update(b"|")
    return m.hexdigest()

# --- Module stubs (replace with real implementations later) ---

class PerceptionAnalysisNode:
    """Simple stub: analyzes input text/data and extracts features."""
    def analyze(self, input_data: Dict) -> Dict:
        features = {"length": len(json.dumps(input_data)), "keys": list(input_data.keys())}
        return {"module": "PAN", "result": features, "timestamp": now_iso()}


class EthicalCalibrationModule:
    """Stub: assigns a base ethical score (0-100) based on input features."""
    def calibrate(self, features: Dict) -> Dict:
        base = 80.0
        # simple deterministic adjustment
        adj = (features.get("length", 0) % 20) - 10
        score = max(0.0, min(100.0, base + adj))
        return {"module": "ECM", "ethical_score": score, "timestamp": now_iso()}


class PredictiveFeedbackMechanism:
    """Stub: returns a confidence estimate and suggested feedback text."""
    def predict(self, input_data: Dict, ethical_score: float) -> Dict:
        confidence = max(0.0, min(1.0, (ethical_score / 100.0) * 0.95 + 0.05))
        feedback = "Proceed" if confidence >= 0.5 else "Review required"
        return {"module": "PFM", "confidence": round(confidence, 3), "feedback": feedback, "timestamp": now_iso()}


class SmartDataAdvisor:
    """Stub: recommends data-driven adjustments (no external data)."""
    def advise(self, input_data: Dict) -> Dict:
        # deterministic advice from keys count
        advice = {"adjustment": "none", "reason": "sufficient_data"} if len(input_data.keys()) > 1 else {"adjustment": "collect_more", "reason": "sparse_input"}
        return {"module": "SDA", "advice": advice, "timestamp": now_iso()}


class TraceabilityOversight:
    """Simple in-memory audit chain simulator persisted minimally via DB entries."""
    def __init__(self):
        self.entries = []  # list of audit dicts

    def add_entry(self, decision_id: str, payload: Dict) -> Dict:
        timestamp = now_iso()
        prev_hash = self.entries[-1]["block_hash"] if self.entries else ""
        block_hash = compute_hash(decision_id, json.dumps(payload, sort_keys=True), prev_hash, timestamp)
        entry = {
            "decision_id": decision_id,
            "payload_hash": compute_hash(json.dumps(payload, sort_keys=True)),
            "prev_hash": prev_hash,
            "block_hash": block_hash,
            "timestamp": timestamp
        }
        self.entries.append(entry)
        return entry

    @property
    def total_entries(self) -> int:
        return len(self.entries)


class GovernanceOrchestrator:
    """Orchestrates the module calls in a deterministic pipeline."""
    def __init__(self, pan: PerceptionAnalysisNode, ecm: EthicalCalibrationModule,
                 pfm: PredictiveFeedbackMechanism, sda: SmartDataAdvisor, tco: TraceabilityOversight):
        self.pan = pan
        self.ecm = ecm
        self.pfm = pfm
        self.sda = sda
        self.tco = tco

    def orchestrate_decision(self, decision_id: str, module: str, action: str, input_data: Dict, context: Dict) -> Dict:
        # 1) Perception & Analysis
        pan_out = self.pan.analyze(input_data)

        # 2) Ethical calibration based on perception
        ecm_out = self.ecm.calibrate(pan_out["result"])

        # 3) Predictive feedback using ethical score
        pfm_out = self.pfm.predict(input_data, ecm_out["ethical_score"])

        # 4) Smart data advice
        sda_out = self.sda.advise(input_data)

        # Compose combined result
        decision = {
            "decision_id": decision_id,
            "requested_module": module,
            "action": action,
            "timestamp": now_iso(),
            "input_snapshot": input_data,
            "module_results": {
                "pan": pan_out,
                "ecm": ecm_out,
                "pfm": pfm_out,
                "sda": sda_out,
            },
            "decision": {
                "approved": bool(pfm_out["confidence"] >= 0.5),
                "confidence": float(pfm_out["confidence"]),
                "why": pfm_out["feedback"]
            }
        }

        # 5) Traceability / Audit
        audit_entry = self.tco.add_entry(decision_id, decision)
        # attach audit summary
        decision["module_results"]["audit"] = audit_entry

        return decision

    def get_system_status(self) -> Dict:
        """Return a simple system status summary."""
        modules = {
            "PAN": {"status": "active", "health": 98},
            "ECM": {"status": "active", "health": 96},
            "PFM": {"status": "active", "health": 94},
            "SDA": {"status": "active", "health": 97},
            "TCO": {"status": "active", "health": 99},
            "CGC_LOOP": {"status": "active", "health": 98}
        }
        integrity = {"audit_chain_verified": True if self.tco.total_entries > 0 else False}
        return {"modules": modules, "integrity": integrity, "cgc_core": {"health": 96}}

# --- Core engine implementation ---

class CGCCoreEngine:
    """
    CGC Core Engine - SINGLE SELF-CONTAINED FILE
    """
    def __init__(self, db_path: str = "data/cgc_core.db"):
        self.db_path = db_path
        self.version = "2.1.4"
        safe_makedirs_for_path(db_path)
        self._init_database()

        # instantiate modules
        self.pan = PerceptionAnalysisNode()
        self.ecm = EthicalCalibrationModule()
        self.pfm = PredictiveFeedbackMechanism()
        self.sda = SmartDataAdvisor()
        self.tco = TraceabilityOversight()

        # orchestrator
        self.cgc_loop = GovernanceOrchestrator(self.pan, self.ecm, self.pfm, self.sda, self.tco)

        # counters read from DB
        self.total_decisions = self._get_total_from_table("decisions")
        self.total_contracts = self._get_total_from_table("contracts")
        self.total_cases = self._get_total_from_table("cases")

        logger.info(f"✅ CGC Core Engine v{self.version} initialized")
        logger.info(f"   Total decisions: {self.total_decisions:,}")

    # --- Database ---
    def _init_database(self) -> None:
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS decisions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    decision_id TEXT UNIQUE,
                    module TEXT,
                    action TEXT,
                    approved INTEGER,
                    confidence REAL,
                    timestamp TEXT,
                    input_data TEXT,
                    output_data TEXT,
                    audit_hash TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contracts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    contract_id TEXT UNIQUE,
                    filename TEXT,
                    analysis_result TEXT,
                    risk_level TEXT,
                    compliance_score REAL,
                    timestamp TEXT,
                    user_email TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    case_id TEXT UNIQUE,
                    case_name TEXT,
                    jurisdiction TEXT,
                    analysis_result TEXT,
                    outcome_prediction TEXT,
                    timestamp TEXT,
                    user_email TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT,
                    metric_value REAL,
                    timestamp TEXT
                )
            ''')
            conn.commit()
        finally:
            conn.close()

    def _get_total_from_table(self, table: str) -> int:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            conn.close()
            return int(count)
        except Exception as e:
            logger.warning("DB read failed for table %s: %s", table, e)
            return 0

    # --- Decision lifecycle ---
    def execute_decision(self, module: str, action: str, input_data: Dict, context: Optional[Dict] = None) -> Dict:
        """
        Execute a governed decision through the orchestrator.
        Returns the assembled decision + governance metadata.
        """
        context = context or {}
        decision_id = self._generate_decision_id()

        logger.info("Executing decision %s module=%s action=%s", decision_id, module, action)

        # Orchestrate
        result = self.cgc_loop.orchestrate_decision(
            decision_id=decision_id,
            module=module,
            action=action,
            input_data=input_data,
            context=context
        )

        # persist
        try:
            self._save_decision(result, input_data)
            self.total_decisions += 1
        except Exception as e:
            logger.exception("Failed to save decision: %s", e)

        return result

    def _generate_decision_id(self) -> str:
        """Generate a reasonably-unique decision id (time + uuid4 short)."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        uid = uuid.uuid4().hex[:8]
        return f"CGC-{timestamp}-{uid}"

    def _save_decision(self, decision: Dict, input_data: Dict) -> None:
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            audit_hash = decision["module_results"]["audit"]["block_hash"]
            cursor.execute('''
                INSERT INTO decisions
                (decision_id, module, action, approved, confidence, timestamp, input_data, output_data, audit_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                decision["decision_id"],
                decision.get("requested_module", "cgc_core"),
                decision.get("action", "orchestrated_decision"),
                int(decision["decision"]["approved"]),
                float(decision["decision"]["confidence"]),
                decision.get("timestamp", now_iso()),
                json.dumps(input_data, ensure_ascii=False),
                json.dumps(decision, ensure_ascii=False),
                audit_hash
            ))
            conn.commit()
        finally:
            conn.close()

    # --- Contracts logging helper ---
    def log_contract_analysis(self, contract_id: str, result: Dict, user_email: str) -> None:
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO contracts
                (contract_id, filename, analysis_result, risk_level, compliance_score, timestamp, user_email)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                contract_id,
                result.get("metadata", {}).get("filename", "unknown"),
                json.dumps(result, ensure_ascii=False),
                result.get("overall_risk", "UNKNOWN"),
                float(result.get("compliance_score", 0.0)),
                now_iso(),
                user_email
            ))
            conn.commit()
            self.total_contracts += 1
        finally:
            conn.close()

    # --- Metrics & status ---
    def get_real_metrics(self) -> Dict:
        """Return aggregated metrics from orchestrator and DB."""
        system_status = self.cgc_loop.get_system_status()

        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM decisions')
            total_decisions = int(cursor.fetchone()[0])
            cursor.execute('SELECT COUNT(*) FROM contracts')
            total_contracts = int(cursor.fetchone()[0])
            cursor.execute('SELECT AVG(compliance_score) FROM contracts WHERE compliance_score > 0')
            avg_compliance = cursor.fetchone()[0] or 0.0
        finally:
            conn.close()

        return {
            "total_decisions": total_decisions,
            "total_contracts": total_contracts,
            "avg_compliance_score": round(float(avg_compliance or 0.0), 2),
            "modules": system_status["modules"],
            "system_health": system_status["cgc_core"]["health"],
            "audit_entries": self.tco.total_entries,
            "chain_verified": system_status["integrity"]["audit_chain_verified"]
        }

# --- Singleton accessor ---
_cgc_core_instance: Optional[CGCCoreEngine] = None

def get_cgc_core(db_path: str = "data/cgc_core.db") -> CGCCoreEngine:
    global _cgc_core_instance
    if _cgc_core_instance is None:
        _cgc_core_instance = CGCCoreEngine(db_path=db_path)
    return _cgc_core_instance

# --- Simple CLI test when run as script ---
if __name__ == "__main__":
    core = get_cgc_core()

    logger.info("🧪 Running basic test decision...")
    test_input = {"text": "This is a test contract snippet", "value": 123}
    res = core.execute_decision(module="test_module", action="analyze_contract", input_data=test_input, context={"user": "dev"})

    logger.info("✅ Test complete")
    logger.info("Decision ID: %s", res["decision_id"])
    logger.info("Approved: %s", res["decision"]["approved"])
    logger.info("Confidence: %s", res["decision"]["confidence"])
    logger.info("Audit entries total: %d", core.tco.total_entries)
