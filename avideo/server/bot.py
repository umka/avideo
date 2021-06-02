import logging
import os
import pdb
import re

from lib.ImagesController import ImagesController

from aiogram import Bot, Dispatcher, executor, types

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=os.environ['BOTKEY'])

dp = Dispatcher(bot)

ic = ImagesController( os.environ['APIKEY'] )

def formatImg(url, width, height):
    return f'<img src="{url}" width="{width}" height="{height}" >'

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(regexp='(^cat[s]?$|puss)')
async def cats(message: types.Message):
    with open('data/cats.jpg', 'rb') as photo:
        '''
        # Old fashioned way:
        await bot.send_photo(
            message.chat.id,
            photo,
            caption='Cats are here 😺',
            reply_to_message_id=message.message_id,
        )
        '''

        await message.reply_photo(photo, caption='Cats are here 😺')

#@dp.message_handler(regexp='(^image[s]?$|^pic)')
@dp.message_handler(commands=['image', 'picture', 'pic'])
async def images(message: types.Message):
    s2 = message.text.split()[1:]
    query = '+'.join(s2)

    result = await ic.get_image(query)

    media = types.MediaGroup()
    for img in result[1:5]:
        media.attach_photo(img['previewURL'])
    logging.info('result sended:' + ','.join(list( map(lambda x: x['previewURL'], result[1:5]) ) ) )

    await message.reply_media_group(media=media)

    #result2 = list(map(lambda item: formatImg(item['previewURL'],item['previewWidth'],item['previewHeight']), result))

    #await message.reply("Images: " + "".join(result2) )

@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
