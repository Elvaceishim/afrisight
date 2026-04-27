import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8888",
});

export async function getSignals(filters = {}) {
  const params = {};
  if (filters.market && filters.market !== "all") params.market = filters.market;
  if (filters.category && filters.category !== "all") params.category = filters.category;
  if (filters.sentiment) params.sentiment = filters.sentiment;
  if (filters.limit) params.limit = filters.limit;
  const res = await api.get("/signals", { params });
  return res.data;
}

export async function triggerPipeline() {
  const res = await api.post("/pipeline/run");
  return res.data;
}

export async function getPipelineStatus() {
  const res = await api.get("/pipeline/status");
  return res.data;
}

export async function getExperiments() {
  const res = await api.get("/experiments");
  return res.data;
}
