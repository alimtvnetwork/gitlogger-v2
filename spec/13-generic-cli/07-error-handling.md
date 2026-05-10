# Error Handling

> **Related specs:**
> - [15-constants-reference.md](15-constants-reference.md) — error message constants (`Err*` naming)
> - [16-verbose-logging.md](16-verbose-logging.md) — verbose debug output for error diagnosis
> - [18-batch-execution.md](18-batch-execution.md) — continue-on-failure pattern for batch operations

## Exit Codes

> **Authoritative contract:** §97 **AC-10** (five-value enum) + **AC-17** (batch partial) + **AC-21** (§97-WINS supersession rule). Implementations MUST define a typed `ExitCode` enum and use it at every call site — bare integer literals other than `os.Exit(0)` are FORBIDDEN. The table below is a quick reference; the §97 ACs are normative.

| Code | Constant         | Meaning                                                                              |
|-----:|------------------|--------------------------------------------------------------------------------------|
| `0`  | `ExitOK`         | Success                                                                              |
| `1`  | `ExitError`      | Generic runtime error (operation failed but invocation was valid)                    |
| `2`  | `ExitMisuse`     | Misuse: unknown command, invalid flags, missing required args                        |
| `3`  | `ExitConfig`     | Configuration error (config file malformed or unreadable)                            |
| `4`  | `ExitBatchPartial` | Batch partial failure (some items succeeded, some failed — `exec` only, AC-17)     |

Codes 5–127 / 128+ / negative are SPEC VIOLATIONS — a top-level normaliser MUST clamp to `ExitError` and log the violation. Exit codes propagated from spawned child processes MUST be re-mapped onto this five-value contract before the parent process exits (e.g. a child's `127` becomes `ExitError` with an actionable stderr message, not a bare `127` leak).

## Error Message Rules

| Rule | Detail |
|------|--------|
| All error format strings in `constants` | `ErrSourceRequired`, `ErrConfigLoad`, etc. |
| Errors print to stderr | Never stdout |
| Exit immediately after error | Don't continue with bad state |
| Messages are actionable | Tell the user what to do, not just what failed |

### Example

```go
// constants/constants_messages.go
const (
    ErrSourceRequired = "Error: source file is required\nUsage: toolname clone <source>"
    ErrConfigLoad     = "Error: could not load config from %s"
    ErrRepoNotFound   = "Error: no repo matches slug '%s'. Run 'toolname scan' first."
)
```

```go
// cmd/clone.go
if source == "" {
    fmt.Fprintln(os.Stderr, constants.ErrSourceRequired)
    os.Exit(int(exit.ExitMisuse)) // AC-10 / AC-21: missing required arg → ExitMisuse (2), NOT 1
}
```

## Batch Operations

For commands that process N items (e.g., pull all repos):

1. **Log per-item failures** but continue processing.
2. **Track success/failure counts**.
3. **Print summary at the end**.
4. **Exit per §97 AC-17:** `ExitOK` (0) if all succeeded, `ExitBatchPartial` (4) if some succeeded and some failed, `ExitError` (1) if **all** items failed. The bare `os.Exit(1)` in the example below is stale prose — refresh implementations to the three-way conditional.

```go
var failed int
for _, repo := range repos {
    err := pull(repo)
    if err != nil {
        fmt.Fprintf(os.Stderr, "[%s] %v\n", repo.Name, err)
        failed++
        continue
    }
    fmt.Printf("[%s] ✓\n", repo.Name)
}

fmt.Printf("\n%d succeeded, %d failed\n", len(repos)-failed, failed)
// AC-17 three-way contract:
switch {
case failed == 0:
    os.Exit(int(exit.ExitOK))
case failed == len(repos):
    os.Exit(int(exit.ExitError)) // all failed
default:
    os.Exit(int(exit.ExitBatchPartial)) // partial — exit 4, NOT 1
}
```

## Error Handling in Functions

- Always check errors immediately after the call.
- Return errors up the stack; let the caller decide.
- In `cmd` package handlers, print the error and exit with the appropriate `ExitCode` enum value (per §97 AC-10 + AC-21) — never a bare integer literal.
- Never use `panic` for expected error conditions.

```go
// ✅ Correct — return error up
func loadFile(path string) ([]byte, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("reading %s: %w", path, err)
    }

    return data, nil
}

// ✅ Correct — handler prints and exits with typed enum
func runImport(args []string) {
    data, err := loadFile(args[0])
    if err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(int(exit.ExitError)) // §97 AC-21: typed enum mandatory
    }
    // process data
}
```

## Contributors

- [**Md. Alim Ul Karim**](https://www.linkedin.com/in/alimkarim) — Creator & Lead Architect. System architect with 20+ years of professional software engineering experience across enterprise, fintech, and distributed systems. Recognized as one of the top software architects globally. Alim's architectural philosophy — consistency over cleverness, convention over configuration — is the driving force behind every design decision in this framework.
  - [Google Profile](https://www.google.com/search?q=Alim+Ul+Karim)
- [Riseup Asia LLC (Top Leading Software Company in WY)](https://riseup-asia.com) (2026)
  - [Facebook](https://www.facebook.com/riseupasia.talent/)
  - [LinkedIn](https://www.linkedin.com/company/105304484/)
  - [YouTube](https://www.youtube.com/@riseup-asia)
