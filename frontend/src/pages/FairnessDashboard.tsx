import { useEffect, useState } from "react";
import { api, type EvaluationReport, type FairnessResponse } from "../lib/api";
import StatusBanner from "../components/StatusBanner";

export default function FairnessDashboard() {
  const [fairness, setFairness] = useState<FairnessResponse | null>(null);
  const [evaluation, setEvaluation] = useState<EvaluationReport | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      api.fairness().then(setFairness),
      api.evaluation().then(setEvaluation).catch(() => setEvaluation(null)),
    ]).catch((e: Error) => setError(e.message));
  }, []);

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
                {fairness.parity.map((cell) => (
                  <tr key={`${cell.dimension}-${cell.key}`} className="border-t border-[var(--mist)]">
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
              </tbody>
            </table>
          </section>
          <p className="text-xs text-[var(--ink)]/60">{fairness.disclaimer}</p>
        </>
      )}

      {evaluation && (
        <section className="rounded-xl border border-[var(--mist)] bg-[var(--card)] p-4">
          <h2 className="text-xl">Synthetic evaluation snapshot</h2>
          <dl className="mt-3 grid gap-2 sm:grid-cols-2 text-sm">
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
