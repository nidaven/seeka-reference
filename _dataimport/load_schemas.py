import json
import weaviate
import os


# Note. alternatively you can set a temporary env variable like this:
if os.getenv("OPENAI_API_KEY") is not None:
    print ("OPENAI_API_KEY is ready")
else:
    print ("OPENAI_API_KEY environment variable not found")

client = weaviate.Client(
  url="http://localhost:8888/",
    additional_headers={
        "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")
    }
)



schema = json.load(open("schemas.json"))


def create_weaviate_schema(client, schema):

    # flush the schema and data
    client.schema.delete_all()
    client.schema.create(schema)


create_weaviate_schema(client, schema)

print(client.schema.get())