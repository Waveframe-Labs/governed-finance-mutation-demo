"""
---
title: "Finance Mutation Demo Runner"
filetype: "source"
type: "execution"
domain: "demo"
version: "0.6.0"
status: "Active"
created: "2026-03-19"
updated: "2026-04-01"

author:
  name: "Shawn C. Wright"

maintainer:
  name: "Waveframe Labs"

license: "Apache-2.0"

ai_assisted: "partial"

anchors:
  - "Finance-Mutation-Demo-Runner-v0.6.0"
---
"""

from pathlib import Path
import json
from typing import Any, Dict

from cricore.interface.governed_execute import governed_execute

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

def load_policy() -> Dict[str, Any]:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def describe_scenario(run_name: str) -> dict[str, str]:
    if "blocked" in run_name:
        return {
            "title": "Unauthorized Financial Action",
            "action": "AI attempts to reallocate $2M from Marketing → Operations",
            "unsafe_outcome": "Funds are reallocated without independent approval.",
        }

    return {
        "title": "Authorized Financial Action",
        "action": "AI proposes reallocation with independent approval.",
        "unsafe_outcome": "Funds are reallocated.",
    }


def execute_mutation(proposal: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "status": "executed",
        "mutation": proposal.get("requested_mutation"),
    }


def extract_human_reason(result: Any) -> list[str]:
    reasons: list[str] = []

    for stage in result.stage_results:
        if not stage.passed:
            if stage.stage_id == "independence":
                reasons.append(
                    "Same individual attempted to propose and approve (role separation violation)"
                )
            elif stage.stage_id == "publication-commit":
                continue
            else:
                reasons.append(f"Failed at stage: {stage.stage_id}")

    if not reasons:
        reasons.append("Unknown validation failure")

    return reasons


# -----------------------------
# Unsafe Execution Path
# -----------------------------

def unsafe_execute(run_name: str, proposal_builder) -> Dict[str, Any]:
    proposal = proposal_builder()
    execution_result = execute_mutation(proposal)

    scenario = describe_scenario(run_name)

    print("\n" + "=" * 50)
    print(f"UNSAFE PATH: {scenario['title']}")
    print("=" * 50)

    print("\nAction:")
    print(scenario["action"])

    print("\nResult:")
    print("⚠️ EXECUTED WITHOUT GOVERNANCE")

    print("\nOutcome:")
    print(f"- {scenario['unsafe_outcome']}")
    print("- No admissibility check was performed")
    print("- No enforced execution boundary was present")

    print("\nExecution Result:")
    print(execution_result)

    return execution_result


# -----------------------------
# Governed Execution Path
# -----------------------------

def governed_execute_demo(run_name: str, proposal_builder, policy: Dict[str, Any]) -> Dict[str, Any]:
    proposal = proposal_builder()
    governed_result = governed_execute(
        proposal=proposal,
        policy=policy,
        execute_fn=execute_mutation,
    )

    scenario = describe_scenario(run_name)

    print("\n" + "=" * 50)
    print(f"GOVERNED PATH: {scenario['title']}")
    print("=" * 50)

    print("\nAction:")
    print(scenario["action"])

    print("\nResult:")
    print("✅ ALLOWED" if governed_result["commit_allowed"] else "❌ BLOCKED")

    print("\nReason:")
    if governed_result["commit_allowed"]:
        print("- Required roles satisfied")
        print("- Independent approval verified")
        print("- Execution was permitted only after CRI-CORE validation")
    else:
        reasons = extract_human_reason(governed_result["result"])
        for reason in reasons:
            print(f"- {reason}")

    print("\nOutcome:")
    if governed_result["blocked"]:
        print("- Execution did not occur")
        print("- The action was stopped at the mutation boundary")
    else:
        print("- Execution occurred only after CRI-CORE allowed it")
        print("- The mutation remained inside the governed path")

    print("\nExecution Result:")
    print(governed_result["execution_result"])

    print("\n[Technical Details]")
    for stage in governed_result["result"].stage_results:
        status = "PASS" if stage.passed else "FAIL"
        print(f"{stage.stage_id}: {status}")
        for message in stage.messages:
            print(f"  → {message}")

    return governed_result


# -----------------------------
# Main
# -----------------------------

def main():
    print("\nRunning finance mutation demo...")
    policy = load_policy()

    print("\n" + "=" * 50)
    print("SCENARIO 1 COMPARISON")
    print("=" * 50)
    print("Unauthorized financial action")
    unsafe_execute("blocked-run", build_blocked_proposal)
    blocked_result = governed_execute_demo("blocked-run", build_blocked_proposal, policy)

    print("\n" + "=" * 50)
    print("SCENARIO 2 COMPARISON")
    print("=" * 50)
    print("Authorized financial action")
    unsafe_execute("allowed-run", build_allowed_proposal)
    allowed_result = governed_execute_demo("allowed-run", build_allowed_proposal, policy)

    print("\n" + "=" * 50)
    print("FINAL TAKEAWAY")
    print("=" * 50)

    if blocked_result["blocked"] and allowed_result["commit_allowed"]:
        print("Without CRI-CORE, both actions execute.")
        print("With CRI-CORE, the unauthorized action is blocked and the authorized action is allowed.")
        print("Execution is no longer optional validation. It is governed at the mutation boundary.")
    else:
        print("Demo completed, but one or more scenarios did not produce the expected outcome.")


if __name__ == "__main__":
    main()