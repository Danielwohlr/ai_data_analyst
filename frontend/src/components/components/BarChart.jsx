"use client"

import { TrendingUp } from "lucide-react"
import { Bar, BarChart, CartesianGrid, Label, XAxis, YAxis } from "recharts"

import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import {
    ChartConfig,
    ChartContainer,
    ChartTooltip,
    ChartTooltipContent,
} from "@/components/ui/chart"

export const description = "A bar chart"


const BarChartDefault = ({ content }) => {

    if (!content) {
        return <div>Loading chart data...</div>;
    }

    let chartConfig = {
        x: {
            label: `${content.axisLabels.x}` || "x Axis",
            color: "var(--chart-1)",
        },
        y: {
            label: `${content.axisLabels.y}` || "y Axis",
            color: "var(--chart-1)",
        },
    };


    return (
        <Card>
            <CardHeader>
                <CardTitle>{content.axisLabels.y} / {content.axisLabels.x}</CardTitle>
            </CardHeader>
            <CardContent>
                <ChartContainer config={chartConfig}>
                    <BarChart
                        accessibilityLayer
                        data={content.chartData}
                        margin={{ top: 10, right: 10, bottom: 20, left: 10 }}>
                        <CartesianGrid vertical={false} />
                        <XAxis
                            dataKey="x"
                            tickLine={false}
                            tickMargin={8}
                            axisLine={false}
                            tickFormatter={(value) => value.slice(0, 3)}
                        >
                            <Label
                                value={content.axisLabels?.x || "X Axis"}
                                offset={-10}
                                position="insideBottom"
                            />
                        </XAxis>
                        <YAxis
                            tickLine={false}
                            axisLine={false}
                            tickMargin={8}
                            tickCount={3}
                        >
                            <Label
                                value={content.axisLabels?.y || "Y Axis"}
                                angle={-90}
                                position="outsideLeft"
                                dy={0}
                                dx={-20}
                                style={{ textAnchor: 'middle' }}
                            />
                        </YAxis>
                        <ChartTooltip
                            cursor={true}
                            content={<ChartTooltipContent />}
                        />
                        <Bar dataKey="y" fill="var(--chart-1)" radius={8} />
                    </BarChart>
                </ChartContainer>
            </CardContent>
        </Card>
    )
}

export default BarChartDefault;