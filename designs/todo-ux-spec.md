# To-Do List App — UX Design Spec

## User Story
As a daily task tracker, I want a clean, single-page to-do list app so that I can create, view,
filter, complete, and delete my daily tasks without friction.

---

## User Flow

```
Page load
  → GET /tasks/summary → render summary bar
  → GET /tasks         → render task list
       │
       ├─ [Active filter: All / Todo / In Progress / Done]
       │     → GET /tasks?status=X → re-render task list
       │
       ├─ [Fill Create Form] → POST /tasks
       │     ├─ success → refresh list + summary bar
       │     └─ error   → inline error below form
       │
       ├─ [Click "Complete" on task] → PATCH /tasks/{id}/complete
       │     ├─ success → re-render that task card (badge turns green, button disabled)
       │     └─ error   → inline error on card
       │
       └─ [Click "Delete" on task] → DELETE /tasks/{id}
             ├─ success → remove card from list, refresh summary bar
             └─ error   → inline error on card
```

---

## Screens & Wireframes

### Screen: Main Page (≥ 768px — desktop/tablet)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  ✅ To-Do List                                                               │
├──────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────────────────┐    │
│  │  Total: 12    Todo: 5    In Progress: 3    Done: 4                   │    │
│  └──────────────────────────────────────────────────────────────────────┘    │
│                                          ← summary bar                        │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌─── Add New Task ─────────────────────────────────────────────────────┐    │
│  │  Title *  [                                              ]            │    │
│  │  Desc     [                                              ]            │    │
│  │  Priority [Medium           ▾]        [  + Add Task  ]               │    │
│  │                                                                       │    │
│  │  ⚠ Title is required.    ← inline error (hidden by default)          │    │
│  └───────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
│  Filter: [All]  [Todo]  [In Progress]  [Done]   ← button group               │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐     │
│  │  Buy groceries                    [● Todo]  [▲ High]                │     │
│  │  Pick up dry-cleaning by Friday                                     │     │
│  │  Created: 2024-06-01                 [Complete ✓]   [Delete 🗑]     │     │
│  ├─────────────────────────────────────────────────────────────────────┤     │
│  │  Draft Q3 report                  [◐ In Progress]  [● Medium]       │     │
│  │                                                                     │     │
│  │  Created: 2024-06-01                 [Complete ✓]   [Delete 🗑]     │     │
│  ├─────────────────────────────────────────────────────────────────────┤     │
│  │  ~~Send invoices~~                [✔ Done]     [▽ Low]              │     │
│  │                                                                     │     │
│  │  Created: 2024-05-30                            [Delete 🗑]          │     │
│  └─────────────────────────────────────────────────────────────────────┘     │
│                                                                               │
│  ← empty-state message appears here when list is empty                        │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Screen: Main Page (375px — mobile)

```
┌────────────────────────────────────────┐
│  ✅ To-Do List                         │
├────────────────────────────────────────┤
│  ┌──────────────────────────────────┐  │
│  │ Total:12  Todo:5  InProg:3  Done:4│  │
│  └──────────────────────────────────┘  │
├────────────────────────────────────────┤
│  ┌─── Add New Task ─────────────────┐  │
│  │  Title *  [                    ] │  │
│  │  Desc     [                    ] │  │
│  │  Priority [Medium           ▾]   │  │
│  │  [      + Add Task (full width)] │  │
│  │  ⚠ Title is required.            │  │
│  └───────────────────────────────── ┘  │
│                                        │
│  [All] [Todo] [In Prog.] [Done]        │
│  ← 4-button strip, wraps if needed    │
│                                        │
│  ┌──────────────────────────────────┐  │
│  │ Buy groceries  [Todo]   [High]   │  │
│  │ Pick up dry-cleaning by Friday   │  │
│  │ 2024-06-01                       │  │
│  │ [Complete ✓]        [Delete 🗑]  │  │
│  ├──────────────────────────────────┤  │
│  │ Draft Q3 report [InProg][Medium] │  │
│  │                                  │  │
│  │ 2024-06-01                       │  │
│  │ [Complete ✓]        [Delete 🗑]  │  │
│  └──────────────────────────────────┘  │
└────────────────────────────────────────┘
```

---

## Color Palette

| Token              | Hex       | Usage                                      |
|--------------------|-----------|--------------------------------------------|
| `--color-bg`       | `#f5f7fa` | Page background                            |
| `--color-surface`  | `#ffffff` | Cards, form, summary bar backgrounds       |
| `--color-border`   | `#e2e8f0` | Card dividers, input borders               |
| `--color-text`     | `#1a202c` | Primary body text                          |
| `--color-muted`    | `#718096` | Secondary text (description, created date) |
| `--color-heading`  | `#2d3748` | Page heading, section labels               |
| `--color-primary`  | `#4f46e5` | "Add Task" button, active filter button    |
| `--color-primary-hover` | `#4338ca` | Primary button hover                  |
| `--color-danger`   | `#e53e3e` | "Delete" button                            |
| `--color-danger-hover` | `#c53030` | Delete hover                          |
| `--color-success`  | `#38a169` | "Complete" button, Done badge              |
| `--color-success-hover` | `#2f855a` | Complete hover                       |
| `--color-disabled` | `#a0aec0` | Disabled button text/border                |

### Status Badge Colors

| Status       | Background | Text      | CSS Class            |
|--------------|------------|-----------|----------------------|
| `todo`       | `#ebf4ff`  | `#2b6cb0` | `.badge--todo`       |
| `in_progress`| `#fffaf0`  | `#c05621` | `.badge--in-progress`|
| `done`       | `#f0fff4`  | `#276749` | `.badge--done`       |

### Priority Badge Colors

| Priority | Background | Text      | CSS Class            |
|----------|------------|-----------|----------------------|
| `low`    | `#f7fafc`  | `#718096` | `.badge--low`        |
| `medium` | `#fffff0`  | `#b7791f` | `.badge--medium`     |
| `high`   | `#fff5f5`  | `#c53030` | `.badge--high`       |

---

## Typography

| Element            | Font Stack                                | Size     | Weight |
|--------------------|-------------------------------------------|----------|--------|
| Page heading (h1)  | `'Inter', 'Segoe UI', system-ui, sans-serif` | 1.5rem  | 700    |
| Section label      | same                                      | 0.75rem  | 600 uppercase |
| Body / task title  | same                                      | 0.95rem  | 500    |
| Description text   | same                                      | 0.875rem | 400    |
| Muted / date       | same                                      | 0.75rem  | 400    |
| Badge text         | same                                      | 0.7rem   | 600 uppercase |
| Button text        | same                                      | 0.875rem | 600    |

**Spacing unit:** 8px (use multiples: 4, 8, 12, 16, 24, 32px)

---

## Component Specs

### Summary Bar (`#summary-bar`)

```
┌──────────────────────────────────────────────────────┐
│  Total  12    Todo  5    In Progress  3    Done  4    │
└──────────────────────────────────────────────────────┘
```

| Property | Value |
|----------|-------|
| Layout | `display: flex; gap: 24px; justify-content: center; flex-wrap: wrap` |
| Background | `--color-surface` with `1px solid --color-border` border |
| Border-radius | 8px |
| Padding | 12px 24px |
| Each stat | label in `--color-muted` 0.75rem + count in `--color-heading` 1.1rem 700 |
| Margin | 0 auto 24px; max-width 900px |

**Behavior:** Refreshed after every create, complete, and delete action.

---

### Create Task Form (`#create-form`)

```
┌─── Add New Task ─────────────────────────────────────────┐
│  Title *  [input text field                            ]  │
│  Desc     [input text field (optional)                 ]  │
│  Priority [select: Low / Medium (default) / High    ▾] ]  │
│                                     [  + Add Task    ]    │
│  ⚠ Error message here (hidden by default)                 │
└──────────────────────────────────────────────────────────┘
```

| Component | States | Behavior |
|-----------|--------|----------|
| `#task-title` input | default, focus, error | Required. Red border + error message shown on submit-while-empty |
| `#task-desc` input | default, focus | Optional. No validation |
| `#task-priority` select | default | Values: low / medium (selected) / high |
| `#add-task-btn` button | default, hover, loading, disabled | Disabled + shows "Adding…" spinner text while POST is in flight |
| `#form-error` span | hidden / visible | Appears below form on API error (non-validation); red `--color-danger` text |

**Layout (desktop):** Title and Desc as full-width rows. Priority select left-aligned, "Add Task" button right-aligned on same row.
**Layout (mobile ≤ 600px):** All fields stacked, "Add Task" button full-width below Priority.

**Success behavior:** On successful POST, clear all form fields, reset priority to "medium", hide error.

---

### Filter Button Group (`#filter-bar`)

```
[All]  [Todo]  [In Progress]  [Done]
```

| Component | States | Behavior |
|-----------|--------|----------|
| Each filter button `.filter-btn` | default, hover, active/selected | Active button: `--color-primary` background, white text. Default: white background, `--color-border` border. Hover: `#eef2ff` background |
| Active button | `.filter-btn--active` | Only one active at a time |

**Behavior:** Clicking a filter button calls `GET /tasks?status=X` (where `all` omits the status param). Replaces the task list contents. Updates active button state.

**Layout:** `display: flex; gap: 8px; flex-wrap: wrap` — buttons wrap naturally on narrow screens.

---

### Task Card (`.task-card`)

```
┌─────────────────────────────────────────────────────────┐
│  Task Title Here                [● Todo]   [▲ High]     │
│  Optional description text here                         │
│  Created: Jun 1, 2024          [Complete ✓] [Delete 🗑] │
└─────────────────────────────────────────────────────────┘
```

| Component | States | Behavior |
|-----------|--------|----------|
| Card `.task-card` | default, done | Done cards: title has `text-decoration: line-through`, opacity 0.65 |
| Title `.task-title` | default, done | 500 weight, `--color-text`; done = strikethrough |
| Description `.task-desc` | default, hidden (if null) | Muted color; omit element entirely if description is null/empty |
| Status badge `.badge .badge--{status}` | todo, in_progress, done | Pill shape; text matches display label: "Todo" / "In Progress" / "Done" |
| Priority badge `.badge .badge--{priority}` | low, medium, high | Pill shape; text: "Low" / "Medium" / "High" |
| Created date `.task-date` | — | Format: `MMM D, YYYY`; muted color |
| Complete button `.btn-complete` | default, hover, disabled | Disabled (greyed out, no pointer) when status is already "done". Text: "Complete" |
| Delete button `.btn-delete` | default, hover, loading | Text: "Delete". Shows "Deleting…" while DELETE in flight |

**Card layout (desktop):**
- Row 1: title (flex-grow) + status badge + priority badge (right-aligned)
- Row 2: description (full width, shown only if non-empty)
- Row 3: created date (left) + action buttons (right)

**Card layout (mobile):**
- Row 1: title (full width)
- Row 2: badges side-by-side
- Row 3: description (if present)
- Row 4: created date
- Row 5: Complete + Delete buttons, each 50% width

**Card border:** `1px solid --color-border`; border-radius 8px; padding 16px; margin-bottom 8px; background `--color-surface`.

**Done card accent:** Left border `3px solid --color-success` to visually distinguish done tasks.

---

### Status & Error Messages (`#list-message`)

A single `<div id="list-message">` below the filter bar and above the task list handles all list-level feedback.

| State | Content | Style |
|-------|---------|-------|
| Loading | "Loading tasks…" | `--color-muted`, centered |
| Empty — fresh (no tasks created) | "No tasks yet. Add your first task above!" | `--color-muted`, centered |
| Empty — filter active | "No tasks match this filter." | `--color-muted`, centered |
| API error | "Failed to load tasks. Please try again." | `--color-danger`, centered |

---

## Interaction Notes

- **Page load:** Fetch summary + tasks simultaneously. Show "Loading tasks…" in list area until both resolve.
- **Loading states:** Buttons show inline text change ("Adding…" / "Deleting…") rather than spinners — keeps it simple with no animation library.
- **Error display:** Form errors → `#form-error` below the form. List errors → `#list-message`. Card-level action errors → small red text appended below the card's action row (`.card-error`), auto-dismiss after 4 seconds.
- **Success feedback:** No toast — the list re-renders with the updated state. For create: form clears. For delete: card fades out (CSS `opacity` transition 200ms) then removes from DOM. For complete: badge and card style update in place.
- **Hover/focus:** All buttons show `cursor: pointer`. Inputs and selects show `outline: 2px solid --color-primary` on focus (no browser default outline). Filter buttons show background tint on hover.
- **Transitions:** Card fade-out on delete: `transition: opacity 200ms ease`. No other animations — keeps dependencies at zero.
- **Disabled complete button:** When a task is done, Complete button gets `disabled` attribute AND `.btn--disabled` class. Never hide it — keep it visible so users can see the task is finished.

---

## Responsive Breakpoints

| Breakpoint | Width       | Layout changes |
|------------|-------------|----------------|
| Mobile     | ≤ 600px     | Form: all fields stacked; "Add Task" full-width. Cards: badges and buttons stacked. Summary bar: wraps to 2×2 grid. |
| Tablet     | 601–900px   | Same as desktop layout but max-width constrained to 100%. |
| Desktop    | ≥ 901px     | Max-width 860px centered. Form: priority + button on one row. Cards: title+badges on one row, date+buttons on one row. |

Page wrapper: `max-width: 860px; margin: 0 auto; padding: 16px`.

---

## CSS Class Naming Conventions

Follow BEM-lite: block name, then element or modifier with double dash.

| Class | Element |
|-------|---------|
| `.task-card` | Task card container |
| `.task-card--done` | Modifier: task is done (strikethrough, dim, green left border) |
| `.task-title` | Task title text |
| `.task-desc` | Task description text |
| `.task-date` | Created date text |
| `.badge` | Base badge (pill shape) |
| `.badge--todo` | Status: todo |
| `.badge--in-progress` | Status: in_progress |
| `.badge--done` | Status: done |
| `.badge--low` | Priority: low |
| `.badge--medium` | Priority: medium |
| `.badge--high` | Priority: high |
| `.filter-btn` | Filter bar button |
| `.filter-btn--active` | Active filter state |
| `.btn-complete` | Complete action button |
| `.btn-delete` | Delete action button |
| `.btn--disabled` | Visual disabled state (mirrors `disabled` attr) |
| `.card-error` | Inline error text below card action row |
| `#summary-bar` | Summary statistics bar |
| `#create-form` | Create task form |
| `#form-error` | Form-level error message |
| `#filter-bar` | Filter button group |
| `#task-list` | Task list container |
| `#list-message` | Loading / empty / error message area |

---

## Open Questions

- [ ] Should the "Complete" button advance status from `todo → in_progress → done` step-by-step, or jump directly to `done` in one click? (Current API is `PATCH /tasks/{id}/complete` which implies a single jump — specced as one-click to `done` unless PO clarifies otherwise.)
