import type { FoodLog } from '../types'

function formatFoodName(name: string): string {
  return name.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())
}

export function FoodLogRow({ log, onDelete }: { log: FoodLog; onDelete: (id: number) => void }) {
  return (
    <div className="flex items-center justify-between border-b border-gray-100 py-3 last:border-0">
      <div>
        <p className="font-medium text-gray-900">{formatFoodName(log.food_name)}</p>
        <p className="text-sm text-gray-500">
          {log.serving_grams}g &middot; {new Date(log.logged_at).toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </p>
      </div>
      <div className="flex items-center gap-4">
        <span className="text-sm font-semibold text-gray-900">{log.calories} kcal</span>
        <button
          onClick={() => onDelete(log.id)}
          className="text-sm text-gray-400 hover:text-red-500"
          aria-label={`Delete ${log.food_name} entry`}
        >
          Remove
        </button>
      </div>
    </div>
  )
}
