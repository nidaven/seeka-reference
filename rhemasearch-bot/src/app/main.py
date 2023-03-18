import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import os
import requests
import aiohttp
import asyncio
from pydantic import BaseModel, Field, validator, HttpUrl
from typing import Optional
import re

async def http_get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()


def sec_to_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return '{:d}h:{:02d}m:{:02d}s'.format(hours, minutes, seconds)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class SermonResult(BaseModel):
    snippet: str
    start_time: str
    sermon_title: str
    url: HttpUrl
    date: str = None
    summary: str = None
    
    # @validator('snippet')
    # def italic(cls, v):
    #     return "<i>" + v + "</i>"
    
    @validator('sermon_title')
    def bold(cls, v):
        return "<b>" + v + "</b>"
    
    def __str__(self):
        #wrap url around text
        timestamp = int(float(self.start_time))
        # link = rf"{self.url}?t={timestamp}"
        link = rf"{self.url}?t={timestamp}"
        title_html_link = f'<a href="{link}">{self.sermon_title}</a>'
        return f"\"...{self.snippet}...\"\n\nSermon: {title_html_link}\nTimestamp: {sec_to_time(timestamp)}"


API_URL = os.environ.get('API_URL')
API_URL = 'http://localhost:8001' #TODO: remove before deployment
TOKEN = os.environ.get('BOT_TOKEN')

overview = 'You can perform either an exact search or a semantic search. \n\n'
semantic_search_desc = 'Semantic search is a search that returns results that are semantically similar to the search term. \n\n'
exact_search = '<b>Exact search:</b> \n/exactsearch <i>search term</i> \n\n'
semantic_search = '<b>Semantic search:</b> \n/search <i>search term</i> \n\n'


def get_unique_sermons_info(results_list):
    """
    This function takes a list of dictionaries as input and returns a list of unique dictionaries.

    Args:
    list_of_dicts (list): A list of dictionaries.

    Returns:
    list: A list of unique dictionaries.
    """
    keys_to_extract = ['sermon_title', 'image_url', 'date', 'summary']
    # print(results_list[0])
    results_list = [{key: d[key] for key in keys_to_extract} for d in results_list]

    tuple_list = [tuple(d.items()) for d in results_list]
    unique_tuples = set(tuple_list)
    unique_dicts = [dict(t) for t in unique_tuples]

    return unique_dicts


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    search_start_desc = "Hi there! I'm Seeka, Enter the search term to search for snippets in sermons."
    full_start_msg = search_start_desc + overview + semantic_search_desc + exact_search + semantic_search
    await context.bot.send_message(chat_id=update.effective_chat.id, text=full_start_msg, parse_mode="HTML")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = overview + semantic_search_desc + exact_search + semantic_search
    await update.message.reply_text(help_text, parse_mode="HTML")


async def search_sermon(update: Update, context: ContextTypes.DEFAULT_TYPE, exact_search=False):
    try:
        search_term = ' '.join(context.args)
        query = str(search_term)
        query_str = '<i>' + query + '</i>'
        await update.message.reply_text("Searching for sermons on: " + query_str, parse_mode="HTML")

        if exact_search == False:
            search_url = API_URL + "/sermon/search?keyword=" + query
        else:
            search_url = API_URL + "/sermon/exactsearch?keyword=" + query

        res = await http_get(search_url)

        if res is None:
            await update.message.reply_text("No results found")
        else:
            #get first 10 results from res
            res = res[:10]
            unique_sermons = get_unique_sermons_info(res)
            await update.message.reply_text("Displaying top " + str(len(res)) + " results across " + str(len(unique_sermons)) + " sermons")
            count = 0
            #for each sermon, get the snippets
            # for sermon in unique_sermons:
            #     if len(sermon['summary']) > 350:
            #         sermon['summary'] = sermon['summary'][:350] + '...'
                
            #     await update.message.reply_text(f'Results from Sermon {count + 1} of {len(unique_sermons)}')
            #     await update.message.reply_photo(photo=sermon['image_url'], caption=f'<b>{sermon["sermon_title"]}</b> \n\n{sermon["date"]} \n\n<b>Summary:</b>\n{sermon["summary"]}', parse_mode="HTML")
            #     snippets = [item for item in res if item['sermon_title'] == sermon['sermon_title']]
            #     for snippet in snippets:
            #         if snippet['url'] is not None:
            #             ep_time = sec_to_time(int(float(snippet['start_time'])))
            #             button = InlineKeyboardButton(text=f'Jump to timestamp on Spotify', url=snippet['url'])
            #             keyboard = InlineKeyboardMarkup([[button]])
            #             if search_term in snippet['snippet']:
            #                 snippet['snippet'] = snippet['snippet'].replace(search_term, f'<b>{search_term}</b>')
            #             await update.message.reply_text(str(SermonResult(**snippet)), parse_mode="HTML", reply_markup=keyboard)
            #             #sleep for 1 second to avoid spamming
            #             await asyncio.sleep(0.5)

            for snippet in res:
                if snippet['url'] is not None:
                    ep_time = sec_to_time(int(float(snippet['start_time'])))
                    button = InlineKeyboardButton(text=f'Listen on Spotify @ {ep_time} ->', url=snippet['url'])
                    keyboard = InlineKeyboardMarkup([[button]])                   
                    search_term_list = search_term.split(' ')
                    for term in search_term_list:
                        snippet['snippet'] = re.sub(r'(?i)(' + term + ')', rf'<i><b>{term}</b></i>', snippet['snippet'])
                    await update.message.reply_text(str(SermonResult(**snippet)), parse_mode="HTML", reply_markup=keyboard)
                    #sleep for 1 second to avoid spamming
                    await asyncio.sleep(0.5)               
                count += 1
            
            await update.message.reply_text(f'End of results')
                 
    except(IndexError, ValueError):
        await update.message.reply_text("Please enter a search term")

async def search_sermon_fuzzy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await search_sermon(update, context)

async def search_sermon_exact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await search_sermon(update, context, exact_search=True)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('search', search_sermon_fuzzy))
    application.add_handler(CommandHandler('exactsearch', search_sermon_exact))
    
    application.run_polling()