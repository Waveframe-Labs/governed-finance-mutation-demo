# Governed Mutation Pipeline Demo (Finance Example)

Deterministic commit gating for AI-assisted system mutations using CRI-CORE.

This demo shows how a proposed system mutation is:

1. Constructed from artifacts  
2. Bound to a governance contract  
3. Materialized into a run  
4. Evaluated by the CRI-CORE enforcement kernel  
5. Deterministically accepted or rejected  

---

## What This Demonstrates

This is a **full pipeline demo**, not a static case study.

It proves that:

- A mutation proposal can be **programmatically constructed**
- Governance constraints can be **bound via a compiled contract**
- Enforcement can be applied **at the commit boundary**
- The system produces a **deterministic decision**:
  - ✅ Commit allowed  
  - ❌ Commit blocked  

---

## Scenario

**Finance — Budget Reallocation**

An AI system proposes reallocating budget between departments.

### Required roles:

- `proposer` — AI system  
- `responsible` — Finance Manager  
- `accountable` — CFO  

### Constraint:

- Separation of duties:
  - `responsible` and `accountable` **must be different identities**

---

## Runs Included

### ❌ Blocked Scenario

- Finance Manager is both:
  - `responsible`
  - `accountable`

**Result:**

```
independence: FAIL
COMMIT BLOCKED
```

---

### ✅ Allowed Scenario

- Roles are assigned to distinct identities:
  - `responsible` → Finance Manager  
  - `accountable` → CFO  

**Result:**

```
independence: PASS
COMMIT ALLOWED
```

---

## Architecture

contracts/finance_policy.json
↓
contract compiler
↓
compiled_contract.json
↓
proposal_normalizer
↓
proposal.json
↓
runner → builds run directory
↓
CRI-CORE kernel
↓
commit_allowed (True / False)

---

## How to Run

```
python -m runner.run_demo
```

---

## Expected Output

```
Running BLOCKED scenario...

independence: FAIL
COMMIT BLOCKED

Running ALLOWED scenario...

independence: PASS
COMMIT ALLOWED
```

---

## Key Concepts

### 1. Proposal Normalization

Transforms artifacts and mutation intent into a canonical proposal structure.

### 2. Contract Compilation

Converts governance policy into a deterministic enforcement artifact.

### 3. Run Materialization

Assembles all required artifacts into a verifiable execution unit.

### 4. Enforcement Pipeline

CRI-CORE evaluates the run across ordered stages:

* structure
* contract validation
* independence
* integrity
* publication
* commit decision

---

## Why This Matters

In real systems, AI recommendations often lack enforceable accountability.

This demo shows how to:

* Prevent invalid decisions from being committed
* Enforce role separation structurally
* Provide deterministic governance at execution time

---

## Positioning

This repository demonstrates:

* AI governance enforcement at runtime
* Deterministic decision systems
* Structured responsibility validation

Applicable to:

* Finance workflows
* Enterprise AI systems
* Autonomous agent governance
* Compliance-critical decision systems

---

## Status

Active development — early system demonstration of CRI-CORE enforcement capabilities.

---

<div align="center">
  <sub>© 2026 Waveframe Labs — Independent Open-Science Research Entity</sub>
</div>