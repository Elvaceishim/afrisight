import { useCallback, useEffect, useState } from "react";
import { getSignals } from "../api/client";
import MarketFilter from "../components/MarketFilter";
import PipelineControls from "../components/PipelineControls";
import SignalFeed from "../components/SignalFeed";

export default function Dashboard() {
  const [signals, setSignals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({ market: "all", category: "all" });

  const fetchSignals = useCallback(async (activeFilters) => {
    setLoading(true);
    setError(null);
    try {
      const data = await getSignals(activeFilters ?? filters);
      setSignals(data);
    } catch (err) {
      setError(err.message ?? "Unknown error");
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchSignals(filters);
  }, []);

  function handleFilterChange(newFilters) {
    setFilters(newFilters);
    fetchSignals(newFilters);
  }

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white">
      <div className="max-w-7xl mx-auto px-4 py-8 flex flex-col gap-6">
        <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold text-white">AfriSight</h1>
            <p className="text-gray-400 mt-1 text-sm">African fintech intelligence, powered by AI</p>
          </div>
          <PipelineControls onPipelineComplete={() => fetchSignals(filters)} />
        </div>

        <MarketFilter onChange={handleFilterChange} />
        <SignalFeed signals={signals} loading={loading} error={error} />
      </div>
    </div>
  );
}
