"""
---
title: "Blocked Finance Mutation Scenario"
filetype: "source"
type: "scenario"
domain: "finance"
version: "0.1.0"
status: "Active"
created: "2026-03-19"
updated: "2026-03-20"

author:
  name: "Shawn C. Wright"

maintainer:
  name: "Waveframe Labs"

license: "Apache-2.0"

ai_assisted: "partial"

anchors:
  - "Finance-Mutation-Blocked-Scenario-v0.1.0"
---
"""

from pathlib import Path
import json

from proposal_normalizer import build_proposal


def build_blocked_proposal():

    artifact_path = Path("scenarios/blocked_artifact.json")
    artifact_path.parent.mkdir(parents=True, exist_ok=True)

    artifact_path.write_text(
        json.dumps(
            {
                "type": "financial_decision",
                "amount": 2000000,
                "currency": "USD",
                "from": "Marketing",
                "to": "Operations",
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    mutation = {
        "domain": "finance",
        "resource": "budget",
        "action": "reallocate",
    }

    contract = {
        "id": "finance-raci",
        "version": "0.1.0",
        "hash": "PLACEHOLDER_HASH",
    }

    actor = {
        "id": "ai-system",
        "type": "agent",
        "declared_role": "proposer",
    }

    # ❌ VIOLATION: same identity for responsible + accountable
    run_context = {
        "identities": {
            "required_roles": [
                "proposer",
                "responsible",
                "accountable",
            ],
            "actors": [
                {
                    "id": "ai-system",
                    "type": "agent",
                    "role": "proposer",
                },
                {
                    "id": "finance_manager",
                    "type": "human",
                    "role": "responsible",
                },
                {
                    "id": "finance_manager",  # ← VIOLATION
                    "type": "human",
                    "role": "accountable",
                },
            ],
            "conflict_flags": {},
        },
        "integrity": {
            "hashes_provided": True,
        },
        "publication": {
            "channel": "internal",
            "authorized": True,
        },
    }

    return build_proposal(
        proposal_id="blocked-proposal",
        actor=actor,
        artifact_paths=[str(artifact_path)],
        mutation=mutation,
        contract=contract,
        run_context=run_context,
    )