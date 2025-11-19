from datetime import datetime # ⬅️ CORRECCIÓN 1: Se importa datetime

class TenantManager:
    def __init__(self):
        self.tenants = {}  # org_id -> tenant_config
    
    def create_tenant(self, org_id, org_name, plan='starter'):
        """Create isolated tenant"""
        self.tenants[org_id] = {
            'org_id': org_id,
            'org_name': org_name,
            'plan': plan,  # starter, professional, enterprise
            'api_quota': self._get_quota(plan),
            'features': self._get_features(plan), # ⬅️ CORRECCIÓN 2: Ahora llama a un método existente
            'created_at': datetime.now()
        }
    
    def _get_quota(self, plan):
        quotas = {
            'starter': {'contracts_per_month': 100, 'users': 5},
            'professional': {'contracts_per_month': 500, 'users': 25},
            'enterprise': {'contracts_per_month': -1, 'users': -1}  # unlimited
        }
        return quotas[plan]
    
    def _get_features(self, plan):
        """Returns features enabled by plan"""
        if plan == 'starter':
            return ['analysis_basic', 'compliance_score']
        elif plan == 'professional':
            return ['analysis_full', 'audit_log', 'reporting']
        return ['analysis_full', 'audit_log', 'reporting', 'custom_models']

# Nota: Este código debe estar en un módulo importado (ej. database.py o tenant_manager.py)