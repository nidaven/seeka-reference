// services/searchService.ts
import weaviate, { WeaviateClient } from "weaviate-ts-client";

const client: WeaviateClient = weaviate.client({
  scheme: "http",
  host: "192.168.1.115:8891",
});

interface Snippet {
  snippet: string;
  start_time: string;
  sermon_title: string;
  url: string;
  image_url?: string;
  date?: string;
  summary?: string;
}

interface Snippets {
  snippets: Snippet[];
}

const queryDefinition = "snippet start_time fromSermon { ... on Sermon {title, url, date, summary, image_url } }";

async function weaviateSearch(searchInput: string): Promise<Snippet[]> {
  const limit = 20;
  const sermon_class = "SermonSegment" 
  const query_definition = queryDefinition 

  const res = await client.graphql
    .get()
    .withNearText({
      concepts: [searchInput],
    })
    .withClassName(sermon_class)
    .withFields(query_definition)
    .withLimit(limit)
    .do();

  const results = res.data.Get.SermonSegment;

  const snippetsList: Snippets = { snippets: results.map((snippet: any) => ({
    snippet: snippet.snippet,
    start_time: snippet.start_time,
    sermon_title: snippet.fromSermon[0].title,
    url: `${snippet.fromSermon[0].url}?t=${Math.floor(parseFloat(snippet.start_time))}`,
    image_url: snippet.fromSermon[0].image_url,
    date: snippet.fromSermon[0].date,
    summary: snippet.fromSermon[0].summary
  }))};

  return snippetsList.snippets.filter((snippet) => snippet.snippet.split(' ').length > 10);
}

export default weaviateSearch