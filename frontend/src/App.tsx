import { NavLink, Route, Routes } from "react-router";
import CitizenSimulator from "./pages/CitizenSimulator";
import ClinicianPortal from "./pages/ClinicianPortal";
import FairnessDashboard from "./pages/FairnessDashboard";

const linkClass = ({ isActive }: { isActive: boolean }) =>
  `px-3 py-2 text-sm tracking-wide ${
    isActive ? "text-[var(--teal-deep)] border-b-2 border-[var(--teal)]" : "text-[var(--ink)]/70"
  }`;

export default function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b border-[var(--mist)] bg-[var(--card)]/80 backdrop-blur">
        <div className="mx-auto max-w-6xl px-4 py-4 flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="brand text-3xl text-[var(--teal-deep)]">Hayah-Pulse</p>
            <p className="text-sm text-[var(--ink)]/70">
              Glass-Box Life-Course Preventive Intelligence
            </p>
          </div>
          <nav className="flex gap-2">
            <NavLink to="/clinician" className={linkClass}>
              Clinician
            </NavLink>
            <NavLink to="/citizen" className={linkClass}>
              Citizen
            </NavLink>
            <NavLink to="/fairness" className={linkClass}>
              Fairness
            </NavLink>
          </nav>
        </div>
      </header>

      <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-8">
        <Routes>
          <Route path="/" element={<ClinicianPortal />} />
          <Route path="/clinician" element={<ClinicianPortal />} />
          <Route path="/citizen" element={<CitizenSimulator />} />
          <Route path="/fairness" element={<FairnessDashboard />} />
        </Routes>
      </main>

      <footer className="border-t border-[var(--mist)] py-3 text-center text-xs text-[var(--ink)]/60">
        Synthetic demo data — not real patients
      </footer>
    </div>
  );
}
