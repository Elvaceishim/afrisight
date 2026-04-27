const MARKET_FLAGS = {
  ng: "🇳🇬",
  ke: "🇰🇪",
  tz: "🇹🇿",
  cd: "🇨🇩",
  et: "🇪🇹",
  "pan-african": "🌍",
  unknown: "🌍",
};

const CATEGORY_COLORS = {
  regulatory: "bg-purple-900 text-purple-200",
  funding: "bg-green-900 text-green-200",
  product_launch: "bg-blue-900 text-blue-200",
  macro_risk: "bg-red-900 text-red-200",
  payments: "bg-yellow-900 text-yellow-200",
  other: "bg-gray-700 text-gray-300",
};

const SENTIMENT_COLORS = {
  positive: "bg-green-500",
  negative: "bg-red-500",
  neutral: "bg-gray-400",
};

export default function SignalCard({ signal }) {
  const flag = MARKET_FLAGS[signal.market] ?? "🌍";
  const catClass = CATEGORY_COLORS[signal.category] ?? CATEGORY_COLORS.other;
  const sentColor = SENTIMENT_COLORS[signal.sentiment] ?? SENTIMENT_COLORS.neutral;
  const confidence = Math.round((signal.confidence_score ?? 0) * 100);

  return (
    <div className="bg-gray-900 border border-gray-700 rounded-xl p-5 flex flex-col gap-3 hover:border-gray-500 transition-colors">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-xl">{flag}</span>
          <span className={`text-xs font-semibold px-2 py-0.5 rounded-full uppercase tracking-wide ${catClass}`}>
            {signal.category.replace("_", " ")}
          </span>
          <span className="flex items-center gap-1 text-xs text-gray-400">
            <span className={`inline-block w-2 h-2 rounded-full ${sentColor}`} />
            {signal.sentiment}
          </span>
        </div>
        <span className="text-xs text-gray-500 whitespace-nowrap">
          {signal.market.toUpperCase()}
        </span>
      </div>

      <h3 className="text-sm font-semibold text-white leading-snug line-clamp-2">{signal.title}</h3>
      <p className="text-sm text-gray-400 leading-relaxed">{signal.summary}</p>

      <div className="flex flex-col gap-1 mt-1">
        <div className="flex justify-between text-xs text-gray-500">
          <span>Confidence</span>
          <span>{confidence}%</span>
        </div>
        <div className="w-full h-1 bg-gray-700 rounded-full overflow-hidden">
          <div
            className="h-full rounded-full bg-orange-500 transition-all"
            style={{ width: `${confidence}%` }}
          />
        </div>
      </div>

      {signal.source_url && (
        <a
          href={signal.source_url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-xs text-orange-400 hover:text-orange-300 truncate"
        >
          {signal.source_url}
        </a>
      )}
    </div>
  );
}
