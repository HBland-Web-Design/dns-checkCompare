# CLAUDE.md — dns-checkCompare

This file provides context for AI assistants working in this repository.

## Project Overview

**dns-checkCompare** is a Python CLI tool that monitors DNS records for unexpected changes. It works by:
1. Establishing a "known good" baseline cache of DNS query results
2. Running on a schedule (via cron) to re-query those same records
3. Comparing current results against the cache and emailing an HTML report when discrepancies are found

**Author:** Harry Bland <info@hbland.co.uk>
**Python version:** 3.10.13
**Repository:** https://github.com/HBland-Web-Design/dns-checkCompare

---

## Repository Structure

```
dns-checkCompare/
├── Dockerfile                  # Python 3.10.13 container with cron support
├── docker-compose.yml          # Production deployment config
├── compose-dev.yml             # Development deployment config
├── cronjob                     # Cron schedule (runs daily at 07:00)
├── README.md                   # User-facing setup documentation
└── source/                     # All application source code
    ├── main.py                 # Entry point — orchestrates the full check cycle
    ├── cache.py                # Cache read/write/compare logic
    ├── report.py               # HTML report generation and email dispatch
    ├── mailer.py               # Routes email to the correct mail provider
    ├── resolve_query.py        # DNS query execution via pydig
    ├── alert.py                # Empty stub — not yet implemented
    ├── checks                  # Configuration: list of records to monitor
    ├── requirements.txt        # Python dependencies
    ├── Templates/
    │   ├── globalReport.html   # HTML template for the all-domains report
    │   └── domainReport.html   # HTML template for per-domain reports
    ├── Reports/                # Output directory for HTML report files (local runs only)
    │   └── .gitkeep
    └── mailProviders/
        ├── __init__.py         # Empty package init
        ├── smtp.py             # SMTP_SSL mail sending implementation
        └── microsoft.py        # Microsoft Graph stub — NOT yet implemented
```

---

## Running the Application

### Prerequisites

Install Python dependencies from inside the `source/` directory:

```bash
pip install -r source/requirements.txt
```

### Command-line usage

The script must be run from the `source/` directory because it resolves `checks` and `Templates/` relative to the working directory using `Path(...).resolve()`.

```bash
cd source/

# Establish a new baseline cache (first-time setup or after intentional DNS changes):
python main.py --reset

# Run a check against the existing cache:
python main.py

# Use a custom .env file:
python main.py -e /path/to/custom.env
```

### Arguments

| Argument | Description |
|---|---|
| `-r` / `--reset` | Resets the cache to the current DNS state (new "known good") |
| `-e` / `--environment` | Path to a custom `.env` file (overrides default `.env` lookup) |

---

## Configuration

### checks file (`source/checks`)

Defines which DNS records to monitor. One record per line, semicolon-delimited. Lines starting with `#` are comments.

```
#DOMAIN;RECORDTYPE
google.com;A
mail.example.com;MX
```

Supported record types are anything `pydig` supports (A, AAAA, MX, TXT, CNAME, NS, etc.).

### Environment Variables

The application loads config from a `.env` file (local) or from OS environment variables (Docker). `.env` is gitignored and must be created manually.

| Variable | Description | Default |
|---|---|---|
| `CACHE_LOCATION` | Path to the cache file | `/opt/hbland/checkcompare/cachefile` |
| `CHECKS_LOCATION` | Path to the checks file | `/opt/hbland/checkcompare/checks` |
| `RECIPIENT` | Email recipient address(es), comma-separated | — |
| `SENDER` | Email sender address | — |
| `MAILER` | Mail provider: `SMTP` or `MSGRAPH` | — |
| `SERVER` | SMTP server hostname | — |
| `PORT` | SMTP server port | — |
| `AUTHENTICATION` | Auth method — currently only `SSL` is supported | — |
| `USERNAME` | SMTP username | — |
| `PASSWORD` | SMTP password | — |
| `TENNANT_ID` | Azure tenant ID (Microsoft Graph) | — |
| `CLIENT_ID` | Azure client ID (Microsoft Graph) | — |
| `CLIENT_SECRET` | Azure client secret (Microsoft Graph) | — |

**Note:** In Docker mode (detected by `HB_RUNTIME=DOCKER`), variables are read directly from the OS environment rather than a `.env` file.

---

## Docker Deployment

### Production

```bash
# Create .env file with required environment variables first
docker-compose up -d
```

The production compose mounts `$PWD/checks` into the container so the checks list can be updated without rebuilding the image.

### Development

```bash
docker-compose -f compose-dev.yml up
```

### Container startup sequence

1. Runs `python main.py --reset` to establish an initial cache baseline
2. Starts cron in the background
3. Tails `/var/log/cron.log` as the foreground process

The cron job fires daily at 07:00 and appends output to `/var/log/cron.log`.

---

## Code Architecture & Data Flow

### Full check cycle (normal run)

```
main.py
  │
  ├─ loadENV() / dockerENV()     → loads config into `env` dict
  ├─ getChecks()                  → parses `checks` file → list of {record, recordType}
  │
  ├─ resolve_query.resolveQuery() → pydig DNS query per check
  │     └─ returns {domain, record, recordType, recordValue}
  │
  ├─ cache.load_cache()           → reads JSON cache file
  ├─ cache.cache_compare()        → compares current vs cached → list of {domain, record,
  │                                  recordType, status, msg?}
  │
  ├─ report.fill_global_template() → builds global HTML report, emails it
  └─ report.fill_domain_template() → builds per-domain HTML reports, emails each one
```

### Reset cycle (`--reset` flag)

```
main.py
  │
  ├─ loadENV() / dockerENV()
  ├─ getChecks()
  ├─ resolve_query.resolveQuery()  (for each check)
  └─ cache.reset_cache()           → truncates cache file, writes current results as JSON
```

### Cache format

The cache file is a JSON array written by `reset_cache()`. Each element is a compact JSON object:

```json
[
{"domain":"google.com","record":"google.com","recordType":"A","recordValue":["142.250.80.46"]},
...
]
```

`save_cache()` writes newline-delimited JSON (not a valid JSON array) — this is a known inconsistency. `reset_cache()` writes a proper JSON array, which is what `load_cache()` reads.

---

## Module Reference

### `main.py`

Entry point. Contains:
- `getChecks()` — reads and parses the `checks` config file
- `groupByDomain(checkResults)` — groups a flat results list by root domain
- `loadENV(envPath)` — parses a `.env` file into a config dict
- `dockerENV()` — reads the same config from OS environment variables
- `getArgs()` — sets up argparse
- `main()` — orchestrates the full run

### `cache.py`

- `load_cache(cachePath)` — reads the JSON cache file; returns `"FileNotFound"` string on missing file
- `save_cache(cache, cachePath)` — writes newline-delimited JSON (used inconsistently; prefer `reset_cache`)
- `reset_cache(cache, cachePath)` — truncates and rewrites the cache as a valid JSON array
- `cache_compare(current_check, cacheLoaded)` — O(n²) comparison; matches on `record` + `recordType`; sets `status` to `"Pass"` or `"Fail"`; attaches `msg` dict with `ExpectedValue`/`CurrentValue` on failures
- `get_response()` / `generate_response_for_key()` — dead code stubs, not called anywhere

### `resolve_query.py`

- `getRootDomain(record)` — uses `tldextract` to extract the registrable domain (e.g. `sub.example.com` → `example.com`)
- `resolveQuery(record, recordType)` — queries DNS via `pydig`; on empty response stores `"No Value for Record"` as the value

### `report.py`

- `fill_global_template(env, results)` — generates one global HTML email across all domains
- `fill_domain_template(env, domains)` — generates one HTML email per domain
- In non-Docker mode, also writes HTML files to `source/Reports/`
- Red title + red table cell on any failure; green on pass

### `mailer.py`

- `main(env, subject, body)` — builds the email envelope and dispatches via the configured `MAILER`
- Currently only `SMTP` is fully wired; `MSGRAPH` branch is a `pass` stub

### `mailProviders/smtp.py`

- `main(server, envelope, content)` — builds a `MIMEMultipart` message and calls `mailSSL()`
- `mailSSL(server, msg)` — sends via `smtplib.SMTP_SSL` with certifi CA bundle
- Multiple recipients are supported (comma-separated `RECIPIENT` value)

### `mailProviders/microsoft.py`

Incomplete stub. Microsoft Graph mail sending is not yet implemented.

---

## Known Issues & Incomplete Areas

| Area | Issue |
|---|---|
| `alert.py` | Empty file — no alerting logic implemented |
| `mailProviders/microsoft.py` | Skeleton only — `MSGRAPH` mailer path is a no-op |
| `mailer.py` `sendMSGRAPH()` | Empty function body |
| `cache.py` `get_response()` / `generate_response_for_key()` | Dead code, never called |
| `cache.py` `save_cache()` vs `reset_cache()` | `save_cache` writes newline-delimited JSON (not a valid array); `load_cache` expects a valid JSON array — only `reset_cache` produces a compatible file |
| `main.py` line 213 | `elif args.reset == False: print("true")` — this branch is unreachable given how argparse `store_true` works; dead code |
| `report.py` | `fill_global_template` accesses `record['msg']` unconditionally on Fail rows but `msg` only exists on failures — a Pass record accessed this way would raise a `KeyError` (currently safe only because Pass rows use a different f-string branch) |
| No tests | No test framework or test files exist |
| No CI/CD | No `.github/workflows/` or any CI configuration |
| Working directory dependency | All `Path(...).resolve()` calls expect the CWD to be `source/`; running from the repo root will fail |

---

## Development Conventions

- **No test suite.** There are no existing tests. When adding new functionality, consider whether it can be validated locally by running a `--reset` followed by a normal run.
- **Working directory is `source/`.** All file path resolution is relative to the directory the script is executed from. Maintain this convention — don't change path logic without updating Docker `WORKDIR` and the cron command too.
- **Environment loading is dual-path.** Docker uses `dockerENV()` (OS env vars); local uses `loadENV()` (`.env` file). Any new config variables must be added to both functions.
- **Cache file is JSON array.** Always use `reset_cache()` to write the cache, not `save_cache()`. If `save_cache()` is ever used it will corrupt the file.
- **HTML reports use Python `.format()` placeholders** (`{title}`, `{rows}`, `{time}`, `{domain}`). Do not use f-strings in templates or add new `{...}` placeholders without updating the corresponding `fill_*_template()` call.
- **Commit style:** Short imperative messages, no ticket prefixes (see git log for examples: `"fix run from location"`, `"Bug Fix"`, `"Adding Compose Dev File"`).
- **No linter or formatter is configured.** Standard Python style (PEP 8) is reasonable but not enforced.

---

## Dependencies

From `source/requirements.txt`:

| Package | Purpose |
|---|---|
| `pydig` | DNS query execution |
| `tldextract` | Extracts registrable domain from a full hostname |
| `certifi` | CA certificate bundle for SSL connections |

Standard library modules also used: `json`, `os`, `argparse`, `pathlib`, `datetime`, `smtplib`, `ssl`, `email.mime`.
