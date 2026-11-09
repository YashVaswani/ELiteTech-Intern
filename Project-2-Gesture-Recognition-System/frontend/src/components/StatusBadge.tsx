interface Props {
  webcamStatus: string
  streamStatus: string
}

const DOT_COLOR: Record<string, string> = {
  active: 'bg-emerald-500',
  open: 'bg-emerald-500',
  requesting: 'bg-amber-500',
  connecting: 'bg-amber-500',
  error: 'bg-red-500',
  closed: 'bg-red-500',
  idle: 'bg-slate-500',
}

export function StatusBadge({ webcamStatus, streamStatus }: Props) {
  return (
    <div className="flex items-center gap-4 text-xs text-slate-400">
      <span className="flex items-center gap-1.5">
        <span className={`h-2 w-2 rounded-full ${DOT_COLOR[webcamStatus] ?? 'bg-slate-500'}`} />
        camera: {webcamStatus}
      </span>
      <span className="flex items-center gap-1.5">
        <span className={`h-2 w-2 rounded-full ${DOT_COLOR[streamStatus] ?? 'bg-slate-500'}`} />
        backend: {streamStatus}
      </span>
    </div>
  )
}
