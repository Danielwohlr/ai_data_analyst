'use client'

import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"


const Message = ({ msg, idx }) => {



    if (msg.role === "assistant") {
        return (

            <div className="flex justify-start">
                <Card
                    className="p-3 w-fit border-none shadow-none bg-white">
                    <CardContent
                        className="p-0 "
                        idx={idx}>
                        {msg.content}
                    </CardContent>
                </Card >
            </div>
        )
    }
    else {
        return (

            <div className="flex justify-start">
                <Card
                    className="p-3 w-fit shadow-none border-none bg-neutral-100">
                    <CardContent
                        className="p-0"
                        key={idx}>
                        {msg.content}
                    </CardContent>
                </Card >
            </div>
        )
    }
}

export default Message;