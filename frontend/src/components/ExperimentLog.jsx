const STATUS_STYLES = {
  FINISHED: "bg-green-900 text-green-300",
  RUNNING: "bg-blue-900 text-blue-300",
  FAILED: "bg-red-900 text-red-300",
  KILLED: "bg-yellow-900 text-yellow-300",
};

function formatDuration(seconds) {
  if (seconds == null) return "—";
  const m = Math.floor(seconds / 60);
  const s = Math.round(seconds % 60);
  return m > 0 ? `${m}m ${s}s` : `${s}s`;
}

export default function ExperimentLog({ runs, loading, error }) {
  if (loading) {
    return <p className="text-gray-500 text-sm animate-pulse">Loading experiments...</p>;
  }

  if (error) {
    return <p className="text-red-400 text-sm">{error}</p>;
  }

  if (!runs || runs.length === 0) {
    return (
      <p className="text-gray-500 text-sm py-8 text-center">
        No experiment runs yet. Trigger the pipeline to create the first run.
      </p>
    );
  }

  return (
    <div className="overflow-x-auto rounded-xl border border-gray-700">
      <table className="w-full text-sm text-gray-300">
        <thead className="bg-gray-800 text-gray-400 text-xs uppercase tracking-wide">
          <tr>
            {["Time", "Articles", "Signals", "Avg Confidence", "Duration", "Model", "Status"].map((h) => (
              <th key={h} className="px-4 py-3 text-left font-semibold whitespace-nowrap">
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-800">
          {runs.map((run) => {
            const statusClass = STATUS_STYLES[run.status] ?? "bg-gray-700 text-gray-300";
            return (
              <tr key={run.run_id} className="hover:bg-gray-800/50 transition-colors">
                <td className="px-4 py-3 whitespace-nowrap text-gray-400 text-xs">
                  {run.start_time ? new Date(run.start_time).toLocaleString() : "—"}
                </td>
                <td className="px-4 py-3">{run.article_count ?? "—"}</td>
                <td className="px-4 py-3">{run.signal_count ?? "—"}</td>
                <td className="px-4 py-3">
                  {run.avg_confidence != null
                    ? `${Math.round(run.avg_confidence * 100)}%`
                    : "—"}
                </td>
                <td className="px-4 py-3">{formatDuration(run.duration_seconds)}</td>
                <td className="px-4 py-3 text-xs text-gray-500 truncate max-w-[140px]">
                  {run.model_name ?? "—"}
                </td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${statusClass}`}>
                    {run.status}
                  </span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
