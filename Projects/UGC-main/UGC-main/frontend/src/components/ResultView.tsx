import { useEffect, useState } from 'react'
import { api, isInFlight, STYLES, type CopyVariant, type Generation } from '../api'
import AutomationPanel from './AutomationPanel'
import CampaignPanel from './CampaignPanel'

interface Props {
  generation: Generation
  onChange: (g: Generation) => void
  onNew: () => void
}

const btn =
  'rounded-lg px-3 py-2 text-sm font-medium border border-gray-700 bg-gray-900 ' +
  'hover:bg-gray-800 disabled:opacity-50 transition'

const STAGES = [
  { status: 'researching', label: 'Strategy', desc: 'finding the angle' },
  { status: 'writing', label: 'Copy', desc: 'writing hooks & caption' },
  { status: 'rendering', label: 'Image', desc: 'rendering the visual' },
]

const STAGE_LABELS: Record<string, string> = {
  strategy: 'strategy',
  copy: 'copywriting',
  image: 'image rendering',
}

const ASPECT_CLASS: Record<string, string> = {
  '9:16': 'aspect-[9/16] max-w-[320px] mx-auto',
  '16:9': 'aspect-video',
  '3:4': 'aspect-[3/4] max-w-md mx-auto',
  '4:5': 'aspect-[4/5] max-w-md mx-auto',
}

function StageTracker({ generation }: { generation: Generation }) {
  const activeIdx = STAGES.findIndex((s) => s.status === generation.status)
  return (
    <div className="rounded-xl border border-gray-800 bg-gray-900/60 p-5 mb-6">
      <div className="flex items-center gap-3">
        {STAGES.map((s, i) => {
          const done = activeIdx > i || generation.status === 'complete'
          const active = activeIdx === i
          return (
            <div key={s.status} className="flex items-center gap-3 flex-1 last:flex-none">
              <div className="flex items-center gap-2">
                <span
                  className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-semibold ${
                    done
                      ? 'bg-emerald-500/20 text-emerald-300'
                      : active
                        ? 'bg-indigo-500/25 text-indigo-300 animate-pulse'
                        : 'bg-gray-800 text-gray-500'
                  }`}
                >
                  {done ? '✓' : i + 1}
                </span>
                <span className={`text-sm ${active ? 'text-white' : done ? 'text-gray-300' : 'text-gray-500'}`}>
                  {s.label}
                </span>
              </div>
              {i < STAGES.length - 1 && <div className="h-px flex-1 bg-gray-800" />}
            </div>
          )
        })}
      </div>
      <p className="text-xs text-gray-500 mt-3 animate-pulse">
        {generation.status === 'queued'
          ? 'Queued…'
          : `Working: ${STAGES[activeIdx]?.desc ?? ''}…`}
      </p>
      {generation.angle && (
        <p className="text-xs text-gray-400 mt-2">
          <span className="text-gray-500">Angle:</span> {generation.angle}
        </p>
      )}
    </div>
  )
}

export default function ResultView({ generation, onChange, onNew }: Props) {
  const [hook, setHook] = useState(generation.hook)
  const [caption, setCaption] = useState(generation.caption)
  const [busy, setBusy] = useState<string | null>(null)
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    setHook(generation.hook)
    setCaption(generation.caption)
  }, [generation.id, generation.hook, generation.caption])

  const inFlight = isInFlight(generation)
  const rendering = generation.status === 'rendering'
  const dirty = hook !== generation.hook || caption !== generation.caption
  const locked = busy !== null || inFlight

  async function run(name: string, fn: () => Promise<Generation>) {
    setBusy(name)
    try {
      onChange(await fn())
    } catch (e) {
      alert(`Failed: ${(e as Error).message}`)
    } finally {
      setBusy(null)
    }
  }

  function copyAll() {
    const text = `${hook}\n\n${caption}\n\n${generation.hashtags.map((h) => `#${h}`).join(' ')}`
    navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 1500)
  }

  function applyVariant(v: CopyVariant) {
    run('variant', () =>
      api.update(generation.id, { hook: v.hook, caption: v.caption, hashtags: v.hashtags }),
    )
  }

  if (generation.status === 'error') {
    const stage = STAGE_LABELS[generation.failed_stage] || 'generation'
    return (
      <div className="rounded-xl border border-red-800 bg-red-950/40 p-6">
        <h3 className="font-semibold text-red-300 mb-2">Failed during {stage}</h3>
        <p className="text-sm text-red-200/80 mb-4">{generation.error}</p>
        <div className="flex gap-2">
          <button
            className={btn}
            disabled={busy !== null}
            onClick={() => run('retry', () => api.retry(generation.id))}
          >
            {busy === 'retry' ? 'Retrying…' : `↻ Retry from ${stage}`}
          </button>
          <button className={btn} onClick={onNew}>← Start over</button>
        </div>
      </div>
    )
  }

  // Nothing to show yet — just the tracker.
  if (inFlight && !rendering) {
    return <StageTracker generation={generation} />
  }

  const aspectClass = ASPECT_CLASS[generation.image_aspect] ?? 'aspect-square'

  return (
    <div>
      {inFlight && <StageTracker generation={generation} />}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Copy */}
        <div className="space-y-4">
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-sm font-medium text-gray-300">Hook</span>
              <span className="text-xs text-gray-500 uppercase">{generation.platform}</span>
            </div>
            <input
              className="w-full rounded-lg bg-gray-900 border border-gray-700 px-3 py-2.5 text-gray-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              value={hook}
              onChange={(e) => setHook(e.target.value)}
            />
          </div>

          {generation.variants.length > 1 && (
            <div>
              <span className="text-sm font-medium text-gray-300 mb-1.5 block">Variants</span>
              <div className="flex flex-wrap gap-2">
                {generation.variants.map((v, i) => {
                  const active = v.hook === generation.hook
                  return (
                    <button
                      key={i}
                      disabled={locked || active}
                      onClick={() => applyVariant(v)}
                      title={v.hook}
                      className={`rounded-lg px-3 py-1.5 text-xs border transition max-w-[220px] truncate ${
                        active
                          ? 'border-indigo-500 bg-indigo-500/15 text-indigo-200'
                          : 'border-gray-700 bg-gray-900 text-gray-400 hover:text-white disabled:opacity-50'
                      }`}
                    >
                      {i + 1}. {v.hook}
                    </button>
                  )
                })}
              </div>
            </div>
          )}

          <div>
            <span className="text-sm font-medium text-gray-300 mb-1.5 block">Caption</span>
            <textarea
              className="w-full rounded-lg bg-gray-900 border border-gray-700 px-3 py-2.5 text-gray-100 min-h-[180px] resize-y focus:outline-none focus:ring-2 focus:ring-indigo-500"
              value={caption}
              onChange={(e) => setCaption(e.target.value)}
            />
          </div>

          <div>
            <span className="text-sm font-medium text-gray-300 mb-1.5 block">Hashtags</span>
            <div className="flex flex-wrap gap-2">
              {generation.hashtags.map((h) => (
                <span key={h} className="rounded-full bg-indigo-500/15 text-indigo-300 px-2.5 py-1 text-xs">
                  #{h}
                </span>
              ))}
            </div>
          </div>

          <div className="flex flex-wrap gap-2 pt-1">
            <button className={btn} disabled={!dirty || locked} onClick={() => run('save', () => api.update(generation.id, { hook, caption }))}>
              {busy === 'save' ? 'Saving…' : 'Save edits'}
            </button>
            <button className={btn} disabled={locked} onClick={() => run('copy', () => api.regenerateCopy(generation.id))}>
              {busy === 'copy' ? 'Rewriting…' : '↻ Regenerate copy'}
            </button>
            <button className={btn} onClick={copyAll}>{copied ? 'Copied ✓' : 'Copy caption'}</button>
          </div>
        </div>

        {/* Image */}
        <div className="space-y-4">
          <div className={`${aspectClass} w-full rounded-xl overflow-hidden border border-gray-800 bg-gray-900 flex items-center justify-center`}>
            {rendering ? (
              <span className="text-gray-500 text-sm animate-pulse">Rendering image…</span>
            ) : generation.image_url ? (
              <img src={generation.image_url} alt="Generated visual" className="w-full h-full object-cover" />
            ) : (
              <span className="text-gray-600 text-sm">No image</span>
            )}
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <select
              className="rounded-lg bg-gray-900 border border-gray-700 px-3 py-2 text-sm"
              value={generation.image_style}
              onChange={(e) =>
                run('image', () => api.regenerateImage(generation.id, { image_style: e.target.value }))
              }
              disabled={locked}
            >
              {STYLES.map((s) => (
                <option key={s} value={s}>{s[0].toUpperCase() + s.slice(1)}</option>
              ))}
            </select>
            <button className={btn} disabled={locked} onClick={() => run('image', () => api.regenerateImage(generation.id, {}))}>
              {busy === 'image' ? 'Rendering…' : '↻ Regenerate image'}
            </button>
            {generation.image_url && !rendering && (
              <a className={btn} href={generation.image_url} download>⬇ Download</a>
            )}
          </div>
        </div>

        <div className="lg:col-span-2 pt-2">
          <button className="text-indigo-400 hover:text-indigo-300 text-sm" onClick={onNew}>
            + Create another post
          </button>
        </div>
      </div>

      <CampaignPanel generation={generation} onChange={onChange} />
      <AutomationPanel generation={generation} />
    </div>
  )
}
