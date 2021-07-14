import asyncio
import itertools
import random
from typing import Dict, List, Optional, Type

import aiohttp
import fake_headers

from . import exceptions


class GetUrl:
    sfw_genres: List[str]
    nsfw_genres: List[str] = [
        'nsfw_neko', 'nsfw_waifu', 'nsfw_trap',
        'blowjob', 'dva', 'hentai'
    ]
    sfw_genres_format_text: Optional[str] = None
    source_and_url: Dict[str, str] = {
        "waifu_sfw": "https://api.waifu.pics/sfw",
        "waifu_nsfw": "https://api.waifu.pics/nsfw",
        "computerfreaker": "https://api.computerfreaker.cf/v1",
    }
    source_and_genres: Dict[str, List[str]] = {
        "waifu_sfw": [
            'neko', 'waifu', 'shinobu', 'megumin',
            'bully', 'cuddle', 'cry', 'hug',
            'awoo', 'kiss', 'lick', 'pat',
            'smug', 'bonk', 'yeet', 'blush',
            'smile', 'wave', 'highfive', 'handhold',
            'nom', 'bite', 'glomp', 'slap',
            'kill', 'kick', 'happy', 'wink',
            'poke', 'dance', 'cringe'
        ],
        "waifu_nsfw": ['nsfw_neko', 'nsfw_waifu', 'nsfw_trap', 'blowjob'],
        "computerfreaker": [
            'neko', 'anime', 'baguette', 'dva',
            'hug', 'yuri', 'hentai'
        ]
    }

    def __new__(cls) -> Type['GetUrl']:
        genres = list(
            dict.fromkeys(
                itertools.chain.from_iterable([
                    cls.source_and_genres[source]
                        for source in cls.source_and_genres
                ])
            )
        )
        cls.sfw_genres = [
            genre
                for genre in genres
                    if genre not in cls.nsfw_genres
        ]
        return super().__new__(cls)

    def __init__(self):
        self._session: Optional[aiohttp.ClientSession] = None
        self._headers: Optional[fake_headers.Headers] = None

    def get_new_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=3.0))

    @property
    def session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = self.get_new_session()
        return self._session

    def get_new_headers(self) -> fake_headers.Headers:
        return fake_headers.Headers()

    @property
    def headers(self) -> fake_headers.Headers:
        if self._headers is None:
            self._headers = self.get_new_headers()
        return self._headers

    async def close(self):
        await self.session.close()

    async def get_url(self, url: str) -> str:
        response = await self.session.get(url, headers=self.headers.generate())
        response_dict = await response.json()

        url = response_dict['url']
        return url

    async def get_url_without_duplicates(self, url: str, received_urls: List[str]) -> str:
        for timeout_sleep in range(1, 5):
            try:
                url = await self.get_url(url)
            except aiohttp.ContentTypeError:
                timeout_sleep = timeout_sleep / 4
            else:
                if url not in received_urls:
                    return url
                timeout_sleep = timeout_sleep / 8
            await asyncio.sleep(timeout_sleep)
        raise exceptions.ManyDuplicates

    def get_url_for_request(self, genre: str) -> str:
        sources: List[str] = [
            source
                for source in self.source_and_genres
                  if genre in self.source_and_genres[source]
        ]
        if len(sources) > 1:
            random.shuffle(sources)
        source = sources[0]
        source_url: str = self.source_and_url[source]

        if genre.startswith("nsfw_"):
            _, genre = genre.split("_")
        url = f"{source_url}/{genre}"
        return url
