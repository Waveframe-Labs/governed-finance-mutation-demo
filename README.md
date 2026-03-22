# Governed Mutation Pipeline Demo (Finance Example)

Deterministic commit gating for AI-assisted system mutations using CRI-CORE.

This repository demonstrates a **working enforcement pipeline** where a proposed system mutation is either **committed or blocked** based on structural governance constraints.

---

## What You Get

This is a **runnable, end-to-end demo** showing:

- Proposal construction from artifacts
- Contract binding via compiled governance policy
- Run materialization into a verifiable execution unit
- Enforcement through the CRI-CORE kernel
- Deterministic commit decision

**Output is binary and reproducible:**
- ✅ Commit allowed  
- ❌ Commit blocked  

---

## Scenario

**Finance — Budget Reallocation**

An AI system proposes reallocating budget between departments.

### Required roles

- `proposer` — AI system  
- `responsible` — Finance Manager  
- `accountable` — CFO  

### Constraint

- Separation of duties:
  - `responsible` and `accountable` must be **different identities**

---

## Runs Included

### ❌ Blocked Scenario

- Finance Manager assigned to both:
  - `responsible`
  - `accountable`

**Result:**
```
independence: FAIL
COMMIT BLOCKED
```

---

### ✅ Allowed Scenario

- Roles assigned to distinct identities:
  - `responsible` → Finance Manager  
  - `accountable` → CFO  

**Result:**
```
independence: PASS
COMMIT ALLOWED
```

---

## Architecture

```
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
runner (builds run directory)
↓
CRI-CORE enforcement pipeline
↓
commit_allowed (True / False)
```

---

## Setup

Install all dependencies:
```
pip install -r requirements.txt
```

---

## Run the Demo

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

## What This Proves

This demo shows that:

* Governance constraints can be enforced **at execution time**
* Responsibility can be validated **structurally, not by convention**
* Invalid system mutations can be **prevented before commit**

---

## Key Concepts

### Proposal Normalization

Transforms artifacts and mutation intent into a canonical proposal.

### Contract Compilation

Converts governance policy into a deterministic enforcement artifact.

### Run Materialization

Builds a structured execution unit for validation.

### Enforcement Pipeline

CRI-CORE evaluates the run across stages:

* structure
* contract validation
* independence
* integrity
* publication
* commit decision

---

## Where This Applies

* Finance and budget systems
* Enterprise AI workflows
* Autonomous agents
* Compliance-critical environments

---

## Status

Early-stage demonstration of CRI-CORE enforcement capabilities.

---

<div align="center">
  <sub>© 2026 Waveframe Labs</sub>
</div>