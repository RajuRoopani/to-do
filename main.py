"""
To-Do List App — FastAPI entry point.
GET / serves the full SPA frontend (inline HTML+CSS+JS).
"""
import uuid
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi import status as http_status
from fastapi.responses import HTMLResponse

import todo_app.storage as storage
from todo_app.models import (
    SummaryResponse, StatusUpdate, TaskCreate, TaskResponse, TaskUpdate,
)

app = FastAPI(title="To-Do List App", version="1.0.0")

_VALID_TRANSITIONS: dict = {
    "todo": {"in_progress"},
    "in_progress": {"todo", "done"},
    "done": {"in_progress"},
}

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def _task_to_response(task: dict) -> TaskResponse:
    return TaskResponse(id=task["id"], title=task["title"], description=task["description"],
                        status=task["status"], priority=task["priority"],
                        created_at=task["created_at"], updated_at=task["updated_at"])

def _get_task_or_404(task_id: str) -> dict:
    task = storage.tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND,
                            detail=f"Task '{task_id}' not found.")
    return task

@app.get("/", response_class=HTMLResponse)
def serve_spa() -> HTMLResponse:
    return HTMLResponse(content=_SPA_HTML)

@app.post("/tasks", response_model=TaskResponse, status_code=http_status.HTTP_201_CREATED)
def create_task(body: TaskCreate) -> TaskResponse:
    task_id = str(uuid.uuid4())
    now = _now_iso()
    task: dict = {"id": task_id, "title": body.title, "description": body.description,
                  "status": "todo", "priority": body.priority, "created_at": now, "updated_at": now}
    storage.tasks[task_id] = task
    return _task_to_response(task)

@app.get("/tasks", response_model=List[TaskResponse])
def list_tasks(
    status_filter: Optional[str] = Query(default=None, alias="status"),
    priority: Optional[str] = Query(default=None),
    search: Optional[str] = Query(default=None),
) -> List[TaskResponse]:
    results = list(storage.tasks.values())
    if status_filter is not None:
        results = [t for t in results if t["status"] == status_filter]
    if priority is not None:
        results = [t for t in results if t["priority"] == priority]
    if search is not None:
        term = search.lower()
        results = [t for t in results if term in t["title"].lower()
                   or (t["description"] and term in t["description"].lower())]
    results.sort(key=lambda t: t["created_at"], reverse=True)
    return [_task_to_response(t) for t in results]

# CRITICAL: /tasks/summary must be before /tasks/{task_id}
@app.get("/tasks/summary", response_model=SummaryResponse)
def get_summary() -> SummaryResponse:
    all_tasks = list(storage.tasks.values())
    return SummaryResponse(total=len(all_tasks),
                           todo=sum(1 for t in all_tasks if t["status"] == "todo"),
                           in_progress=sum(1 for t in all_tasks if t["status"] == "in_progress"),
                           done=sum(1 for t in all_tasks if t["status"] == "done"))

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: str) -> TaskResponse:
    return _task_to_response(_get_task_or_404(task_id))

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, body: TaskUpdate) -> TaskResponse:
    task = _get_task_or_404(task_id)
    if body.title is not None: task["title"] = body.title
    if body.description is not None: task["description"] = body.description
    if body.priority is not None: task["priority"] = body.priority
    task["updated_at"] = _now_iso()
    return _task_to_response(task)

@app.delete("/tasks/{task_id}", status_code=http_status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str) -> None:
    _get_task_or_404(task_id)
    del storage.tasks[task_id]

@app.patch("/tasks/{task_id}/status", response_model=TaskResponse)
def update_status(task_id: str, body: StatusUpdate) -> TaskResponse:
    task = _get_task_or_404(task_id)
    current, target = task["status"], body.status
    if target not in _VALID_TRANSITIONS.get(current, set()):
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid transition: '{current}' -> '{target}'. "
                                   f"Allowed: {sorted(_VALID_TRANSITIONS[current])}.")
    task["status"] = target
    task["updated_at"] = _now_iso()
    return _task_to_response(task)

@app.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: str) -> TaskResponse:
    task = _get_task_or_404(task_id)
    task["status"] = "done"
    task["updated_at"] = _now_iso()
    return _task_to_response(task)

# ---------------------------------------------------------------------------
# Inline SPA — full HTML/CSS/JS served at GET /
# ---------------------------------------------------------------------------
_SPA_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>✅ To-Do List</title>
  <style>
    /* ── CSS custom properties ── */
    :root {
      --color-bg:             #f5f7fa;
      --color-surface:        #ffffff;
      --color-border:         #e2e8f0;
      --color-text:           #1a202c;
      --color-muted:          #718096;
      --color-heading:        #2d3748;
      --color-primary:        #4f46e5;
      --color-primary-hover:  #4338ca;
      --color-danger:         #e53e3e;
      --color-danger-hover:   #c53030;
      --color-success:        #38a169;
      --color-success-hover:  #2f855a;
      --color-disabled:       #a0aec0;
    }

    /* ── Reset & base ── */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
      background: var(--color-bg);
      color: var(--color-text);
      font-size: 0.95rem;
      min-height: 100vh;
    }

    /* ── Page wrapper ── */
    .page-wrap {
      max-width: 860px;
      margin: 0 auto;
      padding: 16px;
    }

    /* ── Header ── */
    header {
      background: var(--color-surface);
      border-bottom: 1px solid var(--color-border);
      padding: 16px 0;
      margin-bottom: 24px;
    }
    header h1 {
      max-width: 860px;
      margin: 0 auto;
      padding: 0 16px;
      font-size: 1.5rem;
      font-weight: 700;
      color: var(--color-heading);
    }

    /* ── Summary bar ── */
    #summary-bar {
      display: flex;
      gap: 24px;
      justify-content: center;
      flex-wrap: wrap;
      background: var(--color-surface);
      border: 1px solid var(--color-border);
      border-radius: 8px;
      padding: 12px 24px;
      margin: 0 auto 24px;
      max-width: 900px;
    }
    .stat-item { display: flex; flex-direction: column; align-items: center; gap: 2px; }
    .stat-label { font-size: 0.75rem; color: var(--color-muted); font-weight: 400; text-transform: uppercase; letter-spacing: 0.04em; }
    .stat-value { font-size: 1.1rem; font-weight: 700; color: var(--color-heading); }

    /* ── Create form ── */
    #create-form {
      background: var(--color-surface);
      border: 1px solid var(--color-border);
      border-radius: 8px;
      padding: 20px 24px 16px;
      margin-bottom: 24px;
    }
    #create-form legend {
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--color-muted);
      margin-bottom: 14px;
    }
    .form-row { display: flex; flex-direction: column; gap: 4px; margin-bottom: 12px; }
    .form-row label { font-size: 0.8rem; font-weight: 500; color: var(--color-muted); }
    .form-row input, .form-row select {
      width: 100%;
      padding: 8px 10px;
      border: 1px solid var(--color-border);
      border-radius: 6px;
      font-family: inherit;
      font-size: 0.9rem;
      color: var(--color-text);
      background: var(--color-surface);
      transition: border-color 0.15s;
    }
    .form-row input:focus, .form-row select:focus {
      outline: 2px solid var(--color-primary);
      border-color: var(--color-primary);
    }
    .form-row input.input-error { border-color: var(--color-danger); }
    .form-bottom-row {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
      margin-top: 4px;
    }
    .form-bottom-row .form-row { flex: 1; min-width: 140px; margin-bottom: 0; }
    #add-task-btn {
      padding: 9px 20px;
      background: var(--color-primary);
      color: #fff;
      border: none;
      border-radius: 6px;
      font-family: inherit;
      font-size: 0.875rem;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
      transition: background 0.15s;
    }
    #add-task-btn:hover:not(:disabled) { background: var(--color-primary-hover); }
    #add-task-btn:disabled { background: var(--color-disabled); cursor: not-allowed; }
    #form-error {
      display: none;
      margin-top: 10px;
      font-size: 0.85rem;
      color: var(--color-danger);
    }
    #form-error.visible { display: block; }

    /* ── Filter bar ── */
    #filter-bar {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 16px;
    }
    .filter-btn {
      padding: 7px 16px;
      background: var(--color-surface);
      border: 1px solid var(--color-border);
      border-radius: 6px;
      font-family: inherit;
      font-size: 0.875rem;
      font-weight: 600;
      color: var(--color-heading);
      cursor: pointer;
      transition: background 0.15s, color 0.15s;
    }
    .filter-btn:hover:not(.filter-btn--active) { background: #eef2ff; }
    .filter-btn--active {
      background: var(--color-primary);
      color: #fff;
      border-color: var(--color-primary);
    }

    /* ── List message ── */
    #list-message {
      text-align: center;
      padding: 32px 16px;
      font-size: 0.95rem;
      color: var(--color-muted);
      display: none;
    }
    #list-message.visible { display: block; }
    #list-message.error { color: var(--color-danger); }

    /* ── Task list ── */
    #task-list { display: flex; flex-direction: column; gap: 8px; }

    /* ── Task card ── */
    .task-card {
      background: var(--color-surface);
      border: 1px solid var(--color-border);
      border-radius: 8px;
      padding: 16px;
      transition: opacity 200ms ease;
    }
    .task-card--done {
      opacity: 0.65;
      border-left: 3px solid var(--color-success);
    }
    .card-row-1 {
      display: flex;
      align-items: flex-start;
      gap: 8px;
      margin-bottom: 6px;
    }
    .task-title {
      flex: 1;
      font-size: 0.95rem;
      font-weight: 500;
      color: var(--color-text);
    }
    .task-card--done .task-title { text-decoration: line-through; }
    .card-badges { display: flex; gap: 6px; flex-shrink: 0; flex-wrap: wrap; }
    .task-desc {
      font-size: 0.875rem;
      color: var(--color-muted);
      margin-bottom: 10px;
      line-height: 1.5;
    }
    .card-row-3 {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      flex-wrap: wrap;
    }
    .task-date {
      font-size: 0.75rem;
      color: var(--color-muted);
    }
    .card-actions { display: flex; gap: 8px; }

    /* ── Badges ── */
    .badge {
      display: inline-block;
      padding: 2px 8px;
      border-radius: 999px;
      font-size: 0.7rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      white-space: nowrap;
    }
    .badge--todo       { background: #ebf4ff; color: #2b6cb0; }
    .badge--in-progress{ background: #fffaf0; color: #c05621; }
    .badge--done       { background: #f0fff4; color: #276749; }
    .badge--low        { background: #f7fafc; color: #718096; }
    .badge--medium     { background: #fffff0; color: #b7791f; }
    .badge--high       { background: #fff5f5; color: #c53030; }

    /* ── Action buttons ── */
    .btn-complete, .btn-delete {
      padding: 6px 14px;
      border-radius: 6px;
      font-family: inherit;
      font-size: 0.875rem;
      font-weight: 600;
      cursor: pointer;
      border: 1px solid;
      transition: background 0.15s, color 0.15s;
      white-space: nowrap;
    }
    .btn-complete {
      background: var(--color-surface);
      color: var(--color-success);
      border-color: var(--color-success);
    }
    .btn-complete:hover:not(:disabled) {
      background: var(--color-success);
      color: #fff;
    }
    .btn-complete.btn--disabled,
    .btn-complete:disabled {
      color: var(--color-disabled);
      border-color: var(--color-disabled);
      cursor: not-allowed;
      background: var(--color-surface);
    }
    .btn-delete {
      background: var(--color-surface);
      color: var(--color-danger);
      border-color: var(--color-danger);
    }
    .btn-delete:hover:not(:disabled) {
      background: var(--color-danger);
      color: #fff;
    }
    .btn-delete:disabled { opacity: 0.6; cursor: not-allowed; }

    /* ── Card error ── */
    .card-error {
      margin-top: 8px;
      font-size: 0.8rem;
      color: var(--color-danger);
    }

    /* ── Responsive ── */
    @media (max-width: 600px) {
      #add-task-btn { width: 100%; }
      .form-bottom-row { flex-direction: column; }
      .form-bottom-row .form-row { width: 100%; }
      .card-row-1 { flex-wrap: wrap; }
      .card-row-3 { flex-direction: column; align-items: flex-start; }
      .card-actions { width: 100%; }
      .btn-complete, .btn-delete { flex: 1; }
      #summary-bar { gap: 16px; }
    }
  </style>
</head>
<body>
  <header>
    <h1>✅ To-Do List</h1>
  </header>

  <main class="page-wrap">
    <!-- Summary bar -->
    <div id="summary-bar" role="region" aria-label="Task summary">
      <div class="stat-item"><span class="stat-label">Total</span><span class="stat-value" id="stat-total">—</span></div>
      <div class="stat-item"><span class="stat-label">Todo</span><span class="stat-value" id="stat-todo">—</span></div>
      <div class="stat-item"><span class="stat-label">In Progress</span><span class="stat-value" id="stat-in-progress">—</span></div>
      <div class="stat-item"><span class="stat-label">Done</span><span class="stat-value" id="stat-done">—</span></div>
    </div>

    <!-- Create form -->
    <fieldset id="create-form" aria-label="Add new task">
      <legend>Add New Task</legend>
      <div class="form-row">
        <label for="task-title">Title <span aria-hidden="true">*</span></label>
        <input type="text" id="task-title" name="task-title" placeholder="Task title" required aria-required="true" />
      </div>
      <div class="form-row">
        <label for="task-desc">Description</label>
        <input type="text" id="task-desc" name="task-desc" placeholder="Optional description" />
      </div>
      <div class="form-bottom-row">
        <div class="form-row">
          <label for="task-priority">Priority</label>
          <select id="task-priority" name="task-priority">
            <option value="low">Low</option>
            <option value="medium" selected>Medium</option>
            <option value="high">High</option>
          </select>
        </div>
        <button type="button" id="add-task-btn">+ Add Task</button>
      </div>
      <div id="form-error" role="alert" aria-live="polite"></div>
    </fieldset>

    <!-- Filter bar -->
    <div id="filter-bar" role="group" aria-label="Filter tasks">
      <button class="filter-btn filter-btn--active" data-filter="all">All</button>
      <button class="filter-btn" data-filter="todo">Todo</button>
      <button class="filter-btn" data-filter="in_progress">In Progress</button>
      <button class="filter-btn" data-filter="done">Done</button>
    </div>

    <!-- List feedback -->
    <div id="list-message" role="status" aria-live="polite"></div>

    <!-- Task list -->
    <div id="task-list" aria-label="Task list"></div>
  </main>

  <script>
    'use strict';

    // ── State ──────────────────────────────────────────────────────────────
    let currentFilter = 'all';

    // ── DOM refs ───────────────────────────────────────────────────────────
    const titleInput    = document.getElementById('task-title');
    const descInput     = document.getElementById('task-desc');
    const priorityInput = document.getElementById('task-priority');
    const addBtn        = document.getElementById('add-task-btn');
    const formError     = document.getElementById('form-error');
    const filterBar     = document.getElementById('filter-bar');
    const taskList      = document.getElementById('task-list');
    const listMessage   = document.getElementById('list-message');
    const statTotal     = document.getElementById('stat-total');
    const statTodo      = document.getElementById('stat-todo');
    const statInProgress= document.getElementById('stat-in-progress');
    const statDone      = document.getElementById('stat-done');

    // ── Helpers ────────────────────────────────────────────────────────────
    function formatDate(iso) {
      const d = new Date(iso);
      return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    }

    function statusLabel(s) {
      return s === 'todo' ? 'Todo' : s === 'in_progress' ? 'In Progress' : 'Done';
    }

    function priorityLabel(p) {
      return p.charAt(0).toUpperCase() + p.slice(1);
    }

    function showListMessage(text, isError = false) {
      listMessage.textContent = text;
      listMessage.className = 'visible' + (isError ? ' error' : '');
    }

    function hideListMessage() {
      listMessage.className = '';
      listMessage.textContent = '';
    }

    function showFormError(text) {
      formError.textContent = text;
      formError.className = 'visible';
    }

    function hideFormError() {
      formError.className = '';
      formError.textContent = '';
      titleInput.classList.remove('input-error');
    }

    // ── Summary bar ────────────────────────────────────────────────────────
    async function refreshSummary() {
      try {
        const res = await fetch('/tasks/summary');
        if (!res.ok) return;
        const data = await res.json();
        statTotal.textContent      = data.total;
        statTodo.textContent       = data.todo;
        statInProgress.textContent = data.in_progress;
        statDone.textContent       = data.done;
      } catch (_) { /* silent — summary failure doesn't break the app */ }
    }

    // ── Build a task card DOM element ──────────────────────────────────────
    function buildCard(task) {
      const isDone = task.status === 'done';

      const card = document.createElement('div');
      card.className = 'task-card' + (isDone ? ' task-card--done' : '');
      card.dataset.taskId = task.id;

      // Row 1: title + badges
      const row1 = document.createElement('div');
      row1.className = 'card-row-1';

      const titleEl = document.createElement('span');
      titleEl.className = 'task-title';
      titleEl.textContent = task.title;

      const badges = document.createElement('div');
      badges.className = 'card-badges';

      const sBadge = document.createElement('span');
      sBadge.className = 'badge badge--' + task.status.replace('_', '-');
      sBadge.textContent = statusLabel(task.status);

      const pBadge = document.createElement('span');
      pBadge.className = 'badge badge--' + task.priority;
      pBadge.textContent = priorityLabel(task.priority);

      badges.appendChild(sBadge);
      badges.appendChild(pBadge);
      row1.appendChild(titleEl);
      row1.appendChild(badges);
      card.appendChild(row1);

      // Row 2: description (omit if empty)
      if (task.description) {
        const descEl = document.createElement('p');
        descEl.className = 'task-desc';
        descEl.textContent = task.description;
        card.appendChild(descEl);
      }

      // Row 3: date + action buttons
      const row3 = document.createElement('div');
      row3.className = 'card-row-3';

      const dateEl = document.createElement('span');
      dateEl.className = 'task-date';
      dateEl.textContent = 'Created: ' + formatDate(task.created_at);

      const actions = document.createElement('div');
      actions.className = 'card-actions';

      const completeBtn = document.createElement('button');
      completeBtn.className = 'btn-complete' + (isDone ? ' btn--disabled' : '');
      completeBtn.textContent = 'Complete ✓';
      completeBtn.disabled = isDone;
      completeBtn.setAttribute('aria-label', 'Mark task as complete');
      completeBtn.addEventListener('click', () => handleComplete(task.id, card, completeBtn));

      const deleteBtn = document.createElement('button');
      deleteBtn.className = 'btn-delete';
      deleteBtn.textContent = 'Delete 🗑';
      deleteBtn.setAttribute('aria-label', 'Delete task');
      deleteBtn.addEventListener('click', () => handleDelete(task.id, card, deleteBtn));

      actions.appendChild(completeBtn);
      actions.appendChild(deleteBtn);
      row3.appendChild(dateEl);
      row3.appendChild(actions);
      card.appendChild(row3);

      return card;
    }

    // ── Load & render tasks ────────────────────────────────────────────────
    async function loadTasks(filter) {
      showListMessage('Loading tasks…');
      taskList.innerHTML = '';

      const url = filter && filter !== 'all' ? '/tasks?status=' + filter : '/tasks';
      try {
        const res = await fetch(url);
        if (!res.ok) throw new Error('API error ' + res.status);
        const tasks = await res.json();

        hideListMessage();
        if (tasks.length === 0) {
          const msg = filter && filter !== 'all'
            ? 'No tasks match this filter.'
            : 'No tasks yet. Add your first task above!';
          showListMessage(msg);
          return;
        }
        tasks.forEach(t => taskList.appendChild(buildCard(t)));
      } catch (_) {
        showListMessage('Failed to load tasks. Please try again.', true);
      }
    }

    // ── Filter buttons ─────────────────────────────────────────────────────
    filterBar.addEventListener('click', e => {
      const btn = e.target.closest('.filter-btn');
      if (!btn) return;
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('filter-btn--active'));
      btn.classList.add('filter-btn--active');
      currentFilter = btn.dataset.filter;
      loadTasks(currentFilter);
    });

    // ── Create task ────────────────────────────────────────────────────────
    addBtn.addEventListener('click', async () => {
      hideFormError();
      const title = titleInput.value.trim();
      if (!title) {
        titleInput.classList.add('input-error');
        showFormError('⚠ Title is required.');
        titleInput.focus();
        return;
      }

      addBtn.disabled = true;
      addBtn.textContent = 'Adding…';

      try {
        const res = await fetch('/tasks', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            title,
            description: descInput.value.trim() || null,
            priority: priorityInput.value,
          }),
        });

        if (!res.ok) {
          const err = await res.json().catch(() => ({}));
          showFormError('⚠ ' + (err.detail || 'Failed to create task.'));
          return;
        }

        // Success: clear form, reload list and summary
        titleInput.value = '';
        descInput.value = '';
        priorityInput.value = 'medium';
        hideFormError();
        await Promise.all([loadTasks(currentFilter), refreshSummary()]);
      } catch (_) {
        showFormError('⚠ Network error. Please try again.');
      } finally {
        addBtn.disabled = false;
        addBtn.textContent = '+ Add Task';
      }
    });

    // Allow Enter key in title/desc to submit
    [titleInput, descInput].forEach(el => {
      el.addEventListener('keydown', e => { if (e.key === 'Enter') addBtn.click(); });
    });

    // ── Complete task ──────────────────────────────────────────────────────
    async function handleComplete(taskId, card, btn) {
      btn.disabled = true;
      btn.textContent = 'Completing…';

      try {
        const res = await fetch('/tasks/' + taskId + '/complete', { method: 'PATCH' });
        if (!res.ok) throw new Error('API error ' + res.status);
        const updated = await res.json();

        // Replace card in-place
        const newCard = buildCard(updated);
        card.replaceWith(newCard);
        await refreshSummary();
      } catch (_) {
        btn.disabled = false;
        btn.textContent = 'Complete ✓';
        showCardError(card, 'Failed to complete task. Please try again.');
      }
    }

    // ── Delete task ────────────────────────────────────────────────────────
    async function handleDelete(taskId, card, btn) {
      btn.disabled = true;
      btn.textContent = 'Deleting…';

      try {
        const res = await fetch('/tasks/' + taskId, { method: 'DELETE' });
        if (!res.ok) throw new Error('API error ' + res.status);

        // Fade out then remove
        card.style.opacity = '0';
        setTimeout(() => {
          card.remove();
          // Show empty message if no cards left
          if (taskList.children.length === 0) {
            const msg = currentFilter && currentFilter !== 'all'
              ? 'No tasks match this filter.'
              : 'No tasks yet. Add your first task above!';
            showListMessage(msg);
          }
        }, 200);
        await refreshSummary();
      } catch (_) {
        btn.disabled = false;
        btn.textContent = 'Delete 🗑';
        showCardError(card, 'Failed to delete task. Please try again.');
      }
    }

    // ── Card-level error ───────────────────────────────────────────────────
    function showCardError(card, text) {
      // Remove existing error if present
      const existing = card.querySelector('.card-error');
      if (existing) existing.remove();

      const errEl = document.createElement('p');
      errEl.className = 'card-error';
      errEl.textContent = text;
      card.appendChild(errEl);

      // Auto-dismiss after 4s
      setTimeout(() => errEl.remove(), 4000);
    }

    // ── Initial page load ──────────────────────────────────────────────────
    (async function init() {
      await Promise.all([refreshSummary(), loadTasks('all')]);
    })();

  </script>
</body>
</html>"""
