import type {
  ClusterPoint,
  Customer,
  KScorePoint,
  Overview,
  PredictRequest,
  PredictResponse,
  SegmentSummary,
} from "./types";

const BASE = "/api";

class ApiError extends Error {}

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${BASE}${path}`);
  if (!response.ok) {
    throw new ApiError(`${response.status} ${response.statusText}`);
  }
  return response.json() as Promise<T>;
}

export const getOverview = () => getJson<Overview>("/overview");
export const getSegmentsSummary = () => getJson<SegmentSummary[]>("/segments/summary");
export const getSegmentCustomers = (segment: string) =>
  getJson<Customer[]>(`/segments/${encodeURIComponent(segment)}/customers`);
export const getKSelection = () => getJson<KScorePoint[]>("/k-selection");
export const getClusters = () => getJson<ClusterPoint[]>("/clusters");

export const segmentExportUrl = (segment: string) => `${BASE}/segments/${encodeURIComponent(segment)}/export`;

export async function predictSegment(payload: PredictRequest): Promise<PredictResponse> {
  const response = await fetch(`${BASE}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({ detail: response.statusText }));
    const detail = Array.isArray(body.detail)
      ? body.detail.map((d: { msg: string }) => d.msg).join(", ")
      : body.detail;
    throw new ApiError(detail ?? "Prediction failed");
  }
  return response.json() as Promise<PredictResponse>;
}
