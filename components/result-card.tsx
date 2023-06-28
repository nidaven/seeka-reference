`use client`

import { Circle } from "lucide-react"
import { History } from "lucide-react"
import { Button } from "./ui/button"
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "./ui/card"
import { Separator } from "./ui/separator"

type Props = {
    title: string
    text: string
    url: string
    //   category: string
    //   author: string
    image: string
    timestamp: string
}

function divmod(x: number, y: number): [number, number] {
    const quotient = Math.floor(x / y)
    const modulus = x % y
    return [quotient, modulus]
}

function sec_to_time(seconds: number): string {
    let [minutes, secs] = divmod(seconds, 60);
    let [hours, remainingMinutes] = divmod(minutes, 60);
    return `${hours}h:${remainingMinutes.toLocaleString('en-US', { minimumIntegerDigits: 2, useGrouping: false })}m:${secs.toLocaleString('en-US', { minimumIntegerDigits: 2, useGrouping: false })}s`
}

function ResultCard({ title, text, image, timestamp }: Props) {

    const formatted_time = sec_to_time(parseInt(timestamp))
    return (
        <Card className="max-w-[780px]">
            <CardHeader className="grid md:grid-cols-[1fr_100px] items-start gap-4 space-y-0">
                <div>
                    <CardDescription className="text-ellipsis p-2">
                        <p className="text-8xl text-center h-16 text-gray-400">&ldquo;</p>
                        <p className="text-md italic">...{text}...</p>
                    </CardDescription>
                    <Separator className="my-4"/>
                    <div className="mt-4" >
                        <div className="m-2 mt-4 flex items-center">
                            <Circle className="mr-2 h-3 w-3 fill-sky-400 text-sky-400" />
                            <div className="text-sm font-medium leading-none text-muted-foreground">{title}</div>
                        </div>
                        <div className="m-1 mt-2 flex items-center">
                            <History className="mr-2 h-3 w-3" />
                            <div className="text-sm text-muted-foreground">{formatted_time}</div>
                        </div>
                    </div>
                </div>
                <div className="flex items-center">
                    <img src={image} alt="description-of-image" className="h-100 w-100 object-cover">
                    </img>
                </div>
            </CardHeader>
        </Card>
    )
}

export default ResultCard