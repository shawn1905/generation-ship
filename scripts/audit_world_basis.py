#!/usr/bin/env python3
"""Read-only evidence audit; stdout is JSON. No canon edits or physics certification.

Run: python3 scripts/audit_world_basis.py > /tmp/world-basis-audit.json
Archive-year/epoch differences are candidates: archive numbers may survive redating.
"""
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ID = re.compile(r"GS-\d{4}-\d{2,}")
EPOCHS = [(2025, 2035, "替代"), (2035, 2050, "竞赛"),
          (2050, 2080, "丰裕"), (2080, 2150, "离心"),
          (2150, 2350, "启航"), (2350, 2500, "落地"),
          (2500, 10000, "双星系")]


def metadata(text):
    match = re.match(r"\A---\r?\n(.*?)\r?\n---", text, re.S)
    if not match:
        return {}
    return dict(re.findall(r"^([a-z_]+):[^\S\n]*(.*)$", match[1], re.M))


def run():
    index = defaultdict(list)
    candidates = []
    inputs = {}
    namespaces = defaultdict(int)
    documents = []
    for path in sorted((ROOT / "artifacts/writing").glob("*.md")):
        text = path.read_text()
        fm = metadata(text)
        rel = path.relative_to(ROOT).as_posix()
        inputs[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
        found = ID.fullmatch(fm.get("archive_id", "").strip())
        if not found:
            continue
        aid = found.group()
        index[aid].append(rel)
        documents.append(rel)
        year = int(aid.split("-")[1])
        coord = fm.get("coord", "").split("×")
        if len(coord) >= 2:
            # Boundary years overlap in prose; do not silently choose one side.
            allowed = [name for lo, hi, name in EPOCHS if lo <= year <= hi]
            if coord[1].strip() not in allowed:
                candidates.append({"path": rel, "archive_id": aid,
                                   "coord": fm.get("coord"), "allowed_by_id_year": allowed})
        front = text.split("---", 2)[1]
        for ns in re.findall(r"^\s*-\s*([a-z]+)/[^\s]+", front, re.M):
            namespaces[ns] += 1

    registry = ROOT / "artifacts/档案登记簿.md"
    mismatches = []
    missing_targets = []
    rows = []
    for n, line in enumerate(registry.read_text().splitlines(), 1):
        if not line.startswith("| GS-"):
            continue
        match = re.search(r"\| (GS-\d{4}-\d{2,}) \| .*?\]\((.*)\) \|", line)
        if not match:
            continue
        aid, target = match.groups()
        path = registry.parent / target
        rows.append(aid)
        if not path.is_file():
            missing_targets.append({"line": n, "archive_id": aid, "target": target})
        elif metadata(path.read_text()).get("archive_id", "").strip() != aid:
            mismatches.append({"line": n, "registry_id": aid,
                               "file_id": metadata(path.read_text()).get("archive_id"),
                               "target": target})

    refs = []
    paths = sorted((ROOT / "core").glob("*.md")) + sorted((ROOT / "ecosystem").glob("*.html"))
    for path in paths:
        text = path.read_text()
        rel = path.relative_to(ROOT).as_posix()
        inputs[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
        for n, line in enumerate(text.splitlines(), 1):
            for aid in sorted(set(ID.findall(line))):
                refs.append({"path": rel, "line": n, "archive_id": aid,
                             "targets": index.get(aid, []), "excerpt": line.strip()[:300]})

    tracked_assets = [p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*")
                      if p.is_file() and p.suffix.lower() in
                      {".blend", ".glb", ".gltf", ".fbx", ".obj", ".stl", ".step", ".stp"}
                      and not any(part in {".git", ".venv", "node_modules"} for part in p.parts)]
    return {
        "scope": "Current local checkout; metadata audit, not semantic or engineering certification",
        "limits": ["ID year can differ from revised document year; epoch findings require review",
                   "Existing reference target does not prove its title/content matches",
                   "Reference ranges are not expanded; parser reads single-line top-level metadata only",
                   "Model inventory covers local files, not remote storage or external applications"],
        "counts": {"writing_documents_with_id": len(documents), "unique_ids": len(index),
                   "registry_rows": len(rows), "reference_occurrences": len(refs)},
        "duplicate_ids": {k: v for k, v in index.items() if len(v) > 1},
        "registry_file_id_mismatches": mismatches,
        "registry_missing_targets": missing_targets,
        "unregistered_writing_ids": sorted(set(index) - set(rows)),
        "epoch_review_candidates": candidates,
        "thread_namespace_occurrences": dict(sorted(namespaces.items())),
        "local_model_files": sorted(tracked_assets),
        "references": refs,
        "input_sha256": dict(sorted(inputs.items())),
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
