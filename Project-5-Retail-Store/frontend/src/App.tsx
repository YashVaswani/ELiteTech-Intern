import { useEffect, useMemo, useState } from "react";
import { getClusters, getKSelection, getOverview, getSegmentCustomers, getSegmentsSummary } from "./api";
import { colorForCluster } from "./colors";
import ClusterScatterChart from "./components/ClusterScatterChart";
import CustomerTable from "./components/CustomerTable";
import KSelectionChart from "./components/KSelectionChart";
import MetricCard from "./components/MetricCard";
import PredictForm from "./components/PredictForm";
import SegmentSummaryTable from "./components/SegmentSummaryTable";
import Tabs from "./components/Tabs";
import type { ClusterPoint, Customer, KScorePoint, Overview, SegmentSummary } from "./types";

const TABS = ["Overview", "Explore segments", "Classify a customer"];

export default function App() {
  const [tab, setTab] = useState(TABS[0]);
  const [overview, setOverview] = useState<Overview | null>(null);
  const [summary, setSummary] = useState<SegmentSummary[]>([]);
  const [kScores, setKScores] = useState<KScorePoint[]>([]);
  const [clusters, setClusters] = useState<ClusterPoint[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [selectedSegment, setSelectedSegment] = useState<string | null>(null);
  const [segmentCustomers, setSegmentCustomers] = useState<Customer[]>([]);

  useEffect(() => {
    Promise.all([getOverview(), getSegmentsSummary(), getKSelection(), getClusters()])
      .then(([ov, sum, ks, cl]) => {
        setOverview(ov);
        setSummary(sum);
        setKScores(ks);
        setClusters(cl);
        setSelectedSegment(sum[0]?.segment ?? null);
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load data"));
  }, []);

  useEffect(() => {
    if (!selectedSegment) return;
    getSegmentCustomers(selectedSegment)
      .then(setSegmentCustomers)
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load customers"));
  }, [selectedSegment]);

  const colorForSegment = useMemo(() => {
    const clusterBySegment = new Map(clusters.map((c) => [c.segment, c.cluster]));
    return (segment: string) => colorForCluster(clusterBySegment.get(segment) ?? 0);
  }, [clusters]);

  if (error) {
    return (
      <div className="mx-auto max-w-2xl p-8">
        <div className="rounded-lg border border-red-800 bg-red-950/50 p-4 text-red-200">
          <p className="font-medium">Couldn't load data from the API.</p>
          <p className="mt-1 text-sm text-red-300">{error}</p>
          <p className="mt-2 text-sm text-red-300">
            Make sure the backend is running (<code>uvicorn api.main:app --port 8000</code>) and that a model
            has been trained (<code>retail-segment train</code>).
          </p>
        </div>
      </div>
    );
  }

  if (!overview) {
    return <div className="p-8 text-slate-400">Loading...</div>;
  }

  return (
    <div className="mx-auto max-w-5xl px-6 py-10">
      <header className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight text-slate-50">Retail Customer Segmentation</h1>
        <p className="mt-1 text-slate-400">
          K-means clustering on Recency, Frequency, and Monetary purchase history.
        </p>
      </header>

      <Tabs tabs={TABS} active={tab} onChange={setTab} />

      <div className="mt-6">
        {tab === "Overview" && (
          <div className="space-y-8">
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
              <MetricCard label="Customers" value={overview.customers.toLocaleString()} />
              <MetricCard label="Segments found" value={String(overview.segments)} />
              <MetricCard
                label="Avg. customer value"
                value={`$${overview.avg_monetary.toLocaleString(undefined, { maximumFractionDigits: 0 })}`}
              />
            </div>

            <section>
              <h2 className="mb-3 text-lg font-semibold text-slate-100">Segment summary</h2>
              <SegmentSummaryTable rows={summary} colorForSegment={colorForSegment} />
            </section>

            <section className="grid grid-cols-1 gap-6 lg:grid-cols-2">
              <div>
                <h2 className="mb-3 text-lg font-semibold text-slate-100">How k was chosen</h2>
                <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4">
                  <KSelectionChart scores={kScores} chosenK={overview.k} />
                </div>
              </div>
              <div>
                <h2 className="mb-3 text-lg font-semibold text-slate-100">Clusters (PCA projection)</h2>
                <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4">
                  <ClusterScatterChart points={clusters} colorForSegment={colorForSegment} />
                </div>
              </div>
            </section>
          </div>
        )}

        {tab === "Explore segments" && (
          <div className="space-y-4">
            <label className="block max-w-xs">
              <span className="mb-1 block text-sm text-slate-300">Segment</span>
              <select
                value={selectedSegment ?? ""}
                onChange={(e) => setSelectedSegment(e.target.value)}
                className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 focus:border-indigo-500 focus:outline-none"
              >
                {summary.map((s) => (
                  <option key={s.segment} value={s.segment}>
                    {s.segment}
                  </option>
                ))}
              </select>
            </label>
            {selectedSegment && <CustomerTable segment={selectedSegment} customers={segmentCustomers} />}
          </div>
        )}

        {tab === "Classify a customer" && <PredictForm />}
      </div>
    </div>
  );
}
