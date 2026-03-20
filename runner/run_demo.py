"""
---
title: "Finance Mutation Demo Runner"
filetype: "source"
type: "execution"
domain: "demo"
version: "0.1.0"
status: "Active"
created: "2026-03-19"
updated: "2026-03-19"

author:
  name: "Shawn C. Wright"

maintainer:
  name: "Waveframe Labs"

license: "Apache-2.0"

ai_assisted: "partial"

anchors:
  - "Finance-Mutation-Demo-Runner-v0.1.0"
---
"""

import json
from pathlib import Path
import shutil

from cricore.enforcement.execution import run_enforcement_pipeline
from compiler.compile_policy import compile_policy

from scenarios.blocked import build_blocked_proposal
from scenarios.allowed import build_allowed_proposal


BASE_RUN_PATH = Path("runs")


def write_json(path: Path, data: dict):
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def build_run(run_name: str, proposal_builder):

    run_path = BASE_RUN_PATH / run_name

    if run_path.exists():
        shutil.rmtree(run_path)

    run_path.mkdir(parents=True)

    # --- 1. Compile policy
    policy = json.loads(Path("contracts/finance_policy.json").read_text())

    compiled_contract = compile_policy(policy)

    # --- 2. Build proposal
    proposal = proposal_builder()

    # --- 3. Extract contract hash
    contract_hash = compiled_contract.get("contract_hash", "MISSING_HASH")

    contract_declaration = {
        "id": policy["contract_id"],
        "version": policy["contract_version"],
        "hash": contract_hash
    }

    # Inject correct contract reference into proposal
    proposal["contract"]["hash"] = contract_hash

    # --- 4. Write required files
    write_json(run_path / "contract.json", contract_declaration)
    write_json(run_path / "compiled_contract.json", compiled_contract)
    write_json(run_path / "proposal.json", proposal)

    # Minimal required artifacts
    (run_path / "report.md").write_text("# Demo Report\n", encoding="utf-8")
    write_json(run_path / "approval.json", {"status": "approved"})
    write_json(run_path / "randomness.json", {"seed": 42})

    # Placeholder hash file (will pass only if kernel doesn’t enforce strict integrity yet)
    (run_path / "SHA256SUMS.txt").write_text("", encoding="utf-8")

    return run_path, proposal


def execute_run(run_name: str, proposal_builder):

    run_path, proposal = build_run(run_name, proposal_builder)

    results, commit_allowed = run_enforcement_pipeline(
        run_path=str(run_path),
        run_context=proposal.get("run_context", {})
    )

    print("\n" + "=" * 50)
    print(f"RUN: {run_name}")
    print("=" * 50)

    for r in results:
        status = "PASS" if r.passed else "FAIL"
        print(f"{r.stage_id}: {status}")
        if not r.passed and r.reason:
            print(f"  → {r.reason}")

    print("\nFINAL DECISION:")
    print("COMMIT ALLOWED" if commit_allowed else "COMMIT BLOCKED")

    return commit_allowed


def main():

    print("\nRunning BLOCKED scenario...")
    blocked = execute_run("blocked-run", build_blocked_proposal)

    print("\nRunning ALLOWED scenario...")
    allowed = execute_run("allowed-run", build_allowed_proposal)

    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)

    print(f"Blocked scenario → {'FAILED (correct)' if not blocked else 'ERROR'}")
    print(f"Allowed scenario → {'PASSED (correct)' if allowed else 'ERROR'}")


if __name__ == "__main__":
    main()