import asyncio
from queue import Empty, Queue
from typing import List, Optional

import aiohttp


class GetUrl(object):
    urls: List[str] = [ # available genres
        'neko', 'waifu', 'shinobu', 'megumin', 'bully',
        'cuddle', 'cry', 'hug', 'awoo', 'kiss', 'lick',
        'pat', 'smug', 'bonk', 'yeet', 'blush', 'smile',
        'wave', 'highfive', 'handhold', 'nom', 'bite',
        'glomp', 'slap', 'kill', 'kick', 'happy', 'wink',
        'poke', 'dance', 'cringe'
    ]

    def __init__(self) -> None:
        self._block_length: int = 500 # number of requests if some queue is empty 
        self._session: Optional[aiohttp.ClientSession] = None

        self.queues = {url: Queue() for url in self.urls} # creating a queue for each genre

    def get_new_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession()

    @property
    def session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = self.get_new_session() # creating new session if session is none
        return self._session

    async def close(self) -> None:
        await self.session.close() # session close

    async def get_urls(self, url: str, queue: Queue) -> None:
        tasks = list()
        for _ in range(self._block_length): # creating tasks for asynchronous requests
            task = asyncio.create_task(self.session.get(url))
            tasks.append(task)

        responses: List[aiohttp.ClientResponse] = await asyncio.gather(*tasks)
        for response in responses:
            result = await response.json()
            if result not in queue.queue: # if it is not a duplicate
                queue.put_nowait(result) # putting result into the queue

    async def get_url(self, genre: str) -> str:
        genre = genre.lower() # api case-sensitive
        queue = self.queues[genre] # getting queue of a certain genre

        url = f"https://api.waifu.pics/sfw/{genre}" # url for the request

        while True: # waiting correct url
            try:
                url: str = queue.get_nowait()['url'] # getting url from the queue
            except KeyError:
                continue
            except Empty:
                await self.get_urls(url, queue) # creating tasks for asynchronous requests (new urls)
            else:
                break
        return url
