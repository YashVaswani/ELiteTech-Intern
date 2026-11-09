interface Props {
  tabs: string[];
  active: string;
  onChange: (tab: string) => void;
}

export default function Tabs({ tabs, active, onChange }: Props) {
  return (
    <div className="flex gap-1 border-b border-slate-800">
      {tabs.map((tab) => (
        <button
          key={tab}
          type="button"
          onClick={() => onChange(tab)}
          className={`px-4 py-2.5 text-sm font-medium transition-colors ${
            tab === active
              ? "border-b-2 border-indigo-500 text-slate-50"
              : "border-b-2 border-transparent text-slate-400 hover:text-slate-200"
          }`}
        >
          {tab}
        </button>
      ))}
    </div>
  );
}
