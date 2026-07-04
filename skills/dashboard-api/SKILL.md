---
name: dashboard-api
description: >-
  Reusable API calls for the Hermes Agent Dashboard at
  http://127.0.0.1:8787. Use for cron health checks, log anomaly
  scanning, gateway status, session activity, and config verification.
  Designed for Substrate-Hermes but usable by any profile.
tags: [hermes, dashboard, monitoring, health-check, substrate-hermes]
---

# Dashboard API

The Hermes Agent Dashboard exposes a read-only REST API at `http://127.0.0.1:8787`. This skill provides ready-made functions for system monitoring and health checks.

## Auth

The session token lives in the dashboard's HTML. Extract it at session start:

```python
import re, urllib.request

def get_token():
    req = urllib.request.Request("http://127.0.0.1:8787/")
    resp = urllib.request.urlopen(req, timeout=10)
    html = resp.read().decode()
    match = re.search(r'__HERMES_SESSION_TOKEN__="([^"]*)"', html)
    if not match:
        raise RuntimeError("Could not extract dashboard token")
    return match.group(1)
```

Token rotates on gateway restart. Always fetch fresh.

## API Endpoints Reference

| Endpoint | Returns | Use Case |
|---|---|---|
| `GET /api/cron/jobs` | All 49 jobs (schedule, status, error, run count) | Cron health check |
| `GET /api/status` | Gateway state, version, platform connections | Pulse check |
| `GET /api/logs` | Last 100 agent + gateway log lines | Anomaly scan |
| `GET /api/sessions/stats` | Total sessions, messages, by-source breakdown | Activity monitoring |
| `GET /api/sessions?limit=N` | N most recent sessions (model, source, msg count) | Recent activity |
| `GET /api/sessions/<id>/messages` | Full message history for one session | Deep dive |
| `GET /api/config` | Full config (depersonalized) | Config verification |
| `GET /api/config/schema` | Every config field with type + description | Discover options |
| `GET /api/skills` | All 119 skills | Skill inventory |
| `GET /api/memory` | Memory providers (holographic active, 7 others) | Memory health |

## Ready-Made Functions

### 1. Cron Health Check

```python
def cron_health_check(token: [REDACTED] -> dict:
    """Check all cron jobs. Returns list of failing jobs."""
    import json, urllib.request

    req = urllib.request.Request(
        "http://127.0.0.1:8787/api/cron/jobs",
        headers={"Authorization": f"Bearer {token}"})
    data = json.loads(urllib.request.urlopen(req, timeout=15).read())

    failing = [j for j in data if j.get("last_status") == "error"]
    return {
        "total": len(data),
        "failing": len(failing),
        "ok": len(data) - len(failing),
        "failed_jobs": [{
            "name": j["name"],
            "profile": j.get("profile_name", j.get("profile", "?")),
            "id": j["id"][:12],
            "error": j.get("last_error", "?")[:200],
            "runs": j.get("repeat", {}).get("completed", 0),
            "schedule": j.get("schedule_display", "?"),
            "last_run": j.get("last_run_at", "?")[:16],
            "next_run": j.get("next_run_at", "?")[:16],
        } for j in failing],
        "profiles": list(set(j.get("profile_name", j.get("profile", "?")) for j in data))
    }
```

### 2. Log Anomaly Scan

```python
def log_scan(token: [REDACTED] since_minutes: int = 60) -> dict:
    """Scan agent+gateway logs for WARNING, ERROR, rate limits."""
    import json, urllib.request
    from collections import Counter
    from datetime import datetime, timezone

    req = urllib.request.Request(
        "http://127.0.0.1:8787/api/logs",
        headers={"Authorization": f"Bearer {token}"})
    data = json.loads(urllib.request.urlopen(req, timeout=15).read())

    lines = data.get("lines", [])
    errors = []
    warnings = Counter()
    rate_limits = []
    timeouts = []

    for l in lines:
        level = l.split()[2] if len(l.split()) > 2 else ""
        msg = l.split(" ", 4)[-1].strip() if " " in l else l.strip()

        if "ERROR" in level or "CRITICAL" in level:
            errors.append(msg[:200])
        elif "rate limit" in msg.lower() or "resourceexhausted" in msg.lower():
            rate_limits.append(msg[:200])
        elif "timeout" in msg.lower():
            timeouts.append(msg[:200])
        elif "WARNING" in level:
            key = msg.split(":")[0] if ":" in msg else msg[:80]
            warnings[key] += 1

    return {
        "total_lines": len(lines),
        "errors": errors[:10],
        "error_count": len(errors),
        "warning_summary": dict(warnings.most_common(10)),
        "rate_limits": rate_limits[:5],
        "timeouts": timeouts[:5],
    }
```

### 3. Gateway Status Check

```python
def gateway_status(token: [REDACTED] -> dict:
    """Check gateway is running, platforms connected, version."""
    import json, urllib.request

    req = urllib.request.Request(
        "http://127.0.0.1:8787/api/status",
        headers={"Authorization": f"Bearer {token}"})
    data = json.loads(urllib.request.urlopen(req, timeout=10).read())

    platforms = data.get("gateway_platforms", {})
    return {
        "version": data.get("version", "?"),
        "gateway": data.get("gateway_state", "?"),
        "active_agents": data.get("active_agents", 0),
        "active_sessions": data.get("active_sessions", 0),
        "gateway_busy": data.get("gateway_busy", False),
        "can_update": data.get("can_update_hermes", False),
        "config_version": data.get("config_version", "?"),
        "latest_config_version": data.get("latest_config_version", "?"),
        "platforms": {name: info.get("state", "?") for name, info in platforms.items()},
        "health_issues": [
            f"{name}: {info.get('error_message', 'disconnected')}"
            for name, info in platforms.items()
            if info.get("state") != "connected"
        ],
    }
```

### 4. Session Activity Summary

```python
def session_activity(token: [REDACTED] limit: int = 5) -> dict:
    """Recent session activity: total stats + last N sessions."""
    import json, urllib.request

    req = urllib.request.Request(
        f"http://127.0.0.1:8787/api/sessions?limit={limit}",
        headers={"Authorization": f"Bearer {token}"})
    data = json.loads(urllib.request.urlopen(req, timeout=10).read())

    req2 = urllib.request.Request(
        "http://127.0.0.1:8787/api/sessions/stats",
        headers={"Authorization": f"Bearer {token}"})
    stats = json.loads(urllib.request.urlopen(req2, timeout=10).read())

    sessions = data.get("sessions", [])
    return {
        "stats": stats,
        "recent": [{
            "id": s["id"][:20],
            "source": s.get("source", "?"),
            "model": s.get("model", "?")[:40],
            "messages": s.get("message_count", s.get("msg_count", "?")),
        } for s in sessions[:limit]],
    }
```

### 5. Full Morning Health Brief

```python
def morning_health_brief(token: [REDACTED] -> str:
    """Combined health check - cron, logs, gateway, activity."""
    import json, urllib.request
    from datetime import datetime

    cron = cron_health_check(token)
    logs = log_scan(token, since_minutes=120)
    gw = gateway_status(token)
    act = session_activity(token, limit=3)

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Hermes Health Brief — {now}",
        "",
        f"## Gateway: {gw['gateway']}",
        f"Version {gw['version']} | Config v{gw['config_version']}/{gw['latest_config_version']} | "
        f"{gw['active_agents']} agents | {gw['active_sessions']} sessions",
    ]

    lines.append("")
    lines.append("## Platforms")
    for name, state in gw["platforms"].items():
        lines.append(f"- {name}: {state}")

    lines.append("")
    lines.append(f"## Cron: {cron['ok']}/{cron['total']} OK, {cron['failing']} failing")
    if cron["failing"] > 0:
        lines.append("")
        lines.append("### Failing Jobs")
        for j in cron["failed_jobs"]:
            lines.append(f"- **{j['name']}** ({j['profile']}): {j['error']}")

    lines.append("")
    lines.append(f"## Logs: {logs['error_count']} errors, {logs['total_lines']} lines")
    if logs["errors"]:
        lines.append("- Errors:")
        for e in logs["errors"][:5]:
            lines.append(f"  - `{e[:100]}`")
    if logs["rate_limits"]:
        lines.append("- Rate limits:")
        for r in logs["rate_limits"][:3]:
            lines.append(f"  - `{r[:100]}`")
    if logs["warning_summary"]:
        lines.append("- Warning frequencies:")
        for w, c in list(logs["warning_summary"].items())[:5]:
            lines.append(f"  - [{c}x] {w}")
    if logs["timeouts"]:
        lines.append("- Timeouts:")
        for t in logs["timeouts"][:3]:
            lines.append(f"  - `{t[:100]}`")

    if "health_issues" in gw and gw["health_issues"]:
        lines.append("")
        lines.append("### Health Issues")
        for h in gw["health_issues"]:
            lines.append(f"- {h}")

    lines.append("")
    lines.append(f"## Recent Sessions ({act['stats'].get('total', '?')} total)")
    for s in act.get("recent", []):
        lines.append(f"- [{s['source']}] {s['model']} — {s['messages']} msgs")

    return "\n".join(lines)
```

## Usage

Load this skill and call any function:

```python
# Load the dashboard-api skill
with skill_view("dashboard-api"):
    token = get_token()
    report = morning_health_brief(token)
    # Write to file or send
    write_file("/tmp/hermes_health_brief.md", report)
```

Or import directly in a script:

```python
import json, urllib.request, re, sys
# ... copy the functions above or import from this skill's reference
```

## Pitfalls

- **Token expires on gateway restart.** Always re-extract from the page HTML. Don't cache it across sessions.
- **API is read-only.** Can't update cron jobs or config from the dashboard. Use `hermes cron` CLI for mutations.
- **No authentication on loopback.** The token guards API endpoints but `auth_required=false` means loopback access is always open. The token is a CSRF/SSRF guard, not user auth.
- **Log endpoint returns last ~100 lines.** For full log files, read `~/.hermes/logs/gateway.log` directly from terminal.
- **Session list is paginated at 50.** Use `?limit=N` for more, but 50 is the max per request.
- **WebSocket at `/ws` needs cookie auth from the SPA.** API token alone won't work. Not usable for scripted access.
