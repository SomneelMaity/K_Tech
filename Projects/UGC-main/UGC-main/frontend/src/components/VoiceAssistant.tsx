import { useEffect, useRef, useState } from 'react'
import { api, type AssistantMessage } from '../api'

/* Minimal typings for the Web Speech API (not in TS dom lib). */
interface SpeechRecognitionLike {
  lang: string
  continuous: boolean
  interimResults: boolean
  start(): void
  stop(): void
  abort(): void
  onresult: ((e: SpeechRecognitionEventLike) => void) | null
  onend: (() => void) | null
  onerror: ((e: { error: string }) => void) | null
}
interface SpeechRecognitionEventLike {
  resultIndex: number
  results: ArrayLike<{ isFinal: boolean; 0: { transcript: string } }>
}

const SpeechRecognitionCtor: (new () => SpeechRecognitionLike) | undefined =
  (window as unknown as Record<string, new () => SpeechRecognitionLike>).SpeechRecognition ??
  (window as unknown as Record<string, new () => SpeechRecognitionLike>).webkitSpeechRecognition

type AssistantState = 'idle' | 'listening' | 'thinking' | 'speaking'

const STATE_LABEL: Record<AssistantState, string> = {
  idle: 'Tap the mic and ask for a post',
  listening: 'Listening…',
  thinking: 'Thinking…',
  speaking: 'Speaking…',
}

interface Props {
  onOpenGeneration: (id: string) => void
}

export default function VoiceAssistant({ onOpenGeneration }: Props) {
  const [open, setOpen] = useState(false)
  const [state, setState] = useState<AssistantState>('idle')
  const [messages, setMessages] = useState<AssistantMessage[]>([])
  const [interim, setInterim] = useState('')
  const [typed, setTyped] = useState('')
  const [handsFree, setHandsFree] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const recognitionRef = useRef<SpeechRecognitionLike | null>(null)
  const finalTranscriptRef = useRef('')
  const messagesRef = useRef<AssistantMessage[]>([])
  const handsFreeRef = useRef(handsFree)
  const openRef = useRef(open)
  const logRef = useRef<HTMLDivElement | null>(null)

  messagesRef.current = messages
  handsFreeRef.current = handsFree
  openRef.current = open

  const voiceSupported = !!SpeechRecognitionCtor

  useEffect(() => {
    logRef.current?.scrollTo({ top: logRef.current.scrollHeight })
  }, [messages, interim, state])

  // Stop everything when the panel closes or the component unmounts.
  useEffect(() => {
    if (!open) stopAll()
    return stopAll
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open])

  function stopAll() {
    recognitionRef.current?.abort()
    recognitionRef.current = null
    window.speechSynthesis?.cancel()
    setInterim('')
    setState('idle')
  }

  function speak(text: string) {
    if (!window.speechSynthesis) {
      if (handsFreeRef.current) startListening()
      else setState('idle')
      return
    }
    window.speechSynthesis.cancel()
    const u = new SpeechSynthesisUtterance(text)
    u.lang = 'en-US'
    u.onend = () => {
      if (openRef.current && handsFreeRef.current) startListening()
      else setState('idle')
    }
    u.onerror = () => setState('idle')
    setState('speaking')
    window.speechSynthesis.speak(u)
  }

  async function send(text: string) {
    const trimmed = text.trim()
    if (!trimmed) {
      setState('idle')
      return
    }
    setError(null)
    const history = [...messagesRef.current, { role: 'user' as const, content: trimmed }]
    setMessages(history)
    setState('thinking')
    try {
      const res = await api.assistantChat(history)
      setMessages([...history, { role: 'assistant', content: res.reply }])
      if (res.generation_id) onOpenGeneration(res.generation_id)
      speak(res.reply)
    } catch (e) {
      setError((e as Error).message)
      setState('idle')
    }
  }

  function startListening() {
    if (!SpeechRecognitionCtor) return
    window.speechSynthesis?.cancel()
    recognitionRef.current?.abort()

    const rec = new SpeechRecognitionCtor()
    rec.lang = 'en-US'
    rec.continuous = false
    rec.interimResults = true
    finalTranscriptRef.current = ''

    rec.onresult = (e) => {
      let finalText = ''
      let interimText = ''
      for (let i = e.resultIndex; i < e.results.length; i++) {
        const r = e.results[i]
        if (r.isFinal) finalText += r[0].transcript
        else interimText += r[0].transcript
      }
      if (finalText) finalTranscriptRef.current += finalText
      setInterim(finalTranscriptRef.current + interimText)
    }
    rec.onend = () => {
      recognitionRef.current = null
      setInterim('')
      const heard = finalTranscriptRef.current.trim()
      if (heard) send(heard)
      else setState('idle')
    }
    rec.onerror = (e) => {
      console.warn('SpeechRecognition error:', e.error)
      const messages: Record<string, string> = {
        'not-allowed':
          'Microphone access was blocked. Click the icon in the address bar to allow it, and check System Settings → Privacy & Security → Microphone.',
        'service-not-allowed':
          'This browser blocked its speech service. Try Chrome, Edge, or Safari.',
        network:
          "Couldn't reach the browser's speech service. Brave and some browsers block it — use Chrome, Edge, or Safari, or type your command below.",
        'audio-capture':
          'No microphone found, or the browser has no mic access in System Settings → Privacy & Security → Microphone.',
        'language-not-supported': 'Speech recognition does not support this language setting.',
      }
      // 'no-speech' / 'aborted' are normal; onend returns to idle silently.
      if (e.error !== 'no-speech' && e.error !== 'aborted') {
        setError(messages[e.error] ?? `Speech recognition failed: ${e.error}`)
      }
    }

    recognitionRef.current = rec
    setState('listening')
    setInterim('')
    rec.start()
  }

  function handleMicClick() {
    if (state === 'listening') {
      recognitionRef.current?.stop() // finalize what was heard so far
    } else if (state === 'speaking') {
      window.speechSynthesis?.cancel()
      startListening() // barge-in: interrupt the reply and talk
    } else if (state === 'idle') {
      startListening()
    }
    // 'thinking' ignores clicks
  }

  function handleTypedSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (state === 'thinking') return
    const text = typed
    setTyped('')
    stopAll()
    send(text)
  }

  const micActive = state === 'listening'

  return (
    <>
      {/* Floating toggle */}
      <button
        onClick={() => setOpen((o) => !o)}
        aria-label="Voice assistant"
        className={`fixed bottom-5 right-5 z-40 flex h-14 w-14 items-center justify-center rounded-full shadow-lg transition-colors ${
          open ? 'bg-gray-700 text-white' : 'bg-indigo-600 text-white hover:bg-indigo-500'
        }`}
      >
        {open ? (
          <span className="text-xl leading-none">×</span>
        ) : (
          <MicIcon className="h-6 w-6" />
        )}
      </button>

      {open && (
        <div className="fixed bottom-24 right-5 z-40 flex w-[min(24rem,calc(100vw-2.5rem))] flex-col overflow-hidden rounded-2xl border border-gray-800 bg-gray-950 shadow-2xl">
          <div className="flex items-center justify-between border-b border-gray-800 px-4 py-3">
            <div>
              <p className="text-sm font-semibold text-white">Assistant</p>
              <p className="text-xs text-gray-500">{STATE_LABEL[state]}</p>
            </div>
            <label className="flex cursor-pointer items-center gap-1.5 text-xs text-gray-400">
              <input
                type="checkbox"
                checked={handsFree}
                onChange={(e) => setHandsFree(e.target.checked)}
                className="accent-indigo-500"
              />
              Hands-free
            </label>
          </div>

          <div ref={logRef} className="max-h-72 min-h-32 space-y-2 overflow-y-auto px-4 py-3">
            {messages.length === 0 && !interim && (
              <p className="text-xs leading-relaxed text-gray-500">
                Try: “Create a witty TikTok post about a budget standing desk”, “How’s my
                latest post doing?”, or “Give my last post a sketch-style image”.
              </p>
            )}
            {messages.map((m, i) => (
              <div
                key={i}
                className={`max-w-[85%] rounded-xl px-3 py-2 text-sm leading-relaxed ${
                  m.role === 'user'
                    ? 'ml-auto bg-indigo-600/80 text-white'
                    : 'mr-auto bg-gray-800 text-gray-100'
                }`}
              >
                {m.content}
              </div>
            ))}
            {interim && (
              <div className="ml-auto max-w-[85%] rounded-xl bg-indigo-600/40 px-3 py-2 text-sm italic text-indigo-100">
                {interim}
              </div>
            )}
            {state === 'thinking' && (
              <div className="mr-auto rounded-xl bg-gray-800 px-3 py-2 text-sm text-gray-400">
                <span className="animate-pulse">…</span>
              </div>
            )}
          </div>

          {error && (
            <p className="border-t border-red-900/50 bg-red-950/40 px-4 py-2 text-xs text-red-200">
              {error}
            </p>
          )}

          <div className="flex items-center gap-2 border-t border-gray-800 px-3 py-3">
            {voiceSupported ? (
              <button
                onClick={handleMicClick}
                disabled={state === 'thinking'}
                aria-label={micActive ? 'Stop listening' : 'Start listening'}
                className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-full transition-colors disabled:opacity-40 ${
                  micActive
                    ? 'animate-pulse bg-red-600 text-white'
                    : 'bg-indigo-600 text-white hover:bg-indigo-500'
                }`}
              >
                <MicIcon className="h-5 w-5" />
              </button>
            ) : (
              <p className="px-1 text-[11px] leading-tight text-amber-300/80">
                Voice input isn’t supported in this browser — type instead.
              </p>
            )}
            <form onSubmit={handleTypedSubmit} className="flex min-w-0 flex-1 gap-2">
              <input
                value={typed}
                onChange={(e) => setTyped(e.target.value)}
                placeholder="…or type a command"
                className="min-w-0 flex-1 rounded-lg border border-gray-800 bg-gray-900 px-3 py-2 text-sm text-white placeholder-gray-600 focus:border-indigo-500 focus:outline-none"
              />
              <button
                type="submit"
                disabled={!typed.trim() || state === 'thinking'}
                className="rounded-lg bg-gray-800 px-3 text-sm text-gray-200 hover:bg-gray-700 disabled:opacity-40"
              >
                Send
              </button>
            </form>
          </div>
        </div>
      )}
    </>
  )
}

function MicIcon({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="currentColor" className={className} aria-hidden="true">
      <path d="M12 14a3 3 0 0 0 3-3V6a3 3 0 1 0-6 0v5a3 3 0 0 0 3 3Z" />
      <path d="M18 11a1 1 0 1 0-2 0 4 4 0 0 1-8 0 1 1 0 1 0-2 0 6 6 0 0 0 5 5.917V19H9a1 1 0 1 0 0 2h6a1 1 0 1 0 0-2h-2v-2.083A6 6 0 0 0 18 11Z" />
    </svg>
  )
}
