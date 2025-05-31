'use client'
import 'github-markdown-css/github-markdown.css'
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import ReactMarkdown from "react-markdown";
import LineChartLinear from "@/components/components/LineChartLinear"
import AreaChartGradient from "@/components/components/AreaChartGradient"
import BarChart from "@/components/components/BarChart"
import BarChartHorizontal from "@/components/components/BarChartHorizontal"
import DataTable from "@/components/components/DataTable";
import LineChartMultiple from "@/components/components/LineChartMultiple"


const Message = ({ msg, idx }) => {

    if (msg.role === "table") {
        return (
            <DataTable content={msg.content} />
        )
    }

    if (msg.role === "lineChart") {
        return (
            <LineChartLinear content={msg.content} />
        )
    }

    if (msg.role === "barChart") {
        return (
            <BarChart content={msg.content} />
        )
    }

    if (msg.role === "barChartHorizontal") {
        return (
            <BarChartHorizontal content={msg.content} />
        )
    }

    if (msg.role === "areaChartGradient") {
        return (
            <AreaChartGradient content={msg.content} />
        )
    }

    if (msg.role === "lineChartMultiple") {
        return (
            <LineChartMultiple content={msg.content} />
        )
    }

    if (msg.role === "assistant") {
        return (

            <div className="flex justify-start">
                <Card
                    className="p-3 max-w-full border-none shadow-none bg-white">
                    <CardContent
                        className="p-0 "
                        idx={idx}>
                        <article className="markdown-body break-words overflow-x-auto max-w-full">
                            <ReactMarkdown>
                                {msg.content}
                            </ReactMarkdown>
                        </article>
                    </CardContent>
                </Card >
            </div>
        )
    }


    if (msg.role === 'user') {
        return (

            <div className="flex justify-start">
                <Card
                    className="p-3 w-fit shadow-none border-none bg-neutral-100">
                    <CardContent
                        className="p-0"
                        key={idx}>
                        {msg.content}
                    </CardContent>
                </Card >
            </div>
        )
    }
}

export default Message;