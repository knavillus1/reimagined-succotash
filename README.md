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

Open <http://localhost:5173> during development. When the frontend is built, the
FastAPI backend serves the compiled files on <http://localhost:8000>.

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
Project definition files live in `backend/project_store`. Optional images can be
placed in `backend/project_store/images` and referenced from the `image` field.

Each JSON file must match this schema:
```json
{
  "id": "my-project",
  "title": "My Project",
  "image": "images/my-image.png",
  "repo_url": "https://github.com/user/my-project",
  "description": "Project description",
  "demo_url": "https://example.com/demo"
}
```
