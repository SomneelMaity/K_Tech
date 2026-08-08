export interface CopyVariant {
  hook: string
  caption: string
  hashtags: string[]
}

export interface CampaignChannel {
  channel: string
  role: string
  action: string
}

export interface CampaignCalendarItem {
  day: string
  channel: string
  asset: string
  message: string
  cta: string
}

export interface CampaignExperiment {
  hypothesis: string
  variant_a: string
  variant_b: string
  metric: string
}

export interface CampaignPlan {
  campaign_name: string
  objective: string
  funnel_stage: string
  primary_audience: string
  positioning: string
  primary_cta: string
  organic_plan: string[]
  paid_plan: string[]
  channel_mix: CampaignChannel[]
  content_calendar: CampaignCalendarItem[]
  kpis: string[]
  experiments: CampaignExperiment[]
  budget_note: string
  utm_campaign: string
  launch_checklist: string[]
}

export interface AutomationRequest {
  platforms: string[]
  daily_budget_usd: number
  duration_days: number
  launch_paid: boolean
  activate_paid: boolean
  dry_run: boolean
  destination_url?: string
  targeting_country: string
}

export interface AutomationStep {
  platform: string
  action: string
  status: string
  message: string
  external_id: string
  url: string
  details: Record<string, unknown>
}

export interface AutomationResult {
  id: string
  generation_id: string
  status: string
  summary: string
  request: AutomationRequest
  steps: AutomationStep[]
  created_at: string
}

export interface Generation {
  id: string
  idea: string
  platform: string
  tone: string
  image_style: string
  angle: string
  audience: string
  hook: string
  caption: string
  hashtags: string[]
  variants: CopyVariant[]
  image_prompt: string
  image_url: string
  image_aspect: string
  campaign_plan: CampaignPlan | null
  automation_runs: AutomationResult[]
  status: string
  failed_stage: string
  error: string
  duration_ms: number
  created_at: string
}

export interface GenerateRequest {
  idea: string
  platform: string
  tone: string
  image_style: string
}

export interface CampaignRequest {
  goal: string
  duration_days: number
  budget_level: string
}

export interface AssistantMessage {
  role: 'user' | 'assistant'
  content: string
}

export interface AssistantChatResponse {
  reply: string
  generation_id: string | null
}

export const IN_FLIGHT_STATUSES = ['queued', 'researching', 'writing', 'rendering']

export const isInFlight = (g: Generation | null) =>
  !!g && IN_FLIGHT_STATUSES.includes(g.status)

const JSON_HEADERS = { 'Content-Type': 'application/json' }

async function req<T>(url: string, init?: RequestInit): Promise<T> {
  const r = await fetch(url, init)
  if (!r.ok) throw new Error((await r.text()) || r.statusText)
  return (await r.json()) as T
}

export const api = {
  generate: (body: GenerateRequest) =>
    req<Generation>('/api/generate', {
      method: 'POST',
      headers: JSON_HEADERS,
      body: JSON.stringify(body),
    }),

  get: (id: string) => req<Generation>(`/api/generations/${id}`),

  list: () => req<Generation[]>('/api/generations'),

  retry: (id: string) =>
    req<Generation>(`/api/generations/${id}/retry`, { method: 'POST' }),

  update: (id: string, body: Partial<Pick<Generation, 'hook' | 'caption' | 'hashtags'>>) =>
    req<Generation>(`/api/generations/${id}`, {
      method: 'PATCH',
      headers: JSON_HEADERS,
      body: JSON.stringify(body),
    }),

  regenerateCopy: (id: string) =>
    req<Generation>(`/api/generations/${id}/regenerate-copy`, { method: 'POST' }),

  regenerateImage: (id: string, body: { image_style?: string; image_prompt?: string }) =>
    req<Generation>(`/api/generations/${id}/regenerate-image`, {
      method: 'POST',
      headers: JSON_HEADERS,
      body: JSON.stringify(body),
    }),

  generateCampaign: (id: string, body: CampaignRequest) =>
    req<Generation>(`/api/generations/${id}/campaign`, {
      method: 'POST',
      headers: JSON_HEADERS,
      body: JSON.stringify(body),
    }),

  launchAutomation: (id: string, body: AutomationRequest) =>
    req<AutomationResult>(`/api/generations/${id}/automation/launch`, {
      method: 'POST',
      headers: JSON_HEADERS,
      body: JSON.stringify(body),
    }),

  assistantChat: (messages: AssistantMessage[]) =>
    req<AssistantChatResponse>('/api/assistant/chat', {
      method: 'POST',
      headers: JSON_HEADERS,
      body: JSON.stringify({ messages }),
    }),

  health: () => req<{ anthropic_configured: boolean; replicate_configured: boolean }>(
    '/api/health',
  ),
}

export const PLATFORMS = ['instagram', 'tiktok', 'x', 'facebook', 'threads']
export const TONES = ['friendly', 'professional', 'witty', 'bold', 'inspirational', 'casual']
export const STYLES = ['photo', 'sketch', 'monochrome', '3d', 'cartoon', 'minimal']
