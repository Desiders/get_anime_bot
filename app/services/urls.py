import asyncio
import itertools
import random
import typing

import aiohttp
import fake_headers

from . import exceptions


class GetUrl:
    __hash__ = None
    __slots__ = (
        '_session',
        '_headers',
    )

    sfw_genres: typing.List[str]
    sfw_genres_format_text: typing.Optional[str] = None

    nsfw_genres = [
        'nsfw_neko', 'nsfw_waifu', 'nsfw_trap', 'blowjob',
        'hentai', 'ass', 'boobs', 'cum',
        'feet', 'spank', 'gasm', 'lesbian',
        'lewd', 'pussy', 'bellevid', 'gif',
        'anal', 'feet', 'holo', 'futanari',
        'hololewd', 'lewdkemo', 'solog', 'feetg',
        'erokemo', 'les', 'lewdk', 'yuri',
    ]

    url_by_source = {
        "waifu_sfw": "https://api.waifu.pics/sfw",
        "waifu_nsfw": "https://api.waifu.pics/nsfw",
        "nekos.fun": "http://api.nekos.fun:8080/api",
        "nekos.life": "https://nekos.life/api/v2/img",
    }

    genres_by_source = {
        "waifu_sfw": [
            'neko', 'waifu', 'shinobu', 'megumin',
            'bully', 'cuddle', 'cry', 'hug',
            'awoo', 'kiss', 'lick', 'pat',
            'smug', 'bonk', 'yeet', 'blush',
            'smile', 'wave', 'highfive', 'handhold',
            'nom', 'bite', 'glomp', 'slap',
            'kill', 'kick', 'happy', 'wink',
            'poke', 'dance', 'cringe',
        ],
        "waifu_nsfw": [
            'nsfw_neko', 'nsfw_waifu', 'nsfw_trap', 'blowjob',
        ],
        "nekos.fun": [
            'kiss', 'lick', 'hug', 'baka',
            'cry', 'poke', 'smug', 'slap',
            'tickle', 'pat', 'laugh', 'feed',
            'cuddle', 'ass', 'blowjob',
            'boobs', 'cum', 'feet', 'hentai',
            'wallpapers', 'spank', 'gasm', 'lesbian',
            'lewd', 'pussy', 'bellevid', 'gif',
            'anal', 'feed', 'animalears', 'feet',
            'holo', 'foxgirl', 'baka', 'neko',
        ],
        "nekos.life": [
            'feet', 'nsfw_trap', 'futanari',
            'hololewd', 'lewdkemo', 'solog', 'feetg',
            'cum', 'erokemo', 'les', 'lewdk',
            'ngif', 'tickle',
        ]
    }

    def __new__(cls) -> 'GetUrl':
        genres = list(
            dict.fromkeys(
                itertools.chain.from_iterable([
                    cls.genres_by_source[source]
                    for source in cls.genres_by_source
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
        self._session: typing.Optional[aiohttp.ClientSession] = None
        self._headers: typing.Optional[fake_headers.Headers] = None

    def get_new_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=1.5),
        )

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
        response_json: dict[str, str] = await response.json()

        return response_json.get("url") or response_json['image']

    async def get_url_without_duplicates(
        self,
        url: str,
        received_urls: typing.List[str],
    ) -> str:
        for _ in range(30):
            try:
                url = await self.get_url(url)
            except aiohttp.ContentTypeError:
                pass
            else:
                if url not in received_urls:
                    return url
            await asyncio.sleep(0.05)
        raise exceptions.ManyDuplicates

    def get_url_for_request(self, genre: str) -> str:
        sources = [
            source
            for source in self.genres_by_source
            if genre in self.genres_by_source[source]
        ]
        if len(sources) > 1:
            random.shuffle(sources)

        source = sources[0]
        source_url = self.url_by_source[source]

        if genre.startswith("nsfw_"):
            _, genre = genre.split("_", maxsplit=1)

        return f"{source_url}/{genre}"
