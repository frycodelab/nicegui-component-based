<img align="left" src="/FRYCODE_LAB.png">

We are focused on developing custom software solutions for different purposes.
This template is the result of the learning curve we had developing many applications.
We want to share it with the community - to help NiceGUI becomming bigger. A big thank you to @zauberzeug/niceGUI for this amazing framework.
<br clear="left"/>

# NiceStack powered by NiceGUI

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![NiceGUI](https://img.shields.io/badge/NiceGUI-3.9-green.svg)
![uv](https://img.shields.io/badge/uv-package%20manager-orange.svg)

A full-stack, batteries-included starter template for building web applications with [NiceGUI](https://nicegui.io/) in pure Python.

NiceStack exists so you don't wire the same plumbing together on every new project. It ships the parts almost every production app needs — already built, tested and connected — so you can delete the demo, keep the foundation, and start building your own app.

<p align="center">
  <img src="/Demo.gif" alt="NiceStack demo" align="center">
</p>

## Why NiceStack

Most stacks force a split brain: a JavaScript framework on the front end, a separate Python service on the back end, and a pile of glue code, build tooling and duplicated models in between. NiceStack keeps the whole stack in one Python codebase, borrowing the ideas that make those ecosystems pleasant to work in while dropping the boilerplate that makes them slow to start:

- **Reusable components.** Self-contained UI building blocks in `components/` (dialogs, dropzone, notifications, password form, …) — compose them across pages instead of copy-pasting markup.
- **Layered like an MVC app.** `models/` holds framework-free domain data, `services/` holds business logic, `views/` render pages, `core/` provides infrastructure. Views stay thin and delegate every rule to the service layer.
- **Pure Python, end to end.** No JS build step, no hand-written REST layer, no client/server model duplication. One language, one mental model, one place to look.

## Features

| Area | What you get |
|---|---|
| **Auth & sessions** | Session-based auth with idle (30 min) and absolute (12 h) timeouts, forced password change on first login |
| **Access control** | Role-based access (`admin` / `user`), bootstrap admin account protected from deletion/demotion |
| **Audit log** | Persistent activity trail (who did what, when, from which IP) with an admin-only review page |
| **Hardening** | Login rate limiting with account lockout (per IP and per username), PBKDF2-HMAC-SHA256 hashing, hardened response headers |
| **Persistence** | SQLAlchemy 2.0 ORM over SQLite in WAL mode, additive schema migrations |
| **i18n** | Live language switching (English / German), no page reload |
| **UI** | Responsive shell with mobile bottom nav, token-based design system with a live component reference page |
| **PWA** | Installable web app: web manifest, service worker and offline app shell |
| **Ops** | Rolling daily file logging with a runtime-adjustable level, pytest suite via the NiceGUI testing plugin |

Authentication, hashing and rate limiting are built on the Python standard library and NiceGUI/Starlette primitives — no external auth service required.

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Quickstart

### Install UV
[https://docs.astral.sh/uv/getting-started/installation/#standalone-installer]

### Start application
```bash
# from the project root
cd app
uv run main.py
```

`uv` resolves dependencies from `pyproject.toml`, creates a virtual environment on first run, and starts the app.

Open [http://localhost:8080](http://localhost:8080) and sign in with the seeded administrator account:

| Username | Password |
|---|---|
| `admin` | `admin` |

You'll be required to set a new password before reaching any other page. The default admin account is created automatically the first time the database is initialized.

## Configuration

App metadata and the listen port live in `config.json`:

```json
{
    "appName": "Production Suite",
    "appVersion": "Beta 1.0",
    "appPort": 8080
}
```

The session-signing secret is resolved by `_get_storage_secret()` in `main.py`:

1. the `STORAGE_SECRET` environment variable, if set;
2. otherwise a strong random secret is generated once and persisted (`0600` permissions) at `data/.storage_secret`, so signed cookies survive restarts.

> **Always set `STORAGE_SECRET` explicitly in production.**

## Using NiceStack as a template

1. Set your app name, version and port in `config.json`.
2. Add a page: create `views/<name>_content.py` with a `content()` function, register a route in the `ui.sub_pages` map in `main.py`, and add a sidebar entry in `header.py`.
3. Add reusable UI in `components/`, domain types in `models/`, business logic in `services/` — keep views thin.
4. Extend the data model in `core/database.py` and its service.
5. Add translations in `services/i18n.py`; strings flow through `t('your.key')`.
6. Remove the demo views you don't need (orders, pallets, packing, print demo, design system, icons) and keep the shell and core.

## Project structure

```
main.py                 Entry point: page routing, layout decorator, run targets
header.py               Application shell: header bar, sidebar, mobile navigation
config.json              App name, version and port

core/
  database.py            SQLAlchemy engine, ORM models, sessions, schema init, seeding
  security.py             Password hashing, rate limiting, auth/session middlewares
  logging_config.py       Rolling file + console logging, runtime log level

models/
  enums.py                Domain enumerations (UserRole)
  user.py                 User data model (plain, dependency-free)
  audit.py                Audit entry model and AuditAction enum (dependency-free)

services/
  user_service.py         User persistence and business rules, password policy
  audit_service.py        Audit trail persistence and queries, audit_record() helper
  i18n.py                  Translation catalog and live language switching
  dashboard_data.py       Sample data for the dashboard view

views/
  *_content.py             One module per page (dashboard, shipping, users, ...)
  login_content.py        Login page and rate-limited login flow
  change_password_content.py  Forced/self-service password change
  audit_content.py        Admin-only audit log review page
  _common.py               Shared view helpers

components/
  dialogs.py, dropzone.py, notifications.py, password_form.py,
  print_component.py, sidebar_hint.py   Reusable UI building blocks

tests/
  conftest.py              Fixtures: NiceGUI testing plugin, isolated temp database
  test_security.py, test_user_service.py, test_audit_service.py, test_ui_smoke.py

assets/                  CSS (design tokens, components), fonts, images, icons, PWA files
certs/                   Self-signed cert.pem / key.pem for local HTTPS
data/                    SQLite database and generated secret (created at runtime)
backup/                  Timestamped database backups (created at runtime)
logs/                    Rolling application logs (created at runtime)
```

## Architecture

### Routing and sub-pages

A single top-level page (`/`) is wrapped by the `with_base_layout` decorator, which applies the theme, global stylesheet and application shell from `header.py`. Inside that shell, `ui.sub_pages` maps client-side routes (`/shipping`, `/orders`, `/users`, …) to their view handlers, so navigation happens without a full page reload. A standalone `/print/{data}` route renders outside the shell for print output.

Most views are rendered through a small `_localized` helper that wraps them in a `ui.refreshable`, so the whole page rebuilds in place when the language changes.

### Layers

| Layer | Responsibility |
|---|---|
| **Views** (`views/`) | One `content()` function per page. Orchestrate layout, delegate all persistence and business logic to services — never talk to the database directly. |
| **Components** (`components/`) | Reusable, self-contained UI building blocks (dialogs, dropzone, toasts, password form, print helper, sidebar hints). Pure presentation. |
| **Models** (`models/`) | Framework-free data structures. `User` is a frozen dataclass, `UserRole` is the RBAC enum — no database or security dependencies, so both are trivial to unit-test in isolation. |
| **Services** (`services/`) | Business logic. `UserService` wraps an open database session and implements account rules (creation, credential verification, password policy, role/activation changes). `AuditService` records and queries the activity trail. `i18n` owns the translation catalog and language state. |
| **Core** (`core/`) | Infrastructure: database session/context manager, security layer (hashing, rate limiting, middlewares), logging configuration. |

## Security

Security is centralized in `core/security.py` and applied globally through two Starlette middlewares. Middlewares run in reverse registration order, so `SecurityHeadersMiddleware` wraps the outside of every response while `AuthMiddleware` runs closest to the application:

```python
app.add_middleware(security.AuthMiddleware)            # inner: runs first on the way in
app.add_middleware(security.SecurityHeadersMiddleware) # outer: runs last, decorates the response
```

### Request lifecycle (`AuthMiddleware`)

Every request is checked, in order:

1. **Internal fast-path** — NiceGUI's own WebSocket/SSE traffic (`/_nicegui`, `/_starlette`) passes through untouched, so realtime updates never hit session storage.
2. **Public allow-list** — `/login`, `/health`, `favicon.ico`, `manifest.json`, `sw.js` and the static asset prefixes (`/assets/css`, `/assets/images`, `/assets/icons`, `/assets/fonts`) are reachable without a session.
3. **Session timeouts** — a 30-minute sliding idle timeout and a 12-hour absolute cap since login are enforced on every request. On expiry the session is cleared and the request redirected to `/login?reason=timeout|expired` (or `401` under `/api/*`).
4. **Forced password change** — a session with `must_change_password` set is confined to `/change-password` (`403` under `/api/*`).
5. **Authentication gate** — any remaining unauthenticated request to a protected route redirects to `/login?redirect_to=<path>` (or `401` under `/api/*`).

Browser navigation gets redirects; requests under `/api/*` get JSON errors — the same middleware serves both page and programmatic clients. Adding a route to the public set is a one-line change to `unrestricted_page_routes` / `_PUBLIC_ASSET_PREFIXES`.

### Sessions

Session state lives in NiceGUI's `app.storage.user`, backed by a cookie signed with `storage_secret`. On login the store holds the user id, username, role, language and the `login_at` / `last_activity` timestamps that drive the timeouts. `logout()` clears the store and redirects to `/login`. `current_user()` re-reads the user from the database on every call, so a role or activation change takes effect on the user's next request without re-login. The login handler rejects open-redirect attempts by requiring `redirect_to` to be a same-site path.

### Role-based access control

`UserRole` (`models/enums.py`) defines `admin` and `user`. `User.is_admin` is the single check that gates admin-only areas: the Users and App Settings entries are hidden from the sidebar and burger menu for non-admins, and admin views enforce the same check server-side through `UserService`. The bootstrap `admin` account can never be deleted, deactivated or demoted, and the service refuses to remove or demote the last remaining admin.

### Password hashing

Passwords are stored as `pbkdf2_sha256$iterations$salt$hash` using PBKDF2-HMAC-SHA256 with 260,000 iterations and a per-password 16-byte salt — standard library only, no external crypto dependency. Verification uses `hmac.compare_digest` for constant-time comparison. A login attempt for an unknown username still runs a dummy hash comparison, so response timing can't be used to enumerate valid accounts.

### Password policy and forced change

New and reset accounts start with a default password and `must_change_password` set; the middleware confines them to `/change-password`. The policy — length 10–64, at least one upper, lower, digit and special character — is defined once in `services/user_service.py` and shared by both server-side validation and the live requirement checklist in the `PasswordChangeForm` component, so the UI and the server can never disagree.

### Login rate limiting

An in-memory sliding-window limiter tracks attempts per key over a 15-minute window; after 5 failed attempts the key is locked out for 30 minutes. The login flow rate-limits on two keys simultaneously — client IP and the targeted username (lowercased) — so neither a single source nor a single account can be brute-forced. The client IP is read from `X-Forwarded-For` when present (put a trusted proxy in front in production). Stale entries are pruned periodically to bound memory use.

> **Note:** the limiter is process-local. For multi-worker or multi-instance deployments, back it with a shared store such as Redis.

### Security headers

`SecurityHeadersMiddleware` sets the following on every response via `setdefault`, so an explicitly set header is never overwritten:

| Header | Value |
|---|---|
| `X-Content-Type-Options` | `nosniff` |
| `X-Frame-Options` | `DENY` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `X-XSS-Protection` | `0` (disables the legacy, exploitable auditor) |
| `Permissions-Policy` | `camera=(self), microphone=(), geolocation=()` |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` |

## Audit log

As an app grows past a single trusted user, "who changed this?" and "who signed in?" stop being answerable from memory. Application logs help, but they are optimized for debugging, rotate away, and aren't something a non-technical administrator can read. The audit log is the accountability layer on top: a durable, human-readable record of the security- and data-relevant actions taken through the app.

**Why it's needed**

- **Accountability** — every sensitive action is attributed to a specific user, so nothing happens anonymously.
- **Incident response** — after a compromise or mistake you can reconstruct exactly what happened, when, and from which IP.
- **Compliance** — many frameworks (ISO 27001, SOC 2, GDPR accountability) expect an access/activity trail for accounts and personal data.
- **Deterrence** — visible logging discourages misuse by insiders who know their actions are recorded.

**What gets recorded**

Each entry stores a UTC timestamp, the acting user, the action, an optional target/detail, and the client IP. The following actions are captured out of the box:

| Category | Actions |
|---|---|
| Authentication | successful sign-in, failed sign-in (including attempts on disabled accounts), sign-out |
| Account security | password change (forced and self-service), admin password reset |
| User management | user created, deleted, role changed, activated, deactivated |
| Profile | profile updated, language changed |

**How it works**

The trail is persisted in a dedicated `audit_log` table (`core/database.py`) and served through `services/audit_service.py`, mirroring the service pattern used for users. Call sites record an event with a single line via the module-level `audit_record(...)` helper, which resolves the acting user from the session and is written so that a logging failure can never break the action it is recording. Administrators review the trail on the **Audit Log** page (`/audit`), which lists recent activity with per-action filtering and a clear-log action; the page and route are admin-only.

Adding a new audited action is a two-step change: add a value to `AuditAction` in `models/audit.py`, then call `audit_record(AuditAction.YOUR_ACTION, target=..., details=...)` at the relevant call site.

> The audit log records **events**, not full before/after snapshots. For point-in-time recovery of the data itself, use the database backups described below.

**Retention and integrity.** The `audit_log` table grows without bound — unlike the rolling application logs, entries are never rotated or expired automatically. For a long-running or high-traffic deployment, periodically archive and prune it (e.g. export rows older than N days, then delete them). The trail is not tamper-proof: it lives in the same database as the rest of the app, and an administrator can clear it from the Audit Log page, so treat it as an accountability aid rather than forensic evidence. If you need stronger guarantees, ship the entries to an append-only external sink (syslog, a log service, or a write-only table on a separate database).

## Database

Persistence uses the SQLAlchemy 2.0 ORM over a single SQLite file at `data/app.db`. The `users` table is mapped by `UserRecord`; the service layer converts ORM rows to the framework-free `User` dataclass before returning them to views, so no ORM objects leak out of an open session.

`get_session()` yields a SQLAlchemy `Session`, commits on success, rolls back on error, and always closes. Each connection is configured via a connect-event listener with:

- `journal_mode = WAL` — concurrent readers during a write
- `synchronous = NORMAL` — the safe, fast companion to WAL
- `busy_timeout = 5000` — wait on locks instead of failing
- `foreign_keys = ON`

`init_db()` creates the schema with `Base.metadata.create_all`, applies additive column migrations for databases created by earlier versions, and seeds the default admin on an empty database.

> **Migrations:** the built-in migrator only *adds* columns. Breaking changes (dropping or renaming columns, changing types) are out of scope for `create_all` — if your project needs a richer schema history, wire in [Alembic](https://alembic.sqlalchemy.org/) and manage migrations there instead.

> **Scaling beyond SQLite:** SQLite is a great default and handles this template comfortably, but it serializes writes (one writer at a time, even under WAL). For low-concurrency and read-heavy workloads that's fine; once you expect roughly **25+ concurrent active users** or write-heavy, multi-worker deployments, move to a client/server database such as **PostgreSQL**. Because all access goes through the SQLAlchemy ORM and `get_session()`, switching is mostly a matter of changing the engine URL (and the SQLite-specific `PRAGMA` connect listener) in `core/database.py`.

### Backups and admin recovery

`core/database.py` provides two maintenance helpers:

- **`backup_database(label=None)`** writes a consistent snapshot of the database into the `backup/` folder as `app-<timestamp>.db`. It uses SQLite's online backup API, so it is safe to run while the app is live, including under WAL. Returns the backup path.
- **`reset_admin_to_default()`** restores the `admin` account to an active admin with the default password (`admin` / `admin`) and the forced-password-change flag, recreating it if it was deleted. It always takes a safety backup first and returns that backup path.

Both are plain functions, so they can be called from a maintenance script, a shell, or wired to a button on the admin settings page:

```bash
uv run python -c "from core.database import backup_database; print(backup_database())"
uv run python -c "from core.database import reset_admin_to_default; print(reset_admin_to_default())"
```

Backups are local by design and are git-ignored (only `backup/.gitkeep` is tracked).

## Language support

Translations live in `services/i18n.py` as a `key -> {lang: text}` catalog. Every translatable element is bound to a per-client language state, so switching the language updates the whole UI live, without a reload. The choice is persisted to the session and to the account row.

Shipped languages: English (`en`), German (`de`). Missing translations fall back to English, then to the key itself. To add a language, extend `LANGUAGES` and provide the corresponding catalog entries.

## Design system

The look and feel is driven by a single stylesheet, `assets/css/global-css.css`, built around CSS custom properties rather than ad-hoc styles:

- **Tokens** — colors, spacing, radii, typography scale and a fluid base font size, declared once under `:root` (`--primary`, `--danger`, `--radius`, `--text-lg`, …). Restyle the app by editing tokens in one place.
- **Component and utility classes** — semantic classes (`.button`, `.card`, `.badge`, `.alert`, `.chip`, `.data-table`, `.dialog-card`, …) and small utilities (`.text-sm`, `.mt-4`, `.flex`, `.gap-2`) applied through NiceGUI's `.classes(...)`.
- **Quasar overrides** — the underlying Quasar widgets (inputs, tabs, steppers, progress bars, pickers) are normalized to match the tokens.

The stylesheet is served as a static file with an mtime cache-buster, so CSS edits only need a browser refresh, not a server restart. The **Design System** page (`/design-system`) renders every token, component and utility live, next to its class name.

## UI components

| Component | Purpose |
|---|---|
| `notifications.py` | Styled HTML toasts. `notify(message, type=...)` for one-shot toasts (`positive` / `negative` / `warning` / `info`); `notify_ongoing(...)` for a spinner toast with a `dismiss()` handle for long tasks. |
| `dialogs.py` | `confirm_dialog(...)` and `info_dialog(...)` awaitable helpers, styled to the design system. |
| `password_form.py` | `PasswordChangeForm` with a live requirement checklist, shared by the forced change-password page and account settings. |
| `dropzone.py` | Drag-and-drop upload zone wrapping `ui.upload`; drop or click to select, entirely in Python. |
| `print_component.py` | Print-optimized document renderer for the standalone `/print/{data}` route (no shell). |
| `sidebar_hint.py` | Tooltip revealing a nav item's label when the sidebar is collapsed. |

## Progressive Web App

The app is installable and works offline for its shell. The pieces are wired in `main.py`:

- **Web manifest** — served at `/manifest.json`, generated from `config.json` so the name, theme and icons stay in sync with the app. Declares `display: standalone`, start URL, theme/background colors and icons (`any` and `maskable`).
- **Service worker** — `assets/pwa/sw.js`, served at `/sw.js` from the origin root (with `Service-Worker-Allowed: /`) so its scope covers the whole app. Static assets under `/assets/` use stale-while-revalidate; page navigations are network-first with an offline fallback; NiceGUI's realtime channels and API routes are never intercepted.
- **Head tags** — manifest link, `theme-color`, Apple touch icon and mobile web-app meta tags are injected globally, plus a small script that registers the service worker on load.

`/manifest.json` and `/sw.js` are allow-listed in `core/security.py`, so they load before authentication and the app is installable from the login screen.

### Changing the app icon

Icons live in `assets/icons/` and are referenced by the manifest (`pwa_manifest` in `main.py`) and the Apple touch-icon head tag. Replace these PNG files, keeping the exact sizes:

| File | Size (px) | Purpose |
|---|---|---|
| `icon-192.png` | 192x192 | Standard icon (required) |
| `icon-512.png` | 512x512 | Standard icon, install/splash (required) |
| `icon-maskable-512.png` | 512x512 | Maskable icon: keep the logo inside the centered ~80% safe zone (~10% padding each side) so Android can crop it to any shape |
| `apple-touch-icon.png` | 180x180 | iOS home-screen icon (no transparency; use a solid background) |

Use square, transparent PNGs for the standard icons and a padded version for the maskable one. If you only supply your own logo, you can regenerate the whole set from a single source image with Pillow (no need to add it as a project dependency):

```bash
uv run --with pillow python -c "from pathlib import Path; from PIL import Image; s=Image.open('assets/images/logo.png').convert('RGBA'); o=Path('assets/icons'); o.mkdir(parents=True, exist_ok=True); [ (lambda c,r: (c.paste(s.resize((int(s.width*r),int(s.height*r)),Image.LANCZOS),((n-int(s.width*r))//2,(n-int(s.height*r))//2),s.resize((int(s.width*r),int(s.height*r)),Image.LANCZOS)), c.save(o/f) if not white else c.convert('RGB').save(o/f)))(Image.new('RGBA',(n,n),(255,255,255,255) if white else (0,0,0,0)), min(int(n*sc)/s.width,int(n*sc)/s.height)) for n,sc,white,f in [(192,1.0,False,'icon-192.png'),(512,1.0,False,'icon-512.png'),(512,0.6,True,'icon-maskable-512.png'),(180,0.85,True,'apple-touch-icon.png')] ]"
```

The `favicon.ico` used by the browser tab is set separately via `favicon=` in the `ui.run(...)` call in `main.py`.

## Logging

`core/logging_config.py` configures a timed rotating file handler (`logs/app.log`, rotated daily) plus a console handler. The active level (`DEBUG`–`CRITICAL`) is persisted to `logs/.log_level` and can be changed live by an admin from App Settings, applying across the whole app without a restart. Setup is idempotent, so it's safe under the dev auto-reloader, and the noisy `watchfiles` reload logger is quieted so its own change events don't feed back into the log.

## Testing

```bash
uv run pytest
```

Tests use the NiceGUI testing plugin (`nicegui.testing.user_plugin`) for UI simulation without a browser. The `temp_db` fixture points the database module at a throwaway SQLite file so tests never touch `data/app.db`. `asyncio_mode = "auto"` and `testpaths = ["tests"]` are set in `pyproject.toml`.

## Running in production

`main.py` defines three run targets at the bottom of the file — enable exactly one:

1. **Development** (default) — auto-reload on file changes.
2. **Production** — bound to `0.0.0.0`, `reload=False`.
3. **Production over HTTPS** — `reload=False` plus TLS using the certificates in `certs/`.

```python
# Production over HTTPS
ui.run(root, host='0.0.0.0', storage_secret=_get_storage_secret(), title=appName,
        port=appPort, favicon='favicon.ico', reconnect_timeout=20, reload=False,
        ssl_certfile='certs/cert.pem', ssl_keyfile='certs/key.pem')
```

The bundled `certs/cert.pem` and `certs/key.pem` are self-signed and intended for local testing only. Replace them with certificates from a trusted authority for real deployments, and always set `STORAGE_SECRET` in the environment.

## Docker Deployment

The repository root ships a `Dockerfile` and a `docker-compose.yaml` that build the app into an image and run it, mounting `./app` into the container so the database (`app/data/`), logs (`app/logs/`) and backups (`app/backup/`) persist on the host.

```python
ui.run(root, storage_secret=_get_storage_secret(),
       host=os.environ['HOST'], title=appName, port=appPort,
       favicon='favicon.ico', reconnect_timeout=20, reload=False)
```

- For **Docker** adjust `main.py` and use the container run target. The storage secret is resolved by `_get_storage_secret()` (which reads `STORAGE_SECRET` from the environment, set in `docker-compose.yaml`), and `HOST` comes from the environment too:

    ```python
    # For Docker
    ui.run(root, storage_secret=_get_storage_secret(), host=os.environ['HOST'])
    ```

    Go one folder back in the terminal where the **docker-compose.yaml** is located and start the stack:

    ```bash
    cd ..
    docker compose up
    ```

Your container builds the image `template:latest` and runs on [http://localhost:8080](http://localhost:8080).

> If you don't set `STORAGE_SECRET` (in your shell or a `.env` file), `_get_storage_secret()` generates a strong random secret and persists it at `app/data/.storage_secret`, which survives restarts via the `./app:/app` mount. Set it explicitly to share one secret across multiple instances.

## Packaging

A standalone build can be produced with PyInstaller (declared as a dependency):

```bash
uv run python -m PyInstaller --name 'ProductionSuite' --onedir main.py \
  --add-data '<path-to>/nicegui;nicegui' --noconfirm --clean
```

## Tech stack

- Python 3.11+
- NiceGUI 3.9 (with Highcharts extra)
- SQLAlchemy 2.0 ORM over SQLite
- pytest / pytest-asyncio
- [uv](https://docs.astral.sh/uv/) for dependency and environment management

## Contributing

Issues and pull requests are welcome. For anything non-trivial, please open an issue first to discuss the approach before investing time in an implementation.
