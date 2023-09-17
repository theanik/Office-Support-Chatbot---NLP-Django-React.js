import { useEffect, useState, useRef } from 'react'
import BotMessage from '../components/BotMessage'
import ChatHeader from '../components/ChatHeader'
import UserMessage from '../components/UserMessage'
import TypingDots from '../components/TypingDots'


function Chat() {
    let prevMassage = JSON.parse(localStorage.getItem("chatMessage")) ?? []
    const [socket, setSocket] = useState(null);
    const [qustionMessage, setQuestionMessage] = useState('');
    const [chatMessage, setChatMessage] = useState(prevMassage)
    const [botTyping, setBotTyping] = useState(false)


    const CHAT_WSS_URL = import.meta.env.VITE_CHAT_WSS_URL
    const messagesRef = useRef(null);


    useEffect(() => {
        let websocketUrl = CHAT_WSS_URL.replace('#room_name#', getRandSocketRoomName())
        setBotTyping(true)
        const newSocket = new WebSocket(websocketUrl);

        newSocket.onmessage = (event) => {
            setBotTyping(true)
            const message = JSON.parse(event.data);
            message.sender = 'bot'

            if (chatMessage.length && message.type == 'connection_info') {
                message.message = 'Welcome back! How may I help you?'
                message.type = "system_message"
            }
            setChatMessage((arrData) => [...arrData, message])
            setBotTyping(false)
        };

        setSocket(newSocket);

        return () => {
            newSocket.close();
        };
    }, []);

    useEffect(() => {
        if (messagesRef.current) {
            messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
        }
        localStorage.setItem('chatMessage', JSON.stringify(chatMessage));
    }, [chatMessage])


    const submitSendMessage = (e) => {
        if (e.key == 'Enter') {
            sendMessage()
        }
    }
    const getRandSocketRoomName = (length = 10) => {
        let result = '';
        const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        const charactersLength = characters.length;
        let counter = 0;
        while (counter < length) {
          result += characters.charAt(Math.floor(Math.random() * charactersLength));
          counter += 1;
        }
        return result;
    }
    

    const sendMessage = () => {
        if (qustionMessage.trim().length < 2) return
        if (qustionMessage.trim().length > 2000) return

        const message = {
            message: qustionMessage,
            sender: 'user'
        };
        setChatMessage(prevArray => [...prevArray, message]);

        socket.send(JSON.stringify(message));
        setQuestionMessage('')
    }

    const clearHistory = () => {
        localStorage.setItem('chatMessage',JSON.stringify(''))
        setChatMessage([{
            message: "All conversation has been removed, let's start a new journey!",
            sender: "bot",
            type: 'system_message'
        }])
    }

    return (
        <>
            <div className="container mx-auto">
                <div className="flex-1 p:2 sm:p-6 justify-between flex flex-col h-screen">
                    <ChatHeader onHistoryClear={clearHistory}/>
                    <div id="messages" ref={messagesRef} className="flex flex-col space-y-4 p-3 overflow-y-auto scrollbar-thumb-blue scrollbar-thumb-rounded scrollbar-track-blue-lighter scrollbar-w-2 scrolling-touch">
                        {chatMessage && chatMessage.map((chat, index) => {
                            if (chat.sender == 'bot') {
                                return <BotMessage chatMessage={chat} key={index} />
                            } else {
                                return <UserMessage chatMessage={chat} key={index} />
                            }
                        })}
                        {botTyping && <TypingDots />}
                    </div>

                    <div className="border-t-2 border-gray-200 px-4 pt-4 mb-2 sm:mb-0">
                        <div className="relative flex">
                            <input value={qustionMessage} onChange={(e) => setQuestionMessage(e.target.value)} onKeyDown={submitSendMessage} type="text" placeholder="Write your message!" className="w-full focus:outline-none focus:placeholder-gray-400 text-gray-600 placeholder-gray-600 pl-4 bg-gray-200 rounded-md py-3" />
                            <div className="absolute right-0 items-center inset-y-0 sm:flex">
                                <button onClick={sendMessage} type="button" className="inline-flex items-center justify-center rounded-lg px-4 py-3 transition duration-500 ease-in-out text-white bg-blue-500 hover:bg-blue-400 focus:outline-none">
                                    <span className="font-bold">Send</span>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </>
    )
}

export default Chat


