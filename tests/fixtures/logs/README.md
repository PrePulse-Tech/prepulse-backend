# Test log fixtures

Synthetic log files for developing and testing the parser and the detection rules.
They are made up. No real servers, users or personal data are involved.

The formats are based on common defaults and will be updated when we receive
real samples from Preface.

| File | Format | Error type | Rule |
|---|---|---|---|
| `nginx-access.log` | nginx combined | PHP errors and HTTP 500 (12 lines with status 500) | #11 |
| `nginx-access.log` | nginx combined | Port scanning (25 lines with 404/401 from `198.51.100.23`) | #21 |
| `php-error.log` | PHP error log | PHP errors and HTTP 500 | #11 |
| `mysql-error.log` | MySQL 8 error log | Database problems | #12 |
| `auth.log` | OpenSSH / auth.log | Brute force login attempts (24 failed logins from `203.0.113.5`) | #22 |
| `syslog.log` | systemd / syslog | Service failure (proposed) | none yet |

## Notes
- IP addresses use the documentation ranges `192.0.2.0/24`, `198.51.100.0/24`
  and `203.0.113.0/24`, so they never point to real hosts.
- Each file also contains normal lines, so the rules can be tested for
  false positives as well as for detection.
- `php-error.log` has multi-line entries (stack traces). The parser must handle them.
