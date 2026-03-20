"""
---
title: "Proposal Inspection Script"
filetype: "source"
type: "utility"
domain: "demo-debug"
version: "0.1.0"
status: "Active"
created: "2026-03-19"
updated: "2026-03-19"

author:
  name: "Shawn C. Wright"
  email: "swright@waveframelabs.org"

maintainer:
  name: "Waveframe Labs"
  url: "https://waveframelabs.org"

license: "Apache-2.0"

ai_assisted: "partial"

anchors:
  - "Proposal-Inspection-Script-v0.1.0"
---
"""

from pathlib import Path
import json

from proposal_normalizer import build_proposal


def main():

    artifact_path = Path("scratch/artifact.json")
    artifact_path.parent.mkdir(parents=True, exist_ok=True)

    artifact_path.write_text(
        json.dumps(
            {
                "type": "financial_decision",
                "amount": 2000000
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
        "hash": "test-hash",
    }

    actor = {
        "id": "ai-system",
        "type": "agent",
        "declared_role": "proposer",
    }

    run_context = {
        "responsible": "finance_manager",
        "accountable": "finance_manager",
    }

    proposal = build_proposal(
        proposal_id="demo-proposal-001",
        actor=actor,
        artifact_paths=[str(artifact_path)],
        mutation=mutation,
        contract=contract,
        run_context=run_context,
    )

    print(json.dumps(proposal, indent=2))


if __name__ == "__main__":
    main()