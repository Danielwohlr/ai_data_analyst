import { configureStore, createSlice } from '@reduxjs/toolkit'

// 1. Create slice
const chatSlice = createSlice({
    name: 'chat',
    initialState: {
        messages: [
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
            { role: 'assistant', content: 'Sure! Here are today’s top headlines: 1) Markets rise... 2) Tech merger... 3) SpaceX launch...' },
            { role: 'user', content: 'Hello, what’s the weather like today?' },
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
            { role: 'assistant', content: 'Sure! Here are today’s top headlines: 1) Markets rise... 2) Tech merger... 3) SpaceX launch...' }
        ]
    },
    reducers: {
        addMessage: (state, action) => {
            state.messages.push(action.payload)
        }
    }
})

export const { addMessage } = chatSlice.actions

// 2. Create store
const store = configureStore({
    reducer: {
        chat: chatSlice.reducer
    }
})

export default store;