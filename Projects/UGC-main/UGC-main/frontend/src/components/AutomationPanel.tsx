import { useState } from 'react'
import { api, isInFlight, type AutomationResult, type Generation } from '../api'

interface Props {
  generation: Generation
}

const primaryBtn =
  'rounded-lg px-4 py-2 text-sm font-semibold bg-emerald-600 hover:bg-emerald-500 ' +
  'disabled:opacity-50 disabled:cursor-not-allowed text-white transition'

const field =
  'rounded-lg bg-gray-900 border border-gray-700 px-3 py-2 text-sm text-gray-100 ' +
  'focus:outline-none focus:ring-2 focus:ring-emerald-500'

function statusClass(status: string) {
  if (status === 'success') return 'text-emerald-300 bg-emerald-500/10 border-emerald-800'
  if (status === 'blocked') return 'text-amber-300 bg-amber-500/10 border-amber-800'
  if (status === 'error') return 'text-red-300 bg-red-500/10 border-red-800'
  return 'text-gray-300 bg-gray-900 border-gray-800'
}

export default function AutomationPanel({ generation }: Props) {
  const [publishX, setPublishX] = useState(generation.platform === 'x')
  const [publishInstagram, setPublishInstagram] = useState(generation.platform !== 'x')
  const [launchPaid, setLaunchPaid] = useState(false)
  const [activatePaid, setActivatePaid] = useState(false)
  const [dryRun, setDryRun] = useState(false)
  const [dailyBudget, setDailyBudget] = useState(10)
  const [durationDays, setDurationDays] = useState(14)
  const [targetingCountry, setTargetingCountry] = useState('US')
  const [destinationUrl, setDestinationUrl] = useState('')
  const [busy, setBusy] = useState(false)
  const [latest, setLatest] = useState<AutomationResult | null>(generation.automation_runs?.[0] ?? null)

  const locked = busy || isInFlight(generation) || generation.status === 'error'
  const platforms = [
    ...(publishX ? ['x'] : []),
    ...(publishInstagram ? ['instagram'] : []),
  ]
  const canLaunch = platforms.length > 0 || launchPaid

  async function launch() {
    setBusy(true)
    try {
      const result = await api.launchAutomation(generation.id, {
        platforms,
        daily_budget_usd: dailyBudget,
        duration_days: durationDays,
        launch_paid: launchPaid,
        activate_paid: activatePaid,
        dry_run: dryRun,
        destination_url: destinationUrl.trim() || undefined,
        targeting_country: targetingCountry.trim().slice(0, 2).toUpperCase() || 'US',
      })
      setLatest(result)
    } catch (e) {
      alert(`Launch failed: ${(e as Error).message}`)
    } finally {
      setBusy(false)
    }
  }

  return (
    <section className="mt-8 border-t border-gray-800 pt-6">
      <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between mb-5">
        <div>
          <p className="text-xs uppercase tracking-[0.18em] text-emerald-300">Automation</p>
          <h2 className="text-lg font-semibold text-white">One-click launch</h2>
          <p className="text-sm text-gray-500 mt-1 max-w-xl">
            Publish the generated content and activate the campaign plan with your selected budget.
          </p>
        </div>
        <button className={primaryBtn} onClick={launch} disabled={locked || !canLaunch}>
          {busy ? 'Launching...' : dryRun ? 'Run preflight' : 'Launch automation'}
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        <div className="rounded-xl border border-gray-800 bg-gray-900/55 p-4">
          <h3 className="text-sm font-semibold text-gray-200 mb-3">Publish</h3>
          <label className="flex items-center gap-2 text-sm text-gray-300 mb-3">
            <input
              type="checkbox"
              checked={publishX}
              onChange={(e) => setPublishX(e.target.checked)}
              disabled={locked}
            />
            X / Twitter
          </label>
          <label className="flex items-center gap-2 text-sm text-gray-300">
            <input
              type="checkbox"
              checked={publishInstagram}
              onChange={(e) => setPublishInstagram(e.target.checked)}
              disabled={locked}
            />
            Instagram
          </label>
        </div>

        <div className="rounded-xl border border-gray-800 bg-gray-900/55 p-4">
          <h3 className="text-sm font-semibold text-gray-200 mb-3">Paid campaign</h3>
          <label className="flex items-center gap-2 text-sm text-gray-300 mb-3">
            <input
              type="checkbox"
              checked={launchPaid}
              onChange={(e) => setLaunchPaid(e.target.checked)}
              disabled={locked}
            />
            Create Meta campaign + ad set
          </label>
          <label className="flex items-center gap-2 text-sm text-gray-300">
            <input
              type="checkbox"
              checked={activatePaid}
              onChange={(e) => setActivatePaid(e.target.checked)}
              disabled={locked || !launchPaid}
            />
            Set paid objects active immediately
          </label>
          <p className="text-xs text-gray-500 mt-3">
            Leave inactive to create the campaign in paused status for review.
          </p>
        </div>

        <div className="rounded-xl border border-gray-800 bg-gray-900/55 p-4">
          <h3 className="text-sm font-semibold text-gray-200 mb-3">Spend</h3>
          <div className="grid grid-cols-3 gap-2">
            <label className="block">
              <span className="text-xs text-gray-500">$/day</span>
              <input
                className={`${field} w-full mt-1`}
                type="number"
                min={1}
                value={dailyBudget}
                onChange={(e) => setDailyBudget(Number(e.target.value))}
                disabled={locked}
              />
            </label>
            <label className="block">
              <span className="text-xs text-gray-500">Days</span>
              <input
                className={`${field} w-full mt-1`}
                type="number"
                min={1}
                max={90}
                value={durationDays}
                onChange={(e) => setDurationDays(Number(e.target.value))}
                disabled={locked}
              />
            </label>
            <label className="block">
              <span className="text-xs text-gray-500">Country</span>
              <input
                className={`${field} w-full mt-1 uppercase`}
                maxLength={2}
                value={targetingCountry}
                onChange={(e) => setTargetingCountry(e.target.value)}
                disabled={locked}
              />
            </label>
          </div>
          <p className="text-xs text-gray-500 mt-3">
            Estimated cap: ${(dailyBudget * durationDays).toFixed(2)}
          </p>
        </div>
      </div>

      <div className="mt-4 grid grid-cols-1 lg:grid-cols-[1fr_auto] gap-3">
        <input
          className={field}
          placeholder="Destination URL for paid traffic, e.g. https://your-site.com/offer"
          value={destinationUrl}
          onChange={(e) => setDestinationUrl(e.target.value)}
          disabled={locked}
        />
        <label className="flex items-center gap-2 rounded-lg border border-gray-800 bg-gray-900/55 px-3 py-2 text-sm text-gray-300">
          <input type="checkbox" checked={dryRun} onChange={(e) => setDryRun(e.target.checked)} disabled={locked} />
          Preflight only
        </label>
      </div>

      {latest && (
        <div className="mt-5 rounded-xl border border-gray-800 bg-gray-950/40 p-4">
          <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
            <h3 className="text-sm font-semibold text-white">Latest launch</h3>
            <span className={`rounded-full border px-2.5 py-1 text-xs capitalize ${statusClass(latest.status)}`}>
              {latest.status}
            </span>
          </div>
          <p className="text-sm text-gray-400 mb-4">{latest.summary}</p>
          <div className="space-y-2">
            {latest.steps.map((step) => (
              <div
                key={`${step.platform}-${step.action}-${step.external_id}-${step.message}`}
                className="rounded-lg border border-gray-800 bg-gray-900/60 p-3"
              >
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-sm font-medium text-white capitalize">{step.platform}</span>
                  <span className="text-xs text-gray-500">{step.action}</span>
                  <span className={`rounded-full border px-2 py-0.5 text-[11px] capitalize ${statusClass(step.status)}`}>
                    {step.status}
                  </span>
                </div>
                <p className="text-sm text-gray-400 mt-2">{step.message}</p>
                {step.url && (
                  <a className="text-xs text-emerald-300 hover:text-emerald-200 mt-2 inline-block" href={step.url} target="_blank">
                    Open published post
                  </a>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="mt-4 rounded-lg border border-amber-800/70 bg-amber-950/20 px-4 py-3 text-xs text-amber-200/80">
        Real launch needs platform credentials in <code>backend/.env</code>. Instagram also needs <code>PUBLIC_BASE_URL</code> so Meta can fetch the generated image.
      </div>
    </section>
  )
}
