# Governed Mutation Pipeline Demo (Finance Example)

**An AI system can move $2M without approval — unless something stops it.**

This demo shows a simple but critical problem:

An AI agent proposes a financial change… and executes it in the same workflow.

No separation of roles.  
No required approval.  
No enforcement at the point of action.

**The change just happens.**

---

## What This Demo Shows

This repository demonstrates how to stop that moment before execution.

The same financial action is executed under two conditions:

### ❌ Without proper enforcement
- The AI proposes and approves the change
- Required roles are not satisfied
- The system executes the action anyway  
→ **The budget is updated**

---

### ✅ With enforcement (CRI-CORE)
- Role separation is validated
- Required approvals are enforced
- The system evaluates the action before execution  
→ **The change is blocked before it happens**

---

## What This Is

This is a **deterministic execution control layer**.

It sits at the point where a system attempts to act and decides:

- ✅ allow the change  
- ❌ block it before execution  

No warnings.  
No after-the-fact auditing.  

**The action either happens — or it doesn’t.**

This approach is model-agnostic — it applies to any system that attempts to execute a real-world action.

---

## Scenario: Finance — Budget Reallocation

An AI system proposes reallocating budget between departments.

### Required Roles

* `proposer` → AI system  
* `responsible` → Finance Manager  
* `accountable` → CFO  

### Rule Enforced

**Separation of duties:**

* `responsible` and `accountable` must be **different people**

---

## Demo Runs

### ❌ Blocked Case (Invalid)

Finance Manager is assigned to both roles:

* `responsible`
* `accountable`

**Result:**

```
independence: FAIL
COMMIT BLOCKED
```

**Why it fails:**

One person cannot approve their own financial decision.

---

### ✅ Allowed Case (Valid)

Roles are separated:

* `responsible` → Finance Manager  
* `accountable` → CFO  

**Result:**

```
independence: PASS
COMMIT ALLOWED
```

---

## Expected Output

The demo runs two scenarios:

### ❌ Blocked Scenario

An AI agent attempts to propose and approve the same $2M reallocation.

```
FINAL DECISION:
COMMIT BLOCKED

SCENARIO RESULT

Result: BLOCKED
Outcome:

* No funds were moved
* Unauthorized financial action was stopped before it executed
```

---

### ✅ Allowed Scenario

Proper role separation is enforced.

```
FINAL DECISION:
COMMIT ALLOWED

SCENARIO RESULT

Result: ALLOWED
Outcome:

* Funds were reallocated with proper authorization
* Action executed only after validation
```

---

## How the Pipeline Works

```
Policy (finance_policy.json)
↓
Contract Compiler
↓
Compiled Contract
↓
Proposal Normalization
↓
Structured Run
↓
CRI-CORE Enforcement
↓
Commit Decision (ALLOW / BLOCK)
```

This pipeline turns a proposed change into a **governed execution that must pass validation before it can commit.**

CRI-CORE acts as a **gatekeeper** — a change cannot proceed unless all validation stages pass.

---

## Run the Demo

Install dependencies:

```
pip install -r requirements.txt
```

Run:

```
python -m runner.run_demo
```

---

## How This Would Be Used

**This pipeline is designed to sit directly in front of execution.**

In a real system:

1. An AI (or user) proposes a change  
2. The proposal is normalized into a standard format  
3. A governance contract is applied  
4. CRI-CORE validates the run  
5. The system:

   - allows the change  
   - or blocks it before execution  

This can sit in front of:

* CI/CD pipelines  
* financial systems  
* autonomous agents  
* compliance-critical workflows  

---

## What This Proves

* Unsafe changes can be **stopped before they happen**  
* Governance rules can be **enforced programmatically**  
* Responsibility can be **validated structurally, not assumed**  
* AI systems can be **constrained without removing autonomy**  

---

## Who This Is For

This demo is relevant for:

### Engineering & Platform Teams

* Enforcing constraints at the commit or deployment boundary  
* Preventing invalid system changes from reaching production  

### AI / ML Teams

* Controlling autonomous or semi-autonomous agent behavior  
* Ensuring AI-generated actions meet governance requirements  

### Compliance & Risk Teams

* Enforcing separation of duties and accountability rules  
* Reducing risk in financial or regulated workflows  

### Organizations Deploying AI Systems

* Adding deterministic safeguards before execution  
* Moving from “monitoring” → **enforcement**  

---

## Status

Early-stage demonstration of CRI-CORE enforcement capabilities.

---

<div align="center">
  <sub>© 2026 Waveframe Labs</sub>
</div>