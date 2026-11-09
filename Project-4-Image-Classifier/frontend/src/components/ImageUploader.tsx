import { useRef, useState } from 'react'

interface ImageUploaderProps {
  onFileSelected: (file: File) => void
  previewUrl: string | null
  disabled: boolean
}

const ACCEPTED_TYPES = ['image/jpeg', 'image/png', 'image/webp']

export function ImageUploader({ onFileSelected, previewUrl, disabled }: ImageUploaderProps) {
  const [isDragging, setIsDragging] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  const handleFile = (file: File | undefined) => {
    if (file && ACCEPTED_TYPES.includes(file.type)) {
      onFileSelected(file)
    }
  }

  return (
    <div
      role="button"
      tabIndex={0}
      aria-label="Upload an image"
      onClick={() => !disabled && inputRef.current?.click()}
      onKeyDown={(e) => e.key === 'Enter' && !disabled && inputRef.current?.click()}
      onDragOver={(e) => {
        e.preventDefault()
        setIsDragging(true)
      }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={(e) => {
        e.preventDefault()
        setIsDragging(false)
        handleFile(e.dataTransfer.files[0])
      }}
      className={`flex min-h-64 cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed p-6 text-center transition-colors ${
        isDragging
          ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-950/30'
          : 'border-slate-300 dark:border-slate-700'
      } ${disabled ? 'pointer-events-none opacity-60' : ''}`}
    >
      <input
        ref={inputRef}
        type="file"
        accept={ACCEPTED_TYPES.join(',')}
        className="hidden"
        onChange={(e) => handleFile(e.target.files?.[0])}
      />
      {previewUrl ? (
        <img
          src={previewUrl}
          alt="Selected upload preview"
          className="max-h-56 rounded-lg object-contain"
        />
      ) : (
        <>
          <p className="text-lg font-medium">Drop a cat or dog photo here</p>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
            or click to browse — JPEG, PNG or WebP
          </p>
        </>
      )}
    </div>
  )
}
