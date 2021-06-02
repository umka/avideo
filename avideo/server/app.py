import asyncio

from aiohttp import web
import os

from lib.ImagesController import ImagesController

import pdb

ic = ImagesController( os.environ['APIKEY'] )

def formatImg(url, width, height):
    return f'<img src="{url}" width="{width}" height="{height}" >'


async def get_image(request):
    key=os.environ['APIKEY']
    query = request.match_info.get('query', "yellow+flower")
    result = await ic.get_image(query)

    result2 = list(map(lambda item: formatImg(item['previewURL'],item['previewWidth'],item['previewHeight']), result))
    print(result2)

    outputText = '<html><head><title>theResult</title></head><body>' + ''.join(result2) + '</body></html>'
    return web.Response(body=outputText, content_type='text/html' )



if __name__ == '__main__':
    print(os.environ['APIKEY'])
    app = web.Application()
    app.add_routes([web.get('/{query}', get_image)])
    web.run_app(app, port=8081)
