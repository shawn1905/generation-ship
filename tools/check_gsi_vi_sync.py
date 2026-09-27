#!/usr/bin/env python3
"""Check that the two GSI visual-standard directories are byte-identical."""

import hashlib
import sys
from pathlib import Path


def inventory(directory: Path) -> dict[str, str]:
    if not directory.is_dir():
        raise FileNotFoundError(directory)
    manifest = directory / "GSI-FILES.txt"
    names = [line.strip() for line in manifest.read_text().splitlines()
             if line.strip() and not line.startswith("#")]
    if len(names) != len(set(names)) or not names:
        raise ValueError(f"invalid or duplicate entries in {manifest}")
    if any(Path(name).name != name for name in names):
        raise ValueError(f"manifest entries must be filenames: {manifest}")
    files = [directory / name for name in names]
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [manifest, *files]}


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: check_gsi_vi_sync.py WORLD_REPO FOUNDRY_REPO", file=sys.stderr)
        return 2
    world = inventory(Path(sys.argv[1]) / "craft/visual-identity/gsi")
    foundry = inventory(Path(sys.argv[2]) / "docs/visual")
    names = sorted(world.keys() | foundry.keys())
    differences = [name for name in names if world.get(name) != foundry.get(name)]
    if differences:
        for name in differences:
            print(f"MISMATCH {name}: world={world.get(name, 'missing')} foundry={foundry.get(name, 'missing')}")
        return 1
    print(f"PASS: {len(names)} GSI visual-standard files match by SHA-256")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
