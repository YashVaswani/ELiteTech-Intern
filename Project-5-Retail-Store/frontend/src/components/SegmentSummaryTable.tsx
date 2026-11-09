import type { SegmentSummary } from "../types";

interface Props {
  rows: SegmentSummary[];
  colorForSegment: (segment: string) => string;
}

const currency = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 0,
});

export default function SegmentSummaryTable({ rows, colorForSegment }: Props) {
  return (
    <div className="overflow-hidden rounded-xl border border-slate-800">
      <table className="w-full text-left text-sm">
        <thead className="bg-slate-900/80 text-slate-400">
          <tr>
            <th className="px-4 py-3 font-medium">Segment</th>
            <th className="px-4 py-3 font-medium">Customers</th>
            <th className="px-4 py-3 font-medium">Avg. recency (days)</th>
            <th className="px-4 py-3 font-medium">Avg. orders</th>
            <th className="px-4 py-3 font-medium">Avg. spend</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800">
          {rows.map((row) => (
            <tr key={row.segment} className="bg-slate-950/40">
              <td className="flex items-center gap-2 px-4 py-3 font-medium text-slate-100">
                <span
                  className="h-2.5 w-2.5 rounded-full"
                  style={{ backgroundColor: colorForSegment(row.segment) }}
                />
                {row.segment}
              </td>
              <td className="px-4 py-3 text-slate-300">{row.customers.toLocaleString()}</td>
              <td className="px-4 py-3 text-slate-300">{row.avg_recency_days}</td>
              <td className="px-4 py-3 text-slate-300">{row.avg_frequency}</td>
              <td className="px-4 py-3 text-slate-300">{currency.format(row.avg_monetary)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
