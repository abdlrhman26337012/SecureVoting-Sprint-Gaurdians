# Threat Model – Secure Voting System

## 1. System Overview

The Secure Voting System is a web-based election platform built on Flask/FastAPI with encrypted ballot storage, multi-factor authentication, and a real-time audit logging pipeline.

**Tech Stack:** Flask/FastAPI · Encrypted Database · MFA Authentication Service · Results Dashboard · Audit Log Service


## 2. Data Flow Diagram (DFD)

### Entities

| Entity | Type | Description |
|---|---|---|
| Voter | External Entity | End user casting a ballot |
| Authentication Service | Process | Handles MFA login and token issuance |
| Voting Application | Process | Receives and processes encrypted votes |
| Database | Data Store | Stores encrypted ballots and voter info |
| Results Dashboard | Process | Aggregates and displays vote counts |
| Audit Log Service | Process | Records all system events |

### Data Flows

Voter ──(Login Credentials)──► Authentication Service
Authentication Service ──(Auth Token)──► Voter
Voter ──(Encrypted Vote)──► Voting Application
Voting Application ──(Encrypted Ballot)──► Database
Database ──(Vote Count)──► Results Dashboard
Authentication Service ──(Logs)──► Audit Log Service
Voting Application ──(Logs)──► Audit Log Service
Database ──(Logs)──► Audit Log Service
Results Dashboard ──(Logs)──► Audit Log Service


### Trust Boundary

A trust boundary exists between the public-facing voter interface and the internal backend components (Voting Application, Database, Results Dashboard, Audit Log Service).

> DFD diagram: 
<img width="592" height="962" alt="Untitled Diagram drawio" src="https://github.com/user-attachments/assets/240f155f-399d-4fcb-9ad4-d74b110dadd0" />


## 3. Attack Tree

**Goal: Manipulate Election Results**


Manipulate Election Results
├── OR ── Voter Spoofing
│         └── AND ── Bypass MFA
│                   └── AND ── Register Fake Voter
│                             └── AND ── Cast Fraudulent Votes
│
├── OR ── Database Tampering
│         └── AND ── Gain DB Access
│                   └── AND ── Alter Stored Ballots
│
├── OR ── Privilege Escalation
│         └── AND ── Exploit Vulnerability
│                   └── AND ── Gain Admin Rights
│                             └── AND ── Modify Vote Tallies
│
└── OR ── Denial of Service
          └── AND ── Flood Server with Requests
                    └── AND ── Block Legitimate Voters


> Attack tree diagram:
<img width="1018" height="568" alt="Untitled Diagram drawio (1)" src="https://github.com/user-attachments/assets/53020211-9d4f-45d0-bc4d-8a824b19d782" />



## 4. STRIDE Analysis

| Threat | Description | Example in System | Mitigation |
|---|---|---|---|
| **Spoofing** | Attacker impersonates a legitimate voter | Fake voter registration with stolen credentials | MFA + government-issued ID verification |
| **Tampering** | Unauthorized modification of data | Altering stored ballots in the database | End-to-end ballot encryption + HMAC integrity checks |
| **Repudiation** | User denies performing an action | Voter claims they never cast a vote | Cryptographically signed audit logs + non-repudiation tokens |
| **Information Disclosure** | Sensitive data exposed to unauthorized parties | Ballot contents or voter PII leaked | AES-256 encryption at rest + TLS in transit + strict access control |
| **Denial of Service** | System made unavailable | Flooding voting endpoint during election window | Rate limiting + WAF + horizontal load balancing |
| **Elevation of Privilege** | Attacker gains higher access than authorized | Regular user gains admin rights to modify results | RBAC + principle of least privilege + privileged access monitoring |



## 5. CVSS v3.1 Risk Assessment

| Threat | Vector | CVSS Score | Severity | Justification |
|---|---|---|---|---|
| Voter Spoofing | AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N | 7.5 | **High** | Enables fraudulent votes, direct integrity impact |
| Database Tampering | AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N | 9.0 | **Critical** | Full compromise of election results |
| Repudiation | AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N | 6.0 | **Medium** | Undermines trust, but does not alter results directly |
| Information Disclosure | AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N | 8.0 | **High** | Violates voter anonymity and confidentiality |
| Denial of Service | AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H | 7.5 | **High** | Prevents legitimate voters from casting ballots |
| Elevation of Privilege | AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H | 9.5 | **Critical** | Full system compromise, results can be modified at will |

> Scores calculated using [NVD CVSS v3.1 Calculator](https://nvd.nist.gov/vuln-metrics/cvss/v3-calculator)



## 6. Mitigations Summary

### Authentication & Identity
- Multi-factor authentication (TOTP or hardware key) enforced on all voter sessions
- Government-issued ID verification during voter registration
- Session tokens expire after inactivity; refresh tokens stored server-side only

### Data Integrity
- Ballots encrypted with AES-256 before storage
- HMAC or digital signatures on each ballot record to detect tampering
- Database access restricted to the Voting Application service account only

### Confidentiality
- TLS 1.3 enforced for all data in transit
- Voter identity decoupled from ballot content at the database level
- PII access logged and alerting on anomalous access patterns

### Availability
- Rate limiting per IP and per authenticated session on the voting endpoint
- WAF rules to detect and block flood patterns
- Load balancer with auto-scaling during peak election hours
- Graceful degradation: read-only mode if write services degrade

### Privilege Control
- Role-Based Access Control (RBAC): Voter / Election Official / System Admin roles with strict separation
- Principle of least privilege enforced at the service and DB account level
- Admin actions require re-authentication and are logged with full context

### Auditability & Non-Repudiation
- All authentication events, votes cast, and admin actions written to the Audit Log Service
- Audit logs are append-only and cryptographically chained (similar to a Merkle tree)
- Log integrity verified periodically by an independent process



## 7. Residual Risks

| Risk | Likelihood | Impact | Accepted / Requires Further Work |
|---|---|---|---|
| Insider threat (malicious admin) | Low | Critical | Requires further work – dual-control on admin actions |
| Zero-day in Flask/FastAPI | Low | High | Accepted – dependency on upstream patching |
| Social engineering of voter | Medium | Medium | Accepted – user education program required |
| Physical DB server access | Very Low | Critical | Accepted – mitigated by cloud infrastructure and HSM |


## 8. Assumptions & Scope

- The voting application runs in a cloud-hosted environment with managed infrastructure security (DDoS protection, disk encryption) handled by the provider.
- Voter device security (malware, keyloggers) is out of scope for this threat model.
- The model covers the online voting flow only; physical/paper backup processes are out of scope.
- Diagrams reflect the system architecture as of the initial design phase and should be updated when components change.

