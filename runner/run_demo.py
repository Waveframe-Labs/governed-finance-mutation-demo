"""
---
title: "Finance Mutation Demo Runner"
filetype: "source"
type: "execution"
domain: "demo"
version: "0.5.0"
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
  - "Finance-Mutation-Demo-Runner-v0.5.0"
---
"""

from datetime import datetime, timezone
from pathlib import Path
import json
import tempfile

from compiler.compile_policy import compile_policy
from cricore.enforcement.execution import run_enforcement_pipeline
from cricore.integrity.finalize import finalize_run_integrity

from scenarios.allowed import build_allowed_proposal
from scenarios.blocked import build_blocked_proposal


# -----------------------------
# Paths
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
# Scenario Mapping
# -----------------------------

def describe_scenario(run_name: str) -> dict:
    if "blocked" in run_name:
        return {
            "title": "Unauthorized Financial Action",
            "action": "AI attempts to reallocate $2M from Marketing → Operations",
        }

    return {
        "title": "Authorized Financial Action",
        "action": "AI proposes reallocation with independent approval",
    }


def extract_human_reason(results) -> list[str]:
    reasons = []

    for r in results:
        if not r.passed:
            if r.stage_id == "independence":
                reasons.append(
                    "Same individual attempted to propose and approve (role separation violation)"
                )
            elif r.stage_id == "publication-commit":
                continue
            else:
                reasons.append(f"Failed at stage: {r.stage_id}")

    if not reasons:
        reasons.append("Unknown validation failure")

    return reasons


# -----------------------------
# Run Construction
# -----------------------------

def build_run(run_name: str, proposal_builder):
    temp_root = Path(tempfile.mkdtemp(prefix="cricore_demo_"))
    run_path = temp_root / run_name
    run_path.mkdir(parents=True)

    (run_path / "validation").mkdir(exist_ok=True)

    policy = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    compiled_contract = compile_policy(policy)

    proposal = proposal_builder()

    contract_hash = compiled_contract.get("contract_hash", "MISSING_HASH")
    proposal["contract"]["hash"] = contract_hash

    write_json(
        run_path / "contract.json",
        {
            "run_id": run_name,
            "contract_id": policy["contract_id"],
            "contract_version": policy["contract_version"],
            "contract_hash": contract_hash,
            "created_utc": utc_now(),
        },
    )

    write_json(run_path / "compiled_contract.json", compiled_contract)
    write_json(run_path / "proposal.json", proposal)

    (run_path / "report.md").write_text("# Demo Report\n", encoding="utf-8")

    write_json(
        run_path / "approval.json",
        {
            "approved_by": "cfo",
            "timestamp": utc_now(),
        },
    )

    write_json(
        run_path / "randomness.json",
        {
            "seed": 42,
        },
    )

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

    scenario = describe_scenario(run_name)

    print("\n" + "=" * 50)
    print(f"SCENARIO: {scenario['title']}")
    print("=" * 50)

    print("\nAction:")
    print(scenario["action"])

    print("\nResult:")
    print("✅ ALLOWED" if commit_allowed else "❌ BLOCKED")

    print("\nReason:")
    if commit_allowed:
        print("- Required roles satisfied")
        print("- Independent approval verified")
    else:
        reasons = extract_human_reason(results)
        for reason in reasons:
            print(f"- {reason}")

    print("\n" + "-" * 50)

    print("\n[Technical Details]")
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        print(f"{r.stage_id}: {status}")
        for m in r.messages:
            print(f"  → {m}")

    return commit_allowed


# -----------------------------
# Main
# -----------------------------

def main():
    print("\nRunning finance mutation demo...")

    blocked = execute_run("blocked-run", build_blocked_proposal)
    allowed = execute_run("allowed-run", build_allowed_proposal)

    print("\n" + "=" * 50)
    print("FINAL TAKEAWAY")
    print("=" * 50)

    if not blocked and allowed:
        print("System correctly blocked an unauthorized financial action and allowed a properly authorized one.")
    else:
        print("Demo completed, but one or more scenarios did not produce the expected outcome.")


if __name__ == "__main__":
    main()