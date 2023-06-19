import Head from "next/head"
import Link from "next/link"

import { siteConfig } from "@/config/site"
import { Layout } from "@/components/layout"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import ResultCard from "@/components/result-card"
import { Separator } from "@/components/ui/separator"

const result = [
  {
    "snippet": "makes sense. Makes sense of love. You know about love? Love is a feeling that you feel when you feel something you never ever... We are talking nonsense because it's nice, it sounds nice, doesn't mean it's true. Love is a feeling that you feel what you feel, something you're doing. I will really not know the feeling if you've never felt it before. Praise the name of Jesus. And I have some of those expectations and perceptions here.",
    "start_time": "1697.48",
    "sermon_title": "Lovecode Conference (17th February 2019) – Pst. Laju Iren ",
    "url": "https://anchor.fm/s/efc0a2c/podcast/play/5744913/https%3A%2F%2Fd3ctxlq1ktw2nl.cloudfront.net%2Fproduction%2F2019-9-6%2F26823621-22050-2-a20786c64b5b6.mp3?t=1697",
    "image_url": "https://d3t3ozftmdmh3i.cloudfront.net/production/podcast_uploaded_episode/2413987/2413987-1570514933629-61f6d8d96b5c3.jpg",
    "date": null,
    "summary": "3 Cardinal Factors in every successful romantic relationship\nRomance\nDuty\nPurpose\n"
  },
  {
    "snippet": "At the end of the day, she looked at me and said, do you love me? He asked Adam, do you love me? He said, who else will I love? Look around.",
    "start_time": "2220.88",
    "sermon_title": "Lovecode Conference (10th February 2019) – Pst. Emmanuel Iren",
    "url": "https://anchor.fm/s/efc0a2c/podcast/play/5744830/https%3A%2F%2Fd3ctxlq1ktw2nl.cloudfront.net%2Fproduction%2F2019-9-6%2F26823574-22050-2-cbc45fc463648.mp3?t=2220",
    "image_url": "https://d3t3ozftmdmh3i.cloudfront.net/production/podcast_uploaded_episode/2413987/2413987-1570514641249-92a30a015d811.jpg",
    "date": null,
    "summary": "In Christ, In love and In trouble\nIf you don’t understand the work attached to relationships it’s the same as not understanding what it is.\nUnderstanding that something is not easy is a good thing, so you can prepare yourself for the work ahead.\n"
  },
  {
    "snippet": "understand the love of Christ, you're willing to lead on your life. But you are going to choose somebody who doesn't understand the same thing and you put yourself in trouble. Praise the name of Jesus. So love is more of a commitment than anything else. Love is not attraction. Let me give you an example. I wonder if you have heard us married people say, don't worry, just be patient. When you get married, you're going to have sex every day if you want. If you had us say, don't worry,",
    "start_time": "2029.28",
    "sermon_title": "Lovecode Conference (17th February 2019) – Pst. Laju Iren ",
    "url": "https://anchor.fm/s/efc0a2c/podcast/play/5744913/https%3A%2F%2Fd3ctxlq1ktw2nl.cloudfront.net%2Fproduction%2F2019-9-6%2F26823621-22050-2-a20786c64b5b6.mp3?t=2029",
    "image_url": "https://d3t3ozftmdmh3i.cloudfront.net/production/podcast_uploaded_episode/2413987/2413987-1570514933629-61f6d8d96b5c3.jpg",
    "date": null,
    "summary": "3 Cardinal Factors in every successful romantic relationship\nRomance\nDuty\nPurpose\n"
  },
  {
    "snippet": "every aspect of okay look at the salvation of your soul you are in love with someone you've never seen it's crazy well maybe you don't realize how crazy you are",
    "start_time": "2796.36",
    "sermon_title": "Faith is Visionary",
    "url": "https://anchor.fm/s/efc0a2c/podcast/play/5744746/https%3A%2F%2Fd3ctxlq1ktw2nl.cloudfront.net%2Fproduction%2F2019-9-5%2F26818957-22050-2-44f094cfd7ad.mp3?t=2796",
    "image_url": "https://d3t3ozftmdmh3i.cloudfront.net/production/podcast_uploaded_episode/2413987/2413987-1570514287102-07c043d16736d.jpg",
    "date": null,
    "summary": "Mark 11:24 KJVS\nTherefore I say unto you, What things soever ye desire, when ye pray, believe that ye receive them, and ye shall have them.\nYou must have the unseen evidence first. Believe you have them first, before you receive.\nHebrews 11:3 KJVS\nThrough faith, we understand that the worlds were framed by the word of God, so that things which are seen were not made of things which do appear.\nThe things we now see were made from things we couldn’t see with the natural eyes, unseen to the natural eyes but not to the eyes of faith.\nHebrews 11:10 KJVS\nFor he looked for a city which hath foundations, whose builder and maker is God. [14] For they that say such things declare plainly that they seek a country. [15] And truly, if they had been mindful of that country from whence they came out, they might have had opportunity to have returned. [16] But now they desire a better country, that is, an heavenly: wherefore God is not ashamed to be called their God: for he hath prepared for them a city.\nThat’s visionary faith because they saw this but now we have this!\n"
  },
]

export default function IndexPage() {
  return (
    <Layout>
      <Head>
        <title>Next.js</title>
        <meta
          name="description"
          content="Next.js template for building apps with Radix UI and Tailwind CSS"
        />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <section className="container grid items-center gap-6 pt-6 pb-8 md:py-10 px-10 ">
        <div className="flex max-w-[980px] flex-col items-start gap-2">
          <h1 className="text-3xl font-extrabold leading-tight tracking-tighter sm:text-3xl md:text-5xl lg:text-6xl">
            Rhemasearch <br className="hidden sm:inline" />
          </h1>
          <p className="max-w-[700px] text-lg text-slate-700 dark:text-slate-400 sm:text-xl items-center justify-center">
            <br className="hidden sm:inline" /> Search across sermons and get accurate timestamps.
          </p>
        </div>
        <div className="flex flex-col items-center gap-4 md:flex-row">
          <Input className="w-full" placeholder="Search for a sermon" />
          <Button className="w-full max-w-lg">Search</Button>
        </div>
      </section>
      <section className="container grid items-center gap-6 pt-2 pb-2 md:py-10 px-2 sm:py-4 ">
        <div className="mx-10 text-gray-400 text-muted-foreground">Found 2 results</div>
        <div className="items-start justify-center gap-6 rounded-lg p-8 md:grid lg:grid-cols-2">
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
