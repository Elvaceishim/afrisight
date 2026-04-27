import { Link, Route, Routes } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Experiments from "./pages/Experiments";

export default function App() {
  return (
    <div>
      <nav className="border-b border-gray-800 bg-[#0a0a0a]">
        <div className="max-w-7xl mx-auto px-4 py-3 flex gap-6">
          <Link
            to="/"
            className="text-sm font-semibold text-gray-300 hover:text-white transition-colors"
          >
            Dashboard
          </Link>
          <Link
            to="/experiments"
            className="text-sm font-semibold text-gray-300 hover:text-white transition-colors"
          >
            Experiments
          </Link>
        </div>
      </nav>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/experiments" element={<Experiments />} />
      </Routes>
    </div>
  );
}
