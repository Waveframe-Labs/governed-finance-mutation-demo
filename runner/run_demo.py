"""
---
title: "Finance Mutation Demo Runner"
filetype: "source"
type: "execution"
domain: "demo"
version: "0.3.1"
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
  - "Finance-Mutation-Demo-Runner-v0.3.1"
---
"""

from datetime import datetime, timezone
from pathlib import Path
import json
import shutil

from compiler.compile_policy import compile_policy
from cricore.enforcement.execution import run_enforcement_pipeline

from cricore.integrity.finalize import finalize_run_integrity

from scenarios.allowed import build_allowed_proposal
from scenarios.blocked import build_blocked_proposal


BASE_RUN_PATH = Path("runs")


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def build_run(run_name: str, proposal_builder):

    run_path = BASE_RUN_PATH / run_name

    if run_path.exists():
        shutil.rmtree(run_path)

    run_path.mkdir(parents=True)

    # -----------------------------
    # Base structure
    # -----------------------------
    (run_path / "validation").mkdir(exist_ok=True)

    policy = json.loads(
        Path("contracts/finance_policy.json").read_text(encoding="utf-8")
    )
    compiled_contract = compile_policy(policy)

    proposal = proposal_builder()

    contract_hash = compiled_contract.get("contract_hash", "MISSING_HASH")

    proposal["contract"]["hash"] = contract_hash

    # -----------------------------
    # Write core artifacts
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
    # 🔥 CRITICAL: finalize integrity ONCE
    # -----------------------------
    finalize_run_integrity(run_path)

    return run_path, proposal


def execute_run(run_name: str, proposal_builder):

    run_path, proposal = build_run(run_name, proposal_builder)

    results, commit_allowed = run_enforcement_pipeline(
        run_path=str(run_path),
        run_context=proposal.get("run_context", {}),
    )

    print(f"\nRUN: {run_name}")

    for r in results:
        status = "PASS" if r.passed else "FAIL"
        print(f"{r.stage_id}: {status}")
        for m in r.messages:
            print(f"  → {m}")

    print("\nFINAL DECISION:")
    print("COMMIT ALLOWED" if commit_allowed else "COMMIT BLOCKED")

    return commit_allowed


def main():
    execute_run("blocked-run", build_blocked_proposal)
    execute_run("allowed-run", build_allowed_proposal)


if __name__ == "__main__":
    main()