import SignalCard from "./SignalCard";

function SkeletonCard() {
  return (
    <div className="bg-gray-900 border border-gray-700 rounded-xl p-5 animate-pulse flex flex-col gap-3">
      <div className="flex gap-2">
        <div className="w-6 h-6 bg-gray-700 rounded" />
        <div className="w-20 h-5 bg-gray-700 rounded-full" />
        <div className="w-14 h-5 bg-gray-700 rounded-full" />
      </div>
      <div className="w-3/4 h-4 bg-gray-700 rounded" />
      <div className="w-full h-3 bg-gray-700 rounded" />
      <div className="w-5/6 h-3 bg-gray-700 rounded" />
      <div className="w-full h-1 bg-gray-700 rounded-full" />
    </div>
  );
}

export default function SignalFeed({ signals, loading, error }) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {Array.from({ length: 6 }).map((_, i) => (
          <SkeletonCard key={i} />
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-16 text-red-400">
        <p className="text-lg font-medium">Failed to load signals</p>
        <p className="text-sm mt-1 text-gray-500">{error}</p>
      </div>
    );
  }

  if (!signals || signals.length === 0) {
    return (
      <div className="text-center py-16 text-gray-500">
        <p className="text-lg">No signals yet.</p>
        <p className="text-sm mt-1">Run the pipeline to start ingesting African fintech news.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
      {signals.map((signal) => (
        <SignalCard key={signal.id} signal={signal} />
      ))}
    </div>
  );
}
