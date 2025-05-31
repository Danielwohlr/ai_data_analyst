"use client"

import { TrendingUp } from "lucide-react"
import { CartesianGrid, Line, LineChart, XAxis, YAxis, Label } from "recharts"

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

export const description = "A multiple line chart"

// Predefined chart configuration for y1 through y5
const chartConfig = {
    x: {
        label: "X Axis",
        color: "var(--chart-1)",
    },
    y1: {
        label: "Series 1",
        color: "var(--chart-1)",
    },
    y2: {
        label: "Series 2",
        color: "var(--chart-2)",
    },
    y3: {
        label: "Series 3",
        color: "var(--chart-3)",
    },
    y4: {
        label: "Series 4",
        color: "var(--chart-4)",
    },
    y5: {
        label: "Series 5",
        color: "var(--chart-5)",
    }
};

const LineChartMultiple = ({ content }) => {
    if (!content) {
        return <div>Loading chart data...</div>;
    }

    // Get all keys that start with 'y' from the first data point to create series
    const seriesKeys = Object.keys(content.chartData[0]).filter(key => key.startsWith('y'));

    // Update labels from content if provided
    seriesKeys.forEach(key => {
        if (content.axisLabels[key]) {
            chartConfig[key].label = content.axisLabels[key];
        }
    });

    return (
        <Card>
            <CardHeader>
                <CardTitle>Multiple Series Chart</CardTitle>
                <CardDescription>{content.axisLabels.x} vs {seriesKeys.map(key => chartConfig[key].label).join(', ')}</CardDescription>
            </CardHeader>
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
                                value="Value"
                                angle={-90}
                                position="outsideLeft"
                                dy={0}
                                dx={-20}
                                style={{ textAnchor: 'middle' }}
                            />
                        </YAxis>
                        <ChartTooltip
                            cursor={false}
                            content={<ChartTooltipContent />}
                        />
                        {seriesKeys.map((key) => (
                            <Line
                                key={key}
                                dataKey={key}
                                type="monotone"
                                stroke={chartConfig[key].color}
                                strokeWidth={2}
                                dot={false}
                            />
                        ))}
                    </LineChart>
                </ChartContainer>
            </CardContent>
        </Card>
    )
}

export default LineChartMultiple; 