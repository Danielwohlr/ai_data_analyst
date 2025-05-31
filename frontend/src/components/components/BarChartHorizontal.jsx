"use client"

import { TrendingUp } from "lucide-react"
import { Bar, BarChart, XAxis, YAxis } from "recharts"

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

export const description = "A horizontal bar chart"

const BarChartHorizontal = ({ content }) => {

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
            <CardContent>
                <ChartContainer config={chartConfig}>
                    <BarChart
                        accessibilityLayer
                        data={content.chartData}
                        layout="vertical"
                        margin={{ top: 10, right: 10, bottom: 20, left: 10 }}
                    >
                        <XAxis type="number" dataKey="x" hide >
                            <Label
                                value={content.axisLabels?.x || "X Axis"}
                                offset={-10}
                                position="insideBottom"
                            />
                        </XAxis>
                        <YAxis
                            dataKey="y"
                            type="category"
                            tickLine={false}
                            tickMargin={10}
                            axisLine={false}
                            tickFormatter={(value) => value.slice(0, 3)}
                        />
                        <ChartTooltip
                            cursor={false}
                            content={<ChartTooltipContent hideLabel />}
                        />
                        <Bar dataKey="x" fill="var(--chart-1)" radius={5} />
                    </BarChart>
                </ChartContainer>
            </CardContent>
        </Card>
    )
}

export default BarChartHorizontal;