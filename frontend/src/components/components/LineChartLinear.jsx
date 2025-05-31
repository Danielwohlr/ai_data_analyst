"use client"

import { TrendingUp } from "lucide-react"
import { CartesianGrid, Line, LineChart, XAxis } from "recharts"

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

export const description = "A linear line chart"


const LineChartLinear = ({ content }) => {

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
                    <LineChart
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
                        />
                        <ChartTooltip
                            cursor={false}
                            content={<ChartTooltipContent hideLabel />}
                        />
                        <Line
                            dataKey="y"
                            type="linear"
                            stroke="var(--chart-1)"
                            strokeWidth={2}
                            dot={false}
                        />
                    </LineChart>
                </ChartContainer>
            </CardContent>
        </Card>
    )
}

export default LineChartLinear;
