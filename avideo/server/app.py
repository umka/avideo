import asyncio
import aiohttp
from aiohttp import web
import json
import os

import pdb

def formatImg(url, width, height):
    return f'<img src="{url}" width="{width}" height="{height}" >'


async def get_food_image(request):
    key=os.environ['APIKEY']
    query = request.match_info.get('query', "yellow+flower")
    url=f'https://pixabay.com/api/?key={key}&q={query}'
    #pdb.set_trace()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as request:
            text = await request.text()
            jsData = json.loads(text)
            result = list(map(lambda item: formatImg(item['previewURL'],item['previewWidth'],item['previewHeight']), jsData['hits']))
            #pdb.set_trace()
            print(request.status)
            print(result)
            outputText = '<html><head><title>theResult</title></head><body>' + ''.join(result) + '</body></html>'
            return web.Response(body=outputText, content_type='text/html' )


if __name__ == '__main__':
    print(os.environ['APIKEY'])
    app = web.Application()
    app.add_routes([web.get('/{query}', get_food_image)])
    web.run_app(app, port=8081)
