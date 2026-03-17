from fastapi import FastAPI
from app.database import engine, Base
from app.routers import sources
import asyncio

# import models so tables register
from app.models import article, broadcast_log, favorite, news_item, source, user
from sqlalchemy import text
from app.database import AsyncSessionLocal

from app.ingestion.scheduler import start_scheduler
from app.processing.worker import start_processor
from app.clustering.worker import start_clusterer
from app.newsletter.worker import newsletter_worker

app = FastAPI(title="AI News Dashboard")
app.include_router(sources.router)


@app.on_event("startup")
async def startup():

    print("🚀 Starting AI News Dashboard...")

    # ✅ STEP 1: Create tables FIRST
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Tables created")

    # ✅ STEP 2: Start workers AFTER tables exist
    asyncio.create_task(start_scheduler())
    async def delayed_processor():
        await asyncio.sleep(10)  # wait for ingestion
        await start_processor()
    asyncio.create_task(delayed_processor())
    asyncio.create_task(start_clusterer())
    asyncio.create_task(newsletter_worker())

    print("✅ All workers started")


@app.get("/")
async def root():
    return {"message": "AI News Dashboard API"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/fix")
async def fix():
    async with AsyncSessionLocal() as db:
        await db.execute(
            text("UPDATE raw_articles SET processed = false WHERE processed IS NULL")
        )
        await db.commit()
    return {"status": "fixed"}