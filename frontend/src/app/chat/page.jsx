'use client'

import ChatArea from '@/components/components/ChatArea';
import ChatUI from '@/components/components/ChatUI'
import ReduxProvider from "@/store/ReduxProvider";

const ChatPage = () => {

    return (
        <>
            <ReduxProvider>
                <ChatUI />
                <ChatArea />
            </ReduxProvider>
        </>
    )
}

export default ChatPage;