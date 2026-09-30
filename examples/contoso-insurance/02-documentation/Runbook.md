# Operational Runbook — PolicyHub

> Output of [02-documentation-playbook.md](../../../02-documentation-playbook.md) — operational procedures for the current system.

---

## Start / Stop Commands

| Component | Start | Stop | User |
|---|---|---|---|
| Agent Portal | Managed by IIS — `iisreset` or App Pool recycle via IIS Manager | `appcmd stop apppool /apppool.name:"PolicyHubAppPool"` | `CONTOSO\svc-policyhub` |
| Customer Portal | Same IIS App Pool as Agent Portal | Same as above | `CONTOSO\svc-policyhub` |
| WCF Services | Same IIS App Pool | Same as above | `CONTOSO\svc-policyhub` |
| Renewal Service | `sc start ContosoRenewalService` | `sc stop ContosoRenewalService` | `CONTOSO\svc-batch` |
| Bordereaux Service | `sc start ContosoBordereaux` | `sc stop ContosoBordereaux` | `CONTOSO\svc-batch` |
| Claims Import | `sc start ContosoClaimsImport` | `sc stop ContosoClaimsImport` | `CONTOSO\svc-batch` |

**⚠️ Critical**: All web components share one App Pool. Recycling it causes ~30 second downtime for all portals and services simultaneously.

---

## Configuration Files

| File | Location | Key Parameters |
|---|---|---|
| `web.config` (Agent) | `D:\Apps\PolicyHub\AgentPortal\web.config` | DB connection, session timeout, auth settings |
| `web.config` (Customer) | `D:\Apps\PolicyHub\CustomerPortal\web.config` | DB connection, WorldPay keys, reCAPTCHA keys |
| `app.config` (Renewal) | `D:\Services\RenewalService\app.config` | DB connection, renewal lead days, batch size |
| `log4net.config` | Each component root folder | Log levels, file paths, rolling policy |

**Sensitive values**: WorldPay merchant credentials and BACS signing keys are stored in `web.config` `appSettings` as encrypted sections (DPAPI machine-level). **Do not copy config files between servers** — encryption is machine-bound.

---

## Database Connection

| Property | Value |
|---|---|
| Server | `SQLPROD01\POLICYHUB` |
| Database | `PolicyHubProd` |
| Auth | Windows Integrated (`CONTOSO\svc-policyhub`) |
| Backup | Full daily 02:00, differential every 4 hours, log every 15 mins |
| Size | ~45 GB data, ~12 GB log |
| RPO | 15 minutes (log backup frequency) |
| RTO | ~2 hours (restore + verify) |

---

## Batch Jobs & Scheduled Tasks

| Job | Schedule | Duration | Impact of Failure |
|---|---|---|---|
| Renewal Service | Daily 01:00 | ~8 mins | Customers don't receive renewal invitations — regulatory risk |
| Claims Import | Hourly :15 | ~2 mins | Claims data delayed — operational impact |
| Bordereaux Extract | 1st of month 06:00 | ~20 mins | Reinsurance reporting delayed — contractual SLA |
| SQL: Archive Old Quotes | Daily 03:00 | ~5 mins | Quote table grows — performance degradation |
| SQL: Update Statistics | Weekly Sun 04:00 | ~15 mins | Query plan degradation |
| SQL: Rebuild Indexes | Monthly 1st Sun 05:00 | ~45 mins | Fragmentation — slow queries |
| SQL: Purge Audit Log | Quarterly | ~10 mins | Database size growth |

---

## Known Issues & Workarounds

| Issue | Symptom | Workaround |
|---|---|---|
| Document Service memory leak | IIS worker process grows to >2 GB after ~500 documents | App Pool recycle scheduled daily at 05:00 |
| Rating Engine cache stale | Factor table changes not reflected until cache expires | Manually recycle App Pool after factor table updates |
| Renewal Service silent failure | Service stops processing but Windows reports "Running" | Check `D:\Logs\RenewalService\` — restart if last log entry >2 hours old |
| Customer Portal slow under load | Response times >5s during Jan/Jun renewal peaks | No current workaround — root cause is synchronous WCF calls to Rating Engine |
| SSRS Report timeout | Bordereaux report times out for >50K policies | Run with date filter to split into smaller ranges |

---

## Monitoring & Alerting

| What | Tool | Alert Threshold |
|---|---|---|
| IIS App Pool state | SCOM | App Pool stopped → email to ops team |
| Windows Service state | SCOM | Service stopped → email to ops team |
| Disk space (D: drive) | SCOM | <10 GB → warning, <5 GB → critical |
| SQL Server | SCOM + DBA manual checks | Blocking queries >30s, deadlocks |
| Application errors | **None** — log4net writes to file only | **⚠️ Gap**: No centralised error alerting |
| Performance metrics | **None** | **⚠️ Gap**: No APM or response time monitoring |

**Observation**: There is no centralised logging or APM. Errors are only discovered when users report them or ops manually checks log files.
