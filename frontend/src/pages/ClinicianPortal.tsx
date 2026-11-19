import { useEffect, useState } from "react";
import { api, type ResidentDetail, type ResidentSummary } from "../lib/api";
import { useSelection } from "../lib/selection";
import StatusBanner from "../components/StatusBanner";

function tierClass(tier: string): string {
  if (tier === "high") return "bg-red-100 text-red-900";
  if (tier === "medium") return "bg-amber-100 text-amber-950";
  if (tier === "baseline_onboarding") return "bg-sky-100 text-sky-950";
  return "bg-[var(--mist)] text-[var(--ink)]";
}

export default function ClinicianPortal() {
  const { residentId, setResidentId } = useSelection();
  const [list, setList] = useState<ResidentSummary[]>([]);
  const [detail, setDetail] = useState<ResidentDetail | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [approved, setApproved] = useState(false);

  useEffect(() => {
    api
      .residents()
      .then((rows) => {
        setList(rows);
        setResidentId((current) => current ?? rows[0]?.resident_id ?? null);
      })
      .catch((e: Error) => setError(e.message));
  }, [setResidentId]);

  useEffect(() => {
    if (!residentId) return;
    setApproved(false);
    api
      .resident(residentId)
      .then(setDetail)
      .catch((e: Error) => setError(e.message));
  }, [residentId]);

  const engine = detail?.engine;
  const resident = detail?.resident;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl text-[var(--teal-deep)]">Clinician Reason-for-Flag</h1>
        <p className="mt-1 text-[var(--ink)]/70">
          Auditable triage card — prioritization only, not a diagnosis.
        </p>
      </div>

      {error && (
        <StatusBanner
          title="API unavailable"
          body={`${error}. Start the API and generate data (make generate; make engine; make api).`}
        />
      )}

      <label className="block text-sm font-medium">
        Select synthetic patient
        <select
          className="mt-2 w-full rounded-md border border-[var(--mist)] bg-[var(--card)] px-3 py-2"
          value={residentId ?? ""}
          onChange={(e) => setResidentId(e.target.value)}
        >
          {list.map((r) => (
            <option key={r.resident_id} value={r.resident_id}>
              {r.display_name} · {r.age}y · {r.resident_segment} · {r.risk_tier ?? "n/a"}
            </option>
          ))}
        </select>
      </label>

      {engine && resident && (
        <section className="rounded-xl border border-[var(--mist)] bg-[var(--card)] p-5 shadow-sm space-y-4">
          <div className="flex flex-wrap gap-2 text-sm">
            <span
              className={`rounded-md px-2.5 py-1 font-medium ${tierClass(engine.risk_tier)}`}
            >
              Tier: {engine.risk_tier}
            </span>
            <span className="rounded-md bg-[var(--mist)] px-2.5 py-1">
              {engine.confidence_badge}
            </span>
            <span className="rounded-md bg-[var(--mist)] px-2.5 py-1">
              Score: {engine.risk_score}
            </span>
            <span className="rounded-md bg-[var(--mist)] px-2.5 py-1">
              Uncertainty: {engine.uncertainty}
            </span>
          </div>

          <div>
            <h2 className="text-xl">Pathway recommendation</h2>
            <p className="mt-1 text-lg text-[var(--teal-deep)] font-medium">
              {engine.pathway_recommendation}
            </p>
            <p className="text-sm text-[var(--ink)]/60">{engine.pathway}</p>
          </div>

          <div>
            <h2 className="text-xl">Top driving factors</h2>
            <ol className="mt-2 space-y-2">
              {engine.top_reasons.map((r) => (
                <li key={`${r.rank}-${r.theme}`} className="rounded-md bg-[var(--sand)] px-3 py-2">
                  <span className="font-medium">
                    {r.rank}. {r.theme}:
                  </span>{" "}
                  {r.detail}
                </li>
              ))}
            </ol>
          </div>

          {engine.household_bundle_hint && (
            <div className="rounded-md border border-[var(--coral)]/30 bg-orange-50 px-3 py-2 text-sm">
              Household care-gap alert: {engine.household_bundle_hint}
            </div>
          )}

          <p className="text-xs text-[var(--ink)]/70 border-t border-[var(--mist)] pt-3">
            {engine.clinical_firewall}
          </p>

          <button
            type="button"
            className="rounded-md bg-[var(--teal)] px-4 py-2 text-white hover:bg-[var(--teal-deep)]"
            onClick={() => setApproved(true)}
          >
            Approve Preventive Order
          </button>
          {approved && (
            <p className="text-sm text-[var(--teal-deep)]">
              Simulated approval recorded for {String(resident.display_name)}.
            </p>
          )}
        </section>
      )}
    </div>
  );
}
