// components/chatUI.jsx
'use client'

import { useState } from 'react'
import { useDispatch } from 'react-redux'
import { addMessage } from '@/store/store.js'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import {
    Card,
    CardContent,
} from "@/components/ui/card"

const ChatUI = () => {
    const [input, setInput] = useState("")
    const dispatch = useDispatch()

    const sendMessage = async () => {
        console.log("send")
        console.log(input)
        dispatch(addMessage({
            role: 'user',
            content: input,
        }))
        setInput("")
    }

    return (
        <div className="fixed bottom-4 left-0 right-0 z-10 flex justify-center px-4">
            <Card className="flex p-2 w-full max-w-2xl mx-auto">
                <CardContent className="flex flex-col p-0 gap-2">
                    <div className="flex flex-row">
                        <Textarea
                            className="text-md w-full h-20 shadow-none resize-none outline-none ring-0 border-0 focus:ring-0 focus:border-0 focus-visible:ring-0 focus-visible:border-0"
                            placeholder="Query anything"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                        />
                        <Button
                            className="rounded-full"
                            onClick={sendMessage}>
                            Send
                        </Button>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}

export default ChatUI
