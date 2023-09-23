import Head from "next/head"
import Link from "next/link"

import { siteConfig } from "@/config/site"
import { Layout } from "@/components/layout"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import ResultCard from "@/components/result-card"
import { Separator } from "@/components/ui/separator"
import { Icons } from "@/components/icons"
import { useState } from "react"
import getConfig from "next/config"
import next from "next/types"

const queryDefinition = "snippet start_time fromSermon { ... on Sermon {title, url, date, summary, image_url } }";

export default function IndexPage() {
  const [searchInput, setSearchInput] = useState('');
  const [result, setResult] = useState([]);
  const [isLoading, setIsLoading] = useState<boolean>(false)

  const handleSearchClick = async () => {
    setIsLoading(true);
  
    try {
      const response = await fetch(`/api/search?searchInput=${searchInput}`);
      const data = await response.json();
      console.log(data);
      setResult(data);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Layout>
      <Head>
        <title>Seeka</title>
        <meta
          name="description"
          content="Next.js template for buildlsing apps with Radix UI and Tailwind CSS"
        />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <section className="container grid items-center gap-6 pt-6 pb-4 md:pt-10 px-10 ">
        <div className="flex max-w-[980px] flex-col items-start gap-2">
          <h1 className="text-3xl font-extrabold leading-tight tracking-tighter sm:text-3xl md:text-5xl lg:text-6xl">
            Seeka <br className="hidden sm:inline" />
          </h1>
          <p className="max-w-[700px] text-lg text-slate-700 dark:text-slate-400 sm:text-xl items-center justify-center">
            <br className="hidden sm:inline" /> Remember only the word or phrase from a sermon? <br></br>Let&apos;s help you find it.
          </p>
        </div>
        <div className="flex flex-col items-center gap-4 md:flex-row">
          <Input
            id="search-input"
            className="w-full"
            placeholder="Search for a sermon"
            value={searchInput}
            onChange={(event) => setSearchInput(event.target.value)}
          />
          <Button disabled={isLoading} onClick={() => handleSearchClick()} className="w-full max-w-lg">
          {isLoading && (
              <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />
            )}
            Search
          </Button>
        </div>
      </section>
      <section className="container grid items-center gap-6 pt-2 pb-2 md:py-10 px-2 sm:py-4 ">
        <div className="items-start justify-center gap-6 rounded-lg p-4 md:grid lg:grid-cols-2">
         {result.length > 0 ? (<div className="m-4 text-muted-foreground">{`Found ${result.length} results`}</div>) : null}
          <div className="col-span-2 grid items-start gap-6">
            {result.map((item, index) => (
              <ResultCard
                key={item.url}
                text={item.snippet}
                title={item.sermon_title}
                url={item.url}
                image={item.image_url}
                timestamp={item.start_time}
              />
            ))}
          </div>
        </div>
      </section>
    </Layout>
  )
}
