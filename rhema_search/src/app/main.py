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
    print ("OPENAI_API_KEY environment variable not found")

client = weaviate.Client(
    url="http://192.168.1.115:8889/",
    additional_headers={
        "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")
    }
)

class Snippet(BaseModel):
    snippet: str 
    start_time: str
    sermon_title: str
    url: str
    date: str = None
    summary: str = None

    @root_validator(pre=True)
    def format_input(cls, values):
        values['sermon_title'] = values['fromSermon'][0]['title']
        values['url'] = values['fromSermon'][0]['url']
        if 'date' in values['fromSermon'][0]:
            values['date'] = values['fromSermon'][0]['date']
        return values

class Snippets(BaseModel):
    snippets: list[Snippet]

class SermonSearchQuery:
    pass


@app.get("/")
def get_home_page():
    return 'Welcome to RhemaSearch'

@app.get("/sermon")
def get_matching_snippets(keyword: str, limit: int = 5):
    sermon_class = "SermonSegment"

    query_definition = [
        "snippet",
        "start_time",
        """fromSermon {
        ... on Sermon {title, url, date}
        }"""
    ]

    near_text_definition = {
        'concepts': [f"{keyword}"]
    }

    result = (
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