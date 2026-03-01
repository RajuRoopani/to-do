# 📝 To-Do List App

A clean, full-stack to-do list application with a REST API backend and modern web frontend. Create tasks, organize by priority, and track progress through a flexible status workflow.

## Features

- **Task CRUD Operations** — Create, read, update, and delete tasks
- **Status Workflow** — Move tasks through a three-state workflow: Todo → In Progress → Done (no skipping)
- **Priority Levels** — Assign low, medium (default), or high priority to each task
- **Filtering & Search** — Filter by status or priority; search titles and descriptions case-insensitively
- **Task Summary** — View aggregate counts of tasks by status
- **Modern Web Interface** — Clean, responsive single-page app with inline HTML/CSS/JS
- **REST API Documentation** — Auto-generated OpenAPI docs at `/docs`
- **Comprehensive Tests** — 30+ pytest tests covering all endpoints and edge cases

## Tech Stack

- **Backend:** Python 3.11+, FastAPI, Pydantic
- **Frontend:** Vanilla HTML5, CSS3, JavaScript (no frameworks)
- **Server:** Uvicorn
- **Testing:** pytest, httpx (TestClient)
- **Storage:** In-memory (ideal for demos; can be replaced with a database)

## Project Structure

```
todo_app/
├── __init__.py                  # Package marker
├── main.py                      # FastAPI app with 8 endpoints + frontend
├── models.py                    # Pydantic request/response models
├── storage.py                   # In-memory task storage
├── requirements.txt             # Python dependencies
├── designs/
│   └── todo-ux-spec.md         # Frontend UX design specification
└── tests/
    ├── __init__.py
    ├── conftest.py             # pytest fixtures (client, reset_storage)
    └── test_tasks.py           # API endpoint tests (30+)
```

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/RajuRoopani/build-a-todo-list-app.git
cd todo_app

# Install dependencies
pip install -r requirements.txt
```

### Running the App

```bash
# Start the server (development mode with auto-reload)
uvicorn todo_app.main:app --reload

# Server will be available at:
# - Frontend: http://localhost:8000
# - API docs: http://localhost:8000/docs
```

Open your browser to **http://localhost:8000** and start creating tasks!

### Running Tests

```bash
# Run all tests with verbose output
pytest todo_app/tests/ -v

# Run a specific test file
pytest todo_app/tests/test_tasks.py -v

# Run a specific test function
pytest todo_app/tests/test_tasks.py::test_create_task -v

# Run with coverage report
pytest todo_app/tests/ --cov=todo_app --cov-report=html
```

## API Reference

The To-Do List App provides 8 REST endpoints for full task management.

### Task Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks` | Create a new task |
| GET | `/tasks` | List all tasks (supports filtering and search) |
| GET | `/tasks/{task_id}` | Get a single task by ID |
| PUT | `/tasks/{task_id}` | Update task fields (title, description, priority) |
| DELETE | `/tasks/{task_id}` | Delete a task (returns 204 No Content) |
| PATCH | `/tasks/{task_id}/status` | Transition task status (with validation) |
| PATCH | `/tasks/{task_id}/complete` | Mark task as done (shortcut endpoint) |
| GET | `/tasks/summary` | Get aggregate task counts by status |

### Frontend

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serve the frontend (single-page app) |

---

## Endpoint Details

### POST /tasks — Create Task

**Request:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "high"
}
```

**Fields:**
- `title` (string, required) — Task title (non-empty)
- `description` (string, optional) — Free-text description
- `priority` (string, default: `"medium"`) — One of: `"low"`, `"medium"`, `"high"`

**Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "todo",
  "priority": "high",
  "created_at": "2024-06-01T12:34:56.789Z",
  "updated_at": "2024-06-01T12:34:56.789Z"
}
```

---

### GET /tasks — List Tasks

**Query Parameters:**
- `status` (optional) — Filter by status: `"todo"`, `"in_progress"`, `"done"`
- `priority` (optional) — Filter by priority: `"low"`, `"medium"`, `"high"`
- `search` (optional) — Case-insensitive substring search on title and description

**Examples:**
```
GET /tasks                              # List all tasks
GET /tasks?status=todo                  # Only todo tasks
GET /tasks?priority=high                # Only high-priority tasks
GET /tasks?status=in_progress&priority=high  # Both filters (AND logic)
GET /tasks?search=grocery               # Tasks with "grocery" in title/description
```

**Response (200 OK):**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": "todo",
    "priority": "high",
    "created_at": "2024-06-01T12:34:56.789Z",
    "updated_at": "2024-06-01T12:34:56.789Z"
  },
  ...
]
```

**Ordering:** Tasks are returned newest first (sorted by `created_at` descending).

---

### GET /tasks/summary — Task Summary

Aggregate task counts grouped by status.

**Response (200 OK):**
```json
{
  "total": 12,
  "todo": 5,
  "in_progress": 3,
  "done": 4
}
```

---

### GET /tasks/{task_id} — Get Single Task

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "todo",
  "priority": "high",
  "created_at": "2024-06-01T12:34:56.789Z",
  "updated_at": "2024-06-01T12:34:56.789Z"
}
```

**Error (404 Not Found):**
```json
{
  "detail": "Task '550e8400-e29b-41d4-a716-446655440000' not found."
}
```

---

### PUT /tasks/{task_id} — Update Task

Update one or more fields. Only provided fields are updated; omitted fields are unchanged.

**Request (all fields optional):**
```json
{
  "title": "Buy groceries and cook dinner",
  "description": "Milk, eggs, bread, chicken",
  "priority": "medium"
}
```

**Response (200 OK):**
Updated task object (same schema as POST response). The `updated_at` timestamp is automatically refreshed.

**Error (404 Not Found):** Same as GET.

---

### DELETE /tasks/{task_id} — Delete Task

Permanently remove a task.

**Response (204 No Content):** Empty body.

**Error (404 Not Found):** Same as GET.

---

### PATCH /tasks/{task_id}/status — Transition Status

Change a task's status with strict validation. Transitions must follow the allowed rules (no skipping).

**Allowed Transitions:**
```
todo          ↔ in_progress
in_progress   ↔ done
todo → in_progress → done (forward)
done → in_progress → todo (backward)
```

**Invalid Transitions (rejected with 400):**
- `todo → done` (must go through `in_progress`)
- `done → todo` (must go through `in_progress`)
- Any other invalid state

**Request:**
```json
{
  "status": "in_progress"
}
```

**Response (200 OK):**
Updated task object with new status and refreshed `updated_at`.

**Error (400 Bad Request):**
```json
{
  "detail": "Invalid transition: 'todo' → 'invalid_state'. Allowed from 'todo': ['in_progress']."
}
```

**Error (404 Not Found):** Same as GET.

---

### PATCH /tasks/{task_id}/complete — Mark as Done

Convenience endpoint to mark a task as `done` in one click. Bypasses transition validation and sets status directly to `done` regardless of current state.

**Request:** No body required.

**Response (200 OK):**
Updated task object with `status: "done"` and refreshed `updated_at`.

**Error (404 Not Found):** Same as GET.

---

## Status Workflow

Tasks progress through a three-state workflow with no skipping allowed. This prevents accidental jumps and ensures clear task progression.

```
                    todo
                     ↕
              in_progress
                     ↕
                    done
```

### Transition Rules

| From | Can Transition To | Cannot Transition To |
|------|-------------------|----------------------|
| `todo` | `in_progress` | `done` (invalid — must go through `in_progress`) |
| `in_progress` | `todo`, `done` | (none) |
| `done` | `in_progress` | `todo` (invalid — must go through `in_progress`) |

### Shortcut: Complete Button

The frontend provides a "Complete" button (using `PATCH /tasks/{id}/complete`) that immediately marks a task `done`, even from `todo` status. Use this for quick task completion; the `PATCH /status` endpoint enforces strict transitions for programmatic workflows.

---

## Priority Levels

Tasks can be assigned one of three priority levels to help organize workload.

| Priority | Visual Indicator | Use Case |
|----------|------------------|----------|
| `low` | Gray/muted badge | Background tasks, nice-to-haves |
| `medium` | Yellow/orange badge (default) | Standard tasks |
| `high` | Red badge | Urgent, time-sensitive work |

When creating a task without specifying priority, `medium` is used as the default.

---

## Error Handling

The API returns standard HTTP status codes and JSON error responses.

| Status | Scenario | Example |
|--------|----------|---------|
| 201 | Task created successfully | POST /tasks |
| 200 | Successful GET, PUT, PATCH | All retrieve/update operations |
| 204 | Task deleted successfully | DELETE /tasks/{id} |
| 400 | Invalid status transition | PATCH with invalid state |
| 422 | Validation failed (invalid fields) | POST with missing title, invalid priority |
| 404 | Task not found | GET, PUT, DELETE, PATCH on non-existent ID |
| 500 | Internal server error | Unexpected error (should not occur in normal operation) |

**Error Response Format:**
```json
{
  "detail": "Human-readable error message"
}
```

---

## Frontend

The frontend is a single-page app (SPA) served from the `GET /` endpoint. It's built with vanilla HTML5, CSS3, and JavaScript—no frameworks or build tools required.

### Key Features

- **Summary Bar** — Displays counts: Total, Todo, In Progress, Done
- **Create Form** — Add new tasks with title, optional description, and priority
- **Filter Buttons** — Quick-filter by All / Todo / In Progress / Done
- **Search** — Case-insensitive search across task titles and descriptions
- **Task Cards** — Display with status badge, priority, creation date, and action buttons
- **Status Badges** — Color-coded: blue (todo), orange (in progress), green (done)
- **Priority Badges** — Color-coded by level: gray (low), yellow (medium), red (high)
- **Complete & Delete** — Per-task action buttons with loading states
- **Responsive Design** — Optimized for desktop (≥ 901px), tablet (601–900px), and mobile (≤ 600px)

### User Flow

1. Page loads → fetch summary and task list
2. User can:
   - **Create**: Fill form and click "Add Task" (POST /tasks)
   - **Filter**: Click filter button to show only tasks with that status (GET /tasks?status=X)
   - **Search**: Enter search term to filter by title/description (GET /tasks?search=X)
   - **Complete**: Click "Complete" button on a task (PATCH /tasks/{id}/complete)
   - **Delete**: Click "Delete" button (DELETE /tasks/{id})
   - **Update Status**: (API-only; frontend uses Complete button for convenience)

### Design

See `/designs/todo-ux-spec.md` for comprehensive UX specification including:
- Wireframes (desktop and mobile)
- Color palette and typography
- Component specifications
- Responsive breakpoints
- Interaction patterns

---

## Development Notes

### Architecture

- **main.py** — FastAPI app with all 8 endpoints + frontend
- **models.py** — Pydantic schemas for request validation and response serialization
- **storage.py** — In-memory dict-based storage (thread-safe for single process; replace with database for production)
- **tests/conftest.py** — pytest fixtures with automatic storage reset
- **tests/test_tasks.py** — Comprehensive test suite (30+ tests)

### Key Implementation Details

1. **Route Order** — `GET /tasks/summary` is declared **before** `GET /tasks/{task_id}` in main.py to prevent FastAPI from capturing `summary` as a dynamic `task_id` parameter.

2. **Query Parameter Alias** — The `status` query parameter in `GET /tasks` uses `alias="status"` to avoid shadowing the FastAPI `status` module.

3. **Status Transitions** — Validated by a `_VALID_TRANSITIONS` dict that defines allowed edges in the status workflow graph.

4. **Timestamps** — All tasks store `created_at` (immutable) and `updated_at` (refreshed on any change) as ISO 8601 strings.

5. **Testing** — conftest.py provides `reset_storage()` autouse fixture to guarantee test isolation.

### Extending the App

To add a database backend:
1. Replace `storage.py` with database models (e.g., SQLAlchemy)
2. Update main.py endpoints to use `session.query()` instead of `storage.tasks`
3. Add database migrations
4. Update conftest.py to set up a test database

To add user authentication:
1. Add User model and auth router (login/register/token)
2. Add `user_id` field to Task model
3. Modify endpoints to filter tasks by authenticated user
4. Update frontend to include auth modal and token storage

---

## Testing

The test suite is comprehensive and organized by endpoint. All tests use the pytest framework with a shared fixture for client and storage reset.

### Test Organization

- **conftest.py** — Common fixtures and setup
- **test_tasks.py** — Tests for all 8 endpoints
  - Task creation (valid, validation errors, defaults)
  - Listing (filters, search, ordering)
  - Single task retrieval (success, 404)
  - Updates (partial, field independence)
  - Deletion (success, 404)
  - Status transitions (valid, invalid)
  - Summary aggregation

### Running Tests

```bash
# All tests
pytest todo_app/tests/ -v

# With coverage
pytest todo_app/tests/ --cov=todo_app

# A specific test
pytest todo_app/tests/test_tasks.py::test_create_task -v
```

### Test Isolation

The `reset_storage()` fixture runs before every test, clearing the in-memory storage. This ensures tests don't interfere with each other and can run in any order.

---

## API Documentation

Once the server is running, browse to **http://localhost:8000/docs** for interactive Swagger UI documentation. You can:
- View all endpoints and their parameters
- See request/response schemas
- Try out endpoints directly in the browser

For ReDoc documentation, visit **http://localhost:8000/redoc**.

---

## Example Workflows

### Create and Complete a Task

```bash
# Create task
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Write report",
    "priority": "high"
  }'
# Returns: {"id": "abc-123", "title": "Write report", "status": "todo", ...}

# Move to in_progress
curl -X PATCH http://localhost:8000/tasks/abc-123/status \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'

# Mark as done (shortcut)
curl -X PATCH http://localhost:8000/tasks/abc-123/complete
# Returns: {..., "status": "done", ...}

# View summary
curl http://localhost:8000/tasks/summary
# Returns: {"total": 1, "todo": 0, "in_progress": 0, "done": 1}
```

### Filter and Search

```bash
# Get all high-priority tasks
curl "http://localhost:8000/tasks?priority=high"

# Get in-progress tasks only
curl "http://localhost:8000/tasks?status=in_progress"

# Search for tasks with "report" in title/description
curl "http://localhost:8000/tasks?search=report"

# Combine filters (AND logic)
curl "http://localhost:8000/tasks?status=todo&priority=high"
```

---

## Known Limitations

- **In-memory storage** — All data is lost when the server restarts. Not suitable for production without a persistent database.
- **Single-process concurrency** — The in-memory dict is not thread-safe for multi-threaded servers. Use a database or process-queue for production.
- **No user authentication** — All tasks are shared globally; no per-user isolation.
- **No tasks persistence** — Consider adding a database (SQLite, PostgreSQL) for persistent data.

---

## License

[MIT License](LICENSE)

---

## Support

For issues or questions, please open an issue on GitHub: https://github.com/RajuRoopani/build-a-todo-list-app
