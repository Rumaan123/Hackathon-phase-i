# Research: Intermediate Todo Features

**Branch**: `002-todo-intermediate` | **Date**: 2026-02-15

## R1: Priority Enum Implementation (Python stdlib)

**Decision**: Use `enum.Enum` with integer values for sort ordering
**Rationale**: Python's `enum` module (stdlib) provides type-safe enumerations. Integer values enable natural sorting — `Priority.HIGH = 1` sorts before `Priority.LOW = 3` using `sorted(tasks, key=lambda t: t.priority.value)`.
**Alternatives considered**:
- Plain strings ("high", "medium", "low") — rejected: no type safety, requires manual sort-order mapping
- `enum.IntEnum` — rejected: unnecessary, regular Enum with `.value` suffices and avoids implicit integer comparisons

## R2: Tag Parsing and Normalization

**Decision**: Split on comma, strip whitespace, lowercase, filter empties, deduplicate preserving order
**Rationale**: `list(dict.fromkeys(...))` is a Python 3.7+ idiom that deduplicates while preserving insertion order. Combined with `str.split(",")`, `str.strip()`, and `str.lower()`, this handles all edge cases in a single pipeline.
**Alternatives considered**:
- `set()` for deduplication — rejected: loses insertion order
- Regex-based parsing — rejected: overkill for comma-separated input

## R3: Search Implementation

**Decision**: List comprehension with `in` operator on lowercased fields
**Rationale**: For in-memory storage with <1000 tasks, a simple `keyword.lower() in field.lower()` substring check is efficient and readable. Python's `in` operator for strings performs substring matching natively.
**Alternatives considered**:
- `re.search()` — rejected: unnecessary complexity for simple substring matching
- Full-text index — rejected: out of scope for in-memory console app

## R4: Sort Implementation

**Decision**: Use `sorted()` with key functions per criterion
**Rationale**: Python's `sorted()` uses Timsort (stable sort), meaning equal elements maintain their relative order. Key functions: `key=lambda t: t.priority.value` for priority, `key=lambda t: t.title.lower()` for alphabetical, `key=lambda t: t.created_at` for date.
**Alternatives considered**:
- `list.sort()` (in-place) — rejected: would modify the internal task list; `sorted()` returns a new list
- Custom comparator — rejected: key functions are simpler and more Pythonic

## R5: DateTime for Creation Tracking

**Decision**: Use `datetime.datetime.now()` from stdlib
**Rationale**: Standard library `datetime` provides sufficient precision for creation timestamp tracking. No timezone handling needed for a single-user console app.
**Alternatives considered**:
- `time.time()` (epoch float) — rejected: less readable for debugging/display
- `datetime.utcnow()` — rejected: deprecated in Python 3.12+; `datetime.now()` is appropriate for local-only app

## R6: Display Formatting

**Decision**: Pipe-separated columns with fixed truncation
**Rationale**: Simple string formatting with `f-strings` and `str.ljust()` / slicing provides adequate table display. No external table library needed.
**Alternatives considered**:
- `tabulate` library — rejected: external dependency violates constitution
- `textwrap` module — rejected: overkill for simple column truncation
