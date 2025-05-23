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
Project detail pages are now rendered by the frontend at `/project/<id>` and
fetch their data from the backend API. The backend no longer serves HTML
templates for project pages.

Project detail pages include an in-browser GitHub repository viewer. The viewer
clones the specified repository using `isomorphic-git` and displays a file tree
and README preview directly in the browser. Markdown and code blocks are
rendered with `react-markdown` and Highlight.js for consistent styling.

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

```bash
DEBUG=1 VITE_ENABLE_DEBUG=true ./dev.sh
```

### Azure Table Storage
`dev.sh` sets the Azure Table Storage variables used by the backend. Override
them if you need to point to a different table account:

```bash
export AZURE_TABLES_ACCOUNT_URL=https://knavillus10portfoliostrg.table.core.windows.net
export AZURE_TABLES_TABLE_NAME=projects
./dev.sh
```

### Adding Projects
Projects are now stored in Azure Table Storage. Each entity uses partition key
`projects` and the project ID as the row key. The project JSON is stored in the
`data` column. Because arrays aren't supported directly, serialize
`exclude_paths` to a JSON string.

Example entity:

```json
{
  "PartitionKey": "projects",
  "RowKey": "another-project",
  "title": "Another Project",
  "image": "images/2.png",
  "repo_url": "https://github.com/example/another-project",
  "description": "This is another sample project to showcase multiple entries.",
  "demo_url": "https://example.com/demo2",
  "exclude_paths": '["dist", "node_modules"]'  # store as JSON string
}
```

Set `AZURE_TABLES_ACCOUNT_URL` and `AZURE_TABLES_TABLE_NAME` before running the
backend. The executing identity must have the **Storage Table Data
Contributor** role so `DefaultAzureCredential` can authenticate.

Global repository exclusions remain in `backend/project_store/GlobalRepoOmissions.json`.
