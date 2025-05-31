"use client"

import { TrendingUp } from "lucide-react"
import { Area, AreaChart, CartesianGrid, XAxis, YAxis, Label } from "recharts"

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

export const description = "An area chart with gradient fill"

const AreaChartGradient = ({ content }) => {

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
                    <AreaChart
                        accessibilityLayer
                        data={content.chartData}
                        margin={{ top: 10, right: 10, bottom: 20, left: 10 }}
                    >
                        <CartesianGrid vertical={false} />
                        <XAxis
                            dataKey="x"
                            tickLine={false}
                            axisLine={false}
                            tickMargin={8}
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
                        <ChartTooltip cursor={false} content={<ChartTooltipContent />} />
                        <defs>
                            <linearGradient id="fillColor" x1="0" y1="0" x2="0" y2="1">
                                <stop
                                    offset="5%"
                                    stopColor="var(--chart-1)"
                                    stopOpacity={0.8}
                                />
                                <stop
                                    offset="95%"
                                    stopColor="var(--chart-1)"
                                    stopOpacity={0.1}
                                />
                            </linearGradient>
                        </defs>
                        <Area
                            dataKey="y"
                            type="natural"
                            fill="url(#fillColor)"
                            fillOpacity={0.4}
                            stroke="var(--chart-1)"
                            stackId="a"
                        />
                    </AreaChart>
                </ChartContainer>
            </CardContent>
        </Card>
    )
}

export default AreaChartGradient;