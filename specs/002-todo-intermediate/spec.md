# Feature Specification: Intermediate Todo Features

**Feature Branch**: `002-todo-intermediate`
**Created**: 2026-02-15
**Status**: Draft
**Input**: User description: "Extend the console todo app with organization and usability features (priorities, tags, search, filter, sort) building on the Basic Level."

## Overview

The Intermediate Level extends the existing Basic todo application with five organization and usability features: task priorities, tags/categories, keyword search, filtering, and sorting. All Basic features (add, delete, update, view, toggle completion) continue to work unchanged. Storage remains in-memory. The console interface is enhanced with table-like formatting to display new fields.

### Goals

1. Allow users to organize tasks with priority levels and tags
2. Enable users to find tasks quickly through search, filter, and sort
3. Maintain full backward compatibility with all Basic features
4. Improve task display to show priority and tags alongside existing fields

### Assumptions

- Priority defaults to "medium" when not specified during task creation
- Tags default to an empty list when not specified during task creation
- Existing Basic commands (add, delete, update, view, mark) retain their current syntax but are extended with optional parameters
- Search is case-insensitive and uses substring matching (e.g., "work" matches "homework")
- Tags are free-form strings normalized to lowercase on input (no predefined tag list); users type them directly when adding/updating tasks
- Creation date is tracked on each task to support date-based sorting

### Non-Goals

- Due dates, recurrence, or reminders (reserved for Advanced Level)
- File or database persistence (storage remains in-memory)
- Web UI, colors, or rich terminal formatting
- Complex tag management UI (no separate tag CRUD operations)
- External library dependencies

## Clarifications

### Session 2026-02-15

- Q: Can users combine multiple filter criteria in a single command? → A: Single filter per command (one criterion at a time). Combined filtering deferred to Advanced level.
- Q: Should search match substrings within words or whole words only? → A: Substring matching (e.g., "work" matches "homework", "workout", "work").
- Q: Should tags be stored as-entered or normalized to lowercase? → A: Normalize to lowercase on input. All tags stored lowercase to simplify deduplication and comparisons.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add Tasks with Priority and Tags (Priority: P1)

As a user, I want to assign a priority level and tags when creating a task so I can organize tasks from the start.

**Why this priority**: Priority and tags are foundational data model changes that all other intermediate features depend on. Without these fields, search/filter/sort have nothing new to operate on.

**Independent Test**: Can be fully tested by adding tasks with various priority/tag combinations and verifying they appear correctly in the task list.

**Acceptance Scenarios**:

1. **Given** the app is running, **When** I add a task with priority "high" and tags "work,urgent", **Then** the task is created with the specified priority and tags, and a success message is displayed with the task ID.
2. **Given** the app is running, **When** I add a task without specifying priority or tags, **Then** the task is created with default priority "medium" and empty tags list.
3. **Given** the app is running, **When** I add a task with an invalid priority (e.g., "critical"), **Then** an error message is displayed indicating valid priority values, and no task is created.
4. **Given** the app is running, **When** I add a task with tags containing extra spaces (e.g., " work , home "), **Then** the tags are trimmed and stored as clean values ("work", "home").

---

### User Story 2 - Enhanced Task Display (Priority: P1)

As a user, I want the task list view to show priority and tags for each task so I can see the full picture at a glance.

**Why this priority**: The display must be updated alongside the data model to ensure new fields are visible. All other features (search, filter, sort) rely on the user being able to see these fields.

**Independent Test**: Can be tested by adding tasks with various priorities and tags, then running the view command and verifying the output format.

**Acceptance Scenarios**:

1. **Given** tasks exist with priorities and tags, **When** I run the view command, **Then** the output shows a table with columns: ID, Title, Description, Priority, Tags, Status.
2. **Given** a task has multiple tags, **When** I view the task list, **Then** tags are displayed as a comma-separated list within the Tags column.
3. **Given** a task has no tags, **When** I view the task list, **Then** the Tags column shows an empty value (e.g., "-" or blank).
4. **Given** no tasks exist, **When** I run the view command, **Then** the message "No tasks exist" is displayed.

---

### User Story 3 - Filter Tasks (Priority: P2)

As a user, I want to filter tasks by status, priority, or tag so I can focus on a specific subset of my task list.

**Why this priority**: Filtering is the most direct way for users to manage larger task lists, reducing noise and focusing attention. It delivers immediate organizational value.

**Independent Test**: Can be tested by adding tasks with varying statuses, priorities, and tags, then applying filters and verifying only matching tasks appear.

**Acceptance Scenarios**:

1. **Given** tasks with mixed priorities exist, **When** I filter by priority "high", **Then** only tasks with high priority are displayed.
2. **Given** tasks with mixed completion statuses exist, **When** I filter by status "completed", **Then** only completed tasks are displayed.
3. **Given** tasks with mixed completion statuses exist, **When** I filter by status "incomplete", **Then** only incomplete tasks are displayed.
4. **Given** tasks with various tags exist, **When** I filter by tag "work", **Then** only tasks that have the "work" tag are displayed.
5. **Given** no tasks match the filter criteria, **When** I apply a filter, **Then** a message "No tasks match the filter" is displayed.
6. **Given** I enter an invalid filter type, **When** I run the filter command, **Then** an error message is displayed listing valid filter options.

---

### User Story 4 - Search Tasks (Priority: P2)

As a user, I want to search tasks by keyword so I can quickly find a specific task by its content.

**Why this priority**: Search provides fast task lookup, complementing filter for larger task lists. It operates across multiple fields (title, description, tags) for comprehensive results.

**Independent Test**: Can be tested by adding tasks with distinct titles, descriptions, and tags, then searching by various keywords and verifying correct matches.

**Acceptance Scenarios**:

1. **Given** tasks exist, **When** I search for a keyword that appears in a task's title, **Then** that task is included in the results.
2. **Given** tasks exist, **When** I search for a keyword that appears in a task's description, **Then** that task is included in the results.
3. **Given** tasks exist with tags, **When** I search for a keyword that matches a tag, **Then** tasks with that tag are included in the results.
4. **Given** tasks exist, **When** I search with mixed case (e.g., "WORK" vs "work"), **Then** the search is case-insensitive and returns matching tasks regardless of case.
5. **Given** tasks exist, **When** I search for a keyword with no matches, **Then** a message "No tasks match the search" is displayed.
6. **Given** no search keyword is provided, **When** I run the search command, **Then** an error message is displayed asking for a keyword.

---

### User Story 5 - Sort Tasks (Priority: P3)

As a user, I want to sort my task list by priority, title, or creation date so I can view tasks in a meaningful order.

**Why this priority**: Sorting enhances how the user views their list but does not add new data or reduce the list. It provides presentation flexibility on top of filter and search.

**Independent Test**: Can be tested by adding tasks with varying priorities, titles, and creation times, then sorting by each criterion and verifying the order.

**Acceptance Scenarios**:

1. **Given** tasks with different priorities exist, **When** I sort by priority, **Then** tasks are displayed with high first, then medium, then low.
2. **Given** tasks exist, **When** I sort by title, **Then** tasks are displayed in alphabetical order (A-Z).
3. **Given** tasks exist, **When** I sort by creation date, **Then** tasks are displayed in chronological order (oldest first).
4. **Given** I provide an invalid sort criterion, **When** I run the sort command, **Then** an error message is displayed listing valid sort options (priority, title, date).

---

### User Story 6 - Update Tasks with Priority and Tags (Priority: P3)

As a user, I want to update the priority and tags of an existing task so I can reorganize tasks as my needs change.

**Why this priority**: Updating priority/tags builds on the core data model changes and enables ongoing task organization. Lower priority because the initial assignment at creation covers most use cases.

**Independent Test**: Can be tested by creating a task, updating its priority and/or tags, then verifying the changes appear in the view.

**Acceptance Scenarios**:

1. **Given** a task exists, **When** I update its priority to "low", **Then** the task's priority is changed and a success message is displayed.
2. **Given** a task exists with tags "work,urgent", **When** I update its tags to "personal,home", **Then** the task's tags are replaced with the new values.
3. **Given** a task exists, **When** I update it with an invalid priority, **Then** an error message is displayed and the task is not modified.

---

### Edge Cases

- What happens when a user adds a task with duplicate tags (e.g., "work,work")? Tags should be deduplicated automatically.
- What happens when a user provides an empty string as a tag (e.g., "work,,home")? Empty tags should be filtered out.
- What happens when searching with special characters? The search should treat them as literal characters.
- What happens when filtering by tag with different casing (e.g., "Work" vs "work")? Tag matching during filter should be case-insensitive.
- What happens when sorting tasks that all have the same priority? They should maintain their relative order (stable sort).
- What happens when the task list is empty and user tries to search/filter/sort? A friendly message should be displayed.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support three priority levels for tasks: "high", "medium", and "low"
- **FR-002**: System MUST default task priority to "medium" when not explicitly specified
- **FR-003**: System MUST reject invalid priority values with a clear error message listing valid options
- **FR-004**: System MUST support assigning zero or more tags to each task as a list of strings
- **FR-005**: System MUST accept tags as comma-separated input, trim whitespace, and normalize to lowercase
- **FR-006**: System MUST deduplicate tags on a task (no duplicate tag values after normalization)
- **FR-007**: System MUST filter out empty tags from input
- **FR-008**: System MUST search tasks by keyword across title, description, and tags fields
- **FR-009**: System MUST perform case-insensitive substring search matching (e.g., "work" matches "homework")
- **FR-010**: System MUST filter tasks by completion status ("completed" or "incomplete")
- **FR-011**: System MUST filter tasks by priority level
- **FR-012**: System MUST filter tasks by tag (case-insensitive matching)
- **FR-020**: System MUST accept only a single filter criterion per command (no combined filters)
- **FR-013**: System MUST sort tasks by priority (high > medium > low)
- **FR-014**: System MUST sort tasks alphabetically by title (A-Z)
- **FR-015**: System MUST sort tasks by creation date (oldest first)
- **FR-016**: System MUST display tasks in an enhanced table format showing ID, Title, Description, Priority, Tags, and Status
- **FR-017**: System MUST allow updating a task's priority and tags after creation
- **FR-018**: System MUST preserve all existing Basic features (add, delete, update, view, mark) without breaking changes
- **FR-019**: System MUST track creation date for each task to support date-based sorting

### Key Entities

- **Task**: Represents a todo item. Attributes: unique identifier, title, description, completion status, priority level (high/medium/low), tags (list of text labels), creation timestamp. A task always has a priority (defaults to medium) and may have zero or more tags.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a task with priority and tags in a single command and see confirmation within 1 second
- **SC-002**: Users can view all tasks with priority and tags displayed in a clear, columnar format
- **SC-003**: Search returns all matching tasks (across title, description, and tags) with zero false negatives for exact keyword matches
- **SC-004**: Filter correctly narrows the task list to only matching items with 100% accuracy
- **SC-005**: Sort reorders the full task list correctly according to the chosen criterion
- **SC-006**: All five Basic features (add, delete, update, view, mark) continue to work identically to their Basic Level behavior
- **SC-007**: Invalid inputs (bad priority, missing keywords, invalid sort/filter options) produce clear error messages without crashing the application
- **SC-008**: 100% of user interactions complete without unhandled exceptions
