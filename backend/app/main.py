from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path

app = FastAPI()

# Path to the built frontend assets
build_path = Path(__file__).resolve().parents[1] / 'frontend' / 'dist'

if build_path.exists():
    app.mount('/', StaticFiles(directory=build_path, html=True), name='static')
else:
    @app.get('/', response_class=HTMLResponse)
    async def placeholder():
        return "<html><body><h1>Hello World</h1></body></html>"
