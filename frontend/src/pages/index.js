import { useState, useEffect } from "react";
import axios from 'axios';
import TypingAnimation from "../components/TypingAnimation";



export default function Home() {
  const [inputValue, setInputValue] = useState('');
  const [chatLog, setChatLog] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();

    setChatLog((prevChatLog) => [...prevChatLog, { type: 'user', message: inputValue }])

    sendMessage(inputValue);

    setInputValue('');
  }

  const sendMessage = (message) => {
    const url = '/api/chat';

    const data = {
      "question": message,

    };

    setIsLoading(true);

    axios.post(url, data).then((response) => {

      setChatLog((prevChatLog) => [...prevChatLog, { type: 'bot', message: response.data.data }])
      setIsLoading(false);
    }).catch((error) => {
      setIsLoading(false);
      console.log(error);
    })
  }

  return (
    <div className="container mx-auto ">
      <div className="flex flex-col h-screen ">
        <h1 className=" bg-clip-text text-center py-3 font-bold text-3xl text-black">Prompt Generator</h1>
        <div className="flex-grow p-6">
          <div className="flex flex-col space-y-4">
            {
              chatLog.map((message, index) => (
                <div key={index} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'
                  }`}>
                  <div className="bg-gray-800 rounded-lg p-4 text-white max-w-sm">
                    {message.message}
                  </div>
                </div>
              ))
            }
            {
              isLoading &&
              <div key={chatLog.length} className="flex justify-start">
                <div className="bg-gray-400 rounded-lg p-4 text-white max-w-sm">
                  <TypingAnimation />
                </div>
              </div>
            }
          </div>
        </div>
        <form onSubmit={handleSubmit} className="flex-none p-6 mx-7">
          <div className="flex rounded-lg border border-gray-700">
            <input type="text" className="flex-grow px-4 py-2 bg-transparent text-black focus:outline-none" placeholder="Type your message..." value={inputValue} onChange={(e) => setInputValue(e.target.value)} />
            <button type="submit" className="bg-gray-500 rounded-lg px-4 py-2 text-white font-semibold focus:outline-none hover:bg-gray-600 transition-colors duration-300">Send</button>
          </div>
        </form>
      </div>
    </div>
  )
}
