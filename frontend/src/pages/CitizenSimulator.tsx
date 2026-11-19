import { useEffect, useMemo, useState } from "react";
import { api, type ResidentDetail } from "../lib/api";
import {
  SUPPORTED_LANGS,
  buildMessagePreview,
  getLabels,
  isRtl,
  isStubLang,
  type Lang,
  type Modality,
} from "../lib/messageTemplates";
import { useSelection } from "../lib/selection";
import StatusBanner from "../components/StatusBanner";

export default function CitizenSimulator() {
  const { residentId } = useSelection();
  const [detail, setDetail] = useState<ResidentDetail | null>(null);
  const [lang, setLang] = useState<Lang>("en");
  const [modality, setModality] = useState<Modality>("clinic");
  const [optOut, setOptOut] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!residentId) return;
    api
      .resident(residentId)
      .then(setDetail)
      .catch((e: Error) => setError(e.message));
  }, [residentId]);

  const labels = useMemo(() => getLabels(lang), [lang]);
  const name = String(detail?.resident.display_name ?? "your family member");
  const engine = detail?.engine;
  const preview = useMemo(
    () => buildMessagePreview(lang, name, engine?.pathway_recommendation),
    [lang, name, engine?.pathway_recommendation],
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl text-[var(--teal-deep)]">Citizen Mobile Simulator</h1>
        <p className="mt-1 text-[var(--ink)]/70">
          WhatsApp / portal style preview with multilingual transparency templates.
        </p>
      </div>

      {!residentId && (
        <StatusBanner
          title="No patient selected"
          body="Open Clinician portal and pick a synthetic resident first."
        />
      )}
      {error && <StatusBanner title="API unavailable" body={error} />}

      <div className="mx-auto max-w-md rounded-[2rem] border border-[var(--ink)]/10 bg-[var(--card)] p-4 shadow-lg">
        <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
          <p className="text-xs uppercase tracking-widest text-[var(--ink)]/50">Hayah-Pulse</p>
          <div className="flex flex-wrap gap-1">
            {SUPPORTED_LANGS.map((code) => (
              <button
                key={code}
                type="button"
                className={`rounded px-2 py-1 text-xs uppercase ${
                  lang === code ? "bg-[var(--teal)] text-white" : "bg-[var(--mist)]"
                }`}
                onClick={() => setLang(code)}
              >
                {code}
              </button>
            ))}
          </div>
        </div>

        <div
          className={`space-y-4 rounded-2xl bg-[var(--sand)] p-4 ${isRtl(lang) ? "text-right" : ""}`}
          dir={isRtl(lang) ? "rtl" : "ltr"}
        >
          {isStubLang(lang) && labels.stubBanner && (
            <p className="rounded-md bg-amber-50 px-2 py-1 text-[11px] text-amber-900">
              {labels.stubBanner}
            </p>
          )}

          <h2 className="text-xl">{labels.title}</h2>

          <div>
            <p className="text-xs font-semibold uppercase tracking-wide opacity-60">
              {labels.whyHeading}
            </p>
            <p className="mt-1 whitespace-pre-line text-sm">{preview}</p>
          </div>

          {engine && (
            <>
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide opacity-60">
                  {labels.dataUsed}
                </p>
                <ul className="mt-1 list-disc ps-4 text-sm">
                  {engine.data_sources_used.map((s) => (
                    <li key={s}>{s}</li>
                  ))}
                </ul>
              </div>
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide opacity-60">
                  {labels.dataNot}
                </p>
                <ul className="mt-1 list-disc ps-4 text-sm">
                  {engine.data_sources_not_used.map((s) => (
                    <li key={s}>{s}</li>
                  ))}
                </ul>
              </div>
              {engine.household_bundle_hint && !optOut && (
                <p className="rounded-md bg-white/70 px-3 py-2 text-sm">
                  {engine.household_bundle_hint}
                </p>
              )}
            </>
          )}

          <div>
            <p className="text-xs font-semibold uppercase tracking-wide opacity-60">
              {labels.choices}
            </p>
            <div className="mt-2 grid gap-2">
              {(Object.keys(labels.modality) as Modality[]).map((key) => (
                <button
                  key={key}
                  type="button"
                  onClick={() => setModality(key)}
                  className={`rounded-md px-3 py-2 text-sm ${
                    isRtl(lang) ? "text-right" : "text-left"
                  } ${
                    modality === key
                      ? "bg-[var(--teal)] text-white"
                      : "bg-white border border-[var(--mist)]"
                  }`}
                >
                  {labels.modality[key]}
                </button>
              ))}
            </div>
          </div>

          <label className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={optOut}
              onChange={(e) => setOptOut(e.target.checked)}
            />
            {labels.optOut}
          </label>
          <p className="text-[11px] opacity-60">{labels.standardCare}</p>
        </div>
      </div>
    </div>
  );
}
