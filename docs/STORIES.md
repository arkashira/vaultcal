# STORIES.md

## Overview
**Product:** vaultcal  
**Goal:** Deliver a secure, self‑hosted contact and calendar server with built‑in guidance, hardening, and management tooling.  
**Target MVP:** Core server deployment, user provisioning, encrypted data storage, basic calendar/contacts CRUD, admin dashboard with security recommendations, and automated backup/restore.

---

## Epics & Backlog

### Epic 1 – Secure Deployment & Infrastructure
| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| 1.1 | **As a System Administrator, I want a one‑click installer script, so that I can deploy vaultcal on a fresh Linux server without manual configuration.** | - Installer runs on Ubuntu 22.04, Debian 12, and Rocky Linux 9.<br>- Detects missing dependencies and installs them.<br>- Generates a self‑signed TLS certificate if none provided.<br>- Creates a systemd service that starts on boot.<br>- Logs installation steps to `/var/log/vaultcal/install.log`. |
| 1.2 | **As a Security Engineer, I want the server to enforce TLS 1.3 with strong cipher suites, so that all client connections are encrypted.** | - Server only accepts TLS 1.3.<br>- Cipher list limited to `TLS_AES_256_GCM_SHA384`, `TLS_CHACHA20_POLY1305_SHA256`.<br>- Connection attempt with weaker protocols is rejected and logged. |
| 1.3 | **As a DevOps Engineer, I want vaultcal to run inside a Docker container with official images, so that I can isolate it from host OS and simplify updates.** | - Official Dockerfile builds a minimal `scratch`/`distroless` image.<br>- Image tags: `latest`, `vX.Y.Z`.<br>- Container exposes ports 443 (HTTPS) and 80 (HTTP redirect).<br>- Health‑check endpoint `/healthz` returns 200 when DB is reachable. |
| 1.4 | **As an Operations Manager, I want automated daily backups to an encrypted S3 bucket, so that data loss risk is minimized.** | - Backup job runs at 02:00 UTC.<br>- Dumps PostgreSQL DB and encrypts with AES‑256‑GCM using a vault‑managed key.<br>- Uploads to configurable S3 bucket with server‑side encryption enabled.<br>- Retains last 30 backups; older ones are pruned. |
| 1.5 | **As a Compliance Officer, I want audit logs stored immutably for 90 days, so that we can satisfy regulatory requirements.** | - All API requests, admin actions, and auth events are written to an append‑only log file.<br>- Log rotation creates daily files with SHA‑256 hash stored in a tamper‑evident manifest.<br>- Manifest is signed with the server’s private key and retained for 90 days. |

### Epic 2 – User & Identity Management
| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| 2.1 | **As an End‑User, I want to register an account with email verification, so that only legitimate users can access my calendar.** | - Registration endpoint `/api/v1/register` accepts email & password.<br>- Sends verification link with time‑limited token (24 h).<br>- Account remains inactive until link is clicked.<br>- Passwords stored with Argon2id (memory = 128 MiB, time = 2). |
| 2.2 | **As a User, I want to enable two‑factor authentication (TOTP), so that my account is protected against credential theft.** | - User can enable TOTP via `/api/v1/2fa/enable`.<br>- QR code complies with RFC 6238.<br>- Login flow prompts for TOTP code after password verification.<br>- Backup codes (10) are generated and can be regenerated. |
| 2.3 | **As an Administrator, I want role‑based access control (RBAC), so that I can delegate permissions safely.** | - Roles: `admin`, `user_manager`, `read_only`.<br>- Permissions matrix documented in `docs/rbac.md`.<br>- Admin UI allows assigning roles to users.<br>- API enforces RBAC on every endpoint (403 on violation). |
| 2.4 | **As a User, I want to import contacts from a vCard file, so that I can quickly migrate my address book.** | - Upload endpoint accepts `.vcf` up to 5 MB.<br>- Parses vCard 3.0/4.0 fields and stores them encrypted.<br>- Returns summary of imported contacts (created/updated/failed). |
| 2.5 | **As a User, I want to export my contacts and calendars in standard formats (vCard, iCal), so that I can back up or migrate data.** | - Export endpoints `/api/v1/contacts/export` and `/api/v1/calendars/export` generate downloadable `.vcf` and `.ics` files.<br>- Files are streamed, encrypted at rest, and deleted after 5 minutes. |

### Epic 3 – Calendar Core Functionality
| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| 3.1 | **As a User, I want to create, edit, and delete calendar events, so that I can manage my schedule.** | - CRUD endpoints `/api/v1/calendars/{id}/events` support RFC 5545 fields.<br>- Event conflicts are detected and returned with a warning flag.<br>- All changes are versioned; `GET /events/{id}?rev=N` returns historic state. |
| 3.2 | **As a User, I want to share a calendar with specific users with read/write permissions, so that teams can collaborate.** | - Share endpoint `/api/v1/calendars/{id}/share` accepts list of user IDs and permission level (`read`, `write`).<br>- Shared users see the calendar in their UI instantly.<br>- Revoking access removes calendar from the other user’s list. |
| 3.3 | **As a User, I want reminders via email and push (WebPush), so that I never miss an event.** | - Reminder settings per event (time before, channels).<br>- Email sent via configurable SMTP server.<br>- WebPush uses VAPID keys; subscription stored encrypted.<br>- Delivery logs are recorded in audit log. |
| 3.4 | **As a Power User, I want to import an iCal feed URL, so that external calendars (e.g., Google) are synced automatically.** | - Feed URL validated (HTTPS, reachable).<br>- Sync runs every 15 min, merging new/updated events.<br>- Conflicts resolved by “most recent edit wins” with user notification. |
| 3.5 | **As a User, I want to search events by title, location, or participant, so that I can find information quickly.** | - Full‑text search endpoint `/api/v1/events/search?q=...` returns ranked results.<br>- Supports filters: date range, calendar ID, tags.<br>- Search respects RBAC (only returns events user can see). |

### Epic 4 – Admin Dashboard & Guidance
| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| 4.1 | **As an Administrator, I want a web dashboard that shows system health, user count, and storage usage, so that I can monitor operations.** | - Dashboard reachable at `https://<host>/admin` (requires admin login).<br>- Widgets: CPU/Memory, DB connection pool, backup status, audit log tail.<br>- Data refreshed every 30 seconds via WebSocket. |
| 4.2 | **As an Administrator, I want security recommendations (e.g., weak passwords, missing 2FA), so that I can harden the deployment.** | - Analyzer runs nightly, scans user DB and config.<br>- Generates a list of findings with severity and remediation steps.<br>- Findings displayed in a “Security Advisor” panel with “Mark as Resolved” button. |
| 4.3 | **As an Administrator, I want to rotate encryption keys without downtime, so that we can comply with key‑rotation policies.** | - Key rotation wizard re‑encrypts data in background batches.<br>- Service remains online; API calls are queued if a batch is in progress.<br>- Completion status shown with progress bar and log link. |
| 4.4 | **As an Administrator, I want to view and export the immutable audit log, so that I can provide evidence during audits.** | - Log viewer supports pagination, filtering by date/user/type.<br>- Export button generates a signed, compressed archive (`.tar.gz.gpg`).<br>- Export respects retention policy (cannot export beyond 90 days). |

### Epic 5 – API & Extensibility (Post‑MVP)
| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| 5.1 | **As a Third‑Party Developer, I want a well‑documented OpenAPI spec, so that I can integrate my app with vaultcal.** | - `/openapi.json` generated automatically.<br>- Docs hosted at `https://<host>/docs` via Redoc.<br>- Includes authentication (Bearer JWT) and rate‑limit details. |
| 5.2 | **As a Developer, I want webhook callbacks for event changes, so that external systems can stay in sync.** | - Configurable webhook URLs per calendar.<br>- Payload follows CloudEvents 1.0 schema.<br>- Retries with exponential backoff up to 5 attempts; failures logged. |
| 5.3 | **As a System Integrator, I want LDAP/Active Directory sync, so that we can reuse existing user directories.** | - Sync job runs hourly, maps LDAP groups to vaultcal roles.<br>- Supports bind‑only and start‑TLS connections.<br>- Conflict resolution policy configurable (e.g., “vault wins”). |

---

## Prioritization for MVP
1. **Epic 1 – Secure Deployment & Infrastructure** (Stories 1.1‑1.5)  
2. **Epic 2 – User & Identity Management** (Stories 2.1‑2.4) – (2.5 deferred to post‑MVP)  
3. **Epic 3 – Calendar Core Functionality** (Stories 3.1‑3.3) – (3.4‑3.5 deferred)  
4. **Epic 4 – Admin Dashboard & Guidance** (Stories 4.1‑4.2) – (4.3‑4.4 deferred)  

Post‑MVP work will address remaining stories in Epics 3‑5.

--- 

*End of STORIES.md*
