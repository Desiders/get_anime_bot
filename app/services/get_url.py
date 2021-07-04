import asyncio
from itertools import chain
from queue import Empty, Queue
from typing import Dict, List, Optional, Union

import aiohttp
from aiohttp import ContentTypeError


class GetUrl(object):
    # available genres and sources
    genres: Dict[str, List[str]] = {
        "waifu": [
            'neko', 'waifu', 'shinobu', 'megumin',
            'bully', 'cuddle', 'cry', 'hug',
            'awoo', 'kiss', 'lick', 'pat',
            'smug', 'bonk', 'yeet', 'blush',
            'smile', 'wave', 'highfive', 'handhold',
            'nom', 'bite', 'glomp', 'slap',
            'kill', 'kick', 'happy', 'wink',
            'poke', 'dance', 'cringe'
        ],
        "computerfreaker": [
            'neko', 'anime', 'baguette', 'dva',
            'hug', 'trap', 'yuri'
        ]
    }

    def __new__(cls):
        cls.clear_genres = {genre for genre in list(
            chain.from_iterable([
                cls.genres[source] for source in cls.genres]))}
        return super().__new__(cls)

    def __init__(self) -> None:
        # number of requests if some queue is empty
        self._block_size: int = 300
        self._session: Optional[aiohttp.ClientSession] = None

        # creating a queue for each genre
        self.queues = {genre: Queue() for genre in self.clear_genres}

    def get_new_session(self) -> aiohttp.ClientSession:
        """
        Get new session
        """
        return aiohttp.ClientSession()

    @property
    def session(self) -> aiohttp.ClientSession:
        """
        Get session
        """
        if self._session is None or self._session.closed:
            # creating new session if session is none
            self._session = self.get_new_session()
        return self._session

    async def close(self) -> None:
        """
        Session close
        """
        await self.session.close()

    async def get_urls(self, url_source: Union[str, List[str]], queue: Queue) -> None:
        """
        Get urls and queue the result
        """
        tasks = list()

        # checking the number of request sources
        if isinstance(url_source, str):
            for _ in range(self._block_size):
                task = asyncio.create_task(self.session.get(url_source))
                tasks.append(task)
        else:
            for _ in range(self._block_size // 2):
                first_task = asyncio.create_task(self.session.get(url_source[0]))
                second_task = asyncio.create_task(self.session.get(url_source[1]))
                tasks.extend([first_task, second_task])

        responses: List[aiohttp.ClientResponse] = await asyncio.gather(*tasks)
        for response in responses:
            try:
                result = await response.json()
            except ContentTypeError:
                continue
            # check for duplicates
            if result not in queue.queue:
                # queue the result
                queue.put_nowait(result)

    async def get_url(self, genre: str) -> str:
        """
        Get url
        """
        # api case-sensitive
        genre = genre.lower()

        # checking the genre source
        genre_from_computerfreaker = genre in self.genres['computerfreaker']
        genre_from_waifu = genre in self.genres['waifu']

        if genre_from_computerfreaker and genre_from_waifu:
            # multiple sources
            url_source = [
                f"https://api.computerfreaker.cf/v1/{genre}",
                f"https://api.waifu.pics/sfw/{genre}"
            ]
        elif genre_from_computerfreaker:
            # one source
            url_source = f"https://api.computerfreaker.cf/v1/{genre}"
        elif genre_from_waifu:
            # one source
            url_source = f"https://api.waifu.pics/sfw/{genre}"
        # missing genre
        else:
            raise KeyError

        # getting a queue of genre
        queue = self.queues[genre]

        iterations = 0

        # waiting a correct url
        while True:
            try:
                # getting url from the queue
                url: str = queue.get_nowait()['url']
            except KeyError:
                continue
            except Empty:
                if iterations >= 4:
                    return None
                iterations += 1
                # requests to getting new urls as there are none
                await self.get_urls(url_source, queue)
            else:
                return url
