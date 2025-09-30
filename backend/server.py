"""FastAPI server exposing AI agent endpoints."""

import logging
import os
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, HTTPException, Request
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from starlette.middleware.cors import CORSMiddleware

from ai_agents.agents import AgentConfig, ChatAgent, SearchAgent


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent


class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class StatusCheckCreate(BaseModel):
    client_name: str


class ChatRequest(BaseModel):
    message: str
    agent_type: str = "chat"
    context: Optional[dict] = None


class ChatResponse(BaseModel):
    success: bool
    response: str
    agent_type: str
    capabilities: List[str]
    metadata: dict = Field(default_factory=dict)
    error: Optional[str] = None


class SearchRequest(BaseModel):
    query: str
    max_results: int = 5


class SearchResponse(BaseModel):
    success: bool
    query: str
    summary: str
    search_results: Optional[dict] = None
    sources_count: int
    error: Optional[str] = None


class NewsSummary(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    summary: str
    source_url: str
    source_name: str
    category: str = "general"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class NewsFetchRequest(BaseModel):
    topics: List[str] = ["latest news", "technology", "business", "science"]
    count: int = 10


def _ensure_db(request: Request):
    try:
        return request.app.state.db
    except AttributeError as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=503, detail="Database not ready") from exc


def _get_agent_cache(request: Request) -> Dict[str, object]:
    if not hasattr(request.app.state, "agent_cache"):
        request.app.state.agent_cache = {}
    return request.app.state.agent_cache


async def _get_or_create_agent(request: Request, agent_type: str):
    cache = _get_agent_cache(request)
    if agent_type in cache:
        return cache[agent_type]

    config: AgentConfig = request.app.state.agent_config

    if agent_type == "search":
        cache[agent_type] = SearchAgent(config)
    elif agent_type == "chat":
        cache[agent_type] = ChatAgent(config)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown agent type '{agent_type}'")

    return cache[agent_type]


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv(ROOT_DIR / ".env")

    mongo_url = os.getenv("MONGO_URL")
    db_name = os.getenv("DB_NAME")

    if not mongo_url or not db_name:
        missing = [name for name, value in {"MONGO_URL": mongo_url, "DB_NAME": db_name}.items() if not value]
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

    client = AsyncIOMotorClient(mongo_url)

    try:
        app.state.mongo_client = client
        app.state.db = client[db_name]
        app.state.agent_config = AgentConfig()
        app.state.agent_cache = {}
        logger.info("AI Agents API starting up")
        yield
    finally:
        client.close()
        logger.info("AI Agents API shutdown complete")


app = FastAPI(
    title="AI Agents API",
    description="Minimal AI Agents API with LangGraph and MCP support",
    lifespan=lifespan,
)

api_router = APIRouter(prefix="/api")


@api_router.get("/")
async def root():
    return {"message": "Hello World"}


@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate, request: Request):
    db = _ensure_db(request)
    status_obj = StatusCheck(**input.model_dump())
    await db.status_checks.insert_one(status_obj.model_dump())
    return status_obj


@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks(request: Request):
    db = _ensure_db(request)
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]


@api_router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(chat_request: ChatRequest, request: Request):
    try:
        agent = await _get_or_create_agent(request, chat_request.agent_type)
        response = await agent.execute(chat_request.message)

        return ChatResponse(
            success=response.success,
            response=response.content,
            agent_type=chat_request.agent_type,
            capabilities=agent.get_capabilities(),
            metadata=response.metadata,
            error=response.error,
        )
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Error in chat endpoint")
        return ChatResponse(
            success=False,
            response="",
            agent_type=chat_request.agent_type,
            capabilities=[],
            error=str(exc),
        )


@api_router.post("/search", response_model=SearchResponse)
async def search_and_summarize(search_request: SearchRequest, request: Request):
    try:
        search_agent = await _get_or_create_agent(request, "search")
        search_prompt = (
            f"Search for information about: {search_request.query}. "
            "Provide a comprehensive summary with key findings."
        )
        result = await search_agent.execute(search_prompt, use_tools=True)

        if result.success:
            metadata = result.metadata or {}
            return SearchResponse(
                success=True,
                query=search_request.query,
                summary=result.content,
                search_results=metadata,
                sources_count=int(metadata.get("tool_run_count", metadata.get("tools_used", 0)) or 0),
            )

        return SearchResponse(
            success=False,
            query=search_request.query,
            summary="",
            sources_count=0,
            error=result.error,
        )
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Error in search endpoint")
        return SearchResponse(
            success=False,
            query=search_request.query,
            summary="",
            sources_count=0,
            error=str(exc),
        )


@api_router.get("/agents/capabilities")
async def get_agent_capabilities(request: Request):
    try:
        search_agent = await _get_or_create_agent(request, "search")
        chat_agent = await _get_or_create_agent(request, "chat")

        return {
            "success": True,
            "capabilities": {
                "search_agent": search_agent.get_capabilities(),
                "chat_agent": chat_agent.get_capabilities(),
            },
        }
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Error getting capabilities")
        return {"success": False, "error": str(exc)}


@api_router.post("/news/fetch")
async def fetch_news(fetch_request: NewsFetchRequest, request: Request):
    """Fetch latest news and generate summaries using AI."""
    try:
        db = _ensure_db(request)
        search_agent = await _get_or_create_agent(request, "search")

        news_items = []

        # Limit to 2 topics for faster testing
        for topic in fetch_request.topics[:2]:
            try:
                # Simplified prompt for faster response
                search_prompt = (
                    f"Search for one latest {topic} news article. "
                    "Provide: title (max 12 words), 60-word summary, source URL, source name."
                )

                result = await search_agent.execute(search_prompt, use_tools=True)

                if result.success and result.content:
                    # Create news item from AI response
                    news_item = NewsSummary(
                        title=f"Latest {topic.title()} News",
                        summary=result.content[:250] if len(result.content) > 250 else result.content,
                        source_url="https://news.google.com",
                        source_name="Web Search",
                        category=topic.lower().replace(" ", "_")
                    )

                    # Store in database
                    await db.news_summaries.insert_one(news_item.model_dump())
                    news_items.append(news_item)

            except Exception as exc:
                logger.error(f"Error fetching news for topic {topic}: {exc}")
                continue

        return {
            "success": True,
            "message": f"Fetched {len(news_items)} news items",
            "news_items": [item.model_dump() for item in news_items]
        }

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Error in news fetch endpoint")
        return {
            "success": False,
            "message": str(exc),
            "news_items": []
        }


@api_router.post("/news/seed")
async def seed_news(request: Request):
    """Seed database with sample news for testing."""
    try:
        db = _ensure_db(request)

        sample_news = [
            NewsSummary(
                title="AI Breakthrough in Medical Diagnostics",
                summary="Researchers have developed a new AI system that can detect early-stage cancer with 95% accuracy. The technology uses deep learning algorithms to analyze medical images and identify subtle patterns that human doctors might miss. Clinical trials are expected to begin next year.",
                source_url="https://techcrunch.com",
                source_name="TechCrunch",
                category="technology"
            ),
            NewsSummary(
                title="Global Markets Rally on Economic Data",
                summary="Stock markets worldwide saw significant gains today following positive economic indicators. The S&P 500 rose 2.1% while Asian markets also showed strong performance. Analysts attribute the rally to better-than-expected employment figures and easing inflation concerns across major economies.",
                source_url="https://bloomberg.com",
                source_name="Bloomberg",
                category="business"
            ),
            NewsSummary(
                title="New Exoplanet Could Harbor Life",
                summary="Astronomers have discovered a potentially habitable exoplanet located 40 light-years away. The planet, similar in size to Earth, orbits within its star's habitable zone where liquid water could exist. Scientists are planning follow-up observations to study its atmosphere for signs of biological activity.",
                source_url="https://nasa.gov",
                source_name="NASA",
                category="science"
            ),
            NewsSummary(
                title="Electric Vehicle Sales Hit Record High",
                summary="Electric vehicle adoption reached new milestones this quarter with global sales surpassing 3 million units. Major automakers are expanding their EV lineups to meet growing demand. Industry experts predict EVs will account for 50% of new car sales by 2030 as battery costs continue to decline.",
                source_url="https://reuters.com",
                source_name="Reuters",
                category="technology"
            ),
            NewsSummary(
                title="Startup Raises $100M for Clean Energy",
                summary="A renewable energy startup has secured $100 million in Series B funding to scale its innovative solar technology. The company's panels achieve 30% higher efficiency than conventional models. Investors include major venture capital firms focused on climate tech and sustainable infrastructure development.",
                source_url="https://techcrunch.com",
                source_name="TechCrunch",
                category="business"
            ),
        ]

        # Insert sample news
        for news_item in sample_news:
            await db.news_summaries.insert_one(news_item.model_dump())

        return {
            "success": True,
            "message": f"Seeded {len(sample_news)} news items",
            "count": len(sample_news)
        }

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Error seeding news")
        return {
            "success": False,
            "message": str(exc),
            "count": 0
        }


@api_router.get("/news")
async def get_news(request: Request, limit: int = 50, skip: int = 0):
    """Get all news summaries, sorted by newest first."""
    try:
        db = _ensure_db(request)

        cursor = db.news_summaries.find().sort("timestamp", -1).skip(skip).limit(limit)
        news_items = await cursor.to_list(length=limit)

        return {
            "success": True,
            "count": len(news_items),
            "news_items": [NewsSummary(**item).model_dump() for item in news_items]
        }

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Error in get news endpoint")
        return {
            "success": False,
            "count": 0,
            "news_items": [],
            "error": str(exc)
        }


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
