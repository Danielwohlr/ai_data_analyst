'use client'

import Message from "@/components/components/Message.jsx";
import { Provider, useDispatch, useSelector } from 'react-redux'


const ChatArea = () => {
    const messages = useSelector((state) => state.chat.messages)

    return (
        <div className="flex flex-col gap-7 overflow-y-auto p-4 w-full max-w-2xl mx-auto">
            {messages.map((msg, idx) => (
                <Message msg={msg} idx={idx}></Message>
            ))}
        </div>
    )
}

export default ChatArea;
