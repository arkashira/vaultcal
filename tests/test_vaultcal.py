from vaultcal import VaultCal, ChecklistItem, ComplianceStatus

def test_verify_checklist():
    vaultcal = VaultCal()
    vaultcal.verify_checklist()
    for item in vaultcal.get_checklist():
        assert item.status != ComplianceStatus.UNKNOWN

def test_export_to_pdf():
    vaultcal = VaultCal()
    vaultcal.verify_checklist()
    pdf_content = vaultcal.export_to_pdf()
    assert "TLS enabled: COMPLIANT" in pdf_content
    assert "Data encryption at rest: COMPLIANT" in pdf_content

def test_get_checklist():
    vaultcal = VaultCal()
    checklist = vaultcal.get_checklist()
    assert len(checklist) == 2
    assert checklist[0].name == "TLS enabled"
    assert checklist[1].name == "Data encryption at rest"
