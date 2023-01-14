import os
from datetime import datetime, timedelta

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.more_info import markup_more_info
from loader import dp
from states.covid_info import GetInfo
from filters import IsPrivate

API_KEY = os.getenv('RAPID_API')
HOST = os.getenv('HOST')
USER_AGENT = os.getenv('USER_AGENT')

today = datetime.today().strftime('%d.%m.%y %H:%M')
past_time = (datetime.today() - timedelta(days=182)).strftime('%d.%m.%y')


async def get_info(country_name):
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": HOST
    }

    url = "https://vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com/api/npm-covid-data/asia"

    response = requests.get(url, headers=headers).json()

    for country in response:
        if country['Country'] == country_name:
            # MAIN DATA
            new_cases = country['NewCases']
            new_deaths = country['NewDeaths']
            new_recovered = country['NewRecovered']

            # statistics
            infection_risk = country['Infection_Risk']
            case_fatality_rate = country['Case_Fatality_Rate']
            recovery_proportion = country['Recovery_Proporation']

            # total data
            active_cases = country['ActiveCases']
            total_deaths = country['TotalDeaths']
            total_recovered = country['TotalRecovered']

            main_message = f"Current data: {today}\n" \
                           f"<b>{country_name.title()}</b>: data for last 6 month (since {past_time})\n\n" \
                           f"New cases: {new_cases}\n" \
                           f"New deaths: {new_deaths}\n" \
                           f"New recovered: {new_recovered}\n\n" \
                           f"<b>\t\tStatistics</b>\n" \
                           f"Infection risk: {infection_risk}\n" \
                           f"Case fatality rate: {case_fatality_rate}\n" \
                           f"Recovery proportion: {recovery_proportion}\n\n" \
                           f"<b>\t\tTotal data\n" \
                           f"Active cases: {active_cases}\n" \
                           f"Total Deaths: {total_deaths}\n" \
                           f"Total revered: {total_recovered}</b>"

            # DETAILS
            state_id = country['id']
            rank = country['rank']
            total_tests = country['TotalTests']
            one_caseevery_x_ppl = country['one_Caseevery_X_ppl']
            one_deathevery_x_ppl = country['one_Deathevery_X_ppl']
            one_testevery_x_ppl = country['one_Testevery_X_ppl']
            deaths_1m_pop = country['Deaths_1M_pop']
            serious_critical = country['Serious_Critical']
            tests_1m_pop = country['Tests_1M_Pop']
            totcases_1m_pop = country['TotCases_1M_Pop']

            details_message = f"Current data: {today}\n" \
                              f"<b>{country_name.title()}</b>: data for last 6 month (since {past_time})\n\n" \
                              f"State id: {state_id}\n" \
                              f"State rank: {rank}\n" \
                              f"Total tests: {total_tests}\n" \
                              f"One Case every x ppl: {one_caseevery_x_ppl}\n" \
                              f"One Death every x ppl: {one_deathevery_x_ppl}\n" \
                              f"One Test every x ppl: {one_testevery_x_ppl}\n" \
                              f"Deaths 1M pop: {deaths_1m_pop}\n" \
                              f"Serious critical: {serious_critical}\n" \
                              f"Tests 1M Pop: {tests_1m_pop}\n" \
                              f"Total cases 1M Pop: {totcases_1m_pop}"

            return main_message, details_message


@dp.message_handler(IsPrivate(), state='*')
async def give_info(message: types.Message, state: FSMContext):
    try:
        info = await get_info(message.text.title())
        await GetInfo.more_info.set()
        await state.set_data({'details': info[1]})
        await message.answer(info[0], reply_markup=markup_more_info)
    except TypeError:
        await GetInfo.choose_country.set()
        await message.reply('Incorrect name')


@dp.callback_query_handler(state=GetInfo.more_info)
async def more_info(call: types.CallbackQuery, state: FSMContext):
    info = await state.get_data()
    if call.data == 'more_info':
        await call.message.edit_reply_markup(reply_markup=None)
        await call.message.answer(info['details'])
        await GetInfo.choose_country.set()
    else:
        await call.message.edit_reply_markup(reply_markup=None)
        await GetInfo.choose_country.set()
