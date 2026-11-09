interface Props {
  consumed: number
  goal: number
}

export function CalorieProgress({ consumed, goal }: Props) {
  const percent = goal > 0 ? Math.min(100, Math.round((consumed / goal) * 100)) : 0
  const remaining = Math.max(0, goal - consumed)

  return (
    <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
      <div className="flex items-baseline justify-between">
        <h2 className="text-sm font-medium text-gray-500">Today's calories</h2>
        <span className="text-sm text-gray-500">{percent}%</span>
      </div>
      <p className="mt-1 text-3xl font-bold text-gray-900">
        {consumed} <span className="text-lg font-normal text-gray-400">/ {goal} kcal</span>
      </p>
      <div className="mt-3 h-3 w-full overflow-hidden rounded-full bg-gray-100">
        <div
          className="h-full rounded-full bg-brand-500 transition-all"
          style={{ width: `${percent}%` }}
        />
      </div>
      <p className="mt-2 text-sm text-gray-500">{remaining} kcal remaining</p>
    </div>
  )
}
