import { useEffect, useState } from "react";
import { getPipelineStatus, triggerPipeline } from "../api/client";

export default function PipelineControls({ onPipelineComplete }) {
  const [running, setRunning] = useState(false);
  const [toast, setToast] = useState(null);
  const [status, setStatus] = useState(null);

  useEffect(() => {
    getPipelineStatus()
      .then(setStatus)
      .catch(() => {});
  }, []);

  async function handleRun() {
    setRunning(true);
    setToast(null);
    try {
      const result = await triggerPipeline();
      setToast({
        type: "success",
        message: `${result.article_count} articles processed — ${result.signal_count} signals found`,
      });
      const updated = await getPipelineStatus();
      setStatus(updated);
      onPipelineComplete?.();
    } catch (err) {
      setToast({ type: "error", message: "Pipeline failed. Check the backend logs." });
    } finally {
      setRunning(false);
      setTimeout(() => setToast(null), 6000);
    }
  }

  return (
    <div className="flex flex-col items-end gap-2">
      <button
        onClick={handleRun}
        disabled={running}
        className="flex items-center gap-2 bg-orange-500 hover:bg-orange-600 disabled:bg-orange-800 disabled:cursor-not-allowed text-white font-semibold px-5 py-2 rounded-lg transition-colors text-sm"
      >
        {running && (
          <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
          </svg>
        )}
        {running ? "Running..." : "Run Pipeline"}
      </button>

      {toast && (
        <div
          className={`text-xs px-3 py-1.5 rounded-lg ${
            toast.type === "success"
              ? "bg-green-900 text-green-300"
              : "bg-red-900 text-red-300"
          }`}
        >
          {toast.message}
        </div>
      )}

      {status?.last_run_at && (
        <p className="text-xs text-gray-500">
          Last run:{" "}
          <span className={status.last_run_status === "completed" ? "text-green-400" : "text-red-400"}>
            {status.last_run_status}
          </span>{" "}
          · {new Date(status.last_run_at).toLocaleString()}
        </p>
      )}
    </div>
  );
}
