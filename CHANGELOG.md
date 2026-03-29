# Changelog

## v0.2.0

Refined governed mutation pipeline demo with improved narrative clarity, execution framing, and human-readable output.

### Added
- Human-readable scenario layer:
  - SCENARIO descriptions
  - SCENARIO RESULT summaries
  - Outcome explanations for each run
- Explicit AI-driven action framing in demo output
- Clear distinction between blocked vs allowed execution paths

### Changed
- Reframed demo from technical validation → execution control demonstration
- Updated README to emphasize:
  - real-world failure scenario (AI executing unapproved actions)
  - prevention at execution time (not detection or audit)
- Improved wording for clarity and impact:
  - “accept” → “execute”
  - stronger execution-boundary emphasis

### Improved
- Demo output now readable by both:
  - engineers (stage-level validation)
  - decision-makers (clear outcomes and consequences)
- Strengthened alignment between:
  - README narrative
  - runner output
  - actual system behavior

### Existing Capabilities (unchanged)
- Allowed and blocked finance scenarios
- Proposal normalization integration
- Contract binding and compiled contract usage
- CRI-CORE enforcement pipeline execution
- Deterministic commit gating

### Features
- Structural independence validation
- End-to-end run materialization
- Reproducible enforcement results

### Notes
- Demonstration repository (non-production)
- Requires external CRI-CORE ecosystem packages
  
---

## v0.1.0

Initial release of governed mutation pipeline demo.

Includes:
- Allowed and blocked finance scenarios
- Proposal normalization integration
- Contract binding and compiled contract usage
- CRI-CORE enforcement pipeline execution
- Deterministic commit gating demonstration

Features:
- Structural independence validation
- End-to-end run materialization
- Reproducible enforcement results

Notes:
- Demonstration repository (non-production)
- Requires external CRI-CORE ecosystem packages