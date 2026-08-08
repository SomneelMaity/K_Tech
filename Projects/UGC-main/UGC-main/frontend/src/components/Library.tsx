import { isInFlight, type Generation } from '../api'

interface Props {
  items: Generation[]
  onOpen: (g: Generation) => void
}

export default function Library({ items, onOpen }: Props) {
  if (items.length === 0) {
    return (
      <p className="text-center text-gray-500 py-16">
        No posts yet. Create your first one to start your library.
      </p>
    )
  }

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
      {items.map((g) => (
        <button
          key={g.id}
          onClick={() => onOpen(g)}
          className="text-left rounded-xl overflow-hidden border border-gray-800 bg-gray-900 hover:border-indigo-600 transition"
        >
          <div className="aspect-square bg-gray-800 flex items-center justify-center">
            {g.image_url ? (
              <img src={g.image_url} alt="" className="w-full h-full object-cover" />
            ) : isInFlight(g) ? (
              <span className="text-indigo-400 text-xs animate-pulse">generating…</span>
            ) : g.status === 'error' ? (
              <span className="text-red-400 text-xs">failed</span>
            ) : (
              <span className="text-gray-600 text-xs">no image</span>
            )}
          </div>
          <div className="p-2.5">
            <p className="text-xs text-gray-300 line-clamp-2">{g.hook || g.idea}</p>
            <p className="text-[10px] text-gray-500 mt-1 uppercase">{g.platform}</p>
          </div>
        </button>
      ))}
    </div>
  )
}
