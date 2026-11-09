import { segmentExportUrl } from "../api";
import type { Customer } from "../types";

interface Props {
  segment: string;
  customers: Customer[];
}

export default function CustomerTable({ segment, customers }: Props) {
  return (
    <div>
      <div className="mb-3 flex items-center justify-between">
        <p className="text-sm text-slate-400">
          {customers.length.toLocaleString()} customers in <span className="text-slate-100">{segment}</span>
        </p>
        <a
          href={segmentExportUrl(segment)}
          className="rounded-lg border border-slate-700 px-3 py-1.5 text-sm text-slate-200 hover:bg-slate-800"
        >
          Download CSV
        </a>
      </div>
      <div className="max-h-96 overflow-y-auto rounded-xl border border-slate-800">
        <table className="w-full text-left text-sm">
          <thead className="sticky top-0 bg-slate-900/95 text-slate-400">
            <tr>
              <th className="px-4 py-2 font-medium">Customer ID</th>
              <th className="px-4 py-2 font-medium">Recency</th>
              <th className="px-4 py-2 font-medium">Frequency</th>
              <th className="px-4 py-2 font-medium">Monetary</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {customers.map((c) => (
              <tr key={c.customer_id}>
                <td className="px-4 py-2 text-slate-300">{c.customer_id}</td>
                <td className="px-4 py-2 text-slate-300">{c.recency}</td>
                <td className="px-4 py-2 text-slate-300">{c.frequency}</td>
                <td className="px-4 py-2 text-slate-300">${c.monetary.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
