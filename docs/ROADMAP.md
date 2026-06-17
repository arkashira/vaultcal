# ROADMAP.md

## Project Vision
**VaultCal** is an autonomous, security-first, self-hosted contact and calendar server. It empowers organizations to reclaim control over their scheduling data while leveraging Axentx's AI capabilities to provide intelligent guidance and automated protection against threats.

## Development Philosophy
We follow the **Axentx Runbook**: features are validated against market signals and our internal datasets before implementation. We prioritize security-by-design and use the `arkashira/surrogate-1-harvest` repository as our canonical source for deployment logic.

---

## Phase 1: MVP (Minimum Viable Product)
**Status:** *Critical Path*
**Goal:** Launch a secure, self-hosted CalDAV/CardDAV server with basic guidance.

### 1.1 Core Infrastructure (MVP-Critical)
*   **Dockerized Deployment:** Create a production-ready `docker-compose.yml` and `k8s` manifests following the `arkashira/surrogate-1-harvest` structure.
*   **CalDAV/CardDAV Engine:** Integrate a hardened Radicale instance or build a custom lightweight server to handle event and contact syncing.
*   **TLS/SSL Automation:** Implement automatic Let's Encrypt certificate generation and rotation to enforce HTTPS by default.

### 1.2 Security & Protection (
