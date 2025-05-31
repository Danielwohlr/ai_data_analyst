'use client'

import Message from "@/components/components/Message.jsx";
import { Provider, useDispatch, useSelector } from 'react-redux'
import AreaChartGradient from "@/components/components/AreaChartGradient.jsx";
import BarChartDefault from "@/components/components/BarChart.jsx";
import BarChartHorizontal from "@/components/components/BarChartHorizontal.jsx";
import LineChartLinear from "@/components/components/LineChartLinear.jsx";
import DataTable from "@/components/components/DataTable.jsx";

const ChatArea = () => {
    const messages = useSelector((state) => state.chat.messages);

    return (
        <div className="flex flex-col gap-2 overflow-y-auto p-4 w-full max-w-2xl mx-auto mb-32">
            <h1 className="mt-4 text-3xl text-center">Hello data analyst</h1>
            <div className="flex flex-col gap-7">
                {messages.map((msg, key) => (
                    <Message msg={msg} key={key}></Message>
                ))}
            </div>
        </div>
    )
}

export default ChatArea;
