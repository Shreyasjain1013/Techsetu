## SHARED PROJECT CONTEXT — STATUS.md

`docs/STATUS.md` is the project's continuously updated working-state file.

Every agent MUST read `docs/STATUS.md` before beginning a major task.

Every agent MUST update `docs/STATUS.md` after completing a major task or whenever a material project-state change occurs.

`docs/STATUS.md` must concisely contain:

- Current goal
- Active subtasks and their status
- Important decisions and technical reasoning
- Files modified
- Current blockers and risks
- Agent handoffs
- Next recommended action

Use:

- `[ ]` Not started
- `[~]` In progress
- `[x]` Completed
- `[!]` Blocked

Do not use `STATUS.md` as a diary.

Record only information that another agent needs to understand the current project state and continue work without relying on previous chat history.

Never rely exclusively on conversation history for project context.

Before starting work, inspect the current project state.

After completing work, verify the result and update `STATUS.md`.

If a decision changes the project's requirements, architecture, database, API, user flow, or AI behavior, update the relevant permanent documentation as well.

`STATUS.md` records current project state; it does not replace permanent documentation.