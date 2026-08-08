const BASE = '/api'

async function request(path, init) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`${res.status}: ${text}`)
  }
  return res.json()
}

export const api = {
  health: () => request('/health'),

  chat: (body) =>
    request('/chat', { method: 'POST', body: JSON.stringify(body) }),

  generateDoc: (body) =>
    request('/documents/generate', {
      method: 'POST',
      body: JSON.stringify(body),
    }),
}
