# Apple Notes Integration via AppleScript

## The `memo` CLI Problem

The `memo` CLI (antoniorodr/memo) for managing Apple Notes via terminal may NOT be installed. When it's missing, use AppleScript via `osascript` instead.

## Reading a Note

```bash
osascript -e 'tell application "Notes" to repeat with n in notes' \
  -e 'if name of n contains "OpenAI key" then' \
  -e 'set foundNote to n' \
  -e 'exit repeat' \
  -e 'end if' \
  -e 'end repeat' \
  -e 'return body of foundNote'
```

**Note:** AppleScript `repeat` loops DO NOT work in a single `osascript -e` line with `&&` chaining. You must pass each line as a separate `-e` argument to the SAME osascript invocation.

## Appending to a Note

```bash
osascript -e 'tell application "Notes" to repeat with n in notes' \
  -e 'if name of n contains "OpenAI key" then' \
  -e 'set currentBody to body of n' \
  -e 'set newEntry to return & "New entry text" & return' \
  -e 'set body of n to currentBody & newEntry' \
  -e 'exit repeat' \
  -e 'end if' \
  -e 'end repeat' \
  -e 'return "done"'
```

## Critical Pitfall: Shell `&` vs AppleScript `return`

- **DO NOT** use shell `&` for string concatenation in AppleScript — it triggers background process error
- **DO NOT** use `\n` in AppleScript strings for newlines — AppleScript ignores them in `-e` mode
- **DO** use AppleScript's `return` constant (the word "return" by itself creates a newline character)
- **DO** pass each AppleScript statement as a separate `osascript -e '...'` argument

## Note Body Format

Note bodies are HTML wrapped in `<div>` tags. Plain text appears as:
```html
<div><h1>Note Title</h1></div>
<div><br></div>
<div>text line</div>
<div>another line</div>
```
