import asyncio
import aiohttp
from aiohttp import web
import pdb
import os


async def get_food_image(request):
    key=os.environ['APIKEY']
    query = request.match_info.get('query', "yellow+flower")
    url=f'https://pixabay.com/api/?key={key}&q={query}'
    #pdb.set_trace()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as request:
            text = await request.text()
            #pdb.set_trace()
            print(request.status)
            print(text)
            return web.Response(text=text)


if __name__ == '__main__':
    print(os.environ['APIKEY'])
    app = web.Application()
    app.add_routes([web.get('/{query}', get_food_image)])
    web.run_app(app, port=8081)
