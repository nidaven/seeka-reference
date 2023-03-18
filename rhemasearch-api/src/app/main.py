from pydantic import BaseModel, root_validator, ValidationError
import fastapi
import weaviate
import os
from loguru import logger
import typing

app = fastapi.FastAPI()

logger.add("out.log", backtrace=True, diagnose=True)

if os.getenv("OPENAI_API_KEY") is not None:
    print ("OPENAI_API_KEY is ready")
else:
    raise ValueError("OPENAI_API_KEY environment variable not found")

if os.getenv("DB_FQDN") is None:
    raise ValueError("DB_FQDN environment variable not found")
else:
    DB_FQDN = os.getenv("DB_FQDN")
    DB_FQDN = 'http://localhost:8887' #TODO: remove before deployment

client = weaviate.Client(
    url=DB_FQDN,
    additional_headers={
        "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")
    }
)

class Snippet(BaseModel):
    snippet: str 
    start_time: str
    sermon_title: str
    url: str
    image_url: str = None
    date: str = None
    summary: str = None

    @root_validator(pre=True)
    def format_input(cls, values):
        values['sermon_title'] = values['fromSermon'][0]['title']
        values['url'] = values['fromSermon'][0]['url'] + '?t=' + str(int(float(values['start_time'])))
        if 'date' in values['fromSermon'][0]:
            values['date'] = values['fromSermon'][0]['date']
        values['summary'] = values['fromSermon'][0]['summary']
        values['image_url'] = values['fromSermon'][0]['image_url']
        return values

class Snippets(BaseModel):
    snippets: list[Snippet]

class SermonSearchQuery:
    pass

sermon_class = "SermonSegment"

query_definition = [
    "snippet",
    "start_time",
    """fromSermon {
    ... on Sermon {title, url, date, summary, image_url}
    }"""
]


@app.get("/")
def get_home_page():
    return 'Welcome to RhemaSearch'

#TODO: entire code to be refactored as into a separate method that returns just the snippets.
#TODO: should accept parameters for limit, keyword, and class object
#TODO: based on query should have mutliple query definitions

@app.get("/sermon/search")
def get_matching_snippets(keyword: str, limit: int = 20, sermon_class: str = sermon_class, query_definition = query_definition):
    sermon_class = sermon_class
    query_definition = query_definition

    near_text_definition = {
        'concepts': [f"{keyword}"]
    }

    result = (
        #TODO: Refactor to database vector search class
        client.query
            .get(sermon_class, 
                query_definition)
            .with_near_text(near_text_definition)
            .with_additional('distance')
            .with_limit(limit)
            .do()
    )['data']['Get']['SermonSegment']

    snippets_list = Snippets(snippets=[Snippet(**snippet) for snippet in result])
    return snippets_list.snippets


@app.get("/sermon/exactsearch")
def get_matching_snippets(keyword: str, limit: int = 20, sermon_class: str = sermon_class, query_definition = query_definition):
    sermon_class = sermon_class
    query_definition = query_definition

    near_text_definition = {
        'concepts': [f"{keyword}"]
    }

    filter_definition = {
        'path': ["snippet"],
        'operator': "Like",
        'valueText': f"{keyword}"
    }

    result = (
        #TODO: Refactor to database vector search class
        client.query
            .get(sermon_class, 
                query_definition)
            .with_near_text(near_text_definition)
            .with_where(filter_definition)
            .with_additional('distance')
            .with_limit(limit)
            .do()
    )['data']['Get']['SermonSegment']
    try:
        snippets_list = Snippets(snippets=[Snippet(**snippet) for snippet in result if keyword in snippet['snippet'].lower()])
    except Exception as e:
        snippets_list = Snippets(snippets=[])
    return snippets_list.snippets