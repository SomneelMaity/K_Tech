"use client";

import { useState } from "react";
import { Send, Mic, MicOff } from "lucide-react";

export function ChatInterface() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<Array<{role: string, content: string}>>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);

  const handleSend = async () => {
    if (!message.trim()) return;

    const userMessage = { role: "user", content: message };
    setMessages(prev => [...prev, userMessage]);
    setMessage("");
    setIsLoading(true);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/query/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: message,
          language: "en",
        }),
      });

      const data = await response.json();
      
      setMessages(prev => [...prev, {
        role: "assistant",
        content: data.answer || "Sorry, I couldn't process that. Please try again."
      }]);
    } catch (error) {
      console.error("Error:", error);
      setMessages(prev => [...prev, {
        role: "assistant",
        content: "I'm having trouble connecting. Please check your internet and try again."
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleVoice = () => {
    setIsListening(!isListening);
    // TODO: Implement voice recognition
  };

  return (
    <div className="flex flex-col h-[600px] border rounded-lg shadow-lg bg-white">
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 mt-20">
            <p className="text-lg mb-2">👋 Welcome to LegalBot!</p>
            <p className="text-sm">Ask me any legal question in English or Hindi</p>
            <div className="mt-6 grid grid-cols-1 gap-2 max-w-md mx-auto text-left">
              <button 
                className="p-3 bg-gray-50 hover:bg-gray-100 rounded text-sm"
                onClick={() => setMessage("How do I file a consumer complaint?")}
              >
                💼 How do I file a consumer complaint?
              </button>
              <button 
                className="p-3 bg-gray-50 hover:bg-gray-100 rounded text-sm"
                onClick={() => setMessage("What are my rights if I'm arrested?")}
              >
                👮 What are my rights if I'm arrested?
              </button>
              <button 
                className="p-3 bg-gray-50 hover:bg-gray-100 rounded text-sm"
                onClick={() => setMessage("I lost money in UPI scam, what should I do?")}
              >
                🚨 I lost money in UPI scam, what should I do?
              </button>
            </div>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-[80%] rounded-lg p-3 ${
                  msg.role === "user"
                    ? "bg-blue-600 text-white"
                    : "bg-gray-100 text-gray-900"
                }`}
              >
                <p className="whitespace-pre-wrap">{msg.content}</p>
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-lg p-3">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: "0.1s"}}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: "0.2s"}}></div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input area */}
      <div className="border-t p-4">
        <div className="flex space-x-2">
          <button
            onClick={toggleVoice}
            className={`p-3 rounded-lg ${
              isListening ? "bg-red-600 text-white" : "bg-gray-200 text-gray-700"
            }`}
            title={isListening ? "Stop listening" : "Start voice input"}
          >
            {isListening ? <MicOff size={20} /> : <Mic size={20} />}
          </button>
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && handleSend()}
            placeholder="Ask your legal question..."
            className="flex-1 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            onClick={handleSend}
            disabled={!message.trim() || isLoading}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            <Send size={20} />
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          ⚠️ This is general information, not legal advice. Consult NALSA/DLSA for your case.
        </p>
      </div>
    </div>
  );
}
