import { type FormEvent, useState } from "react";
import { predictSegment } from "../api";
import type { PredictResponse } from "../types";

export default function PredictForm() {
  const [recency, setRecency] = useState(30);
  const [frequency, setFrequency] = useState(5);
  const [monetary, setMonetary] = useState(250);
  const [result, setResult] = useState<PredictResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      setResult(await predictSegment({ recency, frequency, monetary }));
    } catch (err) {
      setResult(null);
      setError(err instanceof Error ? err.message : "Prediction failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-md">
      <p className="mb-4 text-sm text-slate-400">
        Enter a customer's RFM values to see which segment the trained model assigns them to.
      </p>
      <form
        onSubmit={handleSubmit}
        className="space-y-4 rounded-xl border border-slate-800 bg-slate-900/60 p-5"
      >
        <Field label="Days since last purchase (Recency)" value={recency} onChange={setRecency} min={0} />
        <Field label="Number of orders (Frequency)" value={frequency} onChange={setFrequency} min={1} />
        <Field
          label="Total amount spent (Monetary)"
          value={monetary}
          onChange={setMonetary}
          min={0}
          step={0.01}
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-500 disabled:opacity-50"
        >
          {loading ? "Classifying..." : "Classify"}
        </button>
      </form>

      {result && (
        <div className="mt-4 rounded-lg border border-emerald-800 bg-emerald-950/50 px-4 py-3 text-sm text-emerald-200">
          Predicted segment: <span className="font-semibold">{result.segment}</span> (cluster {result.cluster}
          )
        </div>
      )}
      {error && (
        <div className="mt-4 rounded-lg border border-red-800 bg-red-950/50 px-4 py-3 text-sm text-red-200">
          {error}
        </div>
      )}
    </div>
  );
}

interface FieldProps {
  label: string;
  value: number;
  onChange: (value: number) => void;
  min?: number;
  step?: number;
}

function Field({ label, value, onChange, min, step }: FieldProps) {
  return (
    <label className="block">
      <span className="mb-1 block text-sm text-slate-300">{label}</span>
      <input
        type="number"
        value={value}
        min={min}
        step={step ?? 1}
        required
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 focus:border-indigo-500 focus:outline-none"
      />
    </label>
  );
}
