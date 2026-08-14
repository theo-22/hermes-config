---
name: migrate-mcp-secret-to-keychain
description: Migrate one hardcoded local MCP access key, keyed URL, or plaintext client-config secret into macOS Keychain; route clients through a Keychain-backed local stdio proxy when their config cannot interpolate secrets; remove active plaintext copies; and prove success plus fail-closed behavior without printing the value. Use when a macOS MCP client or proxy contains the same secret in code, JSON/TOML config, URL query parameters, or compatibility files and the user has authorized credential-surface changes.
metadata:
  category: meta
  write_mode: file
  one_line_use: centralize one local MCP secret in Keychain and prove the installed cutover
  fast_pick: "no"
---

# Migrate MCP Secret to Keychain

Move one authorized local machine secret to a single macOS Keychain source while preserving the real MCP workload and eliminating plaintext runtime copies.

## Boundaries

- Treat credential files, Keychain entries, account settings, and provider rotation as protected surfaces. Require explicit authorization before mutation.
- Migrate one named secret and its actual consumers. Do not turn the task into a general credential sweep.
- Never print the secret, a keyed URL, a secret-bearing diff, or a command line containing the literal value.
- Do not rotate or revoke the provider credential unless separately authorized.
- Do not write `keychain://...` into a config unless the installed launcher demonstrably resolves that marker. A marker without a loader is a silent outage.
- Prefer one Keychain-backed local proxy over separate per-client loaders when the clients can share the same MCP implementation.
- Fail closed when Keychain lookup fails or returns an empty value. Do not retain a hardcoded or environment fallback merely to keep the path green.
- Preserve unrelated config and dirty-worktree changes. Claim shared surfaces before writing.

## Workflow

### 1. Resolve the live consumer chain

Trace each active link before choosing the migration:

`client config -> launcher/transport -> proxy or server -> credential reader -> real MCP workload`

Separate active files from history, backups, logs, generated copies, and retired paths. Inspect the installed client configuration rather than assuming its supported fields. Check repo boundaries before write-side git work.

### 2. Inventory copies without exposing the value

Read the existing value into process memory from one authorized live source. Compare exact bytes against a bounded list of active files and output filenames only. Do not run a broad search that includes session logs, shell history, backups, or repositories unrelated to the consumer chain.

Record:

- current source and consumer paths;
- client transport and launcher command;
- Keychain service and account names;
- active plaintext-copy count;
- recovery path if cutover validation fails.

Use a lowercase-dashed service name and an explicit account. Keep the value-free mapping in the machine's secret index when one exists.

### 3. Establish the Keychain source

Store or update the value through macOS `security` while keeping it out of command output. Retrieve it immediately into captured process output and compare in memory with the source value. Stop before deleting any plaintext copy if the entry is missing, empty, or unequal.

The Keychain entry becomes canonical only after this equality check passes and at least one real consumer can load it.

### 4. Make the proxy Keychain-backed

Implement one loader that:

1. invokes `security find-generic-password` with the exact service and account;
2. captures stdout and stderr;
3. checks the exit status;
4. strips and rejects an empty value;
5. raises a value-free error naming only the service/account;
6. caches the result when repeated lookup is unnecessary.

Load lazily at the first authenticated request when import-time lookup would break tests, schema discovery, or harmless startup. Inject the secret only at the outbound request boundary. Keep it out of logs, errors, tool results, and receipts.

### 5. Route every local client through the shared proxy

When a client cannot interpolate Keychain values into a remote HTTP URL, configure it to launch the local proxy over stdio. Reuse the same executable path for every compatible local client rather than embedding the secret in each client's URL or config.

Validate configuration with the real client command or settings reader. A parseable JSON/TOML file is static proof, not connection proof.

### 6. Remove plaintext runtime copies

Only after Keychain retrieval and client configuration validation pass:

- remove hardcoded defaults from proxy/server code;
- remove keyed URLs or literal values from active client configs;
- remove obsolete compatibility copies;
- update bootstrap helpers so reruns verify Keychain and use legacy import only as an explicit recovery path;
- update the value-free secret index and architecture/continuity surfaces when the consumer path changed.

Run `scripts/verify_keychain_cutover.py` against the exact active source/config files. It reads the Keychain value only into memory and prints paths, never the value.

### 7. Prove the installed path

Use `$verify-real-invocation-path` and keep the evidence layers distinct:

1. **Static:** config parses; source contains no hardcoded fallback; bounded plaintext scan returns zero.
2. **Unit:** Keychain present, missing, and empty cases; missing/empty fail closed.
3. **Installed client:** the real client reports the configured MCP server connected through the intended transport.
4. **Positive workload:** a freshly spawned client lists tools and completes one harmless real MCP call.
5. **Negative control:** through the same launcher, substitute a disposable failing `security` command or mock the lookup; the MCP call must fail visibly without exposing the secret.

Do not delete the real Keychain entry to create the negative probe. Do not accept a health response, direct function import, or warmed client as the positive workload.

## Completion criteria

Report complete only when all are true:

- the authorized Keychain entry exists, is nonempty, and matched the pre-cutover value in memory;
- every named active local client resolves the same proxy or loader;
- the bounded active-file scan finds zero plaintext copies;
- missing or empty Keychain state fails closed;
- a fresh installed-path MCP workload succeeds;
- no secret value appears in commands, output, logs, diffs, receipts, or the skill artifacts;
- work-item, continuity, architecture, claim, and git closeout requirements are satisfied.

## Failure modes

- **Keychain as backup, plaintext as runtime:** storing a copy without cutting readers over does not centralize anything.
- **Unresolved marker:** a `keychain://` string is passed to the provider because no launcher expands it.
- **Fallback persistence:** an environment or hardcoded default silently remains a second authority.
- **Config-only proof:** the client file changed, but no fresh client connected or called a tool.
- **Proxy-only proof:** direct Python execution passed while the installed client still uses a keyed URL.
- **Unsafe search:** secret discovery scans histories/backups and creates more exposure in output.
- **Destructive negative test:** removing the real Keychain item creates an avoidable outage.
- **Unrelated rotation:** provider-console key rotation is added without explicit authorization.

## Runtime notes

### Codex and Claude Code

Prefer their live MCP config readers plus a freshly spawned stdio client. Preserve user-level config permissions and validate the exact command/path each reports.

### Hermes or managed workers

Resolve the selected profile and launcher first. Use a Keychain loader only if that installed runtime can access the login Keychain noninteractively; otherwise stop at the demonstrated boundary rather than restoring plaintext.

### GPT or cloud clients

This skill does not move a cloud connector's server-side secret into a local Mac Keychain. Route that case to the connector's supported secret store or a separately authorized server-side design.

## Update backstop

Client config schemas and macOS Keychain behavior can change. Verify the installed client version and real configuration command before copying old JSON/TOML shapes. If the canonical evidence or completion standard changes, update this shared skill rather than creating an actor-local doctrine fork.
