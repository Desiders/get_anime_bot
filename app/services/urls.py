import asyncio
import itertools
import random
from typing import Dict, List, Optional, Type

import aiohttp
import fake_headers

from . import exceptions


class GetUrl:
    genres: List[str]
    genres_format_text: Optional[List[str]] = None
    source_and_url: Dict[str, str] = {
        "waifu": "https://api.waifu.pics/sfw/",
        "computerfreaker": "https://api.computerfreaker.cf/v1/"
    }
    source_and_genres: Dict[str, List[str]] = {
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

    def __new__(cls) -> Type['GetUrl']:
        cls.genres = list(
            dict.fromkeys(
                itertools.chain.from_iterable([
                    cls.source_and_genres[source]
                        for source in cls.source_and_genres
                ])
            )
        )
        return super().__new__(cls)

    def __init__(self):
        self._session: Optional[aiohttp.ClientSession] = None
        self._headers: Optional[fake_headers.Headers] = None

    def get_new_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession()

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
        try:
            response_dict = await response.json()
        except aiohttp.ContentTypeError:
            raise exceptions.SourceBlock
        else:
            url = response_dict['url']
            return response_dict['url']

    async def get_url_without_duplicates(self, url: str, received_urls: List[str]) -> str:
        for iteration in range(1, 4):
            try:
                url = await self.get_url(url)
            except exceptions.SourceBlock:
                if iteration > 1:
                    raise exceptions.SourceBlock
            else:
                if url not in received_urls:
                    return url
            await asyncio.sleep(iteration)
        raise exceptions.UrlNotFound

    def get_url_for_request(self, genre: str) -> str:
        genre = genre.lower()
        if genre not in self.genres:
            raise exceptions.UncnownGenre

        sources: List[str] = [
            source
                for source in self.source_and_genres
                  if genre in self.source_and_genres[source]
        ]
        if len(sources) > 1:
            random.shuffle(sources)

        source = sources[0]
        source_url: str = self.source_and_url[source]
        url = source_url + genre
        return url
