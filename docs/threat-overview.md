# Threat overview: five error types

PrePulse detects five types of problems in server logs. Each type below
describes what it is, how it looks in a log, and which rule detects it.
Thresholds and time windows are not fixed here. They live in the
`detection_rule.config` column, so they can be changed without code.

| # | Error type | Category | Log source | Rule |
|---|---|---|---|---|
| 1 | PHP errors and HTTP 500 | Operations | PHP error log, web server access log | #11 |
| 2 | Database problems | Operations | MySQL / PostgreSQL error log | #12 |
| 3 | Brute force login attempts | Security | auth.log (SSH) | #22 |
| 4 | Port scanning | Security | Web server access log | #21 |
| 5 | Service failure (proposed) | Operations | System log | not yet planned |

## 1. PHP errors and HTTP 500
- **What:** The application crashes or returns server errors to users.
- **Signal:** `PHP Fatal error`, `PHP Warning` and responses with status 500.
- **Detect:** Many 500 responses or fatal errors within a short time window.

## 2. Database problems
- **What:** The application cannot reach or use the database.
- **Signal:** `Too many connections`, `Connection refused`, deadlocks, slow query warnings.
- **Detect:** Repeated database errors within a time window.

## 3. Brute force login attempts
- **What:** Someone guesses passwords on the server.
- **Signal:** Many `Failed password` lines from the same IP address.
- **Detect:** N failed logins from one IP within M minutes (same principle as fail2ban).

## 4. Port scanning
- **What:** Someone probes the server for open services or known paths.
- **Signal:** Many 404 or 401 responses from one IP, often on unusual paths.
- **Detect:** N 4xx responses from one IP within M minutes.

## 5. Service failure (proposed)
- **What:** A service stops or restarts repeatedly.
- **Signal:** `Failed to start`, `Out of memory`, repeated restarts in the system log.
- **Detect:** Service failure messages repeated within a time window.

## Notes
- Brute force and port scanning are security events. The other three are operational.
- N and M for each rule are set in `detection_rule.config`.
- Example IP addresses in test data use documentation ranges
  (`203.0.113.x`, `198.51.100.x`), so no real personal data is in the repository.
