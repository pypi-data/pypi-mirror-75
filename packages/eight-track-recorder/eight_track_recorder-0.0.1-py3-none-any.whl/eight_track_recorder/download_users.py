"""
Download user data
Progressive Download:
    - /users/id?format=jsonh
    - /users/id/liked_mixes?format=jsonh # paginate
    - /users/id/favorite_tracks?format=jsonh # paginate
    - /users/id/following?format=jsonh # paginate
"""

import asyncio
import uuid
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger


async def get_user():
    return {"user": 1}


@logger.catch
async def main():
    pass


if __name__ == "__main__":
    load_dotenv()
    pid = uuid.uuid1()
    Path("./data/users").mkdir(exist_ok=True)
    logger.remove()
    logger.add("logs/users.log", enqueue=True)
    logger.info("Starting Script Exeuction with Process ID: {pid}", pid=pid)
    asyncio.run(main())
    logger.info("Completed Script having Process ID: {pid}", pid=pid)
