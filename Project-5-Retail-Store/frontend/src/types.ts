export interface Overview {
  customers: number;
  segments: number;
  avg_monetary: number;
  k: number;
}

export interface SegmentSummary {
  segment: string;
  customers: number;
  avg_recency_days: number;
  avg_frequency: number;
  avg_monetary: number;
}

export interface Customer {
  customer_id: number;
  recency: number;
  frequency: number;
  monetary: number;
  cluster: number;
  segment: string;
}

export interface KScorePoint {
  k: number;
  inertia: number;
  silhouette: number;
}

export interface ClusterPoint {
  pc1: number;
  pc2: number;
  cluster: number;
  segment: string;
}

export interface PredictRequest {
  recency: number;
  frequency: number;
  monetary: number;
}

export interface PredictResponse {
  cluster: number;
  segment: string;
}
