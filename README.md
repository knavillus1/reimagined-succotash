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
```bash
cd backend/app
uvicorn main:app --reload
```

Open <http://localhost:5173> during development. When the frontend is built, the
FastAPI backend serves the compiled files on <http://localhost:8000>.

### Build Frontend
```bash
cd frontend
npm run build
```
