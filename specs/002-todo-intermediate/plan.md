# Implementation Plan: Intermediate Todo Features

**Branch**: `002-todo-intermediate` | **Date**: 2026-02-15 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-todo-intermediate/spec.md`

## Summary

Extend the existing Basic Level console todo app with five organization features: task priorities (high/medium/low), tags/categories, keyword search, filtering, and sorting. The implementation modifies three existing files (`models.py`, `storage.py`, `cli.py`) and updates `main.py` with new menu options. All Basic features remain backward-compatible. Storage stays in-memory; only Python stdlib is used.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Python standard library only (`dataclasses`, `datetime`, `enum`, `typing`)
**Storage**: In-memory (dict-based, extending existing `InMemoryStorage`)
**Testing**: Manual console testing + pytest (`test_app.py` exists)
**Target Platform**: Console / CLI (cross-platform)
**Project Type**: Single project
**Performance Goals**: All operations complete instantly (in-memory, <100 tasks typical)
**Constraints**: No external libraries, no persistence, no colors/rich formatting
**Scale/Scope**: Single-user console app, <1000 tasks in-memory

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Three-Level Evolution | PASS | Building Intermediate on completed Basic |
| II. 100% Agentic & Spec-Driven | PASS | Using /sp.specify → /sp.plan → /sp.tasks flow |
| III. Tech Stack (Python 3.13+, UV, stdlib) | PASS | No new dependencies needed |
| IV. Extensible Architecture | PASS | Modular design: models → storage → cli → main |
| V. Storage Progression (in-memory) | PASS | Storage remains in-memory for Intermediate |
| VI. Clean Python Standards | PASS | PEP 8, type hints, docstrings, error handling planned |
| No Global Variables | PASS | Using class instances (InMemoryStorage, CLI) |
| Traceability | PASS | Spec, plan, PHRs all maintained |
| Sequential Level Completion | PASS | Basic Level code exists and is complete |

All gates pass. No violations.

## Project Structure

### Documentation (this feature)

```text
specs/002-todo-intermediate/
├── plan.md              # This file
├── research.md          # Phase 0: technology decisions
├── data-model.md        # Phase 1: updated entity model
├── quickstart.md        # Phase 1: dev setup guide
└── tasks.md             # Phase 2 output (/sp.tasks - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── main.py              # CLI entry point — add menu options 7-11 for new features
├── models.py            # Task dataclass — add Priority enum, priority field, tags field, created_at field
├── storage.py           # InMemoryStorage — add search, filter, sort methods
└── cli.py               # CLI class — add search, filter, sort commands + update add/update/view
```

**Structure Decision**: Retain existing flat `src/` layout. No new files needed — all changes extend existing modules. This minimizes diff size and preserves the Basic Level architecture.

## Architecture

### Component Diagram

```text
┌─────────────────────────────────────────────────┐
│                   main.py                        │
│  Menu loop: 1-Add 2-Del 3-Update 4-View 5-Mark │
│  NEW: 6-Search 7-Filter 8-Sort 9-Quit          │
└──────────────────────┬──────────────────────────┘
                       │ delegates to
                       ▼
┌─────────────────────────────────────────────────┐
│                    cli.py                        │
│  Existing: add, delete, update, view, mark      │
│  UPDATED:  add (priority, tags params)          │
│            update (priority, tags params)        │
│            view (enhanced table format)          │
│  NEW:      search(keyword)                      │
│            filter(filter_type, value)            │
│            sort(criterion)                       │
└──────────────────────┬──────────────────────────┘
                       │ calls
                       ▼
┌─────────────────────────────────────────────────┐
│                  storage.py                      │
│  Existing: add_task, get_task_by_id,            │
│            update_task, delete_task,             │
│            list_all_tasks, toggle_complete       │
│  UPDATED:  add_task (priority, tags params)     │
│            update_task (priority, tags params)   │
│  NEW:      search_tasks(keyword) → list[Task]   │
│            filter_tasks(type, value) → list[Task]│
│            sort_tasks(criterion) → list[Task]   │
└──────────────────────┬──────────────────────────┘
                       │ uses
                       ▼
┌─────────────────────────────────────────────────┐
│                  models.py                       │
│  UPDATED Task dataclass:                        │
│    id: int                                      │
│    title: str                                   │
│    description: Optional[str]                   │
│    completed: bool = False                      │
│    NEW: priority: Priority = Priority.MEDIUM    │
│    NEW: tags: list[str] = field(default_factory)│
│    NEW: created_at: datetime = field(default_f) │
│  NEW: Priority(Enum): HIGH, MEDIUM, LOW        │
└─────────────────────────────────────────────────┘
```

### Data Flow

1. **Add with priority/tags**: `main.py` prompts for priority + tags → `cli.add()` parses/validates → `storage.add_task()` creates Task with new fields
2. **Search**: `main.py` prompts for keyword → `cli.search()` → `storage.search_tasks()` filters via list comprehension with `in` operator on lowercased fields
3. **Filter**: `main.py` prompts for filter type + value → `cli.filter()` validates type → `storage.filter_tasks()` returns matching subset
4. **Sort**: `main.py` prompts for criterion → `cli.sort()` → `storage.sort_tasks()` uses `sorted()` with key functions
5. **View**: `cli.view()` renders enhanced table with Priority and Tags columns

## Key Decisions

### D1: Priority Implementation — Enum vs String

| Option | Pros | Cons |
|--------|------|------|
| **Enum (chosen)** | Type safety, IDE support, clear valid values, easy sort ordering | Slightly more code |
| String | Simpler, no import needed | No type safety, validation logic scattered |

**Decision**: Use `enum.Enum` with `Priority.HIGH`, `Priority.MEDIUM`, `Priority.LOW`. Assign integer values (1, 2, 3) for natural sort ordering (high=1 sorts first). Provides centralized validation via `Priority(value)`.

### D2: Tag Storage — List vs Set

| Option | Pros | Cons |
|--------|------|------|
| **List (chosen)** | Preserves insertion order, JSON-serializable, simpler for display | Must deduplicate manually |
| Set | Auto-deduplication | No order guarantee, less intuitive display |

**Decision**: Use `list[str]`. Deduplicate via `list(dict.fromkeys(tags))` to preserve order. Tags normalized to lowercase on input.

### D3: Creation Date Tracking

**Decision**: Add `created_at: datetime` field using `datetime.now()` at task creation. Uses stdlib `datetime` module. Enables sort-by-date without external dependencies.

### D4: Tag Parsing Helper

**Decision**: Create a standalone `parse_tags(raw: str) -> list[str]` function in `models.py` that handles: split by comma, strip whitespace, lowercase, filter empties, deduplicate. This centralizes tag cleaning logic used by both add and update flows.

### D5: Display Format

**Decision**: Use pipe-separated table format with fixed-width truncation. Header row + separator. Description truncated to 20 chars, tags truncated to 15 chars. Format: `ID | Title | Description | Priority | Tags | Status`.

### D6: Filter Command Syntax

**Decision**: Single filter per command with syntax `filter <type> <value>` where type is one of: `status`, `priority`, `tag`. Example: `filter priority high`, `filter status completed`, `filter tag work`.

## Implementation Phases

### Phase A: Data Model Extension (models.py)

1. Add `Priority` enum with HIGH=1, MEDIUM=2, LOW=3
2. Add `parse_tags()` helper function
3. Update `Task` dataclass: add `priority`, `tags`, `created_at` fields with defaults
4. Verify backward compatibility (existing Task creation still works)

### Phase B: Storage Layer Extension (storage.py)

1. Update `add_task()` signature: add `priority` and `tags` parameters with defaults
2. Update `update_task()` signature: add `priority` and `tags` parameters
3. Add `search_tasks(keyword: str) -> list[Task]` method
4. Add `filter_tasks(filter_type: str, value: str) -> list[Task]` method
5. Add `sort_tasks(criterion: str) -> list[Task]` method

### Phase C: CLI Layer Enhancement (cli.py)

1. Update `add()` method: accept and pass priority/tags
2. Update `update()` method: accept and pass priority/tags
3. Update `view()` method: enhanced table with Priority/Tags columns
4. Add `search(keyword: str)` method
5. Add `filter(filter_type: str, value: str)` method
6. Add `sort(criterion: str)` method
7. Update `handle_command()` for new commands (if text-based parsing used)

### Phase D: Main Menu Update (main.py)

1. Add menu options for Search (6), Filter (7), Sort (8)
2. Renumber Quit to option 9
3. Add input prompts for each new operation
4. Update add flow: prompt for optional priority and tags
5. Update update flow: prompt for optional priority and tags

### Phase E: Testing & Validation

1. Test all Basic features still work unchanged
2. Test add with priority/tags combinations
3. Test search across title, description, tags
4. Test filter by status, priority, tag
5. Test sort by priority, title, date
6. Test edge cases: invalid priority, empty tags, no results
7. Run existing test_app.py to verify no regressions

## Testing Strategy

### Manual Console Test Flows

| Test | Input | Expected Output |
|------|-------|-----------------|
| Add with priority | Title: "Buy milk", Priority: "high", Tags: "shopping,errands" | "Task added with ID: 1" |
| Add default priority | Title: "Read book", Priority: (empty), Tags: (empty) | Task created with medium priority, no tags |
| Add invalid priority | Priority: "critical" | "Error: Invalid priority. Valid: high, medium, low" |
| View enhanced | After adding tasks | Table with ID, Title, Desc, Priority, Tags, Status columns |
| Search match | Keyword: "milk" | Shows task "Buy milk" |
| Search no match | Keyword: "xyz" | "No tasks match the search" |
| Search case | Keyword: "BUY" | Shows task "Buy milk" (case-insensitive) |
| Filter priority | Type: "priority", Value: "high" | Only high-priority tasks |
| Filter status | Type: "status", Value: "completed" | Only completed tasks |
| Filter tag | Type: "tag", Value: "shopping" | Tasks with "shopping" tag |
| Filter no match | Type: "priority", Value: "high" (none exist) | "No tasks match the filter" |
| Sort priority | Criterion: "priority" | High → Medium → Low order |
| Sort title | Criterion: "title" | Alphabetical A-Z |
| Sort date | Criterion: "date" | Oldest first |
| Sort invalid | Criterion: "size" | "Error: Invalid sort. Valid: priority, title, date" |

### Edge Case Tests

| Edge Case | Input | Expected |
|-----------|-------|----------|
| Duplicate tags | Tags: "work,work,home" | Stored as ["work", "home"] |
| Empty tags | Tags: "work,,home" | Stored as ["work", "home"] |
| Whitespace tags | Tags: " work , home " | Stored as ["work", "home"] |
| Empty task list + search | Search: "anything" | "No tasks match the search" |
| Empty task list + filter | Filter: priority high | "No tasks match the filter" |
| Empty task list + sort | Sort: priority | "No tasks exist" |

## Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Breaking Basic features during model update | High | Medium | Add new fields with defaults; test Basic flows first |
| Complex CLI input parsing for priority/tags | Medium | Medium | Use simple sequential prompts (not inline flags) |
| Tag edge cases causing crashes | Low | Low | Centralized `parse_tags()` handles all normalization |

## Complexity Tracking

No constitution violations. No complexity justifications needed.
