interface Props {
  label: string
  grams: number
  colorClass: string
}

export function MacroBar({ label, grams, colorClass }: Props) {
  return (
    <div className="flex items-center gap-3">
      <span className={`h-2 w-2 rounded-full ${colorClass}`} />
      <span className="text-sm text-gray-600">{label}</span>
      <span className="ml-auto text-sm font-medium text-gray-900">{grams}g</span>
    </div>
  )
}
