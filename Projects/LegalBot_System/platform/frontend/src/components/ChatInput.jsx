import { useState } from 'react'

const LANGUAGES = [
  { code: 'en', label: 'English' },
  { code: 'hi', label: 'हिंदी' },
  { code: 'bn', label: 'বাংলা' },
  { code: 'te', label: 'తెలుగు' },
  { code: 'mr', label: 'मराठी' },
  { code: 'ta', label: 'தமிழ்' },
  { code: 'gu', label: 'ગુજરાતી' },
  { code: 'kn', label: 'ಕನ್ನಡ' },
  { code: 'pa', label: 'ਪੰਜਾਬੀ' },
  { code: 'ur', label: 'اردو' },
]

export default function ChatInput({ onSend, language, onLanguageChange, loading }) {
  const [text, setText] = useState('')

  function handleSend() {
    if (!text.trim() || loading) return
    onSend(text.trim())
    setText('')
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="px-4 py-3 bg-white dark:bg-slate-800 border-t border-slate-200 dark:border-slate-700">
      <div className="flex items-end gap-2 max-w-3xl mx-auto">
        <select
          value={language}
          onChange={e => onLanguageChange(e.target.value)}
          className="shrink-0 h-10 px-2 rounded-xl border border-slate-200 dark:border-slate-600 bg-slate-50 dark:bg-slate-700 text-slate-700 dark:text-slate-200 text-sm"
          aria-label="Select language"
        >
          {LANGUAGES.map(l => (
            <option key={l.code} value={l.code}>{l.label}</option>
          ))}
        </select>

        <textarea
          value={text}
          onChange={e => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask your legal question... (Enter to send)"
          rows={1}
          disabled={loading}
          className="flex-1 resize-none px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-600 bg-slate-50 dark:bg-slate-700 text-slate-800 dark:text-slate-100 placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 disabled:opacity-50"
          style={{ maxHeight: '120px', overflowY: 'auto' }}
        />

        <button
          onClick={handleSend}
          disabled={!text.trim() || loading}
          className="shrink-0 h-10 w-10 flex items-center justify-center rounded-xl bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 dark:disabled:bg-slate-600 text-white transition-colors"
          aria-label="Send"
        >
          {loading
            ? <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            : <span className="text-base">↑</span>
          }
        </button>
      </div>
      <p className="mt-1 text-center text-xs text-slate-400 dark:text-slate-500">
        Shift+Enter for new line
      </p>
    </div>
  )
}
