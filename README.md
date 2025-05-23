# Reimagined Succotash

Reimagined Succotash is a modern portfolio and project showcase web application. It features a FastAPI backend and a React (Vite + Tailwind CSS) frontend. The app allows users to browse a list of projects, view project details, and explore the source code of each project's repository directly in the browser using an in-browser GitHub repository viewer powered by isomorphic-git and LightningFS.

## Features
- FastAPI backend serving project data and static assets
- Project data stored in Azure Table Storage
- React frontend with responsive, modern UI (Tailwind CSS)
- Project carousel and detail pages
- In-browser repository viewer with syntax highlighting and markdown rendering
- Easy local development with a single startup script (`dev.sh`)

## Local Development
Set `AZURE_TABLES_ACCOUNT_URL` and `AZURE_TABLES_TABLE_NAME` then run `./dev.sh` to start both backend and frontend for local development. Optionally set `ALLOW_ORIGINS` to a comma-separated list of origins for CORS; it defaults to `http://localhost:5173`.

For a production build, run `npm run build` inside the `frontend` directory. The compiled files are placed in `backend/app/static` and served by FastAPI.

## Technologies Used
- Python 3, FastAPI, Uvicorn
- React 18, Vite, Tailwind CSS
- isomorphic-git, LightningFS, highlight.js, react-markdown
- Azure Table Storage

## License
MIT License

