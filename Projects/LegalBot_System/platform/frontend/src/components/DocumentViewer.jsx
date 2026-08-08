export default function DocumentViewer({ doc, onClose }) {
  return (
    <div className="mx-4 mt-2 p-4 rounded-2xl bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-700">
      <div className="flex items-start justify-between gap-2">
        <div>
          <p className="font-semibold text-green-700 dark:text-green-300 text-sm">
            📄 Document Ready
          </p>
          <p className="mt-0.5 text-xs text-green-600 dark:text-green-400 capitalize">
            {doc.doc_type?.replace(/_/g, ' ')}
          </p>
        </div>
        <button
          onClick={onClose}
          className="text-green-400 hover:text-green-700 dark:hover:text-green-200 font-bold text-lg leading-none"
          aria-label="Close"
        >
          ×
        </button>
      </div>

      <a
        href={doc.file_url}
        target="_blank"
        rel="noreferrer"
        className="mt-3 inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-green-600 hover:bg-green-700 text-white text-sm font-medium transition-colors"
      >
        ⬇️ Download PDF
      </a>

      {doc.disclaimer && (
        <p className="mt-3 text-xs text-slate-500 dark:text-slate-400 border-t border-green-100 dark:border-green-800 pt-2">
          {doc.disclaimer}
        </p>
      )}
    </div>
  )
}
