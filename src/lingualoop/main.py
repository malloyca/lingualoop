from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from lingualoop.api.routes import router
from lingualoop.database import initialize_database
from lingualoop.llm import LLMClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database before FastAPI serves requests
    app.state.database_path = initialize_database()

    app.state.llm = LLMClient(
        base_url="http://localhost:1234/v1",
        model="google/gemma-4-e4b",
    )

    yield

    await app.state.llm.close()


web_dir = Path(__file__).resolve().parent / "web"

app = FastAPI(lifespan=lifespan)
app.include_router(router=router)
app.mount("/", StaticFiles(directory=web_dir, html=True), name="web")
