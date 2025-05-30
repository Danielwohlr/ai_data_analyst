'use client'

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea"

//import { runAction } from '@/services/http.js';

import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"

import { useState } from 'react';

const chatUI = () => {

    const [input, setInput] = useState("");

    const sendMessage = async () => {
        console.log("send");
        console.log(input);
        setInput("");
        /*
        const result = await runAction(input);
        */
        console.log(result);
    }

    return (

        <div className="flex w-full items-start justify-center h-screen">
            <div className="flex flex-col items-center mt-8">
                <h1 className="text-xl font-semibold m-6">
                    Hello data analyst!
                </h1>
                <Card className="flex p-2 w-96">
                    <CardContent className="flex flex-col p-0 gap-2">
                        <div className="flex flex-row">
                            <Textarea
                                className="text-md w-full h-28 shadow-none resize-none outline-none ring-0 border-0 focus:ring-0 focus:border-0 focus-visible:ring-0 focus-visible:border-0"
                                placeholder="Search, update, execute anything"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                            >
                            </Textarea>
                            <Button
                                className="rounded-full"
                                onClick={sendMessage}>
                                <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#ffffff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 19V6M5 12l7-7 7 7" /></svg>
                            </Button>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    )

}

export default chatUI;