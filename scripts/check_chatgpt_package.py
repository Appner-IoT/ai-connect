#!/usr/bin/env python3
"""Checks the ChatGPT plugin package (stdlib only, no network).

  python3 scripts/check_chatgpt_package.py            # the working tree
  python3 scripts/check_chatgpt_package.py dist/x.zip # an unpacked copy of a built ZIP

Rules come from the Agent Plugins 1.0.0 manifest schema and the OpenAI submission guide
(https://developers.openai.com/plugins/deploy/submission).
"""

import json
import re
import struct
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT_KEYS = {"$schema", "name", "version", "description", "author", "homepage", "repository",
             "license", "keywords", "extensions"}
AUTHOR_KEYS = {"name", "email", "url"}
NAME = re.compile(r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
URL_FIELDS = ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL")
REQUIRED_INTERFACE = ("displayName", "shortDescription", "longDescription", "developerName",
                      "category", "defaultPrompt", "logo", "composerIcon") + URL_FIELDS
SECRET = re.compile(r"password|passwd|secret|api[_-]?key|bearer\s+[a-z0-9]", re.I)
PACKAGE_ENTRIES = {"plugin.json", "mcp.json", "skills", "assets", "LICENSE"}

errors: list[str] = []


def check(ok: bool, message: str) -> None:
    if not ok:
        errors.append(message)


def inside(root: Path, rel: str) -> Path | None:
    if not rel.startswith("./"):
        return None
    path = (root / rel).resolve()
    return path if root.resolve() in path.parents and path.is_file() else None


def check_manifest(root: Path) -> None:
    manifest = json.loads((root / "plugin.json").read_text())
    extra = set(manifest) - ROOT_KEYS
    check(not extra, f"plugin.json: keys the schema rejects: {sorted(extra)}")
    check(manifest.get("$schema") == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
          "plugin.json: wrong $schema")
    name = manifest.get("name", "")
    check(bool(NAME.match(name)) and len(name) <= 64, "plugin.json: bad name")
    check(re.fullmatch(r"\d+\.\d+\.\d+", manifest.get("version", "")) is not None,
          "plugin.json: version is not x.y.z")
    check(0 < len(manifest.get("description", "")) <= 4000, "plugin.json: description length")
    check(not set(manifest.get("author", {})) - AUTHOR_KEYS, "plugin.json: unknown author key")
    check(0 < len(manifest.get("author", {}).get("name", "")) <= 120, "plugin.json: author.name")

    openai = manifest.get("extensions", {}).get("com.openai", {})
    card = openai.get("interface", {})
    for key in REQUIRED_INTERFACE:
        check(bool(card.get(key)), f"interface.{key} is missing")
    check(len(card.get("displayName", "")) <= 30, "interface.displayName over 30 characters")
    check(len(card.get("shortDescription", "")) <= 30, "interface.shortDescription over 30")
    check(len(card.get("longDescription", "")) <= 4000, "interface.longDescription over 4000")
    check(len(card.get("developerName", "")) <= 80, "interface.developerName over 80")
    for key in URL_FIELDS:
        check(card.get(key, "").startswith("https://") and len(card.get(key, "")) <= 2048,
              f"interface.{key} must be an https URL")
    prompts = card.get("defaultPrompt", [])
    check(isinstance(prompts, list) and 1 <= len(prompts) <= 3, "defaultPrompt: 1 to 3 prompts")
    check(len(set(prompts)) == len(prompts), "defaultPrompt: prompts must differ")
    for prompt in prompts:
        check(len(prompt) <= 128 and "@" not in prompt, f"defaultPrompt too long or has @: {prompt}")
    capabilities = card.get("capabilities", [])
    check(len(capabilities) <= 20 and all(len(c) <= 120 for c in capabilities), "capabilities")
    for key in ("logo", "composerIcon", "logoDark", "composerIconDark"):
        if key in card:
            icon = inside(root, card[key])
            check(icon is not None, f"interface.{key}: {card[key]} is not a file inside the package")
            if icon and icon.suffix == ".png":
                data = icon.read_bytes()
                width, height = struct.unpack(">II", data[16:24])
                check(width == height and 48 <= width <= 4096, f"{card[key]}: not square 48..4096")
                check(len(data) <= 5 * 1024 * 1024, f"{card[key]}: over 5 MiB")

    cases = openai.get("review", {}).get("test_cases", {})
    positive, negative = cases.get("positive", []), cases.get("negative", [])
    check(len(positive) == 5, f"review: {len(positive)} positive test cases, need 5")
    check(len(negative) == 3, f"review: {len(negative)} negative test cases, need 3")
    for case in positive:
        for key in ("description", "prompt", "tools_triggered", "expected_behavior"):
            check(bool(case.get(key)), f"positive test case without {key}: {case.get('prompt')}")
    for case in negative:
        check(set(case) == {"description", "prompt"}, f"negative case keys: {sorted(case)}")
    check(bool(openai.get("publication", {}).get("release_notes")), "publication.release_notes")
    demo = openai.get("review", {}).get("demo_recording_url")
    check(demo is None or demo.startswith("https://"), "review.demo_recording_url must be https")
    check(not SECRET.search(json.dumps(openai.get("review", {}))),
          "review: looks like a credential; reviewer sign-in goes into the portal only")


def check_mcp(root: Path) -> None:
    servers = json.loads((root / "mcp.json").read_text()).get("mcpServers", {})
    check(len(servers) == 1, "mcp.json: exactly one MCP server")
    for name, server in servers.items():
        check(server.get("type") == "streamable-http", f"{name}: type must be streamable-http")
        check(server.get("url", "").startswith("https://"), f"{name}: url must be https")
        check(not server.get("headers"), f"{name}: headers are rejected for public submission")
        auth = server.get("extensions", {}).get("com.openai", {}).get("auth", {})
        check(auth.get("type") == "oauth" and auth.get("client", {}).get("mode") == "dcr",
              f"{name}: expected OAuth with dynamic client registration")
        check("clientId" not in auth.get("client", {}) and "clientSecret" not in json.dumps(auth),
              f"{name}: no client id or secret in the package")


def check_skills(root: Path) -> None:
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    check(len(skills) >= 8, f"only {len(skills)} skills")
    for skill in skills:
        front = re.match(r"---\n(.*?)\n---\n", skill.read_text(), re.S)
        check(front is not None, f"{skill}: no front matter")
        if front:
            fields = dict(l.split(": ", 1) for l in front.group(1).splitlines() if ": " in l)
            check(fields.get("name") == skill.parent.name, f"{skill}: name differs from folder")
            check(len(fields.get("description", "")) > 40, f"{skill}: description too short")
    for doc in sorted((root / "skills").rglob("*.md")):
        for target in re.findall(r"\]\((?!https?://)([^)#]+)", doc.read_text()):
            check((doc.parent / target).is_file(), f"{doc}: broken link {target}")


def main() -> int:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory() as tmp:
        root = target
        if target.suffix == ".zip":
            with zipfile.ZipFile(target) as archive:
                check(archive.testzip() is None, "corrupt ZIP")
                archive.extractall(tmp)
            root = Path(tmp)
            top = {p.name for p in root.iterdir()}
            check(top == PACKAGE_ENTRIES, f"ZIP root holds {sorted(top)}")
        check_manifest(root)
        check_mcp(root)
        check_skills(root)
    for error in errors:
        print("FAIL", error)
    print(f"{target}: {'OK' if not errors else f'{len(errors)} problem(s)'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
