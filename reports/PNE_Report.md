# Protection Needs Elicitation (PNE) – Secure Voting System

## Assets
- Voter registration data
- Authentication credentials (MFA tokens)
- Ballots (encrypted votes)
- Vote counting results
- Audit logs

## Threats
- Spoofing: fake user registration
- Tampering: vote manipulation
- Repudiation: denying vote cast
- Information Disclosure: vote leakage
- Denial of Service: voting system unavailability
- Elevation of Privilege: unauthorized admin access

## Protection Needs
- Confidentiality: encrypt all votes and user data
- Integrity: prevent vote tampering, ensure accurate counting
- Availability: system must remain online during voting
- Authentication & Authorization: enforce MFA and role‑based access
- Auditability: maintain logs for transparency and accountability 
