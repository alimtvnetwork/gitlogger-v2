-- Git Logs root schema, migration 0001.
-- Applied to wp-content/uploads/git-logs/db/root.sqlite by MigrationRunner.

CREATE TABLE IF NOT EXISTS schema_migrations (
    version       TEXT PRIMARY KEY,
    applied_utc   TEXT NOT NULL,
    checksum      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS repos (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    slug          TEXT    NOT NULL UNIQUE,             -- e.g. "acme/web"
    display_name  TEXT    NOT NULL,
    remote_url    TEXT,
    default_branch TEXT   NOT NULL DEFAULT 'main',
    created_utc   TEXT    NOT NULL,
    archived      INTEGER NOT NULL DEFAULT 0 CHECK (archived IN (0,1))
);
CREATE INDEX IF NOT EXISTS idx_repos_archived ON repos(archived);

CREATE TABLE IF NOT EXISTS branches (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_id       INTEGER NOT NULL REFERENCES repos(id) ON DELETE CASCADE,
    name          TEXT    NOT NULL,
    head_sha      TEXT,
    last_run_utc  TEXT,
    UNIQUE (repo_id, name)
);
CREATE INDEX IF NOT EXISTS idx_branches_repo ON branches(repo_id);

CREATE TABLE IF NOT EXISTS runs (
    id              TEXT    PRIMARY KEY,                 -- UUIDv4
    repo_id         INTEGER NOT NULL REFERENCES repos(id) ON DELETE CASCADE,
    branch          TEXT    NOT NULL,
    sha             TEXT    NOT NULL,                    -- 40 hex
    ci_provider     TEXT    NOT NULL,                    -- 'github','gitlab','bitbucket','local',...
    ci_run_url      TEXT,
    triggered_by    TEXT,                                -- WP user_login or 'system'
    status          TEXT    NOT NULL CHECK (status IN ('queued','running','succeeded','failed','cancelled','timed_out')),
    exit_code       INTEGER,
    started_utc     TEXT    NOT NULL,
    finished_utc    TEXT,
    duration_ms     INTEGER,
    event_count     INTEGER NOT NULL DEFAULT 0,
    error_count     INTEGER NOT NULL DEFAULT 0,
    warn_count      INTEGER NOT NULL DEFAULT 0,
    metadata_json   TEXT
);
CREATE INDEX IF NOT EXISTS idx_runs_repo_started ON runs(repo_id, started_utc DESC);
CREATE INDEX IF NOT EXISTS idx_runs_sha          ON runs(sha);
CREATE INDEX IF NOT EXISTS idx_runs_status       ON runs(status);

-- Maps a sha → list of run ids that produced events for that sha.
-- Used to find the per-SHA SQLite file containing event data.
CREATE TABLE IF NOT EXISTS sha_index (
    sha           TEXT    NOT NULL,                      -- 40 hex
    run_id        TEXT    NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
    repo_id       INTEGER NOT NULL REFERENCES repos(id) ON DELETE CASCADE,
    created_utc   TEXT    NOT NULL,
    PRIMARY KEY (sha, run_id)
);
CREATE INDEX IF NOT EXISTS idx_sha_index_run ON sha_index(run_id);

CREATE TABLE IF NOT EXISTS audit (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    ts_utc        TEXT    NOT NULL,
    actor_user_id INTEGER,                               -- NULL for system
    actor_login   TEXT,
    auth_lane     TEXT    NOT NULL CHECK (auth_lane IN ('wp_session','ed25519','system')),
    action        TEXT    NOT NULL,                      -- e.g. 'run.create','run.finalize','admin.gc'
    target_type   TEXT,                                  -- 'run','repo','key',...
    target_id     TEXT,
    request_ip    TEXT,
    request_id    TEXT,
    result        TEXT    NOT NULL CHECK (result IN ('ok','denied','error')),
    detail_json   TEXT
);
CREATE INDEX IF NOT EXISTS idx_audit_ts     ON audit(ts_utc DESC);
CREATE INDEX IF NOT EXISTS idx_audit_actor  ON audit(actor_user_id, ts_utc DESC);
CREATE INDEX IF NOT EXISTS idx_audit_action ON audit(action, ts_utc DESC);
