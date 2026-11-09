import {
  CartesianGrid,
  ComposedChart,
  Legend,
  Line,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { KScorePoint } from "../types";

interface Props {
  scores: KScorePoint[];
  chosenK: number;
}

interface DotProps {
  cx?: number;
  cy?: number;
  payload?: KScorePoint;
}

function makeDotRenderer(chosenK: number, color: string, highlightColor: string) {
  return ({ cx, cy, payload }: DotProps) => {
    if (cx === undefined || cy === undefined || !payload) return <g />;
    const isChosen = payload.k === chosenK;
    return (
      <circle
        key={payload.k}
        cx={cx}
        cy={cy}
        r={isChosen ? 5 : 3}
        fill={color}
        stroke={isChosen ? highlightColor : "none"}
        strokeWidth={2}
      />
    );
  };
}

export default function KSelectionChart({ scores, chosenK }: Props) {
  return (
    <ResponsiveContainer width="100%" height={320}>
      <ComposedChart data={scores} margin={{ top: 10, right: 30, bottom: 10, left: 10 }}>
        <CartesianGrid stroke="#1e293b" />
        <XAxis
          dataKey="k"
          tick={{ fill: "#94a3b8", fontSize: 12 }}
          stroke="#334155"
          label={{
            value: "k (clusters)",
            position: "insideBottom",
            offset: -5,
            fill: "#64748b",
            fontSize: 12,
          }}
        />
        <YAxis
          yAxisId="inertia"
          tick={{ fill: "#94a3b8", fontSize: 12 }}
          stroke="#334155"
          label={{ value: "Inertia", angle: -90, position: "insideLeft", fill: "#64748b", fontSize: 12 }}
        />
        <YAxis
          yAxisId="silhouette"
          orientation="right"
          tick={{ fill: "#94a3b8", fontSize: 12 }}
          stroke="#334155"
          label={{ value: "Silhouette", angle: 90, position: "insideRight", fill: "#64748b", fontSize: 12 }}
        />
        <Tooltip contentStyle={{ backgroundColor: "#0f172a", border: "1px solid #334155", fontSize: 12 }} />
        <Legend wrapperStyle={{ fontSize: 12, color: "#94a3b8" }} />
        <Line
          yAxisId="inertia"
          type="monotone"
          dataKey="inertia"
          name="Inertia (elbow)"
          stroke="#6366f1"
          strokeWidth={2}
          dot={makeDotRenderer(chosenK, "#6366f1", "#c7d2fe")}
        />
        <Line
          yAxisId="silhouette"
          type="monotone"
          dataKey="silhouette"
          name="Silhouette score"
          stroke="#f97316"
          strokeWidth={2}
          dot={makeDotRenderer(chosenK, "#f97316", "#fed7aa")}
        />
      </ComposedChart>
    </ResponsiveContainer>
  );
}
