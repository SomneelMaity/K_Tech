import { useState } from 'react'
import { api, isInFlight, type CampaignPlan, type Generation } from '../api'

interface Props {
  generation: Generation
  onChange: (g: Generation) => void
}

const btn =
  'rounded-lg px-3 py-2 text-sm font-medium border border-gray-700 bg-gray-900 ' +
  'hover:bg-gray-800 disabled:opacity-50 transition'

const field =
  'rounded-lg bg-gray-900 border border-gray-700 px-3 py-2 text-sm text-gray-100 ' +
  'focus:outline-none focus:ring-2 focus:ring-indigo-500'

const GOALS = [
  { value: 'awareness', label: 'Awareness' },
  { value: 'lead generation', label: 'Lead gen' },
  { value: 'conversion', label: 'Conversion' },
  { value: 'engagement', label: 'Engagement' },
]

const BUDGETS = [
  { value: 'starter', label: 'Starter' },
  { value: 'moderate', label: 'Moderate' },
  { value: 'aggressive', label: 'Aggressive' },
]

function joinLines(title: string, items: string[]) {
  return [title, ...items.map((item) => `- ${item}`)].join('\n')
}

function campaignText(plan: CampaignPlan) {
  return [
    plan.campaign_name,
    '',
    `Objective: ${plan.objective}`,
    `Funnel stage: ${plan.funnel_stage}`,
    `Audience: ${plan.primary_audience}`,
    `Positioning: ${plan.positioning}`,
    `CTA: ${plan.primary_cta}`,
    `UTM campaign: ${plan.utm_campaign}`,
    '',
    joinLines('Organic plan', plan.organic_plan),
    '',
    joinLines('Paid plan', plan.paid_plan),
    '',
    joinLines('KPIs', plan.kpis),
    '',
    joinLines('Launch checklist', plan.launch_checklist),
  ].join('\n')
}

function ListBlock({ title, items }: { title: string; items: string[] }) {
  return (
    <div>
      <h3 className="text-sm font-semibold text-gray-200 mb-2">{title}</h3>
      <ul className="space-y-2 text-sm text-gray-400">
        {items.map((item) => (
          <li key={item} className="flex gap-2">
            <span className="mt-2 h-1.5 w-1.5 rounded-full bg-emerald-400 flex-none" />
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default function CampaignPanel({ generation, onChange }: Props) {
  const [goal, setGoal] = useState('awareness')
  const [durationDays, setDurationDays] = useState(14)
  const [budgetLevel, setBudgetLevel] = useState('starter')
  const [busy, setBusy] = useState(false)
  const [copied, setCopied] = useState(false)

  const plan = generation.campaign_plan
  const locked = busy || isInFlight(generation) || generation.status === 'error'

  async function generate() {
    setBusy(true)
    try {
      onChange(
        await api.generateCampaign(generation.id, {
          goal,
          duration_days: durationDays,
          budget_level: budgetLevel,
        }),
      )
    } catch (e) {
      alert(`Failed: ${(e as Error).message}`)
    } finally {
      setBusy(false)
    }
  }

  function copyPlan() {
    if (!plan) return
    navigator.clipboard.writeText(campaignText(plan))
    setCopied(true)
    setTimeout(() => setCopied(false), 1500)
  }

  return (
    <section className="mt-8 border-t border-gray-800 pt-6">
      <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between mb-5">
        <div>
          <p className="text-xs uppercase tracking-[0.18em] text-emerald-300">Campaign</p>
          <h2 className="text-lg font-semibold text-white">Marketing plan</h2>
        </div>
        <div className="flex flex-wrap gap-2">
          <select className={field} value={goal} onChange={(e) => setGoal(e.target.value)} disabled={locked}>
            {GOALS.map((item) => (
              <option key={item.value} value={item.value}>{item.label}</option>
            ))}
          </select>
          <select className={field} value={budgetLevel} onChange={(e) => setBudgetLevel(e.target.value)} disabled={locked}>
            {BUDGETS.map((item) => (
              <option key={item.value} value={item.value}>{item.label}</option>
            ))}
          </select>
          <input
            className={`${field} w-24`}
            type="number"
            min={3}
            max={90}
            value={durationDays}
            onChange={(e) => setDurationDays(Number(e.target.value))}
            disabled={locked}
            aria-label="Duration days"
          />
          <button className={btn} onClick={generate} disabled={locked}>
            {busy ? 'Planning...' : plan ? 'Regenerate plan' : 'Generate plan'}
          </button>
          {plan && (
            <button className={btn} onClick={copyPlan}>
              {copied ? 'Copied' : 'Copy plan'}
            </button>
          )}
        </div>
      </div>

      {!plan ? (
        <div className="rounded-xl border border-gray-800 bg-gray-900/50 px-5 py-6 text-sm text-gray-400">
          No campaign plan yet.
        </div>
      ) : (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
            <div className="rounded-xl border border-gray-800 bg-gray-900/55 p-4 md:col-span-2">
              <p className="text-xs text-gray-500 uppercase mb-1">Campaign name</p>
              <h3 className="font-semibold text-white">{plan.campaign_name}</h3>
            </div>
            <div className="rounded-xl border border-gray-800 bg-gray-900/55 p-4">
              <p className="text-xs text-gray-500 uppercase mb-1">Funnel</p>
              <p className="font-medium text-emerald-200 capitalize">{plan.funnel_stage}</p>
            </div>
            <div className="rounded-xl border border-gray-800 bg-gray-900/55 p-4">
              <p className="text-xs text-gray-500 uppercase mb-1">CTA</p>
              <p className="font-medium text-white">{plan.primary_cta}</p>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
            <div className="lg:col-span-2 space-y-4">
              <div>
                <h3 className="text-sm font-semibold text-gray-200 mb-2">Objective</h3>
                <p className="text-sm text-gray-400">{plan.objective}</p>
              </div>
              <div>
                <h3 className="text-sm font-semibold text-gray-200 mb-2">Positioning</h3>
                <p className="text-sm text-gray-400">{plan.positioning}</p>
              </div>
              <div>
                <h3 className="text-sm font-semibold text-gray-200 mb-2">Audience</h3>
                <p className="text-sm text-gray-400">{plan.primary_audience}</p>
              </div>
            </div>
            <div className="rounded-xl border border-gray-800 bg-gray-900/55 p-4">
              <p className="text-xs text-gray-500 uppercase mb-1">Budget note</p>
              <p className="text-sm text-gray-400">{plan.budget_note}</p>
              <p className="text-xs text-gray-500 uppercase mt-4 mb-1">UTM</p>
              <code className="block rounded-md bg-black/30 px-2 py-1 text-xs text-emerald-200 break-all">
                {plan.utm_campaign}
              </code>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            <ListBlock title="Organic plan" items={plan.organic_plan} />
            <ListBlock title="Paid plan" items={plan.paid_plan} />
          </div>

          <div>
            <h3 className="text-sm font-semibold text-gray-200 mb-3">Channel mix</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {plan.channel_mix.map((item) => (
                <div key={`${item.channel}-${item.role}`} className="rounded-xl border border-gray-800 bg-gray-900/55 p-4">
                  <p className="text-sm font-semibold text-white capitalize">{item.channel}</p>
                  <p className="text-xs text-emerald-300 mt-1">{item.role}</p>
                  <p className="text-sm text-gray-400 mt-2">{item.action}</p>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-gray-200 mb-3">Calendar</h3>
            <div className="overflow-x-auto rounded-xl border border-gray-800">
              <table className="min-w-full text-left text-sm">
                <thead className="bg-gray-900 text-xs uppercase text-gray-500">
                  <tr>
                    <th className="px-3 py-2 font-medium">Day</th>
                    <th className="px-3 py-2 font-medium">Channel</th>
                    <th className="px-3 py-2 font-medium">Asset</th>
                    <th className="px-3 py-2 font-medium">Message</th>
                    <th className="px-3 py-2 font-medium">CTA</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-800 bg-gray-950/30 text-gray-400">
                  {plan.content_calendar.map((item) => (
                    <tr key={`${item.day}-${item.channel}-${item.asset}`}>
                      <td className="px-3 py-3 whitespace-nowrap text-gray-300">{item.day}</td>
                      <td className="px-3 py-3 capitalize">{item.channel}</td>
                      <td className="px-3 py-3">{item.asset}</td>
                      <td className="px-3 py-3 min-w-[220px]">{item.message}</td>
                      <td className="px-3 py-3">{item.cta}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
            <ListBlock title="KPIs" items={plan.kpis} />
            <div>
              <h3 className="text-sm font-semibold text-gray-200 mb-2">Experiments</h3>
              <div className="space-y-3">
                {plan.experiments.map((item) => (
                  <div key={item.hypothesis} className="rounded-xl border border-gray-800 bg-gray-900/55 p-4">
                    <p className="text-sm text-white">{item.hypothesis}</p>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-3 text-xs text-gray-400">
                      <p><span className="text-gray-500">A:</span> {item.variant_a}</p>
                      <p><span className="text-gray-500">B:</span> {item.variant_b}</p>
                    </div>
                    <p className="text-xs text-emerald-300 mt-3">Metric: {item.metric}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <ListBlock title="Launch checklist" items={plan.launch_checklist} />
        </div>
      )}
    </section>
  )
}
