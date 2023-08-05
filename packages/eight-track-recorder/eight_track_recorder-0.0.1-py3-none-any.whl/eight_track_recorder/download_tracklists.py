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


def get_tracklist_url(mix_id: int) -> str:
    """Generate URL for mix tracklist"""
    return "http://8tracks.com/mixes/{}/tracks_for_international.jsonh".format(mix_id)


def load_mix_targets() -> List[Tuple[int, str]]:
    successful_mixes = set()
    completed = set()  # get completed tracklists
    for fpath in Path("data/tracklists").iterdir():
        if fpath.suffix == ".jsonl":
            with open(fpath, "r") as f:
                for line in f.readlines():
                    mix_id = int("".join(x for x in line[10:20] if x.isdigit()))
                    completed.add(mix_id)
    with open("logs/tracklist.log", "r") as logs:
        for row in logs.readlines():
            if "mix_id" in row and row[-4] == "4":
                completed.add(int(row.split("mix_id: ")[1].split(",")[0]))
    for fpath in Path("data/mixes").iterdir():
        if fpath.suffix == ".jsonl":
            with open(fpath, "r") as f:
                for line in f.readlines():
                    mix_id = int("".join(x for x in line[10:20] if x.isdigit()))
                    successful_mixes.add(mix_id)
    mix_ids = {i for i in successful_mixes if i not in completed}
    # with open("data/mix_ids.txt", "r") as infile:
    #     mix_ids = {int(i) for i in infile.readlines() if i not in completed}
    mix_targets = [(m, get_tracklist_url(m)) for m in mix_ids]
    print(f"{len(completed):,} tracklists completed, {len(mix_ids):,} to go")
    return mix_targets


def generate_mix_batches(
    mix_targets: List[Tuple[int, str]], bs: int
) -> Generator[Tuple[int, List[Tuple[int, str]]], None, None]:
    for start in range(0, len(mix_targets), bs):
        end = min(start + bs, len(mix_targets))
        yield (end - start, mix_targets[start:end])


@logger.catch
async def parse_mix(mix_id, tracklist_data) -> Optional[Dict]:
    data = None
    if tracklist_data:
        data = {"mix_id": mix_id, "tracklist": json.loads(tracklist_data)}
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
    mix: Tuple[int, str], client: httpx.AsyncClient
) -> Optional[Dict]:
    tracklist_data = await download((mix[0], mix[1], "tracklist"), client)
    output = await parse_mix(mix[0], tracklist_data)
    return output


@logger.catch
async def bound_acquire_mix(
    sem, mix: Tuple[int, str], client: httpx.AsyncClient
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
            [0]
            + [
                int(x.stem)
                for x in Path("data/tracklists").iterdir()
                if x.suffix == ".jsonl"
            ]
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
            srsly.write_jsonl(
                f"data/tracklists/{idx+1+start_fname_idx:05}.jsonl", mix_data
            )


if __name__ == "__main__":
    load_dotenv()
    pid = uuid.uuid1()
    Path("./data/tracklists/").mkdir(exist_ok=True)
    logger.remove()
    logger.add("logs/tracklist.log", enqueue=True)
    logger.info("Starting Script Exeuction with Process ID: {pid}", pid=pid)
    asyncio.run(main())
    logger.info("Completed Script having Process ID: {pid}", pid=pid)
