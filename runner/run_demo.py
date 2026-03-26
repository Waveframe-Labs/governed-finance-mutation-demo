"""
---
title: "Finance Mutation Demo Runner"
filetype: "source"
type: "execution"
domain: "demo"
version: "0.2.0"
status: "Active"
created: "2026-03-19"
updated: "2026-03-26"

author:
  name: "Shawn C. Wright"

maintainer:
  name: "Waveframe Labs"

license: "Apache-2.0"

ai_assisted: "partial"

anchors:
  - "Finance-Mutation-Demo-Runner-v0.2.0"
---
"""

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from compiler.compile_policy import compile_policy
from cricore.enforcement.execution import run_enforcement_pipeline

from scenarios.allowed import build_allowed_proposal
from scenarios.blocked import build_blocked_proposal


BASE_RUN_PATH = Path("runs")


# -----------------------------
# Utilities
# -----------------------------

def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


# -----------------------------
# Scenario Interpretation Layer
# -----------------------------

def extract_failure_reason(results) -> list:
    reasons = []

    for r in results:
        if not r.passed:
            if r.stage_id == "independence":
                reasons.append(
                    "Same individual attempted to propose and approve the financial action (violates role separation)"
                )
            elif r.stage_id == "publication-commit":
                continue  # handled implicitly
            else:
                reasons.append(f"Failed at stage: {r.stage_id}")

    if not reasons:
        reasons.append("Unknown validation failure")

    return reasons


def print_scenario_result(commit_allowed: bool, results):

    action_description = "Reallocate $2M from Marketing → Operations"

    print("\n" + "=" * 50)
    print("SCENARIO RESULT")
    print("=" * 50)

    print(f"Action: {action_description}\n")

    if commit_allowed:
        print("Result: ALLOWED\n")

        print("Reason:")
        print("- Required roles were satisfied")
        print("- Independent approval was present\n")

        print("Outcome:")
        print("- Funds were reallocated with proper authorization")
        print("- Action executed only after validation\n")

    else:
        reasons = extract_failure_reason(results)

        print("Result: BLOCKED\n")

        print("Reason:")
        for r in reasons:
            print(f"- {r}")

        print("\nOutcome:")
        print("- No funds were moved")
        print("- Unauthorized financial action prevented before execution")
        print("- Required approval conditions were not met\n")


# -----------------------------
# Run Construction
# -----------------------------

def build_run(run_name: str, proposal_builder):

    run_path = BASE_RUN_PATH / run_name

    if run_path.exists():
        shutil.rmtree(run_path)

    run_path.mkdir(parents=True)

    validation_path = run_path / "validation"
    validation_path.mkdir(exist_ok=True)
    write_json(validation_path / "structure.json", {"status": "placeholder"})

    policy = json.loads(
        Path("contracts/finance_policy.json").read_text(encoding="utf-8")
    )
    compiled_contract = compile_policy(policy)

    proposal = proposal_builder()

    contract_hash = compiled_contract.get("contract_hash", "MISSING_HASH")

    contract_declaration = {
        "run_id": run_name,
        "contract_id": policy["contract_id"],
        "contract_version": policy["contract_version"],
        "contract_hash": contract_hash,
        "created_utc": utc_now(),
    }

    proposal["contract"]["hash"] = contract_hash

    contract_path = run_path / "contract.json"
    compiled_contract_path = run_path / "compiled_contract.json"
    proposal_path = run_path / "proposal.json"
    report_path = run_path / "report.md"
    approval_path = run_path / "approval.json"
    randomness_path = run_path / "randomness.json"
    sha_path = run_path / "SHA256SUMS.txt"

    write_json(contract_path, contract_declaration)
    write_json(compiled_contract_path, compiled_contract)
    write_json(proposal_path, proposal)

    report_path.write_text("# Demo Report\n", encoding="utf-8")

    write_json(
        approval_path,
        {
            "approved_by": "cfo",
            "timestamp": utc_now(),
        },
    )

    write_json(
        randomness_path,
        {
            "seed": 42,
        },
    )

    contract_sha = sha256_file(contract_path)

    sha_path.write_text(
        f"{contract_sha} contract.json\n",
        encoding="utf-8",
    )

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

        if not r.passed:
            messages = getattr(r, "messages", None)
            if messages:
                for m in messages:
                    print(f"  → {m}")
            else:
                print("  → No details provided")

    print("\nFINAL DECISION:")
    print("COMMIT ALLOWED" if commit_allowed else "COMMIT BLOCKED")

    # 🔥 NEW LAYER
    print_scenario_result(commit_allowed, results)

    return commit_allowed


# -----------------------------
# Main
# -----------------------------

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
    