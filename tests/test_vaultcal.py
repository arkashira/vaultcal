import pytest
from vaultcal import VaultCal, AuditLog

@pytest.fixture
def vaultcal():
    return VaultCal()

def test_publish_audit_log(vaultcal: VaultCal, caplog):
    audit_log = AuditLog(
        timestamp='2022-01-01T00:00:00',
        checklist_item='example_item',
        status='example_status',
        remediation_link='example_link'
    )
    vaultcal.publish_audit_log(audit_log)
    assert 'Not publishing audit log' in caplog.text

def test_publish_audit_log_with_syslog_endpoint(vaultcal: VaultCal, caplog):
    vaultcal.syslog_endpoint = 'example_endpoint'
    audit_log = AuditLog(
        timestamp='2022-01-01T00:00:00',
        checklist_item='example_item',
        status='example_status',
        remediation_link='example_link'
    )
    vaultcal.publish_audit_log(audit_log)
    assert 'Publishing audit log to example_endpoint' in caplog.text

def test_run_with_log_forwarding(vaultcal: VaultCal, caplog):
    vaultcal.run(True, 'example_endpoint')
    assert 'Publishing audit log to example_endpoint' in caplog.text

def test_run_without_log_forwarding(vaultcal: VaultCal, caplog):
    vaultcal.run(False)
    assert 'Not publishing audit log' in caplog.text
