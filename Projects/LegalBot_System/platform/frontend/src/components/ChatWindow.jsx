import { useEffect, useRef } from 'react'

function Citation({ citation }) {
  return (
    <a
      href={citation.source_url || '#'}
      target="_blank"
      rel="noreferrer"
      className="inline-block mt-1 mr-1 px-2 py-0.5 text-xs rounded-full bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300 hover:underline"
    >
      {citation.act} {citation.section}
    </a>
  )
}

function Message({ msg }) {
  const isUser = msg.role === 'user'
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-3`}>
      <div
        className={`max-w-[80%] px-4 py-3 rounded-2xl text-sm leading-relaxed ${
          isUser
            ? 'bg-blue-600 text-white rounded-br-sm'
            : 'bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 shadow-sm rounded-bl-sm border border-slate-100 dark:border-slate-700'
        }`}
      >
        <p className="whitespace-pre-wrap">{msg.content}</p>
        {!isUser && msg.citations?.length > 0 && (
          <div className="mt-2 pt-2 border-t border-slate-100 dark:border-slate-700">
            <span className="text-xs text-slate-400 dark:text-slate-500">Sources: </span>
            {msg.citations.map((c, i) => <Citation key={i} citation={c} />)}
          </div>
        )}
      </div>
    </div>
  )
}

function TypingIndicator() {
  return (
    <div className="flex justify-start mb-3">
      <div className="px-4 py-3 rounded-2xl rounded-bl-sm bg-white dark:bg-slate-800 shadow-sm border border-slate-100 dark:border-slate-700">
        <div className="flex gap-1 items-center h-4">
          {[0, 1, 2].map(i => (
            <span
              key={i}
              className="w-2 h-2 rounded-full bg-slate-400 dark:bg-slate-500 animate-bounce"
              style={{ animationDelay: `${i * 0.15}s` }}
            />
          ))}
        </div>
      </div>
    </div>
  )
}

export default function ChatWindow({ messages, loading }) {
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  return (
    <div className="flex-1 overflow-y-auto px-4 py-4">
      {messages.length === 0 && !loading && (
        <div className="h-full flex flex-col items-center justify-center text-slate-400 dark:text-slate-500 text-sm">
          <span className="text-4xl mb-3">⚖️</span>
          <p>Ask your legal question to get started.</p>
          <p className="mt-1 text-xs">Answers are grounded in verified Indian law.</p>
        </div>
      )}
      {messages.map((msg, i) => <Message key={i} msg={msg} />)}
      {loading && <TypingIndicator />}
      <div ref={bottomRef} />
    </div>
  )
}
