export type RiskTier = "high" | "medium" | "low" | "baseline_onboarding";

export interface ReasonItem {
  rank: number;
  theme: string;
  detail: string;
}

export interface ResidentSummary {
  resident_id: string;
  display_name: string;
  age: number;
  sex: string;
  district: string;
  household_id: string;
  preferred_language: string;
  resident_segment: string;
  risk_tier?: RiskTier | null;
  pathway?: string | null;
}

export interface EngineOutput {
  resident_id: string;
  risk_score: number;
  risk_tier: RiskTier;
  uncertainty: "HIGH" | "MEDIUM" | "LOW";
  confidence_badge: string;
  top_reasons: ReasonItem[];
  rule_hits: string[];
  pathway: string;
  pathway_recommendation: string;
  clinical_firewall: string;
  data_sources_used: string[];
  data_sources_not_used: string[];
  household_bundle_hint?: string | null;
}

export interface ResidentDetail {
  resident: Record<string, unknown>;
  engine: EngineOutput | null;
}

export interface FairnessResponse {
  funnel: Record<string, number>;
  parity: Array<{
    dimension: string;
    key: string;
    n: number | string;
    recommendation_rate?: number | string | null;
    attendance_rate?: number | string | null;
    suppressed: boolean;
  }>;
  small_cell_threshold: number;
  disclaimer: string;
}

export interface EvaluationReport {
  dataset: string;
  reference_date?: string | null;
  metrics: Record<string, number | null>;
  pass?: Record<string, boolean>;
  disclaimer: string;
}

async function getJson<T>(path: string): Promise<T> {
  const res = await fetch(path);
  if (!res.ok) {
    throw new Error(`${path} failed: ${res.status}`);
  }
  return res.json() as Promise<T>;
}

const API_V1 = "/api/v1";

export const api = {
  health: () => getJson<{ status: string }>(`${API_V1}/health`),
  residents: () => getJson<ResidentSummary[]>(`${API_V1}/residents`),
  resident: (id: string) => getJson<ResidentDetail>(`${API_V1}/residents/${id}`),
  fairness: () => getJson<FairnessResponse>(`${API_V1}/metrics/fairness`),
  evaluation: () => getJson<EvaluationReport>(`${API_V1}/metrics/evaluation`),
};
