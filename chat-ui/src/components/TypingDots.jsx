function TypingDots() {

    return (
        <>
            <div className="flex">
                <img src="./portonics-logo.png" alt="My profile" className="w-6 h-6 rounded-full" />
                    <div className="ml-3 message-typing assistant rounded-lg py-2.5 px-6 mb-4 bg-blue-100 border-blue-100 self-start">
                            <div className="type-indicator">
                                <span>.</span><span>.</span><span>.</span>
                            </div>
                </div>
                        
            </div>
        </>
    )

}

export default TypingDots