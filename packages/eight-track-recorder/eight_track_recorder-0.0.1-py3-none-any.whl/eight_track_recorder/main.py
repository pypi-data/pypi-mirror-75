"""
Application to archive 8tracks.com before it's all gone
"""

import asyncio
import math
import os
from pathlib import Path
from typing import Dict, Optional
from uuid import uuid1

import httpx
from dotenv import load_dotenv
from loguru import logger
from tqdm import tqdm


async def download(client: httpx.AsyncClient, url: str, logger) -> Optional[Dict]:
    try:
        response = await client.get(url=url, allow_redirects=False)
        response.raise_for_status()
        if response.status_code == 200:
            data = response.json()
            logger.info("success")
        else:
            data = None
    except httpx.HTTPError:
        data = None
    finally:
        return data


def chunk(objects, batch_size):
    for start in range(0, len(objects), batch_size):
        end = min(start + batch_size, len(objects))
        yield objects[start:end]


async def batch_process(
    async_func,
    batch_callback_func,
    process_desc,
    client,
    task_limit,
    objects,
    batch_size,
):
    batches = chunk(objects, batch_size)
    total = math.ceil(len(objects) / batch_size)
    async with asyncio.Semaphore(task_limit) as semaphore:
        for batch in tqdm(batches, desc=process_desc, total=total):
            tasks = []
            for obj in batch:
                task = asyncio.ensure_future(async_func(client, semaphore, obj, logger))
                tasks.append(task)
            data = await asyncio.gather(*tasks)
            if batch_callback_func:
                batch_callback_func(data)


async def download_tracklist(client, semaphore, obj):
    await asyncio.sleep(1)


def save_tracklist_data(data):
    pass


async def download_user(client, semaphore, obj):
    """
    Pseudocode:
    - get request to URL, log results
    - return user data if success
    """
    await asyncio.sleep(1)


def save_users_data(data):
    pass


async def download_mix(
    client: httpx.AsyncClient, semaphore: asyncio.Semaphore, mix_id: int, logger
):
    url = f"https://8tracks.com/mixes/{mix_id}?format=jsonh"
    data = await download(client=client, url=url, logger=logger)
    if data:
        return data


async def download_mixes(pid: str, client, task_limit: int, batch_size: int):
    logger.info("Starting 'download_mixes' with process id: {}", pid)
    ids = [65, 134, 162]
    urls = [(f"https://8tracks.com/mixes/{x}?format=jsonh") for x in ids]
    await batch_process(
        async_func=download_mix,
        batch_callback_func=save_mixes_data,
        process_desc="Downloading Mixes",
        client=client,
        task_limit=task_limit,
        objects=urls,
        batch_size=batch_size,
    )


def save_mixes_data(data):
    pass


async def download_tracklists(pid: str, client, task_limit: int, batch_size: int):
    logger.info("Starting 'download_tracklists' with process id: {}", pid)
    ids = [10675310, 15298057, 14252528]
    urls = [
        (f"https://8tracks.com/mixes/{x}/tracks_for_international?format=jsonh")
        for x in ids
    ]
    await batch_process(
        async_func=download_tracklist,
        batch_callback_func=save_tracklist_data,
        process_desc="Downloading Users",
        client=client,
        task_limit=task_limit,
        objects=urls,
        batch_size=batch_size,
    )


async def download_users(pid: str, client, task_limit: int, batch_size: int):
    logger.info("Starting 'download_users' with process id: {}", pid)
    ids = [10675310, 15298057, 14252528]
    urls = [(f"https://8tracks.com/users/{x}?format=jsonh") for x in ids]
    await batch_process(
        async_func=download_user,
        batch_callback_func=save_users_data,
        process_desc="Downloading Users",
        client=client,
        task_limit=task_limit,
        objects=urls,
        batch_size=batch_size,
    )


async def download_liked_mixes(pid: str, client, task_limit: int, batch_size: int):
    """
    - I need the user id, and I can use pagination helper on page to iterate through (how to handle failed requests in sequence?)
    """
    logger.info("Starting 'download_liked_mixes' with process id: {}", pid)
    ids = [10675310, 15298057, 14252528]
    urls = [(f"https://8tracks.com/users/{x}/liked_mixes?format=jsonh") for x in ids]
    await batch_process(
        async_func=download_user,
        batch_callback_func=save_users_data,
        process_desc="Downloading Users",
        client=client,
        task_limit=task_limit,
        objects=urls,
        batch_size=batch_size,
    )


async def download_favorites(pid: str, client, task_limit: int, batch_size: int):
    logger.info("Starting 'download_favorites' with process id: {}", pid)
    ids = [10675310, 15298057, 14252528]
    urls = [(f"https://8tracks.com/users/{x}?format=jsonh") for x in ids]
    await batch_process(
        async_func=download_user,
        batch_callback_func=save_users_data,
        process_desc="Downloading Users",
        client=client,
        task_limit=task_limit,
        objects=urls,
        batch_size=batch_size,
    )


async def download_following(pid: str, client, task_limit: int, batch_size: int):
    """
    I need the user id, and the number of followers (retrieve from users.jsonl files)
    """
    logger.info("Starting 'download_following' with process id: {}", pid)
    ids = [10675310, 15298057, 14252528]
    urls = [(f"https://8tracks.com/users/{x}?format=jsonh") for x in ids]
    await batch_process(
        async_func=download_user,
        batch_callback_func=save_users_data,
        process_desc="Downloading Users",
        client=client,
        task_limit=task_limit,
        objects=urls,
        batch_size=batch_size,
    )


async def archive(pid: str):
    """"""
    tl = int(os.getenv("TASK_LIMIT", 100))
    bs = int(os.getenv("BATCH_SIZE", 1000))
    pool_limits = httpx.PoolLimits(max_keepalive=10, max_connections=100)
    async with httpx.AsyncClient(pool_limits=pool_limits) as client:
        await download_mixes(pid=pid, client=client, task_limit=tl, batch_size=bs)
        await download_tracklists(pid=pid, client=client, task_limit=tl, batch_size=bs)
        await download_users(pid=pid, client=client, task_limit=tl, batch_size=bs)
        await download_liked_mixes(pid=pid, client=client, task_limit=tl, batch_size=bs)
        await download_favorites(pid=pid, client=client, task_limit=tl, batch_size=bs)
        await download_following(pid=pid, client=client, task_limit=tl, batch_size=bs)


def main():
    # logger.remove()
    load_dotenv()
    [Path(f).mkdir(exist_ok=True) for f in ["data", "logs"]]
    pid = uuid1()
    logger.info("Starting Application with Process ID: {}", pid)
    logger.add("logs/main.log", enqueue=True)
    asyncio.run(archive(pid=pid))


if __name__ == "__main__":
    main()
