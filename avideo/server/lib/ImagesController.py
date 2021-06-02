import aiohttp
import json

class ImagesController(object):
    def __init__(self, apikey):
        self.apikey = apikey

    async def get_image(self, query):
        url=f'https://pixabay.com/api/?key={self.apikey}&q={query}'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as request:
                text = await request.text()
                jsData = json.loads(text)
                #result = list(map(lambda item: [item['previewURL'],item['previewWidth'],item['previewHeight']], jsData['hits']))
                return jsData['hits']
