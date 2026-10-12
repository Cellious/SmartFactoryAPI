import { useCallback, useEffect, useState } from "react";
import {
  Activity,
  AlertCircle,
  Boxes,
  BrainCircuit,
  CheckCircle2,
  ClipboardList,
  Factory,
  LayoutDashboard,
  LogOut,
  Package,
  RefreshCw,
  ShieldCheck,
  ScrollText,
  Radio,
  Truck,
  Wrench,
} from "lucide-react";
import "./App.css";

const TOKEN_KEY = "smartfactory_access_token";

const menuItems = [
  { label: "Dashboard", icon: LayoutDashboard },
  { label: "Üretim", icon: Activity },
  { label: "Makineler", icon: Wrench },
  { label: "Stok Yönetimi", icon: Boxes },
  { label: "Siparişler", icon: ClipboardList },
  { label: "Sevkiyat", icon: Truck },
  { label: "AI Üretim Analizi", icon: BrainCircuit },
];

type User = {
  id: number;
  username: string;
  full_name: string;
  role: string;
  active: boolean;
};

type AIAnalysis = {
  model: string;
  statistics: {
    total_production: number;
    total_scrap: number;
    scrap_rate: number;
  };
  machines: Array<{
    machine: string;
    machine_name: string;
    total_production: number;
    total_scrap: number;
    scrap_rate: number;
  }>;
  highest_scrap_machine: {
    machine: string;
    machine_name: string;
    total_production: number;
    total_scrap: number;
    scrap_rate: number;
  } | null;
  analysis: string;
};

type SystemLog = {
  id: string;
  timestamp: string;
  level: "INFO" | "WARNING" | "ERROR" | "SUCCESS";
  source: string;
  message: string;
  operation_id: string | null;
};

type DashboardSummary = {
  total_products: number;
  low_stock_products: number;
  total_stock_value: number;
  total_production: number;
  total_scrap: number;
  overall_scrap_rate: number;
  total_machines: number;
  active_machines: number;
  running_machines: number;
  maintenance_machines: number;
  total_orders: number;
  pending_orders: number;
  producing_orders: number;
  ready_orders: number;
  shipped_orders: number;
  completed_orders: number;
};

async function apiRequest<T>(
  path: string,
  token?: string,
  options: RequestInit = {},
): Promise<T> {
  const headers = new Headers(options.headers);
  headers.set("Accept", "application/json");

  if (options.body) {
    headers.set("Content-Type", "application/json");
  }

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(path, {
    ...options,
    headers,
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error(
        "Oturum doğrulanamadı. Lütfen yeniden giriş yapın.",
      );
    }

    let message = `API isteği başarısız oldu (${response.status}).`;

    try {
      const body = await response.json();
      if (typeof body.detail === "string") {
        message = body.detail;
      }
    } catch {
      // Yanıt JSON değilse genel hata mesajını kullan.
    }

    throw new Error(message);
  }

  return response.json() as Promise<T>;
}

function formatNumber(value: number): string {
  return new Intl.NumberFormat("tr-TR", {
    maximumFractionDigits: 2,
  }).format(value);
}

function formatCurrency(value: number): string {
  return new Intl.NumberFormat("tr-TR", {
    style: "currency",
    currency: "TRY",
    maximumFractionDigits: 2,
  }).format(value);
}

function App() {
  const [token, setToken] = useState(
    () => localStorage.getItem(TOKEN_KEY) ?? "",
  );
  const [user, setUser] = useState<User | null>(null);
  const [dashboard, setDashboard] = useState<DashboardSummary | null>(null);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [loginLoading, setLoginLoading] = useState(false);
  const [error, setError] = useState("");
  const [aiAnalysis, setAiAnalysis] = useState<AIAnalysis | null>(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState("");
  const [activeSection, setActiveSection] = useState("Dashboard");
  const [logs, setLogs] = useState<SystemLog[]>([]);
  const [logsLoading, setLogsLoading] = useState(false);
  const [logsConnected, setLogsConnected] = useState(false);
  const [logsError, setLogsError] = useState("");
  const [logLevel, setLogLevel] = useState("ALL");

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY);
    setToken("");
    setUser(null);
    setDashboard(null);
    setPassword("");
    setError("");
  }, []);

  const loadDashboard = useCallback(async (accessToken: string) => {
    setLoading(true);
    setError("");

    try {
      const [currentUser, summary] = await Promise.all([
        apiRequest<User>("/api/auth/me", accessToken),
        apiRequest<DashboardSummary>(
          "/api/dashboard/summary",
          accessToken,
        ),
      ]);

      setUser(currentUser);
      setDashboard(summary);
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Beklenmeyen bir hata oluştu.";

      if (message.includes("Oturum doğrulanamadı")) {
        logout();
      } else {
        setError(message);
      }
    } finally {
      setLoading(false);
    }
  }, [logout]);

  async function handleAnalyzeProduction() {
    setAiLoading(true);
    setAiError("");

    try {
      const result = await apiRequest<AIAnalysis>(
        "/api/ai/production-analysis",
        token,
        { method: "POST" },
      );
      setAiAnalysis(result);
    } catch (err) {
      setAiError(
        err instanceof Error
          ? err.message
          : "AI analizi sirasinda beklenmeyen bir hata olustu.",
      );
    } finally {
      setAiLoading(false);
    }
  }

  useEffect(() => {
    if (token) {
      void loadDashboard(token);
    }
  }, [token, loadDashboard]);

  const refreshLogs = useCallback(async () => {
    if (!token || user?.role !== "ADMIN") return;

    setLogsLoading(true);
    setLogsError("");

    try {
      const result = await apiRequest<{ items: SystemLog[]; count: number }>(
        "/api/admin/logs?limit=100",
        token,
      );
      setLogs((current) => {
        const liveIds = new Set(current.map((item) => item.id));
        const merged = [...current.filter((item) => liveIds.has(item.id)), ...result.items];
        const unique = new Map<string, SystemLog>();
        for (const item of merged) unique.set(item.id, item);
        return [...unique.values()]
          .sort((a, b) => b.timestamp.localeCompare(a.timestamp))
          .slice(0, 500);
      });
    } catch (err) {
      setLogsError(err instanceof Error ? err.message : "Loglar yenilenemedi.");
    } finally {
      setLogsLoading(false);
    }
  }, [token, user?.role]);

  useEffect(() => {
    if (!token || user?.role !== "ADMIN" || activeSection !== "Sistem Logları") {
      setLogsConnected(false);
      return;
    }

    let cancelled = false;
    const controller = new AbortController();

    async function loadLogs() {
      await refreshLogs();

      try {
        const response = await fetch("/api/admin/logs/stream", {
          headers: { Accept: "text/event-stream", Authorization: `Bearer ${token}` },
          signal: controller.signal,
        });
        if (!response.ok || !response.body) {
          throw new Error(`Canlı log bağlantısı başarısız (${response.status}).`);
        }

        if (!cancelled) setLogsConnected(true);
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";

        while (!cancelled) {
          const { value, done } = await reader.read();
          if (done) break;
          buffer += decoder.decode(value, { stream: true });
          const events = buffer.split(/\r?\n\r?\n/);
          buffer = events.pop() ?? "";

          for (const event of events) {
            const dataLine = event.split(/\r?\n/).find((line) => line.startsWith("data:"));
            if (!dataLine) continue;
            try {
              const entry = JSON.parse(dataLine.slice(5).trim()) as SystemLog;
              if (!cancelled) {
                setLogs((current) => [entry, ...current.filter((item) => item.id !== entry.id)].slice(0, 500));
              }
            } catch {
              // Bozuk SSE mesajını atla; bağlantıyı sürdür.
            }
          }
        }
      } catch (err) {
        if (!cancelled && !controller.signal.aborted) {
          setLogsConnected(false);
          setLogsError(err instanceof Error ? err.message : "Canlı log bağlantısı kesildi.");
        }
      }
    }

    void loadLogs();
    return () => {
      cancelled = true;
      controller.abort();
    };
  }, [token, user?.role, activeSection, refreshLogs]);

  async function handleLogin(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoginLoading(true);
    setError("");

    try {
      const result = await apiRequest<{
        access_token: string;
        token_type: string;
      }>("/api/auth/login", undefined, {
        method: "POST",
        body: JSON.stringify({
          username: username.trim(),
          password,
        }),
      });

      localStorage.setItem(TOKEN_KEY, result.access_token);
      setToken(result.access_token);
      setPassword("");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Giriş sırasında bir hata oluştu.",
      );
    } finally {
      setLoginLoading(false);
    }
  }

  if (!token) {
    return (
      <main className="login-page">
        <section className="login-brand">
          <div className="login-logo"><Factory size={30} /></div>
          <span className="login-brand-name">SmartFactory</span>
          <span className="login-brand-caption">PRODUCTION MANAGEMENT</span>
          <h1>Üretiminizi tek merkezden yönetin.</h1>
          <p>Üretim, stok, makineler ve siparişler için merkezi yönetim paneli.</p>
          <div className="login-feature">
            <ShieldCheck size={19} />
            <span>JWT tabanlı kimlik doğrulama</span>
          </div>
        </section>

        <section className="login-form-section">
          <form className="login-card" onSubmit={handleLogin}>
            <div className="login-card-icon"><Factory size={23} /></div>
            <p className="eyebrow">YÖNETİM PANELİ</p>
            <h2>Hoş geldiniz</h2>
            <p className="login-description">
              Devam etmek için hesabınızla giriş yapın.
            </p>

            {error && (
              <div className="error-message" role="alert">
                <AlertCircle size={17} />
                <span>{error}</span>
              </div>
            )}

            <label htmlFor="username">Kullanıcı adı</label>
            <input
              id="username"
              name="username"
              autoComplete="username"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              placeholder="Kullanıcı adınızı girin"
              required
            />

            <label htmlFor="password">Parola</label>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="Parolanızı girin"
              required
            />

            <button className="primary-button" type="submit" disabled={loginLoading}>
              {loginLoading ? "Giriş yapılıyor..." : "Giriş yap"}
            </button>

            <div className="login-security">
              <ShieldCheck size={16} />
              Kimlik doğrulama SmartFactory API üzerinden yapılır.
            </div>
          </form>
        </section>
      </main>
    );
  }

  if (!user || !dashboard) {
    return (
      <main className="loading-page">
        {error ? (
          <div className="loading-card">
            <AlertCircle size={28} />
            <h2>Veriler yüklenemedi</h2>
            <p>{error}</p>
            <button className="primary-button" onClick={() => void loadDashboard(token)}>
              Yeniden dene
            </button>
            <button className="secondary-button" onClick={logout}>
              Oturumu kapat
            </button>
          </div>
        ) : (
          <div className="loading-card">
            <RefreshCw className="spin-icon" size={28} />
            <h2>SmartFactory yükleniyor</h2>
            <p>Kullanıcı ve dashboard bilgileri API üzerinden alınıyor.</p>
          </div>
        )}
      </main>
    );
  }

  const metrics = [
    {
      label: "Toplam üretim",
      value: formatNumber(dashboard.total_production),
      unit: "adet",
      icon: Package,
      color: "blue",
    },
    {
      label: "Toplam fire",
      value: formatNumber(dashboard.total_scrap),
      unit: `${formatNumber(dashboard.overall_scrap_rate)}% oran`,
      icon: Activity,
      color: "orange",
    },
    {
      label: "Stok değeri",
      value: formatCurrency(dashboard.total_stock_value),
      unit: `${formatNumber(dashboard.total_products)} ürün`,
      icon: Boxes,
      color: "purple",
    },
    {
      label: "Toplam sipariş",
      value: formatNumber(dashboard.total_orders),
      unit: `${formatNumber(dashboard.pending_orders)} bekliyor`,
      icon: ClipboardList,
      color: "green",
    },
  ];

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon"><Factory size={23} /></div>
          <div>
            <div className="brand-name">SmartFactory</div>
            <div className="brand-caption">PRODUCTION SYSTEM</div>
          </div>
        </div>

        <div className="nav-label">ANA MENÜ</div>
        <nav className="navigation">
          {[...menuItems, ...(user.role === "ADMIN" ? [{ label: "Sistem Logları", icon: ScrollText }] : [])].map(({ label, icon: Icon }) => (
            <a
              key={label}
              className={`nav-item ${activeSection === label ? "active" : ""}`}
              href={label === "Dashboard" ? "#dashboard" : `#${label.toLowerCase().replace(/\s+/g, "-")}`}
              onClick={(event) => {
                event.preventDefault();
                setActiveSection(label);
                setError("");
                if (label === "Sistem Logları") {
                  document.getElementById("system-logs")?.scrollIntoView({ behavior: "smooth", block: "start" });
                } else if (label === "Dashboard") {
                  document.getElementById("dashboard")?.scrollIntoView({ behavior: "smooth", block: "start" });
                } else if (label === "AI Üretim Analizi") {
                  document.getElementById("ai-analysis")?.scrollIntoView({
                    behavior: "smooth",
                    block: "start",
                  });
                  setAiError("");
                } else {
                  setError(`${label} ekranı sonraki geliştirme adımında eklenecek.`);
                }
              }}
            >
              <Icon size={18} />
              {label}
            </a>
          ))}
        </nav>

        <div className="nav-label secondary-label">OTURUM</div>
        <div className="sidebar-user">
          <div className="avatar">{user.full_name.slice(0, 1).toUpperCase()}</div>
          <div className="sidebar-user-info">
            <strong>{user.full_name}</strong>
            <span>{user.role}</span>
          </div>
        </div>
        <button className="logout-button" onClick={logout}>
          <LogOut size={17} /> Oturumu kapat
        </button>
        <div className="sidebar-bottom">
          <ShieldCheck size={18} />
          <div><strong>API bağlantısı</strong><span>Kimlik doğrulandı</span></div>
          <CheckCircle2 size={16} className="secure-check" />
        </div>
      </aside>

      <main className="main-content" id="dashboard">
        <header className="topbar">
          <div className="breadcrumb">Yönetim Paneli <span>/</span> <strong>Genel Bakış</strong></div>
          <div className="topbar-actions">
            <div className="system-status"><span className="status-dot" /> API bağlantısı aktif</div>
            <div className="profile">
              <div className="avatar">{user.full_name.slice(0, 1).toUpperCase()}</div>
              <div className="profile-copy"><strong>{user.full_name}</strong><span>{user.role}</span></div>
            </div>
          </div>
        </header>

        <section className="page-heading">
          <div>
            <div className="eyebrow">ÜRETİM VE OPERASYON</div>
            <h1>Dashboard</h1>
            <p>Fabrikanızın gerçek operasyonel verilerine genel bakış.</p>
          </div>
          <button className="refresh-button" onClick={() => void loadDashboard(token)} disabled={loading}>
            <RefreshCw size={15} className={loading ? "spin-icon" : ""} />
            {loading ? "Yükleniyor..." : "Verileri yenile"}
          </button>
        </section>

        {error && (
          <div className="error-message dashboard-error" role="alert">
            <AlertCircle size={17} /> {error}
            <button onClick={() => setError("")}>Kapat</button>
          </div>
        )}

        <div className="live-notice">
          <CheckCircle2 size={17} />
          <span>Veriler SmartFactory API üzerinden alınıyor. Bu ekrandaki özetler demo değildir.</span>
        </div>

        <section className="metrics-grid">
          {metrics.map(({ label, value, unit, icon: Icon, color }) => (
            <article className="metric-card" key={label}>
              <div className="metric-top">
                <span>{label}</span>
                <div className={`metric-icon ${color}`}><Icon size={19} /></div>
              </div>
              <div className="metric-value">{value}</div>
              <div className="metric-foot">{unit}</div>
              <div className={`metric-accent ${color}-accent`} />
            </article>
          ))}
        </section>

        <section className="charts-grid">
          <article className="panel">
            <div className="panel-heading">
              <div><h2>Üretim özeti</h2><p>Backend tarafından hesaplanan toplamlar</p></div>
            </div>
            <div className="summary-list">
              <div><span>Toplam üretim</span><strong>{formatNumber(dashboard.total_production)}</strong></div>
              <div><span>Toplam fire</span><strong>{formatNumber(dashboard.total_scrap)}</strong></div>
              <div><span>Genel fire oranı</span><strong>{formatNumber(dashboard.overall_scrap_rate)}%</strong></div>
              <div className="summary-progress">
                <div style={{ width: `${Math.min(100, Math.max(0, dashboard.overall_scrap_rate))}%` }} />
              </div>
            </div>
            <p className="subtle-note">Günlük grafikler için ayrı bir zaman serisi endpoint'i sonraki adımda ele alınacak.</p>
          </article>

          <article className="panel">
            <div className="panel-heading">
              <div><h2>Makine durumu</h2><p>API makine özeti</p></div>
            </div>
            <div className="summary-list">
              <div><span>Toplam makine</span><strong>{formatNumber(dashboard.total_machines)}</strong></div>
              <div><span>Aktif makine</span><strong>{formatNumber(dashboard.active_machines)}</strong></div>
              <div><span>Çalışan makine</span><strong>{formatNumber(dashboard.running_machines)}</strong></div>
              <div><span>Bakım durumunda</span><strong>{formatNumber(dashboard.maintenance_machines)}</strong></div>
            </div>
          </article>
        </section>

        <section className="bottom-grid">
          <article className="panel">
            <div className="panel-heading">
              <div><h2>Stok ve sipariş özeti</h2><p>Gerçek API verileri</p></div>
            </div>
            <div className="summary-list">
              <div><span>Toplam ürün</span><strong>{formatNumber(dashboard.total_products)}</strong></div>
              <div><span>Düşük stoklu ürün</span><strong>{formatNumber(dashboard.low_stock_products)}</strong></div>
              <div><span>Bekleyen sipariş</span><strong>{formatNumber(dashboard.pending_orders)}</strong></div>
              <div><span>Üretimdeki sipariş</span><strong>{formatNumber(dashboard.producing_orders)}</strong></div>
              <div><span>Hazır sipariş</span><strong>{formatNumber(dashboard.ready_orders)}</strong></div>
              <div><span>Sevk edilen sipariş</span><strong>{formatNumber(dashboard.shipped_orders)}</strong></div>
              <div><span>Tamamlanan sipariş</span><strong>{formatNumber(dashboard.completed_orders)}</strong></div>
            </div>
          </article>

          <article className="panel ai-panel" id="ai-analysis">
            <div className="ai-panel-heading">
              <div className="ai-heading-icon"><BrainCircuit size={22} /></div>
              <div>
                <h2>AI Üretim Analizi</h2>
                <p>Ollama destekli gerçek üretim değerlendirmesi</p>
              </div>
            </div>

            <p className="ai-description">
              Üretim, fire ve makine performansı verilerini yapay zekâ ile
              değerlendir. Analiz mevcut API verileri kullanılarak oluşturulur.
            </p>

            <div className="ai-footer">
              <span><span className="status-dot" /> Yerel model altyapısı</span>
              <button
                className="primary-button"
                onClick={() => void handleAnalyzeProduction()}
                disabled={aiLoading}
              >
                {aiLoading ? (
                  <><RefreshCw size={15} className="spin-icon" /> Analiz ediliyor...</>
                ) : (
                  <><BrainCircuit size={15} /> {aiAnalysis ? "Yeniden analiz et" : "Analiz başlat"}</>
                )}
              </button>
            </div>

            {aiError && (
              <div className="error-message" role="alert">
                <AlertCircle size={17} />
                <span>{aiError}</span>
              </div>
            )}

            {aiLoading && (
              <div className="ai-result-loading">
                Model üretim verilerini değerlendiriyor. Bu işlem biraz sürebilir.
              </div>
            )}

            {aiAnalysis && (
              <div className="ai-result">
                <div className="ai-result-meta">
                  <span>Model: {aiAnalysis.model}</span>
                  <span>Üretim: {formatNumber(aiAnalysis.statistics.total_production)}</span>
                  <span>Fire: {formatNumber(aiAnalysis.statistics.total_scrap)}</span>
                  <span>Fire oranı: %{formatNumber(aiAnalysis.statistics.scrap_rate)}</span>
                </div>

                {aiAnalysis.highest_scrap_machine && (
                  <div className="ai-highest-scrap">
                    <strong>En yüksek fire oranı</strong>
                    <span>{aiAnalysis.highest_scrap_machine.machine_name}</span>
                    <span>%{formatNumber(aiAnalysis.highest_scrap_machine.scrap_rate)}</span>
                  </div>
                )}

                <h3>Makine performansları</h3>
                <div className="ai-machine-list">
                  {aiAnalysis.machines.map((machine) => (
                    <div className="ai-machine-row" key={machine.machine}>
                      <div>
                        <strong>{machine.machine_name}</strong>
                        <span>{machine.machine} · Üretim: {formatNumber(machine.total_production)}</span>
                      </div>
                      <div className="ai-machine-scrap">
                        <strong>%{formatNumber(machine.scrap_rate)}</strong>
                        <span>Fire: {formatNumber(machine.total_scrap)}</span>
                      </div>
                    </div>
                  ))}
                </div>

                <h3>Yapay zekâ değerlendirmesi</h3>
                <div className="ai-analysis-text">{aiAnalysis.analysis}</div>
              </div>
            )}
          </article>
        </section>

        {user.role === "ADMIN" && (
          <section className="panel system-logs-panel" id="system-logs">
            <div className="panel-heading system-logs-heading">
              <div>
                <h2><ScrollText size={20} /> Sistem Logları</h2>
                <p>API ve AI işlemlerinin canlı kayıtları</p>
              </div>
              <div className="system-logs-actions">
                <span className={`log-connection ${logsConnected ? "connected" : ""}`}>
                  <Radio size={14} /> {logsConnected ? "Canlı bağlantı" : "Bağlantı bekleniyor"}
                </span>
                <button className="secondary-button" onClick={() => setActiveSection("Dashboard")}>
                  Dashboard'a dön
                </button>
              </div>
            </div>

            {logsError && <div className="error-message" role="alert"><AlertCircle size={17} /> {logsError}</div>}

            <div className="system-logs-toolbar">
              <label htmlFor="log-level">Seviye</label>
              <select id="log-level" value={logLevel} onChange={(event) => setLogLevel(event.target.value)}>
                <option value="ALL">Tüm kayıtlar</option>
                <option value="INFO">INFO</option>
                <option value="SUCCESS">SUCCESS</option>
                <option value="WARNING">WARNING</option>
                <option value="ERROR">ERROR</option>
              </select>
              <button className="secondary-button" onClick={() => void refreshLogs()} disabled={logsLoading}>
                {logsLoading ? "Yükleniyor..." : "Yenile"}
              </button>
              <span>{logs.length} kayıt</span>
            </div>

            <div className="system-logs-table-wrap">
              <table className="system-logs-table">
                <thead><tr><th>Zaman</th><th>Seviye</th><th>Kaynak</th><th>Mesaj</th><th>İşlem ID</th></tr></thead>
                <tbody>
                  {logs.filter((item) => logLevel === "ALL" || item.level === logLevel).map((item) => (
                    <tr key={item.id}>
                      <td>{new Date(item.timestamp).toLocaleString("tr-TR")}</td>
                      <td><span className={`log-level log-${item.level.toLowerCase()}`}>{item.level}</span></td>
                      <td>{item.source}</td>
                      <td className="log-message">{item.message}</td>
                      <td className="log-operation">{item.operation_id ?? "—"}</td>
                    </tr>
                  ))}
                  {!logsLoading && logs.filter((item) => logLevel === "ALL" || item.level === logLevel).length === 0 && (
                    <tr><td colSpan={5} className="logs-empty">Henüz gösterilecek kayıt yok.</td></tr>
                  )}
                </tbody>
              </table>
            </div>
          </section>
        )}

        <footer className="footer">
          <span>© 2026 SmartFactory API</span>
          <span>Giriş yapan kullanıcı: {user.username}</span>
        </footer>
      </main>
    </div>
  );
}

export default App;
