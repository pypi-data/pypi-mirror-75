from asyncimg import Generator
import asyncio
from PIL import Image

g = Generator()
print(dir(g))

link = 'https://res-3.cloudinary.com/crunchbase-production/image/upload/c_lpad,f_auto,q_auto:eco/v1440924046/wi1mlnkbn2jluko8pzkj.png'
loop = asyncio.get_event_loop()

image = loop.run_until_complete(g.fart(link))

Image.open(image).show()