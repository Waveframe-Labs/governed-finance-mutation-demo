"""
---
title: "Finance Mutation Demo Runner"
filetype: "source"
type: "execution"
domain: "demo"
version: "0.4.0"
status: "Active"
created: "2026-03-19"
updated: "2026-03-31"

author:
  name: "Shawn C. Wright"

maintainer:
  name: "Waveframe Labs"

license: "Apache-2.0"

ai_assisted: "partial"

anchors:
  - "Finance-Mutation-Demo-Runner-v0.4.0"
---
"""

from datetime import datetime, timezone
from pathlib import Path
import json
import shutil
import tempfile

from compiler.compile_policy import compile_policy
from cricore.enforcement.execution import run_enforcement_pipeline
from cricore.integrity.finalize import finalize_run_integrity

from scenarios.allowed import build_allowed_proposal
from scenarios.blocked import build_blocked_proposal


# -----------------------------
# Paths (SAFE)
# -----------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent
CONTRACT_PATH = ROOT_DIR / "contracts" / "finance_policy.json"


# -----------------------------
# Utilities
# -----------------------------

def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# -----------------------------
# Run Construction
# -----------------------------

def build_run(run_name: str, proposal_builder):

    # 🔥 use temp dir instead of repo runs/
    temp_root = Path(tempfile.mkdtemp(prefix="cricore_demo_"))
    run_path = temp_root / run_name
    run_path.mkdir(parents=True)

    (run_path / "validation").mkdir(exist_ok=True)

    policy = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    compiled_contract = compile_policy(policy)

    proposal = proposal_builder()

    contract_hash = compiled_contract.get("contract_hash", "MISSING_HASH")
    proposal["contract"]["hash"] = contract_hash

    # -----------------------------
    # Core artifacts
    # -----------------------------

    write_json(run_path / "contract.json", {
        "run_id": run_name,
        "contract_id": policy["contract_id"],
        "contract_version": policy["contract_version"],
        "contract_hash": contract_hash,
        "created_utc": utc_now(),
    })

    write_json(run_path / "compiled_contract.json", compiled_contract)
    write_json(run_path / "proposal.json", proposal)

    (run_path / "report.md").write_text("# Demo Report\n", encoding="utf-8")

    write_json(run_path / "approval.json", {
        "approved_by": "cfo",
        "timestamp": utc_now(),
    })

    write_json(run_path / "randomness.json", {
        "seed": 42,
    })

    # -----------------------------
    # FINALIZE (single point)
    # -----------------------------

    finalize_run_integrity(run_path)

    return run_path, proposal


# -----------------------------
# Execution
# -----------------------------

def execute_run(run_name: str, proposal_builder):

    run_path, proposal = build_run(run_name, proposal_builder)

    results, commit_allowed = run_enforcement_pipeline(
        run_path=str(run_path),
        run_context=proposal.get("run_context", {}),
    )

    print("\n" + "=" * 50)
    print(f"RUN: {run_name}")
    print("=" * 50)

    for r in results:
        status = "PASS" if r.passed else "FAIL"
        print(f"{r.stage_id}: {status}")
        for m in r.messages:
            print(f"  → {m}")

    print("\nFINAL DECISION:")
    print("COMMIT ALLOWED" if commit_allowed else "COMMIT BLOCKED")

    return commit_allowed


# -----------------------------
# Main
# -----------------------------

def main():
    execute_run("blocked-run", build_blocked_proposal)
    execute_run("allowed-run", build_allowed_proposal)


if __name__ == "__main__":
    main()