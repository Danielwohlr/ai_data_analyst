import { configureStore, createSlice } from '@reduxjs/toolkit'


const template_messages = [
    { role: 'user', content: 'Hello, what’s the weather like today?' },
    { role: 'assistant', content: 'The weather is sunny and 24°C in your location.' },
    { role: 'user', content: 'Thanks! Can you summarize the news headlines?' },
    { role: 'assistant', content: 'Sure! Here are today’s top headlines: 1) Markets rise... 2) Tech merger... 3) SpaceX launch...' },
    { role: 'user', content: 'Hello, what’s the weather like today?' },
    {
        role: 'lineChart', content: {
            chartData: [
                { x: "January", y: 186 },
                { x: "February", y: 305 },
                { x: "March", y: 237 },
                { x: "April", y: 73 },
                { x: "May", y: 209 },
                { x: "June", y: 214 },
            ],
            axisLabels: { x: "Month", y: "Some value" }
        }
    },
    { role: 'assistant', content: 'The weather is sunny and 24°C in your location.' },
    { role: 'user', content: 'Thanks! Can you summarize the news headlines?' },
    {
        role: 'areaChartGradient', content: {
            chartData: [
                { x: "January", y: 186 },
                { x: "February", y: 305 },
                { x: "March", y: 237 },
                { x: "April", y: 73 },
                { x: "May", y: 209 },
                { x: "June", y: 214 },
            ],
            axisLabels: { x: "Month", y: "Some value" }
        }
    },
    {
        role: 'assistant', content: `
# Sales Report

Here is the **monthly sales data** for Q1:

| Month | Sales |
|-------|-------|
| Jan   | 100   |
| Feb   | 200   |
| Mar   | 300   |

## Summary

- January sales were low.
- February sales doubled.
- March sales increased by 50%.

\`\`\`js
// Sample sales calculation
const totalSales = 100 + 200 + 300;
console.log(totalSales);
\`\`\`
` },
    { role: 'user', content: 'Hello, what’s the weather like today?' },
    {
        "role": "barChart",
        "content": {
            "chartData": [
                { "x": "Marketing Assistant", "y": 561.09 },
                { "x": "Order Administrator", "y": 462.75 },
                { "x": "Accounting Manager", "y": 737.45 },
                { "x": "Assistant Sales Representative", "y": 719.69 },
                { "x": "Assistant Sales Agent", "y": 560.88 },
                { "x": "Owner/Marketing Assistant", "y": 185.96 },
                { "x": "Marketing Manager", "y": 497.57 },
                { "x": "Sales Representative", "y": 544.57 },
                { "x": "Sales Agent", "y": 458.29 },
                { "x": "Owner", "y": 507.07 },
                { "x": "Sales Manager", "y": 667.77 },
                { "x": "Sales Associate", "y": 639.89 }
            ],
            "axisLabels": {
                "x": "Customer Segment",
                "y": "Average Order Value"
            }
        }
    },
    {
        role: 'barChart', content: {
            chartData: [
                { x: "January", y: 186 },
                { x: "February", y: 305 },
                { x: "March", y: 237 },
                { x: "April", y: 73 },
                { x: "May", y: 209 },
                { x: "June", y: 214 },
            ],
            axisLabels: { x: "Month", y: "Some value" }
        }
    },
    {
        role: 'barChartHorizontal', content: {
            chartData: [
                { y: "January", x: 186 },
                { y: "February", x: 305 },
                { y: "March", x: 237 },
                { y: "April", x: 73 },
                { y: "May", x: 209 },
                { y: "June", x: 214 },
            ],
            axisLabels: { y: "Month", x: "Some value" }
        }
    },
    { role: 'assistant', content: 'The weather is sunny and 24°C in your location.' },
    { role: 'user', content: 'Thanks! Can you summarize the news headlines?' },
    { role: 'assistant', content: 'Sure! Here are today’s top headlines: 1) Markets rise... 2) Tech merger... 3) SpaceX launch...' },
    {
        role: 'table', content: {
            data: [
                [
                    "INV001", "Paid", "$250.00", "Credit Card",
                ],
                [
                    "INV001", "Paid", "$250.00", "Credit Card",
                ],
                [
                    "INV001", "Paid", "$250.00", "Credit Card",
                ],
                [
                    "INV001", "Paid", "$250.00", "Credit Card",
                ],
                [
                    "INV001", "Paid", "$250.00", "Credit Card",
                ],
                [
                    "INV001", "Paid", "$250.00", "Credit Card",
                ],
                [
                    "INV001", "Paid", "$250.00", "Credit Card",
                ]
            ],
            labels: ["Invoice", "Status", "Method", "Amount"]
        }
    }
]

// 1. Create slice
const chatSlice = createSlice({
    name: 'chat',
    initialState: {
        messages: [
            { role: 'assistant', content: '' },
            { role: 'assistant', content: '' },
            { role: 'assistant', content: '' },
            {
                role: 'lineChartMultiple',
                content: {
                    chartData: [
                        { x: "January", y1: 186, y2: 80, y3: 120, y4: 90, y5: 150 },
                        { x: "February", y1: 305, y2: 200, y3: 180, y4: 160, y5: 220 },
                        { x: "March", y1: 237, y2: 120, y3: 140, y4: 110, y5: 180 },
                        { x: "April", y1: 73, y2: 190, y3: 160, y4: 130, y5: 200 },
                        { x: "May", y1: 209, y2: 130, y3: 150, y4: 120, y5: 170 },
                        { x: "June", y1: 214, y2: 140, y3: 170, y4: 140, y5: 190 }
                    ],
                    axisLabels: {
                        x: "Month",
                        y1: "Desktop Users",
                        y2: "Mobile Users",
                        y3: "Tablet Users",
                        y4: "Smart TV Users",
                        y5: "Other Devices"
                    }
                }
            }
        ]
    },
    reducers: {
        addMessage: (state, action) => {
            state.messages.push(action.payload)
        }
    }
})

export const { addMessage } = chatSlice.actions

export const selectLastMessages = (state, count = 1) => {
    return state.chat.messages.slice(-count);
};

// 2. Create store
const store = configureStore({
    reducer: {
        chat: chatSlice.reducer
    }
})

export default store;