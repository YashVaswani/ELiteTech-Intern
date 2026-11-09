import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { deleteLog, getDailySummary } from '../api/logs'
import { CalorieProgress } from '../components/CalorieProgress'
import { FoodLogRow } from '../components/FoodLogRow'
import { MacroBar } from '../components/MacroBar'
import type { DailySummary } from '../types'

function todayIso(): string {
  return new Date().toISOString().slice(0, 10)
}

export function DashboardPage() {
  const [summary, setSummary] = useState<DailySummary | null>(null)
  const [error, setError] = useState<string | null>(null)

  async function refresh() {
    try {
      setSummary(await getDailySummary(todayIso()))
    } catch {
      setError('Could not load today\'s summary.')
    }
  }

  useEffect(() => {
    refresh()
  }, [])

  async function handleDelete(logId: number) {
    await deleteLog(logId)
    refresh()
  }

  if (error) {
    return <p className="p-8 text-center text-red-500">{error}</p>
  }

  if (!summary) {
    return <p className="p-8 text-center text-gray-500">Loading...</p>
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6 p-6">
      <CalorieProgress consumed={summary.total_calories} goal={summary.goal_calories} />

      <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
        <h2 className="mb-3 text-sm font-medium text-gray-500">Macros today</h2>
        <div className="space-y-2">
          <MacroBar label="Protein" grams={summary.total_protein_g} colorClass="bg-blue-500" />
          <MacroBar label="Carbs" grams={summary.total_carbs_g} colorClass="bg-amber-500" />
          <MacroBar label="Fat" grams={summary.total_fat_g} colorClass="bg-pink-500" />
        </div>
      </div>

      <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
        <div className="mb-2 flex items-center justify-between">
          <h2 className="text-sm font-medium text-gray-500">Food diary</h2>
          <Link to="/scan" className="text-sm font-medium text-brand-600 hover:underline">
            + Log food
          </Link>
        </div>
        {summary.entries.length === 0 ? (
          <p className="py-6 text-center text-sm text-gray-400">
            Nothing logged yet today. Scan a meal to get started.
          </p>
        ) : (
          summary.entries.map((log) => (
            <FoodLogRow key={log.id} log={log} onDelete={handleDelete} />
          ))
        )}
      </div>
    </div>
  )
}
