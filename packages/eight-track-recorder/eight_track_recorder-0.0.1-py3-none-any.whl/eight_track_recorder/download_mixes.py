"""
Application to archive data from 8tracks.com before it's gone.

2020-07-17
Daniel Cooper <dcooper01sp@protonmail.com>
"""

import asyncio
import json
import math
import os
import uuid
from pathlib import Path
from typing import Dict, Generator, List, Optional, Tuple

import httpx
import srsly
from dotenv import load_dotenv
from loguru import logger
from tqdm import tqdm


def get_mix_url(mix_id: int) -> str:
    """Generate URL for mix"""
    return "http://8tracks.com/mixes/{}.jsonh".format(mix_id)


def get_tracklist_url(mix_id: int) -> str:
    """Generate URL for mix tracklist"""
    return "http://8tracks.com/mixes/{}/tracks_for_international.jsonh".format(mix_id)


def load_mix_targets() -> List[Tuple[int, str]]:
    completed = set()  # get completed mixes
    for fpath in Path("data/mixes").iterdir():
        if fpath.suffix == ".jsonl":
            with open(fpath, "r") as f:
                for line in f.readlines():
                    mix_id = int("".join(x for x in line[10:20] if x.isdigit()))
                    completed.add(mix_id)
    with open("logs/mixes.log", "r") as logs:
        for row in logs.readlines():
            if "mix_id" in row and row[-4] == "4":
                completed.add(int(row.split("mix_id: ")[1].split(",")[0]))
    # with open("data/mix_ids.txt", "r") as infile:
    # mix_ids = {int(i) for i in infile.readlines() if int(i) not in completed}
    # mix_targets = [(m, get_mix_url(m)) for m in mix_ids]
    mix_ids = {i for i in range(1, 8900000) if i not in completed}
    mix_targets = [(m, get_mix_url(m)) for m in mix_ids]
    print(f"{len(completed):,} mixes completed, {len(mix_ids):,} to go")
    return mix_targets


# def load_mix_targets(fpath: str) -> List[Tuple[int, str, str]]:
#     completed = set()  # get completed mixes
#     for fpath in Path("data/mixes").iterdir():
#         if fpath.is_file() and fpath.suffix == ".jsonl"
#     with open("logs/mixes.log", "r") as logs:
#         for row in logs.readlines():
#             if "success" in row or row[-4] == 4:
#                 completed.add(int(row.split("mix_id ")[1].split(" ")[0]))
#     mix_ids = {i for i in range(1, 8900000) if i not in completed}
#     with open(fpath, "r") as infile:
#         mix_ids = {int(i) for i in infile.readlines()}
#         mix_targets = [(m, get_mix_url(m), get_tracklist_url(m)) for m in mix_ids]
#     return mix_targets


def generate_mix_batches(
    mix_targets: List[Tuple[int, str]], bs: int
) -> Generator[Tuple[int, List[Tuple[int, str]]], None, None]:
    for start in range(0, len(mix_targets), bs):
        end = min(start + bs, len(mix_targets))
        yield (end - start, mix_targets[start:end])


@logger.catch
async def parse_mix(mix_id, mix_data) -> Optional[Dict]:
    data = None
    if mix_data:
        data = {"mix_id": mix_id, "mix": json.loads(mix_data)}
    return data


@logger.catch
async def download(
    mt: Tuple[int, str, str], client: httpx.AsyncClient
) -> Optional[str]:
    data = None
    try:
        response = await client.get(url=mt[1], allow_redirects=False)
        response.raise_for_status()
        if response.status_code == 200:
            data = response.text
            logger.info(
                "mix_id: {mix}, category: {cat} url: {url} success with http: {r}",
                mix=mt[0],
                cat=mt[2],
                url=mt[1],
                r=response.status_code,
            )
        elif response.is_redirect:
            logger.error(
                "mix_id: {mix}, category: {cat} url: {url} redirect with http: {r}",
                mix=mt[0],
                cat=mt[2],
                url=mt[1],
                r=response.status_code,
            )
    except httpx.HTTPError:
        logger.error(
            "mix_id: {mix}, category: {cat} url: {url} failed with http: {r}",
            mix=mt[0],
            cat=mt[2],
            url=mt[1],
            r=response.status_code,
        )
    except Exception as e:
        logger.error(
            "mix_id: {mix}, category: {cat} url: {url}  failed with {e} (generic error)",
            mix=mt[0],
            cat=mt[2],
            url=mt[1],
            e=e,
        )
    finally:
        return data


@logger.catch
async def acquire_mix(
    mix: Tuple[int, str, str], client: httpx.AsyncClient
) -> Optional[Dict]:
    mix_data = await download((mix[0], mix[1], "mix"), client)
    # mix_tracklist_data = await download((mix[0], mix[2], "tracklist"), client)
    output = await parse_mix(mix[0], mix_data)
    return output


@logger.catch
async def bound_acquire_mix(
    sem, mix: Tuple[int, str, str], client: httpx.AsyncClient
) -> Optional[Dict]:
    # NOTE: Typeshed missing for asyncio.locks.Semaphore (https://github.com/python/mypy/issues/8826#issuecomment-628916664)
    async with sem:
        return await acquire_mix(mix, client)


@logger.catch
async def main():
    """Docstring goes here"""
    bs = int(os.getenv("BATCH_SIZE"))
    tl = int(os.getenv("TASK_LIMIT"))
    mka = int(os.getenv("MAX_KEEP_ALIVE"))
    mc = int(os.getenv("MAX_CONNECTIONS"))
    mt = load_mix_targets()
    mt_batches = generate_mix_batches(mt, bs)
    tmb = math.ceil(len(mt) / bs)
    pool_limits = httpx.PoolLimits(max_keepalive=mka, max_connections=mc)
    async with httpx.AsyncClient(pool_limits=pool_limits) as client:
        start_fname_idx = max(
            [int(x.stem) for x in Path("data/mixes").iterdir() if x.suffix == ".jsonl"]
        )
        for idx, mb in enumerate(
            tqdm(mt_batches, desc="Processing Batches", total=tmb)
        ):
            asem = asyncio.Semaphore(tl)
            tasks = []
            for mix in mb[1]:
                task = asyncio.ensure_future(bound_acquire_mix(asem, mix, client))
                tasks.append(task)
            mixes = await asyncio.gather(*tasks)
            mix_data = [x for x in mixes if x]
            srsly.write_jsonl(f"data/mixes/{idx+1+start_fname_idx:05}.jsonl", mix_data)


if __name__ == "__main__":
    load_dotenv()
    pid = uuid.uuid1()
    Path("./data/mixes").mkdir(exist_ok=True)
    logger.remove()
    logger.add("logs/mixes.log", enqueue=True)
    logger.info("Starting Script Exeuction with Process ID: {pid}", pid=pid)
    asyncio.run(main())
    logger.info("Completed Script having Process ID: {pid}", pid=pid)
