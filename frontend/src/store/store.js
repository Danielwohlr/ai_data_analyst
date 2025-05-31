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
            { role: 'assistant', content: 'The weather is sunny and 24°C in your location.' },
            { role: 'user', content: 'Thanks! Can you summarize the news headlines?' },
            { role: 'assistant', content: 'Sure! Here are today’s top headlines: 1) Markets rise... 2) Tech merger... 3) SpaceX launch...' },
            { role: 'user', content: 'Hello, what’s the weather like today?' },
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