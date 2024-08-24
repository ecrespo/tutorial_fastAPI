import time
from fastapi import Request
from app.utils.LoggerSingleton import logger


async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url} took {process_time:.8f} seconds")
    return response