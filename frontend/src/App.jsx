import { useEffect, useState } from "react";
import { getHistory, uploadCSV, login, logout, downloadReport } from "./api";
import "./App.css";
import { Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  ArcElement,
  Tooltip,
  Legend
);

function numOrDash(x) {
  if (x === null || x === undefined) return "-";
  if (Number.isFinite(x)) return Math.round(x * 100) / 100;
  return x;
}

function isLoggedIn() {
  return !!localStorage.getItem("access_token");
}

export default function App() {
  const [authed, setAuthed] = useState(isLoggedIn());
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [history, setHistory] = useState([]);
  const [err, setErr] = useState("");
  const [msg, setMsg] = useState("");
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  async function loadHistory() {
    try {
      setErr("");
      const data = await getHistory();
      setHistory(data);
    } catch {
      setErr("Unauthorized or failed to load history");
    }
  }

  async function handleDownloadReport() {
    try {
      setErr("");
      const blob = await downloadReport();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "report.pdf";
      a.click();
      window.URL.revokeObjectURL(url);
    } catch {
      setErr("Report download failed");
    }
  }

  useEffect(() => {
    if (authed) loadHistory();
  }, [authed]);

  async function handleLogin() {
    if (!username || !password) {
      setErr("Enter username & password");
      return;
    }
    try {
      setErr("");
      await login(username, password);
      setAuthed(true);
      setMsg("Logged in ✓");
    } catch {
      setErr("Login failed");
    }
  }

  function handleLogout() {
    logout();
    setAuthed(false);
    setHistory([]);
    setMsg("");
    setErr("");
  }

  async function handleUpload() {
    if (!file) {
      setErr("Please select a CSV file");
      return;
    }
    try {
      setUploading(true);
      setErr("");
      setMsg("");
      await uploadCSV(file);
      setMsg("File uploaded successfully ✓");
      setFile(null);
      document.getElementById("fileInput").value = "";
      await loadHistory();
    } catch {
      setErr("Upload failed");
    } finally {
      setUploading(false);
    }
  }

  const latest = history[0];

  // Enhanced color palette for pie chart
  const pieColors = [
    '#6366f1', // Indigo
    '#8b5cf6', // Purple
    '#ec4899', // Pink
    '#f59e0b', // Amber
    '#10b981', // Emerald
    '#3b82f6', // Blue
    '#f43f5e', // Rose
    '#14b8a6', // Teal
  ];

  if (!authed) {
    return (
      <div className="container" style={{ maxWidth: 400, margin: "auto", display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ width: '100%' }}>
          <h1 className="title" style={{ textAlign: 'center', marginBottom: 32 }}>Login</h1>
          {err && <div className="alert error">{err}</div>}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            <input 
              className="inputFile" 
              placeholder="Username" 
              value={username} 
              onChange={e => setUsername(e.target.value)} 
            />
            <input 
              className="inputFile" 
              type="password" 
              placeholder="Password" 
              value={password} 
              onChange={e => setPassword(e.target.value)}
              onKeyPress={e => e.key === 'Enter' && handleLogin()}
            />
            <button className="btn" onClick={handleLogin}>Login</button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container">

      <div className="header">
        <h1 className="title">ChemInSight</h1>
        <div className="actions">
          <input 
            id="fileInput" 
            className="inputFile" 
            type="file" 
            accept=".csv" 
            onChange={e => setFile(e.target.files[0])} 
          />
          <div className="uploadBtnContainer">
            <button className="btn uploadBtn" onClick={handleUpload} disabled={uploading}>
              {uploading ? "Uploading..." : "Upload CSV"}
            </button>
          </div>
        </div>
      </div>

      {err && <div className="alert error">{err}</div>}
      {msg && <div className="alert success">{msg}</div>}

      <div className="dashboardGrid">

        <div className="card">
          <h3>Equipment Overview</h3>
          <div className="kpis">
            <div className="kpi">
              <div className="kpiLabel">Total</div>
              <div className="kpiValue">{numOrDash(latest?.summary?.total_equipment)}</div>
            </div>
            <div className="kpi">
              <div className="kpiLabel">Flow Rate</div>
              <div className="kpiValue">{numOrDash(latest?.summary?.avg_flowrate)}</div>
            </div>
            <div className="kpi">
              <div className="kpiLabel">Pressure</div>
              <div className="kpiValue">{numOrDash(latest?.summary?.avg_pressure)}</div>
            </div>
            <div className="kpi">
              <div className="kpiLabel">Temperature</div>
              <div className="kpiValue">{numOrDash(latest?.summary?.avg_temperature)}</div>
            </div>
          </div>
          <div className="cardFooter">
            <button className="btn downloadBtn" onClick={handleDownloadReport} disabled={uploading}>
              Download Report
            </button>
          </div>
        </div>

        <div className="card pieCard">
          <Pie
            data={{
              labels: Object.keys(latest?.summary?.type_distribution || {}),
              datasets: [{
                data: Object.values(latest?.summary?.type_distribution || {}),
                backgroundColor: pieColors,
                borderColor: '#1e293b',
                borderWidth: 3,
                hoverOffset: 15,
                hoverBorderColor: '#fff',
                hoverBorderWidth: 3
              }]
            }}
            options={{
              maintainAspectRatio: true,
              responsive: true,
              plugins: {
                legend: { 
                  position: 'bottom',
                  labels: {
                    color: '#f8fafc',
                    font: {
                      size: 13,
                      weight: 600,
                      family: 'Inter'
                    },
                    padding: 15,
                    usePointStyle: true,
                    pointStyle: 'circle'
                  }
                },
                tooltip: {
                  backgroundColor: 'rgba(15, 23, 42, 0.95)',
                  titleColor: '#f8fafc',
                  bodyColor: '#cbd5e1',
                  borderColor: '#3b82f6',
                  borderWidth: 1,
                  padding: 12,
                  displayColors: true,
                  callbacks: {
                    label: function(context) {
                      const label = context.label || '';
                      const value = context.parsed || 0;
                      const total = context.dataset.data.reduce((a, b) => a + b, 0);
                      const percentage = ((value / total) * 100).toFixed(1);
                      return `${label}: ${value} (${percentage}%)`;
                    }
                  }
                }
              },
              animation: {
                animateRotate: true,
                animateScale: true,
                duration: 1500,
                easing: 'easeInOutQuart'
              }
            }}
          />
        </div>

        <div className="card">
          <h3>Upload History</h3>
          <div className="list">
            {history.length === 0 ? (
              <div style={{ textAlign: 'center', color: 'var(--muted)', padding: '40px 20px' }}>
                No uploads yet
              </div>
            ) : (
              history.map(item => (
                <div className="item" key={item.id}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <b style={{ color: 'var(--primary)' }}>{item.filename}</b>
                    <span style={{ fontSize: 12, color: 'var(--muted)' }}>{item.uploaded_at}</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        <div className="card">
          <h3>System Status</h3>
          <div className="statusGrid">
            <div className="statusItem">
              <div className="statusDot" style={{ background: '#10b981', color: '#10b981' }}></div>
              <div>
                <div className="statusLabel">Active Equipment</div>
                <div className="statusValue">{numOrDash(latest?.summary?.total_equipment)}</div>
              </div>
            </div>
            <div className="statusItem">
              <div className="statusDot" style={{ background: '#f59e0b', color: '#f59e0b' }}></div>
              <div>
                <div className="statusLabel">Data Points</div>
                <div className="statusValue">{history.length}</div>
              </div>
            </div>
            <div className="statusItem">
              <div className="statusDot" style={{ background: '#3b82f6', color: '#3b82f6' }}></div>
              <div>
                <div className="statusLabel">Last Upload</div>
                <div className="statusValue">{latest ? 'Today' : 'None'}</div>
              </div>
            </div>
          </div>
        </div>

      </div>

      <div className="logoutContainer">
        <button className="logout-btn" onClick={handleLogout}>Logout</button>
      </div>
    </div>
  );
}