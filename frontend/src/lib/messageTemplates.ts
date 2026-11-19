/** Deterministic citizen outreach copy. EN/AR full; UR/TL are stubs. */

export type Lang = "en" | "ar" | "ur" | "tl";
export type Modality = "clinic" | "tele" | "home";

export const SUPPORTED_LANGS: Lang[] = ["en", "ar", "ur", "tl"];

const STUB_LANGS: ReadonlySet<Lang> = new Set(["ur", "tl"]);

export function isStubLang(lang: Lang): boolean {
  return STUB_LANGS.has(lang);
}

export function isRtl(lang: Lang): boolean {
  return lang === "ar" || lang === "ur";
}

type Labels = {
  title: string;
  whyHeading: string;
  dataUsed: string;
  dataNot: string;
  choices: string;
  optOut: string;
  standardCare: string;
  selectPatient: string;
  greeting: string;
  nextStep: string;
  stubBanner: string;
  modality: Record<Modality, string>;
};

const LABELS: Record<Lang, Labels> = {
  en: {
    title: "Transparency & Choice Ledger",
    whyHeading: "Why you are receiving this",
    dataUsed: "Data used",
    dataNot: "Not accessed",
    choices: "Your meaningful choices",
    optOut: "Manage predictive outreach preferences (opt out)",
    standardCare:
      "Opting out of predictive outreach does not affect standard guideline care.",
    selectPatient: "Select a patient on the Clinician screen first.",
    greeting: "Hello",
    nextStep: "Please choose how you would like to attend.",
    stubBanner: "",
    modality: {
      clinic: "Book Primary Care Clinic",
      tele: "Start with Tele-Consultation",
      home: "Request Home Nurse Visit",
    },
  },
  ar: {
    title: "سجل الشفافية والاختيار",
    whyHeading: "لماذا تصلك هذه الرسالة",
    dataUsed: "البيانات المستخدمة",
    dataNot: "لم يتم الوصول إليها",
    choices: "خياراتك",
    optOut: "إدارة تفضيلات التواصل التنبؤي (إلغاء الاشتراك)",
    standardCare:
      "إلغاء الاشتراك في التواصل التنبؤي لا يؤثر على الرعاية وفق الإرشادات القياسية.",
    selectPatient: "يرجى اختيار مريض من شاشة الطبيب أولاً.",
    greeting: "مرحباً",
    nextStep: "يرجى اختيار طريقة الحضور المناسبة لكم.",
    stubBanner: "",
    modality: {
      clinic: "حجز عيادة الرعاية الأولية",
      tele: "بدء استشارة عن بُعد",
      home: "طلب زيارة منزلية",
    },
  },
  ur: {
    title: "شفافیت اور انتخاب کا ریکارڈ (stub)",
    whyHeading: "آپ کو یہ پیغام کیوں مل رہا ہے",
    dataUsed: "استعمال شدہ ڈیٹا",
    dataNot: "غیر استعمال شدہ",
    choices: "آپ کے اختیارات",
    optOut: "پیش گوئی پر مبنی رابطے کی ترجیحات (اختیار ختم)",
    standardCare:
      "پیش گوئی پر مبنی رابطے سے انکار معیاری رہنما اصول کی دیکھ بھال کو متاثر نہیں کرتا۔",
    selectPatient: "پہلے کلینیشن اسکرین سے مریض منتخب کریں۔",
    greeting: "السلام علیکم",
    nextStep: "براہ کرم حاضری کا طریقہ منتخب کریں۔",
    stubBanner: "Urdu copy is a prototype stub — not production translation.",
    modality: {
      clinic: "پرائمری کیئر کلینک بک کریں",
      tele: "ٹیلی مشاورت سے شروع کریں",
      home: "گھر پر نرس وزٹ کی درخواست",
    },
  },
  tl: {
    title: "Transparency & Choice Ledger (stub)",
    whyHeading: "Bakit natatanggap mo ito",
    dataUsed: "Data na ginamit",
    dataNot: "Hindi na-access",
    choices: "Iyong mga pagpipilian",
    optOut: "I-manage ang predictive outreach (opt out)",
    standardCare:
      "Ang pag-opt out sa predictive outreach ay hindi nakakaapekto sa standard guideline care.",
    selectPatient: "Pumili muna ng pasyente sa Clinician screen.",
    greeting: "Kumusta",
    nextStep: "Piliin kung paano mo gustong dumalo.",
    stubBanner: "Tagalog copy is a prototype stub — not production translation.",
    modality: {
      clinic: "Mag-book ng Primary Care Clinic",
      tele: "Magsimula sa Tele-Consultation",
      home: "Humiling ng Home Nurse Visit",
    },
  },
};

export function getLabels(lang: Lang): Labels {
  return LABELS[lang];
}

/** Plain-language invitation; never invents diagnoses. */
export function buildWhyMessage(
  lang: Lang,
  name: string,
  pathwayRecommendation: string | null | undefined,
): string {
  const labels = getLabels(lang);
  if (!pathwayRecommendation) return labels.selectPatient;

  if (lang === "ar") {
    return (
      `${labels.greeting} — تصلك هذه الرسالة لأن ${name} قد أُعطي أولوية للمسار الوقائي التالي: ` +
      `${pathwayRecommendation}. هذه أولوية تواصل سكاني وليست تشخيصاً طبياً.`
    );
  }
  if (lang === "ur") {
    return (
      `${labels.greeting} — ${name} کو درج ذیل احتیاطی راستے کی ترجیح دی گئی ہے: ` +
      `${pathwayRecommendation}. یہ آبادیاتی ترجیح ہے، طبی تشخیص نہیں۔`
    );
  }
  if (lang === "tl") {
    return (
      `${labels.greeting} — Natanggap mo ito dahil si ${name} ay na-prioritize para sa: ` +
      `${pathwayRecommendation}. Ito ay population outreach prioritization, hindi diagnosis.`
    );
  }
  return (
    `${labels.greeting} — You are receiving this because ${name} has been prioritized for: ` +
    `${pathwayRecommendation}. This is population outreach prioritization, not a clinical diagnosis. ` +
    `${labels.nextStep}`
  );
}

export function buildMessagePreview(
  lang: Lang,
  name: string,
  pathwayRecommendation: string | null | undefined,
): string {
  const labels = getLabels(lang);
  const why = buildWhyMessage(lang, name, pathwayRecommendation);
  return `${why}\n\n${labels.nextStep}`;
}
