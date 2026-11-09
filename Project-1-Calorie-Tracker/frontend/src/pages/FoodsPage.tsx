import { useEffect, useMemo, useState } from 'react'
import { listFoods } from '../api/foods'
import { createLog } from '../api/logs'
import type { FoodItem } from '../types'

function formatFoodName(name: string): string {
  return name.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())
}

export function FoodsPage() {
  const [foods, setFoods] = useState<FoodItem[]>([])
  const [query, setQuery] = useState('')
  const [grams, setGrams] = useState<Record<string, number>>({})
  const [loggedFood, setLoggedFood] = useState<string | null>(null)

  useEffect(() => {
    listFoods().then(setFoods)
  }, [])

  const filtered = useMemo(
    () => foods.filter((f) => f.food_name.includes(query.toLowerCase().replace(/ /g, '_'))),
    [foods, query],
  )

  async function handleLog(food: FoodItem) {
    const servingGrams = grams[food.food_name] ?? 100
    await createLog(food.food_name, servingGrams)
    setLoggedFood(food.food_name)
    setTimeout(() => setLoggedFood(null), 1500)
  }

  return (
    <div className="mx-auto max-w-2xl space-y-4 p-6">
      <h1 className="text-xl font-bold text-gray-900">Food database</h1>
      <input
        type="text"
        placeholder="Search foods..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
      />

      <div className="divide-y divide-gray-100 rounded-xl border border-gray-200 bg-white">
        {filtered.map((food) => (
          <div key={food.food_name} className="flex items-center justify-between gap-3 p-4">
            <div>
              <p className="font-medium text-gray-900">{formatFoodName(food.food_name)}</p>
              <p className="text-sm text-gray-500">{food.calories_per_100g} kcal / 100g</p>
            </div>
            <div className="flex items-center gap-2">
              <input
                type="number"
                min={1}
                value={grams[food.food_name] ?? 100}
                onChange={(e) =>
                  setGrams((prev) => ({ ...prev, [food.food_name]: Number(e.target.value) }))
                }
                className="w-20 rounded-md border border-gray-300 px-2 py-1 text-sm"
              />
              <button
                onClick={() => handleLog(food)}
                className="rounded-md bg-brand-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-brand-700"
              >
                {loggedFood === food.food_name ? 'Logged!' : 'Log'}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
