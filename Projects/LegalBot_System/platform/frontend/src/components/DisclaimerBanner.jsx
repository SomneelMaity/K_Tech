import { useState } from 'react'

export default function DisclaimerBanner() {
  const [visible, setVisible] = useState(true)
  if (!visible) return null

  return (
    <div className="flex items-start gap-2 px-4 py-2 bg-amber-50 dark:bg-amber-900/30 border-b border-amber-200 dark:border-amber-700 text-amber-800 dark:text-amber-200 text-xs">
      <span className="mt-0.5 shrink-0">⚠️</span>
      <span className="flex-1">
        <strong>Important:</strong> LegalBot provides general legal information only — not legal advice.
        For serious matters, consult a lawyer. Free aid: NALSA&nbsp;<strong>1516</strong>.
      </span>
      <button
        onClick={() => setVisible(false)}
        className="shrink-0 text-amber-600 dark:text-amber-400 hover:text-amber-900 dark:hover:text-amber-100 font-bold"
        aria-label="Dismiss"
      >
        ×
      </button>
    </div>
  )
}
