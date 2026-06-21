import pytest
from vaultcal import (
    TLSCertificate,
    RadicaleConfig,
    generate_tls_certificate,
    create_radicale_config,
    generate_firewall_rules,
    run_setup_wizard,
)


def test_generate_tls_certificate_happy():
    domain = "example.com"
    cert = generate_tls_certificate(domain)
    assert isinstance(cert, TLSCertificate)
    assert domain in cert.cert
    assert domain in cert.key


def test_generate_tls_certificate_invalid_domain():
    with pytest.raises(ValueError):
        generate_tls_certificate("   ")


def test_create_radicale_config_happy():
    cert_path = "/etc/radicale/certs/example.com.crt"
    key_path = "/etc/radicale/certs/example.com.key"
    cfg = create_radicale_config(cert_path, key_path)
    assert isinstance(cfg, RadicaleConfig)
    assert cfg.cert_path == cert_path
    assert cfg.key_path == key_path
    assert "XML-RPC" in cfg.blocked_methods
    assert "DAV" in cfg.blocked_methods


def test_create_radicale_config_missing_path():
    with pytest.raises(ValueError):
        create_radicale_config("", "/some/key")


def test_generate_firewall_rules_happy():
    port = 5232
    rules = generate_firewall_rules(port)
    assert isinstance(rules, list)
    assert len(rules) == 2
    assert f"--dport {port}" in rules[0]
    assert "ACCEPT" in rules[0]
    assert "DROP" in rules[1]


def test_generate_firewall_rules_invalid_port():
    with pytest.raises(ValueError):
        generate_firewall_rules(0)


def test_run_setup_wizard_happy():
    domain = "example.org"
    result = run_setup_wizard(domain)
    # Certificate checks
    cert: TLSCertificate = result["certificate"]
    assert domain in cert.cert
    assert domain in cert.key
    # Config checks
    cfg: RadicaleConfig = result["config"]
    assert domain in cfg.cert_path
    assert domain in cfg.key_path
    assert "XML-RPC" in cfg.blocked_methods
    assert "DAV" in cfg.blocked_methods
    # Firewall checks
    fw_rules = result["firewall_rules"]
    assert any(str(5232) in rule for rule in fw_rules)


def test_run_setup_wizard_invalid_domain():
    with pytest.raises(ValueError):
        run_setup_wizard("")
