## Codex Environment Setup
Go to https://chatgpt.com/codex/settings/environments, select or create your github-connected environment then Edit -> Advanced and copy-paste install.sh into the startup script textbox. Save

## Local Development

### Python Virtual Environment

Create and activate a virtual environment before installing Python dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
Run the FastAPI backend from the repository root so package imports work correctly:
```bash
uvicorn backend.app.main:app --reload
```

The backend expects a PostgreSQL database connection string in the
`DATABASE_URL` environment variable. For example:

```bash
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/portfolio
```

Tables are created automatically on startup.

Open <http://localhost:5173> during development. When the frontend is built, the
FastAPI backend serves the compiled files on <http://localhost:8000>.
Project detail pages are now rendered by the frontend at `/project/<id>` and
fetch their data from the backend API. The backend no longer serves HTML
templates for project pages.

### Build Frontend
```bash
cd frontend
npm run build
```

### Run Both Frontend and Backend
```bash
./dev.sh
```

### Debug Logging
Set the `DEBUG` environment variable to `1` for verbose backend logs and
`VITE_ENABLE_DEBUG=true` for frontend console logs. Example:

```bash
DEBUG=1 VITE_ENABLE_DEBUG=true ./dev.sh
```

### Adding Projects
Add new records directly to the `projects` table using any PostgreSQL client.
All columns correspond to the API fields shown below:
```sql
INSERT INTO projects (id, title, image, repo_url, description, demo_url)
VALUES ('my-project', 'My Project', 'images/my-image.png',
        'https://github.com/user/my-project',
        'Project description', 'https://example.com/demo');
```
Image files can still be placed under `backend/project_store/images` and
referenced from the `image` column.
