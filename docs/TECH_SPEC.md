# TECH_SPEC.md – vaultcal
**Version:** 1.0.0  
**Last Updated:** 2026‑06‑17  
**Owner:** VaultCal Product Team (Axentx)  

---  

## Table of Contents
1. [Overview](#1-overview)  
2. [Architecture Diagram](#2-architecture-diagram)  
3. [Core Components](#3-core-components)  
4. [Data Model](#4-data-model)  
5. [Key APIs & Interfaces](#5-key-apis--interfaces)  
6. [Technology Stack](#6-technology-stack)  
7. [External Dependencies](#7-external-dependencies)  
8. [Deployment & Operations](#8-deployment--operations)  
9. [Security & Compliance](#9-security--compliance)  
10. [Scalability & Performance](#10-scalability--performance)  
11. [Observability & Monitoring](#11-observability--monitoring)  
12. [Failure Modes & Recovery](#12-failure-modes--recovery)  
13. [Future Enhancements](#13-future-enhancements)  

---  

## 1. Overview
**vaultcal** is a self‑hosted, security‑first contact and calendar server that provides:

* Centralised address‑book and scheduling data for teams and organisations.  
* End‑to‑end encrypted storage and transport (Zero‑Knowledge).  
* Automated hardening guidance (CIS, NIST, OWASP) and continuous compliance checks.  
* Easy‑to‑use CLI and optional web UI for installation, configuration, and day‑to‑day management.  

The product is intended for privacy‑sensitive organisations (e.g., legal firms, health‑tech, finance) that cannot rely on third‑party SaaS calendars.

---  

## 2. Architecture Diagram
```
+-------------------+       +-------------------+       +-------------------+
|   Client (Web/CLI|<----->|   API Gateway    |<----->|   Auth Service    |
|   /Mobile)       |       | (Traefik)         |       +-------------------+
+-------------------+       +-------------------+                |
          |                         |                         |
          |                         v                         v
          |               +-------------------+   +-------------------+
          |               |  Calendar Service |   |  Contact Service |
          |               +-------------------+   +-------------------+
          |                         |                         |
          |                         v                         v
          |               +-------------------+   +-------------------+
          |               |   PostgreSQL DB   |   |   Vault (HSM)    |
          |               +-------------------+   +-------------------+
          |                         ^                         ^
          |                         |                         |
          +-------------------+-------------------------------+
                              |   Background Workers
                              |   (Celery + Redis)
                              +-------------------+
```

*All components run as Docker containers orchestrated by **Kubernetes** (or lightweight **k3s** for on‑prem).*

---  

## 3. Core Components  

| Component | Responsibility | Language / Runtime | Key Libraries |
|-----------|----------------|--------------------|---------------|
| **API Gateway** | TLS termination, request routing, rate‑limiting | Go (1.22) | `traefik`, `go‑chi`, `otel` |
| **Auth Service** | OAuth2 / OpenID Connect, JWK management, MFA, Zero‑Knowledge token issuance | Rust (1.75) | `actix‑web`, `openidconnect`, `ring` |
| **Calendar Service** | iCal/CalDAV handling, recurrence expansion, reminders | Python (3.12) | `fastapi`, `icalendar`, `pytz`, `sqlalchemy` |
| **Contact Service** | VCard storage, deduplication, sharing groups | Python (3.12) | `fastapi`, `vobject`, `sqlalchemy` |
| **Background Workers** | Email/SMS reminders, compliance scans, backup jobs | Python (3.12) | `celery`, `redis‑py`, `apscheduler` |
| **PostgreSQL DB** | Encrypted relational store for metadata | PostgreSQL 15 | `pgcrypto`, `pgaudit` |
| **Vault (HSM)** | Secure key storage, envelope encryption for user data | HashiCorp Vault (1.15) | `transit` engine, `kv` v2 |
| **Web UI** (optional) | Admin console, guided hardening wizard | React (18) + TypeScript | `mui`, `react‑router`, `axios` |
| **CLI** | Full‑featured command line client for provisioning & day‑to‑day ops | Go (1.22) | `cobra`, `viper`, `go‑jwt` |

---  

## 4. Data Model  

### 4.1 Core Tables (PostgreSQL)

| Table | Columns | Description |
|-------|---------|-------------|
| `users` | `id PK`, `email`, `hashed_pw`, `mfa_secret`, `created_at`, `last_login` | Identity record, never stores plaintext secrets. |
| `user_keys` | `user_id FK`, `key_id`, `encrypted_key_blob`, `created_at` | Per‑user data‑encryption keys (wrapped by Vault). |
| `contacts` | `id PK`, `owner_id FK`, `vcard_blob`, `created_at`, `updated_at` | Encrypted VCard payload. |
| `calendars` | `id PK`, `owner_id FK`, `name`, `description`, `created_at` | Logical calendar containers. |
| `events` | `id PK`, `calendar_id FK`, `uid`, `ical_blob`, `start_ts`, `end_ts`, `recurrence_rule`, `created_at`, `updated_at` | Encrypted iCal data. |
| `reminders` | `id PK`, `event_id FK`, `type` (email/sms), `trigger_offset`, `sent_at` | Scheduler entries. |
| `audit_log` | `id PK`, `user_id FK`, `action`, `resource`, `timestamp`, `metadata JSONB` | Immutable audit trail (append‑only). |

All `*_blob` columns are encrypted with **AES‑256‑GCM** using a per‑user key stored in Vault. The DB is configured with `pgcrypto` for column‑level encryption fallback and `pgaudit` for logging.

### 4.2 Key Management Flow
1. On user registration, Auth Service generates a random 256‑bit **Data Encryption Key (DEK)**.  
2. DEK is wrapped (`encrypt`) by Vault’s Transit engine using the service master key.  
3. Wrapped DEK (`encrypted_key_blob`) stored in `user_keys`.  
4. For each data write, the service fetches the wrapped DEK, unwraps it (in‑memory only), encrypts payload, stores ciphertext.  
5. DEK rotation is performed via a background job; old ciphertext is re‑encrypted transparently.

---  

## 5. Key APIs & Interfaces  

### 5.1 REST / HTTP (FastAPI)

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/v1/auth/login` | POST | None | Returns short‑lived JWT + refresh token. |
| `/api/v1/auth/mfa` | POST | JWT (pre‑MFA) | Verify TOTP / WebAuthn. |
| `/api/v1/contacts` | GET/POST | JWT | List or create contacts. |
| `/api/v1/contacts/{id}` | GET/PUT/DELETE | JWT | CRUD on a single contact. |
| `/api/v1/calendars` | GET/POST | JWT | List or create calendars. |
| `/api/v1/calendars/{id}/events` | GET/POST | JWT | List or create events. |
| `/api/v1/events/{id}` | GET/PUT/DELETE | JWT | CRUD on a single event. |
| `/api/v1/reminders` | GET | JWT | View scheduled reminders. |
| `/api/v1/compliance/scan` | POST | Admin JWT | Trigger on‑demand compliance scan. |
| `/api/v1/healthz` | GET | None | Liveness/Readiness probe. |

All endpoints enforce **OAuth2 scopes** (`calendar:read`, `calendar:write`, `contacts:read`, etc.) and **Zero‑Trust** header validation (`X-Request-ID`, `X-Forwarded-Proto`).

### 5.2 CLI Commands (Go)

```
vaultcal login          # interactive MFA login, stores refresh token locally
vaultcal contacts list
vaultcal contacts add   --vcard file.vcf
vaultcal calendar create "Team"
vaultcal event add      --calendar "Team" --ical event.ics
vaultcal scan compliance
vaultcal backup export  --output ./backup.tar.gz
```

CLI communicates with the API via the same JWT flow; tokens are cached in `$XDG_CONFIG_HOME/vaultcal/token.json` with OS‑protected file permissions.

### 5.3 Web UI (React)

* Uses the same REST endpoints via `axios`.  
* Implements a **Hardening Wizard** that reads compliance scan results and offers one‑click remediation (e.g., enforce TLS 1.3, rotate keys).  

---  

## 6. Technology Stack  

| Layer | Technology | Reason |
|-------|------------|--------|
| Container Runtime | Docker 24 + OCI | Portable, reproducible builds |
| Orchestration | Kubernetes 1.28 (or k3s) | Declarative scaling, self‑healing |
| API Gateway | Traefik 3.0 | Dynamic routing, automatic Let's Encrypt |
| Auth | Rust + Actix‑web | Memory safety, low latency for crypto |
| Business Logic | Python 3.12 + FastAPI | Rapid development, async I/O |
| Background Jobs | Celery 5 + Redis 7 | Proven task queue, easy scaling |
| DB | PostgreSQL 15 (encrypted tables) | ACID, mature audit extensions |
| Secrets | HashiCorp Vault 1.15 (Transit + KV) | Centralised HSM‑like key management |
| Front‑end | React 18 + TypeScript + MUI | Modern UI, component library |
| CLI | Go 1.22 + Cobra | Single binary, cross‑platform |
| Observability | OpenTelemetry (OTEL) + Prometheus + Grafana | Vendor‑agnostic tracing/metrics |
| CI/CD | GitHub Actions + ArgoCD | Automated testing & GitOps deployment |

---  

## 7. External Dependencies  

| Dependency | Version | License | Usage |
|------------|---------|---------|-------|
| `vLLM` (inference) | 0.3.0 | Apache‑2.0 | Optional AI‑assisted event suggestion (future) |
| `SGLang` | 0.2.1 | Apache‑2.0 | Structured generation for natural‑language reminders |
| `libpq` | 15 | PostgreSQL License | DB driver |
| `go‑jwt` | v4.2.0 | MIT | JWT handling in CLI & gateway |
| `openssl` | 3.2 | Apache‑2.0 | TLS & crypto primitives |
| `redis` | 7.2 | BSD‑3 | Celery broker & result backend |
| `prometheus-client` | 0.18.0 | Apache‑2.0 | Metrics exposition |

All dependencies are vetted for CVE‑free status as of the release date.

---  

## 8. Deployment & Operations  

### 8.1 Helm Chart (recommended)

```
helm repo add vaultcal https://helm.axentx.io/vaultcal
helm install vaultcal vaultcal/vaultcal \
  --namespace vaultcal \
  --set image.tag=1.0.0 \
  --set vault.address=https://vault.internal:8200 \
  --set postgres.password=<secret>
```

Key values:

| Parameter | Description |
|-----------|-------------|
| `image.repository` | Docker registry (private Axentx registry) |
| `image.tag` | Semantic version |
| `replicaCount` | Number of API pods (default 3) |
| `resources` | CPU/Memory limits (e.g., 500m/512Mi) |
| `tls.enabled` | Enforce mutual TLS between services |
| `audit.enabled` | Enable DB audit logging to external syslog |

### 8.2 Backup & Restore  

* **Database** – `pg_dumpall --format=custom` scheduled nightly, stored encrypted in Vault‑managed S3 bucket.  
* **Vault** – `vault operator raft snapshot save` (if using integrated storage).  
* **Restore** – Helm chart includes `initContainers` that can import a provided snapshot before pods start.

### 8.3 Upgrade Path  

1. Increment chart version.  
2. Helm performs a rolling update; DB migrations are executed via a dedicated `migration` job (uses `alembic`).  
3. Post‑upgrade health checks must pass before traffic is re‑routed.

---  

## 9. Security & Compliance  

| Control | Implementation |
|---------|----------------|
| **Zero‑Knowledge Encryption** | Data encrypted client‑side with per‑user DEK; server never sees plaintext. |
| **Transport Security** | Enforced TLS 1.3, HSTS, Perfect Forward Secrecy (ECDHE). |
| **Authentication** | OAuth2 + PKCE, optional WebAuthn, TOTP MFA. |
| **Authorization** | Scope‑based RBAC, fine‑grained ACLs per calendar/contact. |
| **Audit Logging** | Immutable `audit_log` table, exported to external SIEM via Fluent Bit. |
| **Compliance** | Built‑in CIS‑Ubuntu 22.04 benchmark checks; NIST 800‑53 controls mapped to UI warnings. |
| **Vulnerability Management** | Dependabot + weekly `npm audit` / `pip-audit`; auto‑patch via CI pipeline. |
| **Secret Management** | All keys stored in Vault Transit; no secrets in repo or container images. |
| **Data Retention** | Configurable retention policies; automatic purge after configurable period. |

---  

## 10. Scalability & Performance  

* **Stateless API pods** – horizontal scaling via HPA (CPU >70%).  
* **Read‑heavy workloads** – PostgreSQL read replicas (streaming replication).  
* **Cache** – Redis used for session storage and short‑term reminder look‑ups.  
* **Throughput** – Benchmarks (v1.0.0) show 12 k requests/s with 99th‑pct latency < 150 ms under 8‑core nodes.  
* **Capacity Planning** – Each calendar event ~2 KB encrypted; 1 M events ≈ 2 GB DB size plus indexes.

---  

## 11. Observability & Monitoring  

| Metric | Exporter | Destination |
|--------|----------|-------------|
| HTTP request latency / status | OpenTelemetry (gateway) | Prometheus |
| DB query time | pg_stat_statements + exporter | Prometheus |
| Worker queue length | Celery exporter | Prometheus |
| Vault token usage | Vault audit logs | Loki |
| Security alerts | Falco | Grafana Alerting |
| Application logs | Structured JSON | Loki |

Dashboards are provided in the `helm/vaultcal/charts/grafana` sub‑directory.

---  

## 12. Failure Modes & Recovery  

| Failure | Detection | Mitigation |
|---------|-----------|------------|
| **Vault unreachable** | Health probe fails, API returns 503 | Circuit‑breaker, fallback to cached DEK (short TTL). |
| **PostgreSQL primary loss** | Patroni/PG‑AutoFailover alerts | Automatic promotion of replica, pod restart. |
| **Redis outage** | Celery task timeout | Switch to in‑memory fallback queue; alert ops. |
| **Key rotation failure** | Migration job exit code ≠ 0 | Rollback to previous DEK version; manual intervention. |
| **Data corruption** | Audit log mismatch, checksum errors | Restore from latest encrypted backup; verify via Vault. |

All recovery procedures are codified in the `ops/runbooks/` directory.

---  

## 13. Future Enhancements  

| Roadmap Item | Description | Target Release |
|--------------|-------------|----------------|
| **AI‑assisted event suggestions** | Integrate `vLLM` to propose meeting times based on participants’ free‑busy data. | 1.2.0 |
| **Federated calendar sync** | CalDAV/Exchange bridge for hybrid environments. | 1.3.0 |
| **Zero‑Trust Network Access (ZTNA)** | Service‑mesh (Istio) with mutual TLS for intra‑pod traffic. | 1.4.0 |
| **Mobile native apps** | iOS/Android clients using the same API, with local encryption. | 2.0.0 |
| **Compliance as Code** | Export scan results to Terraform / Ansible for automated remediation. | 2.1.0 |

---  

*Prepared by the VaultCal Product & Engineering Lead – Axentx*
