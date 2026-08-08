import { useState } from 'react'
import { api } from './api.js'
import SegmentSelector from './components/SegmentSelector.jsx'
import DisclaimerBanner from './components/DisclaimerBanner.jsx'
import ChatWindow from './components/ChatWindow.jsx'
import ChatInput from './components/ChatInput.jsx'
import EmergencyResources from './components/EmergencyResources.jsx'
import DocumentViewer from './components/DocumentViewer.jsx'
import './App.css'

const SEGMENT_LABELS = {
  's5-employment': 'Employment & Labour',
  's10-msme': 'MSME & Small Business',
}

export default function App() {
  const [segment, setSegment] = useState(null)
  const [conversationId, setConversationId] = useState(null)
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [language, setLanguage] = useState('en')
  const [emergencyResources, setEmergencyResources] = useState(null)
  const [generatedDoc, setGeneratedDoc] = useState(null)
  const [error, setError] = useState(null)

  async function sendMessage(text) {
    if (!text.trim() || loading) return
    setMessages(prev => [...prev, { role: 'user', content: text, citations: [] }])
    setLoading(true)
    setError(null)
    setEmergencyResources(null)

    try {
      const res = await api.chat({
        conversation_id: conversationId || undefined,
        message: text,
        segment,
        language,
      })
      if (res.conversation_id) setConversationId(res.conversation_id)
      if (res.emergency_resources?.length) setEmergencyResources(res.emergency_resources)
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: res.answer,
        citations: res.citations || [],
        disclaimer: res.disclaimer,
      }])
    } catch (e) {
      const msg = e.message || ''
      if (msg.includes('quota') || msg.includes('503')) {
        setError('AI service quota exceeded. Please check your Gemini API key at https://aistudio.google.com/app/apikey')
      } else if (msg.startsWith('503')) {
        setError(msg.replace(/^503: /, ''))
      } else {
        setError('Could not reach the server. Please try again.')
      }
      setMessages(prev => prev.slice(0, -1))
    } finally {
      setLoading(false)
    }
  }

  function handleSelectSegment(seg) {
    setSegment(seg)
    setMessages([])
    setConversationId(null)
    setEmergencyResources(null)
    setGeneratedDoc(null)
    setError(null)
  }

  if (!segment) {
    return <SegmentSelector onSelect={handleSelectSegment} />
  }

  return (
    <div className="flex flex-col h-screen bg-slate-50 dark:bg-slate-900">
      <DisclaimerBanner />

      {/* Top bar */}
      <div className="flex items-center gap-3 px-4 py-2 bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 shadow-sm">
        <button
          onClick={() => setSegment(null)}
          className="text-sm text-blue-600 dark:text-blue-400 hover:underline"
        >
          ← Change domain
        </button>
        <span className="text-sm font-semibold text-slate-700 dark:text-slate-200">
          {SEGMENT_LABELS[segment]}
        </span>
      </div>

      {emergencyResources && (
        <EmergencyResources
          resources={emergencyResources}
          onDismiss={() => setEmergencyResources(null)}
        />
      )}

      {generatedDoc && (
        <DocumentViewer
          doc={generatedDoc}
          onClose={() => setGeneratedDoc(null)}
        />
      )}

      {error && (
        <div className="mx-4 mt-2 px-4 py-2 bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300 rounded-lg text-sm">
          {error}
        </div>
      )}

      <ChatWindow messages={messages} loading={loading} />

      <ChatInput
        onSend={sendMessage}
        language={language}
        onLanguageChange={setLanguage}
        loading={loading}
      />
    </div>
  )
}
