export default function EmergencyResources({ resources, onDismiss }) {
  return (
    <div className="mx-4 mt-2 p-4 rounded-2xl bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-700">
      <div className="flex items-start justify-between gap-2">
        <div>
          <p className="font-semibold text-red-700 dark:text-red-300 text-sm">
            🚨 Your safety comes first
          </p>
          <p className="mt-1 text-xs text-red-600 dark:text-red-400">
            Please contact one of these free, confidential helplines immediately.
          </p>
        </div>
        <button
          onClick={onDismiss}
          className="text-red-400 hover:text-red-700 dark:hover:text-red-200 font-bold text-lg leading-none"
          aria-label="Dismiss"
        >
          ×
        </button>
      </div>

      <div className="mt-3 grid grid-cols-2 sm:grid-cols-3 gap-2">
        {resources.map((r, i) => (
          <a
            key={i}
            href={`tel:${r.number}`}
            className="flex flex-col items-center p-2 rounded-xl bg-white dark:bg-red-900/40 border border-red-100 dark:border-red-800 hover:bg-red-50 dark:hover:bg-red-900/60 transition-colors"
          >
            <span className="text-xl font-bold text-red-600 dark:text-red-300">{r.number}</span>
            <span className="text-xs text-slate-500 dark:text-slate-400 text-center mt-0.5">{r.label}</span>
          </a>
        ))}
      </div>
    </div>
  )
}
