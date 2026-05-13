#!/usr/bin/env bash
# Fail if any public HTML entry page is missing GA4 (gtag.js + measurement ID).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
readonly GA_ID="G-XXQSMBERJM"
readonly GTAG_HREF="https://www.googletagmanager.com/gtag/js?id=${GA_ID}"

errors=0

check_file() {
  local f="$1"
  if [[ ! -f "$f" ]]; then
    printf 'ERROR: missing file: %s\n' "$f" >&2
    errors=$((errors + 1))
    return
  fi
  if ! grep -qF "$GA_ID" "$f"; then
    printf 'ERROR: %s — missing measurement ID %s\n' "$f" "$GA_ID" >&2
    errors=$((errors + 1))
  fi
  if ! grep -qF "$GTAG_HREF" "$f"; then
    printf 'ERROR: %s — missing gtag.js loader for %s\n' "$f" "$GA_ID" >&2
    errors=$((errors + 1))
  fi
  if ! grep -qE 'src="[^"]*assets/js/analytics\.js"' "$f"; then
    printf 'ERROR: %s — missing shared assets/js/analytics.js script tag\n' "$f" >&2
    errors=$((errors + 1))
  fi
}

check_file "$ROOT/index.html"
check_file "$ROOT/affiliates/index.html"

while IFS= read -r -d '' f; do
  check_file "$f"
done < <(find "$ROOT/free-tools" -type f -name 'index.html' -print0)

if [[ "$errors" -ne 0 ]]; then
  printf 'GA HTML check failed (%s issue(s)).\n' "$errors" >&2
  exit 1
fi

printf 'OK: GA4 (%s) present in all checked HTML entry pages.\n' "$GA_ID"