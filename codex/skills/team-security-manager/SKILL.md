---
name: team-security-manager
description: Use for threat modeling and security review around auth, permissions, secrets, user input, shell execution, external integrations, data handling, and supply-chain or abuse risk.
---

# Team Security Manager

Use when:
- the change touches trust boundaries,
- secrets or credentials are involved,
- auth, permissions, payments, or external APIs changed,
- untrusted input, shell execution, or filesystem access is involved.

## First Steps

1. Read `AGENTS.md` and `team/config.yaml` if present.
2. Read the active work packet, design brief, and touched code.
3. Read `references/security-checklist.md`.

## Workflow

1. Identify assets, entry points, actors, and trust boundaries.
2. Check authn/authz, secret exposure, injection paths, data leakage, insecure defaults, and dependency risk.
3. Decide whether the system fails open or closed on errors.
4. Produce concrete mitigations and missing-validation notes.

## Output

Return:
- severity-ordered findings,
- attack or failure path,
- fail-open or fail-closed assessment,
- concrete mitigations,
- what still needs validation.

## Guardrails

- Prefer fail-closed recommendations.
- Do not accept “internal only” as a blanket safety argument.
- Flag missing validation for risky surfaces.
