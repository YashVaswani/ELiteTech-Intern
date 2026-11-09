// A fixed, colorblind-friendlier palette so the same cluster always gets the
// same color across every chart/table in the app.
const PALETTE = ["#6366f1", "#f97316", "#10b981", "#ec4899", "#06b6d4", "#eab308", "#8b5cf6", "#ef4444"];

export function colorForCluster(cluster: number): string {
  return PALETTE[cluster % PALETTE.length];
}
