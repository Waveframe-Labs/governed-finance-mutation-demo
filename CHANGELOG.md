# Changelog

## v0.3.0 — Execution Boundary Demonstration

Refined the governed mutation pipeline demo to align with CRI-CORE execution-boundary enforcement and simplify the demo into a minimal, runnable example.

### Added
- Explicit unsafe vs governed execution comparison:
  - UNSAFE PATH (no enforcement)
  - GOVERNED PATH (CRI-CORE enforcement)
- Clear execution outcome framing:
  - allowed vs blocked
  - execution vs non-execution
- Final takeaway emphasizing mutation-boundary control

### Changed
- Replaced validation-oriented language with enforcement / authorization semantics:
  - “validation” → “authorization”
  - “accepted” → “executed”
- Updated runner output to reflect execution control model
- Simplified demo architecture:
  - removed dependency on contract compiler and proposal normalizer
  - direct use of `governed_execute` interface
- Updated README for faster:
  - install → run → understand flow
- Strengthened unsafe vs governed contrast in output

### Improved
- Demo now runs directly against `cricore>=0.12.0` from PyPI
- Reduced setup complexity and external dependencies
- Improved clarity for both:
  - engineers (stage-level output)
  - decision-makers (clear execution outcomes)
- Eliminated terminology drift across:
  - README
  - runner output
  - system behavior

### Behavioral Guarantees Demonstrated
- Unauthorized action → blocked before execution  
- Authorized action → allowed to execute  
- Deterministic enforcement at the mutation boundary  

### Notes
- Demonstration repository (non-production)
- Designed as a minimal, runnable example of execution-boundary enforcement

---

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
- Reframed demo from validation → execution control demonstration
- Updated README to emphasize:
  - real-world failure scenario (AI executing unapproved actions)
  - prevention at execution time (not detection or audit)
- Improved wording for clarity and impact:
  - “accept” → “execute”

### Improved
- Demo output now readable by both:
  - engineers (stage-level output)
  - decision-makers (clear outcomes and consequences)

### Notes
- Demonstration repository (non-production)

---

## v0.1.0

Initial release of governed mutation pipeline demo.

### Includes
- Allowed and blocked finance scenarios
- CRI-CORE enforcement pipeline execution
- Deterministic commit gating demonstration

### Features
- Structural independence validation
- Reproducible enforcement results

### Notes
- Demonstration repository (non-production)