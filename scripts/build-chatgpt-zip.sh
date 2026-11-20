#!/usr/bin/env bash
# Build the ZIP uploaded to the ChatGPT plugin directory (OpenAI Platform → Plugins).
#
#   scripts/build-chatgpt-zip.sh [git ref, default HEAD]
#
# The ZIP holds only what ChatGPT reads: plugin.json, mcp.json, skills/, assets/ and LICENSE.
# It is cut from a commit with `git archive`, so the same commit always gives the same bytes;
# uncommitted changes are not included.
set -euo pipefail
cd "$(dirname "$0")/.."
ref="${1:-HEAD}"
version="$(git show "$ref:plugin.json" | python3 -c 'import json,sys; print(json.load(sys.stdin)["version"])')"
mkdir -p dist
out="dist/appner-chatgpt-$version.zip"
rm -f "$out"
git archive --format=zip -o "$out" "$ref" plugin.json mcp.json skills assets LICENSE
python3 scripts/check_chatgpt_package.py "$out"
echo "$out  $(git rev-parse --short "$ref")  sha256 $(shasum -a 256 "$out" | cut -d' ' -f1)"
