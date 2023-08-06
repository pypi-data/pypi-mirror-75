import os
import asyncio
import functools
from asyncimg._util import get_image
from io import BytesIO
from asyncimg._generator import generate_lovers, generate_frame, generate_stars, generate_colors


class Generator:
    def __init__(self):
        self.lovers_bg = os.path.join(os.path.dirname(__file__), 'assets', 'love.png')
        self.frame_bg = os.path.join(os.path.dirname(__file__), 'assets', 'frame.png')
        self.star_filter = os.path.join(os.path.dirname(__file__), 'assets', 'stars.png')
        self.font = os.path.join(os.path.dirname(__file__), 'assets', 'font.ttf')

    async def lovers(self, boy: str, girl: str) -> BytesIO:
        """
        Generate a lovers card

        Parameters
            boy     Link of boy's image
            girl    Link of girl's image
        """

        args = {
            'boy_image_bytes': await get_image(boy),
            'girl_image_bytes': await get_image(girl),
            'bg_path': self.lovers_bg
        }

        func = functools.partial(generate_lovers, **args)
        image = await asyncio.get_event_loop().run_in_executor(None, func)
        return image

    async def frame(self, profile: str) -> BytesIO:
        """
        Photo in a frame

        Parameters
            profile     Profile pic image
        """

        args = {
            'image_bytes': await get_image(profile),
            'bg_path': self.frame_bg
        }

        func = functools.partial(generate_frame, **args)
        image = await asyncio.get_event_loop().run_in_executor(None, func)

        return image

    async def stars(self, profile):
        """
        Star filtered photo

        Parameters
            profile     Profile pic image
        """
        args = {
            'image_bytes': await get_image(profile),
            'filter_path': self.star_filter
        }
        func = functools.partial(generate_stars, **args)
        image = await asyncio.get_event_loop().run_in_executor(None, func)

        return image

    async def colors(self, profile):
        """
        Star filtered photo

        Parameters
            profile     Profile pic image
        """
        args = {
            'image_bytes': await get_image(profile),
            'font_path': self.font
        }
        func = functools.partial(generate_colors, **args)
        image = await asyncio.get_event_loop().run_in_executor(None, func)

        return image
