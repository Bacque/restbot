from aiogram import types
from aiogram.dispatcher import FSMContext

import requests

from loader import dp
from keyboards.inline.news_menu import start, middle, end
from states.covid_news import GetNews
from states.covid_info import GetInfo
from filters import IsPrivate


async def get_news():

    url = "https://vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com/api/news/get-coronavirus-news/0"

    headers = {
        "X-RapidAPI-Key": "2d21880ffcmsh4af669a56379968p14ec84jsn4b232373db9e",
        "X-RapidAPI-Host": "vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers).json()

    news_list = list()

    for new_info in response['news']:
        title = new_info['title']
        link = new_info['link']
        publication_date = new_info['imageFileName'][:24]
        content = new_info['content']
        reference = new_info['reference']

        msg = f"Publication date: {publication_date}\n" \
              f"<a href='{link}'><b>{title}</b></a>\n\n" \
              f"Content:\n{content}\n\n" \
              f"<b>Reference: {reference}</b>"

        news_list.append(msg)

    return news_list


@dp.message_handler(IsPrivate(), text='/news', state='*')
async def news_command(message: types.Message, state: FSMContext):
    news_list = await get_news()
    await state.set_data({'data': news_list})

    await GetNews.news_menu.set()
    await state.update_data({'position': 0})

    await message.answer(news_list[0], reply_markup=start)


@dp.callback_query_handler(state=GetNews.news_menu)
async def switch_menu(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    news_list = data['data']

    position_info = await state.get_data()
    position = position_info['position']

    try:
        if call.data == 'close':
            await GetInfo.choose_country.set()
            await call.message.edit_reply_markup(reply_markup=None)
        elif call.data == 'next' and position == 8:
            await state.update_data({'position': position + 1})
            await call.message.edit_text(news_list[position + 1], reply_markup=end)
        elif call.data == 'previous' and position == 1:
            await state.update_data({'position': position - 1})
            await call.message.edit_text(news_list[position - 1], reply_markup=start)
        else:
            if call.data == 'next':
                await state.update_data({'position': position + 1})
                await call.message.edit_text(news_list[position + 1], reply_markup=middle)
            elif call.data == 'previous':
                await state.update_data({'position': position - 1})
                await call.message.edit_text(news_list[position - 1], reply_markup=middle)
    except Exception as ex:
        print(ex)
