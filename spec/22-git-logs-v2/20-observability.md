# Observability (v2)

**Version:** 2.3.0  
**Updated:** 2026-04-25

What the plugin exposes for monitoring, dashboards, and alerting. v2 keeps it simple — no external dependencies — but standardizes the surface so v3 can plug in StatsD/Prometheus without API churn.

---

## Surfaces

### 1. WP Site Health card

Registered via `site_status_tests` filter. Renders under **Tools → Site Health → Status**.

| Test | Pass criterion | Fail message |
|------|----------------|--------------|
| `git-logs-db-writable` | SQLite file exists, writable, journal mode WAL. | "Plugin DB unavailable: <reason>" — links to logs. |
| `git-logs-migration-current` | `MigrationState` row matches `ConfigKv.PluginVersion`. | "Migration pending. Re-activate plugin." |
| `git-logs-recent-activity` | At least one `AuditTrail` row in last 7 days. | Informational warning only. |

### 2. Metrics endpoint (text/plain)

```
GET /wp-json/git-logs/v2/metrics
Auth: WP App Password + Permission `HistoryView`
```

Returns a Prometheus exposition-format body. Counters reset on plugin reload.

```
# HELP gitlogs_push_total Total push attempts grouped by outcome
# TYPE gitlogs_push_total counter
gitlogs_push_total{outcome="accepted"} 14210
gitlogs_push_total{outcome="rejected",code="GL-AUTH-TEMPTOKEN-INVALID"} 3
gitlogs_push_total{outcome="rejected",code="GL-RATE-LIMIT-EXCEEDED"} 12

# HELP gitlogs_log_lines_total Total log lines persisted
# TYPE gitlogs_log_lines_total counter
gitlogs_log_lines_total{kind="log"} 1402901
gitlogs_log_lines_total{kind="error"} 8442

# HELP gitlogs_pipeline_active Pipelines with HasError=1
# TYPE gitlogs_pipeline_active gauge
gitlogs_pipeline_active 4

# HELP gitlogs_ingest_latency_seconds Wall-clock per /append-log call
# TYPE gitlogs_ingest_latency_seconds summary
gitlogs_ingest_latency_seconds{quantile="0.5"} 0.014
gitlogs_ingest_latency_seconds{quantile="0.95"} 0.082
gitlogs_ingest_latency_seconds{quantile="0.99"} 0.180
gitlogs_ingest_latency_seconds_count 14210

# HELP gitlogs_db_size_bytes SQLite file size
# TYPE gitlogs_db_size_bytes gauge
gitlogs_db_size_bytes 41943040

# HELP gitlogs_plugin_info Static info
# TYPE gitlogs_plugin_info gauge
gitlogs_plugin_info{version="2.3.0",php="8.2.10",wp="6.5.2"} 1
```

### 3. Internal counters (storage)

Counters live in WP transients keyed `gitlogs_metric_*` so they survive PHP request boundaries without a DB write per increment. A scheduled `wp_cron` job (every 5 min) snapshots them to `ConfigKv` so a process restart loses at most 5 minutes of counter granularity.

| Counter | Increment site |
|---------|---------------|
| `gitlogs_metric_push_accepted` | After successful `/append-log` insert |
| `gitlogs_metric_push_rejected_<GL-CODE>` | One per reject code in `15-error-codes.md` |
| `gitlogs_metric_log_lines_log` | + `count(Logs)` per accepted push |
| `gitlogs_metric_log_lines_error` | + `count(ErrorLogs)` per accepted push |
| `gitlogs_metric_ingest_latency_us` | Histogram-style: bucket array of microseconds |

### 4. Logs (the plugin's own diagnostic logs)

Distinct from CI/CD log entries. Written by `inc/Logging/Logger.php` to:

- **PHP error_log** for `Warn` and above.
- **`AuditTrail` table** for security-relevant outcomes (auth/authz, migration runs).
- **Stdout** when `WP_DEBUG_LOG=stdout` — useful in containerized hosts.

`LogLevelMin` in `ConfigKv` gates emission. Default `Info`. Setting to `Trace` is intended for short-lived debugging only.

---

## Recommended dashboards (Grafana sketch)

1. **Push Health** — `rate(gitlogs_push_total[5m])` split by `outcome`; alert if `rejected/accepted > 0.05` for 10 min.
2. **Rate-limit pressure** — `rate(gitlogs_push_total{code="GL-RATE-LIMIT-EXCEEDED"}[5m])`; alert if non-zero for 15 min.
3. **Active error pipelines** — `gitlogs_pipeline_active`; alert if > 0 sustained for 30 min.
4. **Ingest p95** — `gitlogs_ingest_latency_seconds{quantile="0.95"}`; alert if > 250 ms for 10 min.
5. **DB growth** — `gitlogs_db_size_bytes`; warn at 500 MiB, page at 1 GiB (operator should run retention).

---

## Retention (out of scope but referenced)

v2 ships **no automatic retention**. Operators run `wp git-logs prune --older-than=30d` (a planned WP-CLI command in v2.4) to control DB size. This doc only commits to surfacing `gitlogs_db_size_bytes` so ops can decide.

---

## What v2 explicitly does NOT ship

- No StatsD / OTLP push.
- No tracing (no spans, no OpenTelemetry).
- No anomaly detection.
- No log shipping to external sinks.

All of the above are deferred and may live in a future `gitlogs-observability` companion plugin.
