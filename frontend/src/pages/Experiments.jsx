import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getExperiments } from "../api/client";
import ExperimentLog from "../components/ExperimentLog";

export default function Experiments() {
  const [runs, setRuns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getExperiments()
      .then(setRuns)
      .catch((err) => setError(err.message ?? "Failed to load experiments"))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white">
      <div className="max-w-7xl mx-auto px-4 py-8 flex flex-col gap-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold">Experiment Runs</h1>
          <Link
            to="/"
            className="text-sm text-orange-400 hover:text-orange-300 transition-colors"
          >
            ← Back to Dashboard
          </Link>
        </div>
        <ExperimentLog runs={runs} loading={loading} error={error} />
      </div>
    </div>
  );
}
