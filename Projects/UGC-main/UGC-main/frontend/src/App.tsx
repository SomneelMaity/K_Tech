import { useEffect, useState } from 'react'
import { api, isInFlight, type Generation, type GenerateRequest } from './api'
import InputForm from './components/InputForm'
import ResultView from './components/ResultView'
import Library from './components/Library'
import VoiceAssistant from './components/VoiceAssistant'

type View = 'create' | 'result' | 'library'

export default function App() {
  const [view, setView] = useState<View>('create')
  const [loading, setLoading] = useState(false)
  const [current, setCurrent] = useState<Generation | null>(null)
  const [library, setLibrary] = useState<Generation[]>([])
  const [error, setError] = useState<string | null>(null)
  const [health, setHealth] = useState<{ anthropic_configured: boolean; replicate_configured: boolean } | null>(null)

  async function refreshLibrary() {
    try {
      setLibrary(await api.list())
    } catch {
      /* backend may be starting up */
    }
  }

  useEffect(() => {
    refreshLibrary()
    api.health().then(setHealth).catch(() => setHealth(null))
  }, [])

  // Poll while the pipeline runs in the background.
  useEffect(() => {
    const active = current
    if (!active || !isInFlight(active)) return
    const id = active.id
    const timer = setInterval(async () => {
      try {
        const g = await api.get(id)
        setCurrent((prev) => (prev?.id === id ? g : prev))
        if (!isInFlight(g)) refreshLibrary()
      } catch {
        /* transient network error - keep polling */
      }
    }, 1500)
    return () => clearInterval(timer)
  }, [current])

  async function handleGenerate(req: GenerateRequest) {
    setLoading(true)
    setError(null)
    try {
      const g = await api.generate(req)
      setCurrent(g)
      setView('result')
      refreshLibrary()
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setLoading(false)
    }
  }

  function handleChange(g: Generation) {
    setCurrent(g)
    refreshLibrary()
  }

  async function handleAssistantOpen(id: string) {
    try {
      const g = await api.get(id)
      setCurrent(g)
      setView('result')
      refreshLibrary()
    } catch {
      /* post may have just been created; polling will pick it up */
    }
  }

  const demoMode = health && (!health.anthropic_configured || !health.replicate_configured)

  return (
    <div className="min-h-screen max-w-5xl mx-auto px-5 py-8">
      <header className="flex items-center justify-between mb-8">
        <button onClick={() => setView('create')} className="text-left">
          <h1 className="text-xl font-bold text-white">Faceless UGC Factory</h1>
          <p className="text-xs text-gray-500">Idea  caption + image, in seconds</p>
        </button>
        <nav className="flex gap-1 text-sm">
          {(['create', 'library'] as View[]).map((v) => (
            <button
              key={v}
              onClick={() => {
                if (v === 'library') refreshLibrary()
                setView(v)
              }}
              className={`px-3 py-1.5 rounded-lg capitalize ${
                view === v ? 'bg-gray-800 text-white' : 'text-gray-400 hover:text-white'
              }`}
            >
              {v}
            </button>
          ))}
        </nav>
      </header>

      {demoMode && (
        <div className="mb-6 rounded-lg border border-amber-700/50 bg-amber-950/30 px-4 py-2.5 text-sm text-amber-200/90">
          Demo mode - {!health?.anthropic_configured && 'no ANTHROPIC_API_KEY'}
          {!health?.anthropic_configured && !health?.replicate_configured && ' · '}
          {!health?.replicate_configured && 'no REPLICATE_API_TOKEN'}. Add keys to{' '}
          <code className="bg-black/30 px-1 rounded">backend/.env</code> for real output.
        </div>
      )}

      {error && (
        <div className="mb-6 rounded-lg border border-red-800 bg-red-950/40 px-4 py-2.5 text-sm text-red-200">
          {error}
        </div>
      )}

      {view === 'create' && (
        <div className="max-w-2xl mx-auto">
          <InputForm onSubmit={handleGenerate} loading={loading} />
        </div>
      )}

      {view === 'result' && current && (
        <ResultView generation={current} onChange={handleChange} onNew={() => setView('create')} />
      )}

      {view === 'library' && (
        <Library
          items={library}
          onOpen={(g) => {
            setCurrent(g)
            setView('result')
          }}
        />
      )}

      <VoiceAssistant onOpenGeneration={handleAssistantOpen} />
    </div>
  )
}
