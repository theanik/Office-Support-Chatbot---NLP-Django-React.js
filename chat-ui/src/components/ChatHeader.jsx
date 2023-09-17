import { useState } from "react"
import ClearChatModal from "./ClearChatModal"


function ChatHeader(props) {
    const { onHistoryClear } = props
    const [showModal , setShowModal] = useState(false);

    const openModal = () => {
        setShowModal(true)
    }

    const closeModal = () => {
        setShowModal(false)
    }

    
    return (
        <>
            <div className="flex sm:items-center justify-between py-3 border-b-2 border-gray-200">
                <div className="relative flex items-center space-x-4">
                    <div className="relative">
                        <span className="absolute text-green-500 right-0 bottom-0">
                            <svg width="20" height="20">
                                <circle cx="8" cy="8" r="8" fill="currentColor"></circle>
                            </svg>
                        </span>
                        <img src="./port-bot.png" alt="" className="w-10 sm:w-16 h-10 sm:h-16 rounded-full" />
                    </div>
                    <div className="flex flex-col leading-tight">
                        <div className="text-2xl mt-1 flex items-center">
                            <span className="text-gray-700 mr-3">PortBot</span>
                        </div>
                        <span className="text-lg text-gray-600">Always here to assist you!</span>
                    </div>
                </div>
                
                <div className="flex justify-items-end items-center">
                    <div className="p-3 hover:bg-gray-100 rounded-lg cursor-pointer">
                      <span className="text-3xl text-gray-600" onClick={openModal}>&#9776;</span>
                    </div>
                </div>
            </div>
           {showModal && <ClearChatModal onClose={closeModal}  onClearHistory={onHistoryClear} />}
            
        </>
    )

}

export default ChatHeader