"""vaultcal – a tiny wizard for a hardened Radicale setup."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class TLSCertificate:
    """Simple container for a TLS certificate and its private key."""

    cert: str
    key: str


@dataclass(frozen=True)
class RadicaleConfig:
    """Configuration values that would be written to Radicale's config file."""

    cert_path: str
    key_path: str
    blocked_methods: List[str]


def _validate_domain(domain: str) -> None:
    if not isinstance(domain, str) or not domain.strip():
        raise ValueError("Domain must be a non‑empty string.")


def _validate_port(port: int) -> None:
    if not isinstance(port, int) or not (1 <= port <= 65535):
        raise ValueError("Port must be an integer between 1 and 65535.")


def generate_tls_certificate(domain: str) -> TLSCertificate:
    """
    Simulate the creation of a TLS certificate for *domain*.

    The function does **not** contact Let’s Encrypt – it returns deterministic
    placeholder strings that contain the domain name, which is sufficient for
    unit‑testing the surrounding logic.

    Parameters
    ----------
    domain: str
        The fully qualified domain name for which the certificate is created.

    Returns
    -------
    TLSCertificate
        An object containing placeholder PEM‑like strings.
    """
    _validate_domain(domain)
    cert = f"---BEGIN CERTIFICATE for {domain}---\n...certificate data...\n---END CERTIFICATE---"
    key = f"---BEGIN PRIVATE KEY for {domain}---\n...key data...\n---END PRIVATE KEY---"
    return TLSCertificate(cert=cert, key=key)


def create_radicale_config(cert_path: str, key_path: str) -> RadicaleConfig:
    """
    Produce a hardened Radicale configuration.

    The configuration blocks the insecure XML‑RPC and DAV methods.

    Parameters
    ----------
    cert_path: str
        Path where the TLS certificate will be stored.
    key_path: str
        Path where the TLS private key will be stored.

    Returns
    -------
    RadicaleConfig
        The configuration object.
    """
    if not cert_path or not key_path:
        raise ValueError("Both cert_path and key_path must be non‑empty strings.")
    blocked = ["XML-RPC", "DAV"]
    return RadicaleConfig(cert_path=cert_path, key_path=key_path, blocked_methods=blocked)


def generate_firewall_rules(port: int) -> List[str]:
    """
    Generate simple iptables rules that allow traffic only to *port*.

    The rules are returned as strings; they are **not** executed.

    Parameters
    ----------
    port: int
        The port number that should be exposed.

    Returns
    -------
    List[str]
        Two iptables commands – one to ACCEPT the desired port and one to DROP
        everything else.
    """
    _validate_port(port)
    accept_rule = f"iptables -A INPUT -p tcp --dport {port} -j ACCEPT"
    drop_rule = "iptables -A INPUT -p tcp -j DROP"
    return [accept_rule, drop_rule]


def run_setup_wizard(domain: str, port: int = 5232) -> dict:
    """
    Orchestrate the whole setup process.

    * Generates a TLS certificate (simulated).
    * Creates a Radicale configuration that references the generated cert.
    * Produces firewall rules for the given *port*.

    Returns a dictionary with the three artifacts for easy inspection.

    Parameters
    ----------
    domain: str
        Domain name for which the certificate is generated.
    port: int, optional
        Port to protect with firewall rules (default 5232).

    Returns
    -------
    dict
        Keys: ``certificate`` (TLSCertificate), ``config`` (RadicaleConfig),
        ``firewall_rules`` (list of str).
    """
    _validate_domain(domain)
    _validate_port(port)

    certificate = generate_tls_certificate(domain)

    # In a real deployment these would be written to disk; here we just
    # construct plausible file names.
    cert_path = os.path.join("/etc/radicale/certs", f"{domain}.crt")
    key_path = os.path.join("/etc/radicale/certs", f"{domain}.key")
    config = create_radicale_config(cert_path, key_path)

    firewall_rules = generate_firewall_rules(port)

    return {
        "certificate": certificate,
        "config": config,
        "firewall_rules": firewall_rules,
    }
