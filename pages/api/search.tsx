import { NextApiRequest, NextApiResponse } from "next";
import weaviateSearch from "./services/weaviatedb";

import getConfig from "next/config"

const { publicRuntimeConfig } = getConfig();

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { searchInput } = req.query;

  let searchService;
  
  if (publicRuntimeConfig.VECTOR_LIBRARY === "weaviate") {
    searchService = weaviateSearch;
  } else {
    return res.status(500).json({ error: "Invalid vector library configuration" });
  }

  try {
    const results = await searchService(searchInput);
    res.status(200).json(results);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}