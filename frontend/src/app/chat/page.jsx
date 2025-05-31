'use client'

import ChatArea from '@/components/components/ChatArea';
import InputBox from '@/components/components/InputBox'
import ReduxProvider from "@/store/ReduxProvider";

const ChatPage = () => {

    return (
        <>
            <ReduxProvider>
                <InputBox />
                <ChatArea />
            </ReduxProvider>
        </>
    )
}

export default ChatPage;