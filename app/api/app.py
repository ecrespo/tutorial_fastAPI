import json
import asyncio
from sse_starlette.sse import EventSourceResponse
from fastapi import APIRouter
SCORES_FILE = "app/api/scores.json"

route = APIRouter(
    prefix="/api",
    tags=["Live Scores"],
    responses={404: {"description": "Not Found"}},
)



async def event_generator():
    with open(SCORES_FILE, "r") as file:
        scores = json.load(file)
    for score in scores:
        await asyncio.sleep(5)
        yield f"Match Summary: {json.dumps(score)}\n\n"

@route.get("/live-scores")
async def live_scores_endpoint():
    return EventSourceResponse(event_generator())


