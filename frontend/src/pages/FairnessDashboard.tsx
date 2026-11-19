import { useEffect, useMemo, useState } from "react";
import { api, type EvaluationReport, type FairnessResponse } from "../lib/api";
import StatusBanner from "../components/StatusBanner";

const MASK = "<10 — Suppressed for Privacy";

export default function FairnessDashboard() {
  const [fairness, setFairness] = useState<FairnessResponse | null>(null);
  const [evaluation, setEvaluation] = useState<EvaluationReport | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [suppressedOnly, setSuppressedOnly] = useState(false);

  useEffect(() => {
    Promise.all([
      api.fairness().then(setFairness),
      api.evaluation().then(setEvaluation).catch(() => setEvaluation(null)),
    ]).catch((e: Error) => setError(e.message));
  }, []);

  const rows = useMemo(() => {
    if (!fairness) return [];
    return suppressedOnly
      ? fairness.parity.filter((c) => c.suppressed)
      : fairness.parity;
  }, [fairness, suppressedOnly]);

  const suppressedCount = fairness?.parity.filter((c) => c.suppressed).length ?? 0;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl text-[var(--teal-deep)]">Public Health & Fairness Monitor</h1>
        <p className="mt-1 text-[var(--ink)]/70">
          Conversion funnel, segment parity, and small-cell privacy shield.
        </p>
      </div>

      {error && <StatusBanner title="API unavailable" body={error} />}

      {fairness && (
        <>
          <section className="grid gap-3 sm:grid-cols-5">
            {Object.entries(fairness.funnel).map(([k, v]) => (
              <div
                key={k}
                className="rounded-lg border border-[var(--mist)] bg-[var(--card)] px-3 py-4"
              >
                <p className="text-xs uppercase tracking-wide text-[var(--ink)]/50">{k}</p>
                <p className="mt-1 text-2xl font-semibold text-[var(--teal-deep)]">{v}</p>
              </div>
            ))}
          </section>

          <div className="flex flex-wrap items-center justify-between gap-3 rounded-lg border border-[var(--coral)]/30 bg-orange-50 px-4 py-3 text-sm">
            <div>
              <p className="font-semibold text-[var(--coral)]">Small-cell privacy shield</p>
              <p className="opacity-80">
                Cells with n &lt; {fairness.small_cell_threshold} display{" "}
                <code className="rounded bg-white/80 px-1">{MASK}</code>. Currently suppressed:{" "}
                {suppressedCount}.
              </p>
            </div>
            <label className="flex items-center gap-2 whitespace-nowrap">
              <input
                type="checkbox"
                checked={suppressedOnly}
                onChange={(e) => setSuppressedOnly(e.target.checked)}
              />
              Show suppressed cells only
            </label>
          </div>

          <section className="overflow-x-auto rounded-xl border border-[var(--mist)] bg-[var(--card)]">
            <table className="min-w-full text-sm">
              <thead className="bg-[var(--sand)] text-left">
                <tr>
                  <th className="px-3 py-2">Dimension</th>
                  <th className="px-3 py-2">Key</th>
                  <th className="px-3 py-2">n</th>
                  <th className="px-3 py-2">Recommendation rate</th>
                  <th className="px-3 py-2">Suppressed</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((cell) => (
                  <tr
                    key={`${cell.dimension}-${cell.key}`}
                    className={`border-t border-[var(--mist)] ${
                      cell.suppressed ? "bg-orange-50/60" : ""
                    }`}
                  >
                    <td className="px-3 py-2">{cell.dimension}</td>
                    <td className="px-3 py-2">{cell.key}</td>
                    <td className="px-3 py-2 font-medium">
                      {cell.suppressed ? (
                        <span className="text-[var(--coral)]">{String(cell.n)}</span>
                      ) : (
                        cell.n
                      )}
                    </td>
                    <td className="px-3 py-2">{String(cell.recommendation_rate ?? "—")}</td>
                    <td className="px-3 py-2">{cell.suppressed ? "yes" : "no"}</td>
                  </tr>
                ))}
                {rows.length === 0 && (
                  <tr>
                    <td className="px-3 py-4 text-[var(--ink)]/60" colSpan={5}>
                      No suppressed cells in this view.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </section>
          <p className="text-xs text-[var(--ink)]/60">{fairness.disclaimer}</p>
        </>
      )}

      {evaluation && (
        <section className="rounded-xl border border-[var(--mist)] bg-[var(--card)] p-4">
          <h2 className="text-xl">Synthetic evaluation snapshot</h2>
          <div className="mt-3 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {[
              ["lift_vs_age_only", "Lift vs age-only"],
              ["small_cell_leak_count", "Small-cell leaks"],
              ["caregap_catch_rate_hayah", "Hayah catch rate"],
              ["uncertainty_abstain_rate", "Uncertainty abstain"],
            ].map(([key, label]) => (
              <div key={key} className="rounded-lg bg-[var(--sand)] px-3 py-3">
                <p className="text-xs uppercase tracking-wide text-[var(--ink)]/50">{label}</p>
                <p className="mt-1 text-xl font-semibold text-[var(--teal-deep)]">
                  {evaluation.metrics[key] ?? "—"}
                </p>
              </div>
            ))}
          </div>
          <dl className="mt-4 grid gap-2 sm:grid-cols-2 text-sm">
            {Object.entries(evaluation.metrics).map(([k, v]) => (
              <div key={k} className="flex justify-between gap-4 border-b border-[var(--mist)] py-1">
                <dt className="text-[var(--ink)]/60">{k}</dt>
                <dd className="font-medium">{v ?? "—"}</dd>
              </div>
            ))}
          </dl>
          <p className="mt-3 text-xs opacity-60">{evaluation.disclaimer}</p>
        </section>
      )}
    </div>
  );
}
