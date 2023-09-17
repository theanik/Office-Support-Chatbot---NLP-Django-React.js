import showdown from 'showdown'
import axios from 'axios';
import { useState } from 'react';

function BoxMessage(props) {
    const [showSuccess, setShowSuccess] = useState('')
    const createMarkup = (text) => {
        let converter = new showdown.Converter()
        return `${converter.makeHtml(text)}`
    }

    const submitFeedback = () => {
        let reqData = JSON.stringify({
            "feedbackData": {
                "label": props.chatMessage?.label,
                "qcontext": props.chatMessage?.qcontext
            }
        })
        axios.post(`${import.meta.env.VITE_BASE_URL}/store-feedback`, reqData)
          .then(function (response) {
            setShowSuccess(response.data.message)
          })
          .catch(function (error) {
            console.log(error);
          });
    }
    return (
        <>
        <div className="chat-message">
            <div className="flex">
                <div className="flex items-end w-10/12">
                    <div className="flex flex-col space-y-2 text-lg mx-2 order-2 items-start">
                        <div className="flex">
                            <span className="px-4 py-2 rounded-lg inline-block rounded-bl-none bg-gray-300 text-gray-600 break-word-word" dangerouslySetInnerHTML={{ __html: createMarkup(props.chatMessage.message) }}></span>

                        </div>
                    </div>
                    <img src="./port-bot.png" alt="My profile" className="w-6 h-6 rounded-full order-1" />
                </div>

                <div className="flex items-end w-2/12 ">
                    {(props.chatMessage.type !== 'system_message') &&  <span className='cursor-pointer' onClick={submitFeedback} ><img src="./dislike.png" alt="Dislike" className="w-6 h-6 rounded p-1 ml-2 opacity-20 hover:opacity-100" /></span>}
                </div>
            </div>
            {showSuccess && <p className='text-sm ml-8 py-2 text-green-600'>{showSuccess} ✔️</p>}
        </div>
        </>
    )
}

export default BoxMessage