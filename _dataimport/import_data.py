import json
import weaviate
from uuid import uuid5, NAMESPACE_DNS
import os
import glob
import time

test_length = 30

#pass record index
def add_sermon_to_batch(sermon_record):
    record = {
        "title" : sermon_record["episode_name"],
        "duration" : sermon_record["duration"],
        "url" : sermon_record["audio_url"],
        "summary" : sermon_record["text_summary"],
        "image_url" : sermon_record["image_url"],
        "date" : sermon_record["date"]

    }
    return {
        "record" : record,
        "class" : "Sermon",
        "uuid": str(uuid5(NAMESPACE_DNS, sermon_record["episode_name"].replace(" ","_")))
    }

#pass record index
def add_sermon_segment_to_batch(segment_record):
    record = {
        "snippet" : segment_record["transcript"].strip(),
        "start_time" : str(segment_record["start"]),
        "end_time" : str(segment_record["end"])
    }
    return {
        "record" : record,
        "class" : "SermonSegment",
        "uuid": str(uuid5(NAMESPACE_DNS, record['snippet'].replace(" ","_")+str(len(record['snippet']))))
    }

def handle_results(results):
    if results is not None:
        for result in results:
            if 'result' in result and 'errors' in result['result'] and  'error' in result['result']['errors']:
                for message in result['result']['errors']['error']:
                    print(message['message'])

def import_data(client: weaviate.Client, batch_size, length=None):
    os.chdir('/home/daven/projects/faithwalk/resources/sermons/cci/metadata')

    sermons_info = json.load(open('services.json'))

    os.chdir('/home/daven/projects/faithwalk/resources/sermons/cci/transcripts')

    episodes = glob.glob('episode*')
    episode_idxs = [int(episode.split('episode')[1]) for episode in episodes]
    episode_idxs = sorted(episode_idxs)

    segment_count = 0
    episode_count = 0
    for idx in episode_idxs:
        print(idx)
        sermon_object = add_sermon_to_batch(sermons_info[str(idx)])
        print(sermon_object)
        
        client.data_object.create(sermon_object['record'], sermon_object['class'], sermon_object['uuid'])

        segment = json.load(open('episode'+str(idx) + '/transcript_30secs.json'))
        length_of_segment = len(segment)

        for item in range(0, length_of_segment):
            segment_object = add_sermon_segment_to_batch(segment[str(item)])
            print(segment_object)
            client.batch.add_data_object(segment_object['record'], segment_object['class'], segment_object['uuid'])
            client.batch.add_reference(segment_object['uuid'], segment_object['class'], 'fromSermon', sermon_object['uuid'], sermon_object["class"])
             
            segment_count += 1
            if segment_count == test_length:
                result = client.batch.create_objects()
                result_refs = client.batch.create_references()
                handle_results(result)
                handle_results(result_refs)
                #sleep for 60 seconds
                time.sleep(60)
                segment_count = 0
        episode_count += 1
        if episode_count == 10:
            break
        

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

print(client.is_ready())

import_data(client, test_length)