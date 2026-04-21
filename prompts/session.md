# Agent Session Prompt

Build the Wildcard Management System (WMS).
Requirements:
- Web app to manage prompts for "The Wildcard Project"
- Tech Stack: FastAPI, HTMX, Tailwind CSS, SQLite, WeasyPrint
- Adhere strictly to the `Composite Agentic Instructions: Web Applications`.
- Core milestones:
  1. Backend init (SQLAlchemy async, Alembic, configuration via pydantic-settings, DB seed).
  2. Idea Dashboard (CRUD operations via HTMX).
  3. Print Studio (Select approved prompts to create a batch).
  4. PDF Generation Logic (Render 3x3 grids of cards on US Letter paper with crop marks).
- Write integration tests to explicitly cover all requested requirements.
- Use the Playwright verification tool to test frontend UI visually.
