import { useEffect, useMemo, useState } from "react";
import { api, type ResidentDetail } from "../lib/api";
import { useSelection } from "../lib/selection";
import StatusBanner from "../components/StatusBanner";

type Lang = "en" | "ar";
type Modality = "clinic" | "tele" | "home";

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

  const copy = useMemo(() => {
    const name = String(detail?.resident.display_name ?? "your family member");
    const engine = detail?.engine;
    const whyEn = engine
      ? `You are receiving this because ${name} has been prioritized for: ${engine.pathway_recommendation}.`
      : "Select a patient on the Clinician screen first.";
    const whyAr = engine
      ? `تصلك هذه الرسالة لأن ${name} قد أُعطي أولوية لـ: ${engine.pathway_recommendation}.`
      : "يرجى اختيار مريض من شاشة الطبيب أولاً.";
    return {
      why: lang === "en" ? whyEn : whyAr,
      title: lang === "en" ? "Transparency & Choice Ledger" : "سجل الشفافية والاختيار",
      dataUsed: lang === "en" ? "Data used" : "البيانات المستخدمة",
      dataNot: lang === "en" ? "Not accessed" : "لم يتم الوصول إليها",
      choices: lang === "en" ? "Your meaningful choices" : "خياراتك",
    };
  }, [detail, lang]);

  const engine = detail?.engine;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl text-[var(--teal-deep)]">Citizen Mobile Simulator</h1>
        <p className="mt-1 text-[var(--ink)]/70">
          WhatsApp / portal style preview with bilingual transparency.
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
        <div className="mb-3 flex items-center justify-between">
          <p className="text-xs uppercase tracking-widest text-[var(--ink)]/50">Hayah-Pulse</p>
          <div className="flex gap-1">
            <button
              type="button"
              className={`rounded px-2 py-1 text-xs ${lang === "en" ? "bg-[var(--teal)] text-white" : "bg-[var(--mist)]"}`}
              onClick={() => setLang("en")}
            >
              EN
            </button>
            <button
              type="button"
              className={`rounded px-2 py-1 text-xs ${lang === "ar" ? "bg-[var(--teal)] text-white" : "bg-[var(--mist)]"}`}
              onClick={() => setLang("ar")}
            >
              AR
            </button>
          </div>
        </div>

        <div className={`space-y-4 rounded-2xl bg-[var(--sand)] p-4 ${lang === "ar" ? "text-right" : ""}`} dir={lang === "ar" ? "rtl" : "ltr"}>
          <h2 className="text-xl">{copy.title}</h2>
          <div>
            <p className="text-xs font-semibold uppercase tracking-wide opacity-60">
              {lang === "en" ? "Why you are receiving this" : "لماذا تصلك هذه الرسالة"}
            </p>
            <p className="mt-1 text-sm">{copy.why}</p>
          </div>

          {engine && (
            <>
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide opacity-60">
                  {copy.dataUsed}
                </p>
                <ul className="mt-1 list-disc ps-4 text-sm">
                  {engine.data_sources_used.map((s) => (
                    <li key={s}>{s}</li>
                  ))}
                </ul>
              </div>
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide opacity-60">
                  {copy.dataNot}
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
              {copy.choices}
            </p>
            <div className="mt-2 grid gap-2">
              {(
                [
                  ["clinic", lang === "en" ? "Book Primary Care Clinic" : "حجز عيادة الرعاية الأولية"],
                  ["tele", lang === "en" ? "Start with Tele-Consultation" : "بدء استشارة عن بُعد"],
                  ["home", lang === "en" ? "Request Home Nurse Visit" : "طلب زيارة منزلية"],
                ] as const
              ).map(([key, label]) => (
                <button
                  key={key}
                  type="button"
                  onClick={() => setModality(key)}
                  className={`rounded-md px-3 py-2 text-sm text-left ${
                    modality === key
                      ? "bg-[var(--teal)] text-white"
                      : "bg-white border border-[var(--mist)]"
                  }`}
                >
                  {label}
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
            {lang === "en"
              ? "Manage predictive outreach preferences (opt out)"
              : "إدارة تفضيلات التواصل التنبؤي (إلغاء الاشتراك)"}
          </label>
          <p className="text-[11px] opacity-60">
            {lang === "en"
              ? "Opting out of predictive outreach does not affect standard guideline care."
              : "إلغاء الاشتراك في التواصل التنبؤي لا يؤثر على الرعاية وفق الإرشادات القياسية."}
          </p>
        </div>
      </div>
    </div>
  );
}
