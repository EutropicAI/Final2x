import argparse
import json
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PACKAGE_JSON = ROOT / "package.json"
PYPROJECT_TOML = ROOT / "core" / "pyproject.toml"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check that the desktop, Python core, and optional release tag versions match."
    )
    parser.add_argument("--tag", help="Release tag to compare with the shared version, for example v4.1.0")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    with PACKAGE_JSON.open(encoding="utf-8") as file:
        desktop_version = json.load(file).get("version")

    with PYPROJECT_TOML.open("rb") as file:
        core_version = tomllib.load(file).get("project", {}).get("version")

    if not isinstance(desktop_version, str):
        print("package.json must contain a string version", file=sys.stderr)
        return 1

    if not isinstance(core_version, str):
        print("core/pyproject.toml must contain a string project.version", file=sys.stderr)
        return 1

    if desktop_version != core_version:
        print(
            f"Version mismatch: package.json={desktop_version}, "
            f"core/pyproject.toml={core_version}",
            file=sys.stderr,
        )
        return 1

    expected_tag = f"v{desktop_version}"
    if args.tag is not None and args.tag != expected_tag:
        print(
            f"Release tag mismatch: tag={args.tag}, expected={expected_tag}",
            file=sys.stderr,
        )
        return 1

    print(f"Version check passed: {desktop_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
