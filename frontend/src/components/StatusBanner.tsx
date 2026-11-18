export default function StatusBanner({
  title,
  body,
}: {
  title: string;
  body: string;
}) {
  return (
    <div className="rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-950">
      <p className="font-semibold">{title}</p>
      <p className="mt-1 opacity-90">{body}</p>
    </div>
  );
}
