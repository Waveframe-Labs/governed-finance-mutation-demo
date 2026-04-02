# Governed Mutation Pipeline Demo (Finance Example)

**An AI system can move $2M without approval — unless something stops it.**

This demo shows a simple but critical problem:

An AI proposes a financial change… and executes it in the same workflow.

No separation of roles.  
No required approval.  
No control at the point of action.

**The change just happens.**

---

## What This Demo Shows

This demo runs the **same financial action twice**:

### ❌ Without enforcement
- The AI proposes and approves the change  
- Required roles are violated  
- The system executes the action anyway  
→ **Funds are reallocated**

---

### ✅ With CRI-CORE enforcement
- Role separation is enforced  
- Required approvals are verified  
- The action is evaluated at the execution boundary  
→ **The change is blocked before it happens**

---

## What This Is

This is a **deterministic execution control layer**.

It sits at the exact point where a system attempts to act and decides:

- ✅ allow execution  
- ❌ block execution  

No warnings.  
No after-the-fact auditing.  

**The action either happens — or it doesn’t.**

---

## Install

```
pip install cricore
```

---

## Run

```
python -m runner.run_demo
```

---

## Scenario: Finance — Budget Reallocation

An AI system proposes reallocating budget between departments.

### Required Roles

* `proposer` → AI system  
* `responsible` → Finance Manager  
* `accountable` → CFO  

### Rule

**Separation of duties:**

`responsible` and `accountable` must be different people.

---

## What Happens

### ❌ Blocked Case (Invalid)

Finance Manager is assigned to both roles.

```
independence: FAIL
COMMIT BLOCKED
```

**Result:**
- No funds are moved  
- The action is stopped at the mutation boundary  

---

### ✅ Allowed Case (Valid)

Roles are properly separated.

```
independence: PASS
COMMIT ALLOWED
```

**Result:**
- Funds are reallocated  
- Execution occurs only after authorization  

---

## Expected Behavior

When you run the demo:

- Without CRI-CORE → both actions execute  
- With CRI-CORE → unauthorized action is blocked  

```
Execution is no longer assumed.
It is explicitly authorized or blocked at the mutation boundary.
```

---

## How It Works

```
Proposed Action
↓
CRI-CORE Enforcement
↓
commit_allowed = true / false
↓
Execution (or no execution)
```

CRI-CORE acts as a **control point**, not a validator.

It determines whether execution is permitted.

---

## Where This Applies

This pattern can be used anywhere a system performs real actions:

- AI agents and autonomous systems  
- financial workflows  
- CI/CD pipelines  
- compliance-critical operations  

---

## What This Proves

- Unsafe actions can be **stopped before execution**  
- Governance rules can be **enforced deterministically**  
- Responsibility can be **verified structurally**  
- AI systems can be **controlled without removing autonomy**  

---

## Who This Is For

**Engineering / Platform Teams**
- Enforce constraints at deployment or commit boundaries  

**AI / ML Teams**
- Control AI-generated actions before execution  

**Compliance / Risk Teams**
- Enforce separation of duties and accountability  

**Organizations deploying AI**
- Move from monitoring → **enforcement**

---

## Status

Demonstration of CRI-CORE as an execution-boundary enforcement layer.

---

<div align="center">
  <sub>© 2026 Waveframe Labs</sub>
</div>
