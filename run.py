import uvicorn

from app.utils.LoggerSingleton import logger


def main():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, workers=4)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.info(f"An error occurred: {e}")