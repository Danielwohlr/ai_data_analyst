"use client"

import { TrendingUp } from "lucide-react"
import { Bar, BarChart, CartesianGrid, Label, XAxis, YAxis } from "recharts"

import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import {
    ChartConfig,
    ChartContainer,
    ChartTooltip,
    ChartTooltipContent,
} from "@/components/ui/chart"

export const description = "A stacked bar chart with a legend"

// Predefined chart configuration for the tooltip chart


const Tooltip = ({ content }) => {
    if (!content) {
        return <div>Loading chart data...</div>;
    }

    // Get all keys except 'x' from the first data point to create series
    const seriesKeys = Object.keys(content.chartData[0]).filter(key => key !== 'x');

    let chartConfig = {
        x: {
            label: content.axisLabels.x || "X Axis",
            color: "var(--chart-1)",
        },
        y1: {
            label: content.axisLabels.y1 || "Series 1",
            color: "var(--chart-1)",
        },
        y2: {
            label: content.axisLabels.y2 || "Series 2",
            color: "var(--chart-2)",
        }
    };

    return (
        <Card>
            <CardHeader>
                <CardTitle>{seriesKeys.map(key => content.axisLabels[key]).join(' / ')}</CardTitle>
            </CardHeader>
            <CardContent>
                <ChartContainer config={chartConfig}>
                    <BarChart
                        accessibilityLayer
                        data={content.chartData}
                        margin={{ top: 10, right: 10, bottom: 20, left: 10 }}
                    >
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
                                value="Value"
                                angle={-90}
                                position="outsideLeft"
                                dy={0}
                                dx={-20}
                                style={{ textAnchor: 'middle' }}
                            />
                        </YAxis>
                        {seriesKeys.map((key, index) => (
                            <Bar
                                key={key}
                                dataKey={key}
                                stackId="a"
                                fill={chartConfig[key].color}
                                radius={index === 0 ? [0, 0, 8, 8] : [8, 8, 0, 0]}
                            />
                        ))}
                        <ChartTooltip
                            content={
                                <ChartTooltipContent
                                    hideLabel
                                    className="w-[180px]"
                                    formatter={(value, name, item, index) => (
                                        <>
                                            <div
                                                className="h-2.5 w-2.5 shrink-0 rounded-[2px] bg-(--color-bg)"
                                                style={
                                                    {
                                                        "--color-bg": chartConfig[name].color,
                                                    }
                                                }
                                            />
                                            {content.axisLabels[name]}
                                            <div className="text-foreground ml-auto flex items-baseline gap-0.5 font-mono font-medium tabular-nums">
                                                {value}
                                            </div>
                                            {index === seriesKeys.length - 1 && (
                                                <div className="text-foreground mt-1.5 flex basis-full items-center border-t pt-1.5 text-xs font-medium">
                                                    Total
                                                    <div className="text-foreground ml-auto flex items-baseline gap-0.5 font-mono font-medium tabular-nums">
                                                        {seriesKeys.reduce((sum, key) => sum + item.payload[key], 0)}
                                                    </div>
                                                </div>
                                            )}
                                        </>
                                    )}
                                />
                            }
                            cursor={false}
                        />
                    </BarChart>
                </ChartContainer>
            </CardContent>
        </Card>
    )
}

export default Tooltip; 