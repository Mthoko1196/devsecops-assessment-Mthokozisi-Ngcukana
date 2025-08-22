#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/secret_scan.py" --path "$ROOT/tests/test_leaks" --format json --fail-on medium
echo "OK: basic scan executed"