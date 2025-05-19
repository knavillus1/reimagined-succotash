## Codex Environment Setup
Go to https://chatgpt.com/codex/settings/environments, select or create your github-connected environment then Edit -> Advanced and copy-paste install.sh into the startup script textbox. Save

## Local Development

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Build Frontend
```bash
cd frontend
npm run build
```

### Backend
```bash
cd backend/app
uvicorn main:app --reload
```
