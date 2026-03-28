# Operating Loop

## Baseline Loop

1. Human provides the brief.
2. Codex clarifies the objective and updates the active backlog item.
3. Codex and Claude refine architecture until the design is ready enough to execute.
4. Codex issues or approves a bounded work packet.
5. Claude runs the execution chain:
   - research if needed,
   - design refinement,
   - implementation,
   - security, performance, or UX evaluation when needed,
   - independent review.
6. Claude updates reports, handoff state, and durable memory.
7. Codex reviews the result.
8. If feedback exists, Codex sends another cycle.
9. If approved, Codex chooses the next work packet or closes the milestone.

## Delegation Heuristics

Delegate when:
- the task is bounded,
- the output contract is clear,
- file ownership is disjoint,
- local work can continue while the task runs.

Do not delegate when:
- the next action is blocked on that answer,
- the scope is too entangled to specify well,
- the only likely output is a vague opinion.

## Repair Loop

Use a closed loop:
1. detect failure,
2. identify the narrow cause,
3. patch the smallest coherent fix,
4. rerun the narrowest meaningful validation,
5. rerun broader gates only if needed,
6. update the work log if the failure taught something durable.

## Gate Discipline

Each work packet should move through these checkpoints:
- ready for implementation,
- validation evidence collected,
- review complete,
- Codex decision recorded.
