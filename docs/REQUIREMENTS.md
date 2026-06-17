# REQUIREMENTS.md  

**Project:** vaultcal  
**Owner:** AxentX – Security‑Focused Self‑Hosted Contact & Calendar Server  
**Version:** 1.0.0  
**Last Updated:** 2026‑06‑17  

---  

## 1. Overview  

vaultcal is a self‑hosted service that provides secure storage, synchronization, and management of contacts and calendar events. It is intended for privacy‑conscious organizations that require on‑premise control, end‑to‑end encryption, and built‑in hardening guidance. The product must be easy to install, configure, and operate while delivering enterprise‑grade security and reliability.

---  

## 2. Scope  

| In‑Scope | Out‑of‑Scope |
|----------|--------------|
| • Self‑hosted deployment (Docker, Kubernetes, binary) | • Cloud‑hosted SaaS offering |
| • Contact & calendar data model (vCard, iCalendar) | • Integration with proprietary calendar protocols (e.g., Microsoft Exchange) |
| • End‑to‑end encryption of data at rest and in transit | • Real‑time video conferencing |
| • Role‑based access control (RBAC) and audit logging | • Mobile client apps (only API access) |
| • Automated security hardening recommendations | • Third‑party UI themes |

---  

## 3. Functional Requirements  

| ID | Requirement | Description |
|----|-------------|-------------|
| **FR‑1** | **Installation & Bootstrap** | Provide a single‑command installer for Docker Compose and a Helm chart for Kubernetes. The installer must verify system prerequisites, generate TLS certificates, and create an initial admin user with a strong random password. |
| **FR‑2** | **Data Model** | Support storage of contacts (vCard 4.0) and calendar events (iCalendar RFC 5545). Each object must be versioned to enable conflict resolution and historical rollback. |
| **FR‑3** | **End‑to‑End Encryption** | All data must be encrypted at rest using AES‑256‑GCM with keys derived from a master passphrase stored only in memory. In‑transit traffic must use TLS 1.3 with server‑side mutual authentication optional. |
| **FR‑4** | **User & Role Management** | Implement RBAC with three built‑in roles: **Admin**, **Editor**, **Viewer**. Admins can create users, assign roles, and manage encryption keys. Editors can create/modify contacts & events; Viewers have read‑only access. |
| **FR‑5** | **API Layer** | Expose a RESTful JSON API conforming to the CalDAV and CardDAV specifications (subset sufficient for CRUD). The API must be documented with OpenAPI 3.0 and include a Swagger UI. |
| **FR‑6** | **Web UI** | Provide a responsive single‑page application (SPA) for managing contacts and calendars. The UI must consume the REST API, enforce RBAC client‑side, and display security recommendations (e.g., password strength, key rotation). |
| **FR‑7** | **Synchronization** | Support multi‑node replication using Raft consensus. Nodes must automatically sync contacts/events while preserving encryption (data never leaves encrypted at rest). |
| **FR‑8** | **Backup & Restore** | Offer encrypted backup snapshots (binary blobs) that can be stored off‑site. Restore must verify integrity via SHA‑256 hash and require the master passphrase. |
| **FR‑9** | **Audit Logging** | Record all privileged actions (login, user creation, key rotation, data delete) to an append‑only log. Logs must be signed with an HMAC‑SHA256 key and optionally forwarded to syslog or a SIEM. |
| **FR‑10** | **Security Guidance** | On first‑run and on demand, display a checklist of hardening steps (e.g., rotate keys, enable MFA, restrict IP ranges). The system must be able to auto‑apply safe defaults (e.g., disable password login, enforce MFA). |
| **FR‑11** | **Extensibility Hooks** | Provide a plugin interface (Go plugins or gRPC) for custom validation, notification (email/webhook), and import/export adapters. |
| **FR‑12** | **Metrics & Health** | Export Prometheus‑compatible metrics (request latency, replication lag, encryption errors) and expose `/healthz` and `/readyz` endpoints. |

---  

## 4. Non‑Functional Requirements  

| ID | Category | Requirement |
|----|----------|-------------|
| **NFR‑1** | **Performance** | API latency ≤ 150 ms for 95 % of requests under a load of 500 concurrent users. Replication lag ≤ 2 seconds under normal network conditions. |
| **NFR‑2** | **Scalability** | System must scale horizontally to at least 10 nodes, each handling up to 1 M contacts and 5 M events. |
| **NFR‑3** | **Security** | - All dependencies must be scanned with Snyk and have no critical CVEs. <br>- Enforce CSP, X‑Content‑Type‑Options, Referrer‑Policy in the UI. <br>- Support MFA (TOTP) for admin accounts. |
| **NFR‑4** | **Reliability** | Achieve 99.9 % uptime (≤ 8.76 h downtime per year). Automatic failover to a healthy replica within 30 seconds of node failure. |
| **NFR‑5** | **Data Integrity** | Use Merkle‑tree hashes for each data block; any corruption must be detected on read and reported in logs. |
| **NFR‑6** | **Observability** | Logs must be structured (JSON) and include request IDs. Metrics must be retained for at least 30 days. |
| **NFR‑7** | **Maintainability** | Codebase must achieve ≥ 80 % unit test coverage and ≥ 70 % integration test coverage. CI pipeline must run lint, static analysis (golangci‑lint), and security scans on every PR. |
| **NFR‑8** | **Portability** | The Docker image must be ≤ 150 MB (Alpine base). Helm chart must support Kubernetes 1.26+. |
| **NFR‑9** | **Compliance** | Provide exportable data in GDPR‑compatible format (JSON‑LD) and support data‑subject deletion requests within 24 hours. |
| **NFR‑10** | **Usability** | Installation wizard must complete in ≤ 5 minutes on a fresh VM (2 CPU, 4 GB RAM). UI must pass WCAG 2.1 AA accessibility tests. |

---  

## 5. Constraints  

1. **Technology Stack** – Primary implementation language is Go 1.22; UI must be built with React 18 and TypeScript.  
2. **Licensing** – All third‑party libraries must be compatible with Apache‑2.0 or MIT licenses.  
3. **Resource Limits** – The service must run on a minimum of 2 CPU cores and 2 GB RAM per node.  
4. **Data Residency** – Encryption keys may never be persisted to disk; they must be derived from a passphrase supplied at startup or via a KMS (AWS KMS, HashiCorp Vault).  
5. **External Dependencies** – Only official Docker Hub images and Helm charts from trusted repositories may be used.  

---  

## 6. Assumptions  

| ID | Assumption |
|----|------------|
| **A‑1** | Customers have the ability to provision TLS certificates or will rely on the built‑in self‑signed generation. |
| **A‑2** | The target environment provides a reliable time source (NTP) for token expiration and log timestamps. |
| **A‑3** | Users will manage MFA devices (e.g., Google Authenticator) themselves; the system only provides QR code enrollment. |
| **A‑4** | Network latency between nodes will not exceed 100 ms under normal operation. |
| **A‑5** | Backup storage will be a POSIX‑compatible filesystem or object store that supports streaming writes. |
| **A‑6** | The product will be sold to enterprises that already have an identity provider (IdP) for SSO; integration via OpenID Connect is optional for v1.1. |

---  

## 7. Acceptance Criteria  

1. **Installation** – A new user can run `curl … | sh` and have a fully functional vaultcal cluster (single‑node Docker) up and running within 5 minutes.  
2. **Encryption** – Attempting to read the underlying SQLite/PostgreSQL files without the master passphrase yields only ciphertext.  
3. **RBAC** – An Editor cannot delete a user or rotate keys; attempts are logged and return HTTP 403.  
4. **Backup/Restore** – A backup created on a 1 M contact dataset can be restored on a fresh cluster with data integrity verified by SHA‑256.  
5. **Performance** – Load test with 500 concurrent users shows 95 % of API calls complete ≤ 150 ms.  
6. **Security Guidance** – The “Hardening Checklist” appears on first login and can be marked complete; the system automatically disables password login after 30 days if MFA is enabled.  

---  

## 8. Glossary  

- **RBAC** – Role‑Based Access Control  
- **MFA** – Multi‑Factor Authentication  
- **KMS** – Key Management Service  
- **Raft** – Consensus algorithm for replication  
- **CalDAV / CardDAV** – Standard protocols for calendar and contact synchronization  

---  

*Prepared by the VaultCal Product & Engineering Lead, AxentX*
