import {
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { ClusterPoint } from "../types";

interface Props {
  points: ClusterPoint[];
  colorForSegment: (segment: string) => string;
}

export default function ClusterScatterChart({ points, colorForSegment }: Props) {
  const segments = [...new Set(points.map((p) => p.segment))];
  const bySegment = segments.map((segment) => ({
    segment,
    data: points.filter((p) => p.segment === segment),
  }));

  return (
    <ResponsiveContainer width="100%" height={360}>
      <ScatterChart margin={{ top: 10, right: 10, bottom: 10, left: 0 }}>
        <CartesianGrid stroke="#1e293b" />
        <XAxis
          type="number"
          dataKey="pc1"
          name="PC1"
          tick={{ fill: "#94a3b8", fontSize: 12 }}
          stroke="#334155"
        />
        <YAxis
          type="number"
          dataKey="pc2"
          name="PC2"
          tick={{ fill: "#94a3b8", fontSize: 12 }}
          stroke="#334155"
        />
        <Tooltip
          cursor={{ strokeDasharray: "3 3" }}
          contentStyle={{ backgroundColor: "#0f172a", border: "1px solid #334155", fontSize: 12 }}
        />
        <Legend wrapperStyle={{ fontSize: 12, color: "#94a3b8" }} />
        {bySegment.map(({ segment, data }) => (
          <Scatter key={segment} name={segment} data={data} fill={colorForSegment(segment)} opacity={0.75} />
        ))}
      </ScatterChart>
    </ResponsiveContainer>
  );
}
