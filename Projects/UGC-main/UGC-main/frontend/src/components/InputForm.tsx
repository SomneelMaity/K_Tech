import { useState } from 'react'
import { PLATFORMS, STYLES, TONES, type GenerateRequest } from '../api'

interface Props {
  onSubmit: (req: GenerateRequest) => void
  loading: boolean
}

const label = 'block text-sm font-medium text-gray-300 mb-1.5'
const field =
  'w-full rounded-lg bg-gray-900 border border-gray-700 px-3 py-2.5 text-gray-100 ' +
  'focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent'

export default function InputForm({ onSubmit, loading }: Props) {
  const [idea, setIdea] = useState('')
  const [platform, setPlatform] = useState('instagram')
  const [tone, setTone] = useState('friendly')
  const [imageStyle, setImageStyle] = useState('photo')

  function submit(e: React.FormEvent) {
    e.preventDefault()
    if (!idea.trim()) return
    onSubmit({ idea: idea.trim(), platform, tone, image_style: imageStyle })
  }

  return (
    <form onSubmit={submit} className="space-y-5">
      <div>
        <label className={label}>Your idea, product, or rough script</label>
        <textarea
          className={`${field} min-h-[140px] resize-y`}
          placeholder="e.g. A productivity app that turns voice notes into to-do lists. Launching this week, targeting busy founders…"
          value={idea}
          onChange={(e) => setIdea(e.target.value)}
        />
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div>
          <label className={label}>Platform</label>
          <select className={field} value={platform} onChange={(e) => setPlatform(e.target.value)}>
            {PLATFORMS.map((p) => (
              <option key={p} value={p}>{p[0].toUpperCase() + p.slice(1)}</option>
            ))}
          </select>
        </div>
        <div>
          <label className={label}>Tone</label>
          <select className={field} value={tone} onChange={(e) => setTone(e.target.value)}>
            {TONES.map((t) => (
              <option key={t} value={t}>{t[0].toUpperCase() + t.slice(1)}</option>
            ))}
          </select>
        </div>
        <div>
          <label className={label}>Image style</label>
          <select className={field} value={imageStyle} onChange={(e) => setImageStyle(e.target.value)}>
            {STYLES.map((s) => (
              <option key={s} value={s}>{s[0].toUpperCase() + s.slice(1)}</option>
            ))}
          </select>
        </div>
      </div>

      <button
        type="submit"
        disabled={loading || !idea.trim()}
        className="w-full rounded-lg bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed px-4 py-3 font-semibold text-white transition"
      >
        {loading ? 'Generating…' : 'Generate post ✨'}
      </button>
    </form>
  )
}
