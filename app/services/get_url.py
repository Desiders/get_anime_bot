import asyncio
import queue
from typing import List, Optional

import aiohttp
import ujson


class GetUrl(object):
    urls: List[str] = [
        'neko', 'waifu', 'shinobu', 'megumin', 'bully',
        'cuddle', 'cry', 'hug', 'awoo', 'kiss', 'lick', 
        'pat', 'smug', 'bonk', 'yeet', 'bluhs', 'smile',
        'wave', 'highfive', 'handhold', 'nom', 'bite',
        'glomp', 'slap', 'kill', 'kick', 'happy', 'wink',
        'poke', 'dance', 'cringe'
    ]

    def __init__(self) -> None:
        self._block_length: int = 60
        self._session: Optional[aiohttp.ClientSession] = None

        self.queues = {url: queue.Queue() for url in self.urls}
        self.queues.update({"random": queue.Queue()})

    def get_new_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession()

    @property
    def session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = self.get_new_session()
        return self._session

    async def close(self) -> None:
        await self.session.close()
    
    async def get_urls(self, url: str, queue: queue.Queue) -> None:
        tasks = list()
        for _ in range(self._block_length):
            task = asyncio.create_task(self.session.get(url))
            tasks.append(task)

        responses: List[aiohttp.ClientResponse] = await asyncio.gather(*tasks)
        for response in responses:
            result = await response.json(loads=ujson.loads)
            if result not in queue.queue:
                queue.put_nowait(result)

    async def get_url(self, genre: str):
        genre = genre.lower()
        queue = self.queues[genre]
        url = f"https://api.waifu.pics/sfw/{genre}"
        if queue.empty():
            await self.get_urls(url, queue)
        while True:
            try:
                url: str = queue.get_nowait()['url']
            except queue.Empty:
                await self.get_urls(url, queue)
            else:
                if not url.endswith(".png"):
                    break
        return url
