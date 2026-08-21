# Tailscale MCP Reboot Recovery

Read this only when a role or MCP client loses connector reachability after a reboot and the route depends on Tailscale Serve or Funnel.

## Distinguish the layers

A healthy local MCP process does not prove that a remote connector can reach it. Verify the chain from the inside out:

1. **Local service:** confirm the LaunchAgent/process, loopback listener, and local health or MCP endpoint.
2. **Installed launch path:** inspect the exact launcher used by `launchd`, including any network setup it performs before starting the server.
3. **Tailscale readiness:** parse `tailscale status --json`; require `BackendState == "Running"` and `Self.Online == true`. Exit code zero alone is not readiness proof.
4. **Published map:** inspect `tailscale funnel status` or `tailscale serve status` and compare every binding with the intended public/private boundary.
5. **External behavior:** probe the public hostname from the real route. For an OAuth-protected MCP SSE entry, an unauthenticated `401` with the OAuth discovery challenge proves more than a generic `200` health page.
6. **Affected role:** have the role or connector that originally failed perform its real startup/read action. This is the acceptance gate.

Keep configuration, local process health, tailnet state, public reachability, and affected-client acceptance as separate claims.

## Reboot-specific failure patterns

- `tailscale status --json` can exit successfully while the backend is stopped or offline. A shell loop that tests only command success may proceed too early and fail once.
- A `RunAtLoad` one-shot will not repair itself if the GUI-managed network extension becomes ready later. Give the binding owner bounded polling and launchd retry-on-unsuccessful-exit behavior.
- Do not swallow Serve/Funnel failures with `|| true`; that converts a missing route into a misleadingly healthy launcher.
- Use one owner for published-route state. The MCP launcher should start MCP; a dedicated Tailscale binding launcher should own Serve/Funnel desired state.
- Prefer explicit loopback targets such as `127.0.0.1` in machine-checked route maps, while allowing equivalent existing `localhost` values during diagnosis.
- If Tailscale reports a missing launch daemon or broken system-extension state, reinstalling the current official signed/notarized standalone package can be appropriate. Treat the privileged install as a user gate, then verify the installed version, active extension, online state, and published map separately.

## Preserve the access boundary

Repairing reachability does not authorize broader exposure. Determine and enforce the intended boundary independently of the outage repair.

For the proven local layout as of 2026-08-20:

- public `:443` points to the MCP bridge on `127.0.0.1:5600`;
- public `:8443` is absent;
- dashboard routes stay tailnet-only on `:5443` and `:5088`;
- the public MCP bridge has explicit MCP, OAuth, health, schema, and authenticated Action routes, with no general dashboard API pass-through or browser catch-all.

If a retired public binding may persist in Tailscale state, make its absence part of the boot-time desired-state script. Make removal idempotent: check whether the binding exists before issuing `off` if the CLI treats an already-absent handler as an error.

## Acceptance evidence

Require evidence on both sides of the boundary:

- local MCP health succeeds and the service PID remains stable;
- the public MCP/OAuth path has its expected response, including the OAuth challenge on unauthenticated SSE;
- public dashboard paths are denied and the retired public dashboard port is absent;
- the same dashboard paths succeed over the intended tailnet-only entries;
- the binding LaunchAgent finishes successfully or remains ready to retry a readiness failure;
- the affected role completes the startup/read that originally failed.

If no reboot is performed during the repair session, report reboot persistence as structurally guarded but not yet reboot-proven. Do not substitute unit tests, route-map output, or the fixer's self-report for the affected role's acceptance.

## Proven instance

On 2026-08-20, Orchestrator registry reads failed after reboot while the local MCP service was healthy. The binding script had mistaken command success for Tailscale readiness, its one-shot LaunchAgent did not retry, the MCP launcher was a second Funnel writer that suppressed failures, and the Tailscale system extension required an official standalone update. The repair added state-aware readiness, retry-on-failure, single-writer route ownership, and external route checks. It also removed public dashboard `:8443` and the public-root dashboard proxy while preserving authenticated MCP/Action routes. Ted then confirmed Orchestrator startup succeeded; public denial and tailnet-positive probes both passed.
