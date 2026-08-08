const SEGMENTS = [
  {
    id: 's5-employment',
    title: 'Employment & Labour',
    description: 'Unpaid salary, gratuity, PF/ESI issues, wrongful termination, POSH, maternity benefits.',
    icon: '👤',
    color: 'blue',
  },
  {
    id: 's10-msme',
    title: 'MSME & Small Business',
    description: 'Delayed payments, cheque bounce, licences, contract disputes, GST basics.',
    icon: '🏪',
    color: 'green',
  },
]

const COLOR = {
  blue: 'border-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20',
  green: 'border-green-400 hover:bg-green-50 dark:hover:bg-green-900/20',
}

export default function SegmentSelector({ onSelect }) {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-slate-50 dark:bg-slate-900 px-4">
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold text-slate-800 dark:text-slate-100">⚖️ LegalBot</h1>
        <p className="mt-2 text-slate-500 dark:text-slate-400 text-sm max-w-md">
          Free AI legal information assistant for every Indian. Choose your domain to get started.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full max-w-xl">
        {SEGMENTS.map(seg => (
          <button
            key={seg.id}
            onClick={() => onSelect(seg.id)}
            className={`text-left p-5 rounded-2xl border-2 bg-white dark:bg-slate-800 shadow-sm transition-colors cursor-pointer ${COLOR[seg.color]}`}
          >
            <div className="text-3xl mb-2">{seg.icon}</div>
            <div className="font-semibold text-slate-800 dark:text-slate-100">{seg.title}</div>
            <div className="mt-1 text-sm text-slate-500 dark:text-slate-400">{seg.description}</div>
          </button>
        ))}
      </div>

      <p className="mt-8 text-xs text-slate-400 dark:text-slate-500 text-center max-w-sm">
        LegalBot provides general legal information only — not legal advice.
        Free legal aid: NALSA <strong>1516</strong>
      </p>
    </div>
  )
}
