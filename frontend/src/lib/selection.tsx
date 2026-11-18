import {
  createContext,
  useContext,
  useMemo,
  useState,
  type Dispatch,
  type ReactNode,
  type SetStateAction,
} from "react";

interface SelectionState {
  residentId: string | null;
  setResidentId: Dispatch<SetStateAction<string | null>>;
}

const SelectionContext = createContext<SelectionState | null>(null);

export function SelectionProvider({ children }: { children: ReactNode }) {
  const [residentId, setResidentId] = useState<string | null>(null);
  const value = useMemo(() => ({ residentId, setResidentId }), [residentId]);
  return (
    <SelectionContext.Provider value={value}>{children}</SelectionContext.Provider>
  );
}

export function useSelection() {
  const ctx = useContext(SelectionContext);
  if (!ctx) throw new Error("useSelection requires SelectionProvider");
  return ctx;
}
