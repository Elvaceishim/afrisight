import { useState } from "react";

const MARKETS = [
  { value: "all", label: "ALL" },
  { value: "ng", label: "🇳🇬 NG" },
  { value: "ke", label: "🇰🇪 KE" },
  { value: "tz", label: "🇹🇿 TZ" },
  { value: "cd", label: "🇨🇩 DRC" },
  { value: "et", label: "🇪🇹 ET" },
];

const CATEGORIES = [
  { value: "all", label: "All Categories" },
  { value: "regulatory", label: "Regulatory" },
  { value: "funding", label: "Funding" },
  { value: "product_launch", label: "Product Launch" },
  { value: "macro_risk", label: "Macro Risk" },
  { value: "payments", label: "Payments" },
  { value: "other", label: "Other" },
];

export default function MarketFilter({ onChange }) {
  const [market, setMarket] = useState("all");
  const [category, setCategory] = useState("all");

  function handleMarket(value) {
    setMarket(value);
    onChange?.({ market: value, category });
  }

  function handleCategory(e) {
    const value = e.target.value;
    setCategory(value);
    onChange?.({ market, category: value });
  }

  return (
    <div className="flex flex-wrap items-center gap-3">
      <div className="flex flex-wrap gap-1.5">
        {MARKETS.map((m) => (
          <button
            key={m.value}
            onClick={() => handleMarket(m.value)}
            className={`px-3 py-1 rounded-full text-xs font-semibold transition-colors ${
              market === m.value
                ? "bg-orange-500 text-white"
                : "bg-gray-800 text-gray-400 hover:bg-gray-700"
            }`}
          >
            {m.label}
          </button>
        ))}
      </div>

      <select
        value={category}
        onChange={handleCategory}
        className="bg-gray-800 text-gray-300 text-xs border border-gray-700 rounded-lg px-3 py-1.5 focus:outline-none focus:border-orange-500"
      >
        {CATEGORIES.map((c) => (
          <option key={c.value} value={c.value}>
            {c.label}
          </option>
        ))}
      </select>
    </div>
  );
}
