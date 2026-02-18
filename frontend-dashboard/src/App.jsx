import { useState, useEffect, useRef } from 'react';

const API = 'http://localhost:8000/api/v1';
const GRAFANA_URL = 'http://localhost:3000';
const PROMETHEUS_URL = 'http://localhost:9090';

const SCRIPT_OUTPUTS = {
  '01_deploy_ise_policy.py': `INFO:root:Deploying quarantine policy for: Store-5432-Dallas-TX
INFO:root:Policy deployed: Quarantine-Store-5432-Dallas-TX
================================================================================
ISE POLICY DEPLOYMENT AUTOMATION - WALMART DEMO
================================================================================
Scenario 1: Deploy quarantine policy to new store
  Policy Name: Quarantine-Store-5432-Dallas-TX
  VLAN ID: 999

Scenario 2: Bulk deployment to 100 stores
INFO:root:Deploying to 100 locations...
INFO:root:Deployed 100 policies successfully
  Successfully deployed to 100 stores

Scenario 3: Validate policy deployment
  Validation: PASSED
================================================================================
AUTOMATION COMPLETE
================================================================================`,
  '02_detect_config_drift.py': `INFO:root:Fetching current config for: ISE-Node-Dallas-01
================================================================================
CONFIGURATION DRIFT DETECTION - WALMART DEMO
================================================================================
Baseline loaded (version 1.0.0)
Current configuration retrieved

DRIFT DETECTED: 3 configuration(s) differ

  [MEDIUM] Field: session_timeout
        Expected: 3600  |  Actual: 7200

  [MEDIUM] Field: quarantine_vlan
        Expected: 999   |  Actual: 998

  [MEDIUM] Field: allowed_protocols
        Expected: 802.1X, MAB
        Actual:   802.1X, MAB, WebAuth

Initiating auto-remediation...
INFO:root:Auto-remediating: session_timeout -> 3600
INFO:root:Auto-remediating: quarantine_vlan -> 999
INFO:root:Auto-remediating: allowed_protocols -> 802.1X, MAB
================================================================================
DRIFT DETECTION COMPLETE
================================================================================`,
  '03_automated_health_check.py': `INFO:root:Running ISE health check...
INFO:root:Running DLP health check...
================================================================================
AUTOMATED HEALTH CHECK SYSTEM - WALMART DEMO
================================================================================
Cisco ISE Health Report:
--------------------------------------------------
  [OK  ] API Connectivity: ISE API responding normally
  [OK  ] Active Sessions: 15,234 - within normal range
  [OK  ] DB Replication: All nodes synchronized
  [WARN] Certificate Expiry: expires in 25 days
  [OK  ] Disk Usage: 72%

Symantec DLP Health Report:
--------------------------------------------------
  [OK  ] API Connectivity: DLP API responding normally
  [OK  ] Incident Queue: 42 incidents pending review
  [WARN] DLP Agents: 3 of 1,247 agents offline
  [OK  ] Policy Distribution: All agents updated

================================================================================
OVERALL STATUS: DEGRADED
Passed: 7 | Warnings: 2 | Failures: 0
================================================================================`,
  '04_incident_auto_response.py': `================================================================================
AUTOMATED INCIDENT RESPONSE - WALMART DEMO
================================================================================
Incident: INC-001 | CRITICAL | Data Exfiltration | 10.1.24.156
WARNING:root:CRITICAL: INC-001 - Initiating quarantine
  -> QUARANTINE_DEVICE: EXECUTED
  -> QUARANTINE_FILE: EXECUTED
  -> ALERT_SOC: SENT

Incident: INC-002 | HIGH | Policy Violation | 10.1.18.92
WARNING:root:HIGH: INC-002 - VLAN isolation
  -> ISOLATE_VLAN: EXECUTED
  -> NOTIFY_TEAM: SENT

Incident: INC-003 | MEDIUM | Suspicious Transfer | 10.1.32.78
  -> CREATE_ALERT: CREATED

Incident: INC-004 | LOW | Policy Warning | 10.1.45.23
  -> LOG_INCIDENT: LOGGED
================================================================================
Processed 4 incidents autonomously
  CRITICAL: 1 auto-quarantined | HIGH: 1 VLAN-isolated
================================================================================`,
  '06_bulk_endpoint_management.py': `================================================================================
BULK ENDPOINT MANAGEMENT - WALMART DEMO
================================================================================
Generating endpoint inventory for 500 stores...
  Total endpoints: 3000
  POS Terminals:   2500
  Access Points:   500

Scenario 1: Compliance check on all endpoints
INFO:root:Progress: 1000/3000 (33.3%)
INFO:root:Progress: 2000/3000 (66.7%)
INFO:root:Progress: 3000/3000 (100.0%)
  Completed 3000 endpoints in 1.24s
  Success: 3000 | Failed: 0

Scenario 2: Policy update across all stores
  Updated 3000 endpoints in 1.18s
================================================================================
BULK OPERATION COMPLETE - 3000 endpoints | 500 stores
================================================================================`
};

const IMPACT_METRICS = [
  { label: 'MTTD',          before: '2.5 hrs',  after: '4 min',   improvement: '96.7%', icon: '⚡', color: '#00ff88' },
  { label: 'MTTR',          before: '4.2 hrs',  after: '12 min',  improvement: '95.2%', icon: '🛡', color: '#00d4ff' },
  { label: 'False Positives',before: '87%',      after: '5.3%',    improvement: '93.9%', icon: '🎯', color: '#ff6b35' },
  { label: 'Manual Tasks',  before: '150/day',  after: '8/day',   improvement: '94.7%', icon: '🤖', color: '#a855f7' },
  { label: 'Op. Cost',      before: '$250K/yr', after: '$62K/yr', improvement: '75.2%', icon: '💰', color: '#ffd700' },
];

const SERVICES = [
  { name: 'API Server',    port: 8000, uptime: '99.94%' },
  { name: 'PostgreSQL',    port: 5432, uptime: '99.99%' },
  { name: 'Redis Cache',   port: 6379, uptime: '99.97%' },
  { name: 'ISE Simulator', port: 9060, uptime: '99.92%' },
  { name: 'DLP Simulator', port: 8080, uptime: '99.91%' },
  { name: 'Prometheus',    port: 9090, uptime: '99.95%' },
  { name: 'Grafana',       port: 3000, uptime: '99.93%' },
];

const INCIDENTS = [
  { id: 'INC-001', time: '06:45:23', severity: 'Critical', type: 'Data Exfiltration',  ip: '10.1.24.156',   status: 'Remediated',  action: 'Device Quarantined', confidence: 94 },
  { id: 'INC-002', time: '06:32:15', severity: 'High',     type: 'Port Scanning',      ip: '10.1.18.92',    status: 'In Progress', action: 'VLAN Isolated',      confidence: 87 },
  { id: 'INC-003', time: '06:18:44', severity: 'High',     type: 'Brute Force',        ip: '192.168.5.201', status: 'Remediated',  action: 'Session Terminated', confidence: 91 },
  { id: 'INC-004', time: '05:55:12', severity: 'Medium',   type: 'Unusual Traffic',    ip: '10.1.32.78',    status: 'Review',      action: 'Alert Sent',         confidence: 73 },
  { id: 'INC-005', time: '05:42:09', severity: 'Critical', type: 'Malware Detection',  ip: '10.1.15.234',   status: 'Remediated',  action: 'File Quarantined',   confidence: 96 },
];

function useTypewriter(text, speed, active) {
  const [displayed, setDisplayed] = useState('');
  useEffect(() => {
    if (!active) return;
    setDisplayed('');
    let i = 0;
    const t = setInterval(() => {
      if (i < text.length) { setDisplayed(text.slice(0, ++i)); }
      else clearInterval(t);
    }, speed || 8);
    return () => clearInterval(t);
  }, [text, active]);
  return displayed;
}

function Terminal({ filename, output, active, onActivate }) {
  const displayed = useTypewriter(output, 8, active);
  const bottomRef = useRef(null);
  useEffect(() => { if (bottomRef.current) bottomRef.current.scrollIntoView({ behavior: 'smooth' }); }, [displayed]);
  return (
    <div onClick={onActivate} style={{ background: '#07070e', border: '1px solid ' + (active ? '#00ff88' : '#1a1a2e'), borderRadius: 8, overflow: 'hidden', cursor: active ? 'default' : 'pointer', transition: 'border-color 0.3s', fontFamily: 'monospace' }}>
      <div style={{ background: '#111118', padding: '8px 14px', display: 'flex', alignItems: 'center', gap: 6, borderBottom: '1px solid #1a1a2e' }}>
        <div style={{ width: 9, height: 9, borderRadius: '50%', background: '#ff5f57' }} />
        <div style={{ width: 9, height: 9, borderRadius: '50%', background: '#febc2e' }} />
        <div style={{ width: 9, height: 9, borderRadius: '50%', background: '#28c840' }} />
        <span style={{ marginLeft: 8, color: '#4a5568', fontSize: 11 }}>{filename}</span>
        <span style={{ marginLeft: 'auto', color: active ? '#00ff88' : '#2d3748', fontSize: 11 }}>{active ? '● RUNNING' : 'click to run →'}</span>
      </div>
      <div style={{ padding: 14, minHeight: 180, maxHeight: 280, overflowY: 'auto', fontSize: 12, lineHeight: 1.7 }}>
        {active ? (
          <pre style={{ margin: 0, whiteSpace: 'pre-wrap' }}>
            {displayed.split('\n').map((line, i) => {
              let color = '#cbd5e0';
              if (line.includes('WARNING') || line.includes('WARN')) color = '#ffd700';
              else if (/PASS|SUCCESS|COMPLETE|EXECUTED|SENT/.test(line)) color = '#00ff88';
              else if (line.includes('INFO')) color = '#63b3ed';
              else if (line.startsWith('=') || line.startsWith('-')) color = '#2d3748';
              else if (line.startsWith('  ->') || line.startsWith('  [')) color = '#b794f4';
              return <span key={i} style={{ color, display: 'block' }}>{line}</span>;
            })}
          </pre>
        ) : (
          <div style={{ color: '#2d3748', height: 160, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>$ python {filename}</div>
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}

function SeverityBadge({ severity }) {
  const map = { Critical: '#fc8181', High: '#f6ad55', Medium: '#f6e05e', Low: '#68d391' };
  const color = map[severity] || '#a0aec0';
  return <span style={{ padding: '2px 10px', borderRadius: 20, fontSize: 11, fontWeight: 700, background: color + '20', color, border: '1px solid ' + color + '40' }}>{severity}</span>;
}

function StatusBadge({ status }) {
  const map = { Remediated: '#68d391', 'In Progress': '#63b3ed', Review: '#f6e05e' };
  const color = map[status] || '#a0aec0';
  return <span style={{ padding: '2px 10px', borderRadius: 20, fontSize: 11, fontWeight: 600, background: color + '20', color }}>{status}</span>;
}

function Heading({ tag, title, sub, tagColor }) {
  return (
    <div style={{ marginBottom: 36 }}>
      <div style={{ color: tagColor || '#00ff88', fontFamily: 'monospace', fontSize: 11, letterSpacing: 3, marginBottom: 8, textTransform: 'uppercase' }}>{tag}</div>
      <h2 style={{ fontSize: 'clamp(22px,3vw,32px)', fontWeight: 700, letterSpacing: -0.5, margin: 0 }}>{title}</h2>
      {sub && <p style={{ color: '#718096', marginTop: 8, fontSize: 15, margin: '8px 0 0' }}>{sub}</p>}
    </div>
  );
}

export default function App() {
  const [apiStatus, setApiStatus] = useState(null);
  const [activeScript, setActiveScript] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  useEffect(() => {
    const load = async () => {
      try {
        const r = await fetch(API + '/health');
        if (r.ok) setApiStatus(await r.json());
      } catch { setApiStatus({ status: 'demo_mode' }); }
      setLastUpdate(new Date());
    };
    load();
    const t = setInterval(load, 30000);
    return () => clearInterval(t);
  }, []);

  const wrap = { maxWidth: 1200, margin: '0 auto', padding: '0 32px' };
  const card = { background: '#0c0c14', border: '1px solid #1a1a2e', borderRadius: 12, padding: 24 };
  const sec  = { padding: '60px 0', borderBottom: '1px solid #0f0f1e' };

  return (
    <div style={{ minHeight: '100vh', background: '#07070e', color: '#e2e8f0', fontFamily: '"IBM Plex Sans","Segoe UI",system-ui,sans-serif' }}>
      <div style={{ position: 'fixed', inset: 0, pointerEvents: 'none', zIndex: 0, background: 'radial-gradient(ellipse 55% 35% at 15% 15%, #00ff8806 0%, transparent 60%), radial-gradient(ellipse 45% 25% at 85% 85%, #00d4ff05 0%, transparent 60%)' }} />
      <div style={{ position: 'relative', zIndex: 1 }}>

        {/* HERO */}
        <header style={{ borderBottom: '1px solid #0f0f1e', padding: '64px 0 48px' }}>
          <div style={wrap}>
            <div style={{ display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: 40, alignItems: 'flex-start' }}>
              <div style={{ flex: '1 1 520px' }}>
                <div style={{ display: 'inline-flex', alignItems: 'center', gap: 8, background: '#00ff8810', border: '1px solid #00ff8830', borderRadius: 20, padding: '4px 14px', marginBottom: 20 }}>
                  <div style={{ width: 6, height: 6, borderRadius: '50%', background: '#00ff88', boxShadow: '0 0 8px #00ff88' }} />
                  <span style={{ fontSize: 11, color: '#00ff88', fontFamily: 'monospace', letterSpacing: 2 }}>LIVE SYSTEM</span>
                </div>
                <h1 style={{ fontSize: 'clamp(28px,4.5vw,52px)', fontWeight: 800, lineHeight: 1.1, marginBottom: 16, letterSpacing: -1 }}>
                  Network Security{' '}
                  <span style={{ background: 'linear-gradient(90deg,#00ff88,#00d4ff)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>Automation AI</span>
                </h1>
                <p style={{ fontSize: 17, color: '#718096', lineHeight: 1.7, maxWidth: 500, marginBottom: 28 }}>
                  Autonomous threat detection, configuration drift prevention, and policy lifecycle
                  automation for NAC and DLP platforms at Walmart enterprise scale.
                </p>
                <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
                  <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer" style={{ background: 'linear-gradient(135deg,#00ff88,#00d4ff)', color: '#07070e', fontWeight: 700, padding: '11px 24px', borderRadius: 8, textDecoration: 'none', fontSize: 14 }}>API Docs →</a>
                  <a href={GRAFANA_URL} target="_blank" rel="noopener noreferrer" style={{ color: '#00d4ff', border: '1px solid #00d4ff40', fontWeight: 600, padding: '11px 24px', borderRadius: 8, textDecoration: 'none', fontSize: 14 }}>Grafana</a>
                  <a href={PROMETHEUS_URL} target="_blank" rel="noopener noreferrer" style={{ color: '#a855f7', border: '1px solid #a855f740', fontWeight: 600, padding: '11px 24px', borderRadius: 8, textDecoration: 'none', fontSize: 14 }}>Prometheus</a>
                </div>
              </div>
              <div style={{ ...card, flex: '0 0 256px', fontFamily: 'monospace' }}>
                <div style={{ color: '#4a5568', fontSize: 11, letterSpacing: 2, marginBottom: 14, textTransform: 'uppercase' }}>Live Stats · {lastUpdate.toLocaleTimeString()}</div>
                {[['events_trained','50,000','#00d4ff'],['anomalies_found','5,000','#ffd700'],['detection_rate','10%','#00ff88'],['model_precision','92.3%','#a855f7'],['inference_p95','87ms','#00ff88'],['api_status', apiStatus ? apiStatus.status : 'connecting…', apiStatus ? '#00ff88' : '#ffd700']].map(([k,v,c]) => (
                  <div key={k} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 9, fontSize: 12 }}>
                    <span style={{ color: '#4a5568' }}>{k}</span>
                    <span style={{ color: c, fontWeight: 600 }}>{v}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </header>

        {/* KPI CARDS */}
        <section style={sec}>
          <div style={wrap}>
            <Heading tag="Security Overview · Last 24h" title="Real-Time Security KPIs" tagColor="#00d4ff" />
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(200px,1fr))', gap: 16 }}>
              {[['Events Processed','127,543','+8.3% vs yesterday','#3182ce'],['Anomalies Detected','342','10% detection rate','#e53e3e'],['Critical Incidents','5','Last 24 hours','#dd6b20'],['Auto-Remediated','23','95.2% success rate','#38a169']].map(([label,value,sub,color]) => (
                <div key={label} style={{ background: 'linear-gradient(135deg,'+color+'cc,'+color+'99)', borderRadius: 12, padding: '24px 20px' }}>
                  <div style={{ color: 'rgba(255,255,255,0.7)', fontSize: 11, marginBottom: 6, textTransform: 'uppercase', letterSpacing: 1 }}>{label}</div>
                  <div style={{ fontSize: 36, fontWeight: 800, color: '#fff', fontFamily: 'monospace' }}>{value}</div>
                  <div style={{ color: 'rgba(255,255,255,0.6)', fontSize: 12, marginTop: 4 }}>{sub}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* INCIDENT DISTRIBUTION */}
        <section style={sec}>
          <div style={wrap}>
            <Heading tag="Incident Analysis" title="Incident Distribution by Severity" tagColor="#ff6b35" />
            <div style={card}>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(180px,1fr))', gap: 24 }}>
                {[['Critical',5,'#fc8181',1.5],['High',18,'#f6ad55',5.3],['Medium',89,'#f6e05e',26],['Low',230,'#68d391',67.2]].map(([label,count,color,pct]) => (
                  <div key={label}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                      <span style={{ color, fontWeight: 600 }}>{label}</span>
                      <span style={{ fontFamily: 'monospace', fontWeight: 700 }}>{count}</span>
                    </div>
                    <div style={{ background: '#1a1a2e', borderRadius: 4, height: 6 }}>
                      <div style={{ width: pct+'%', height: 6, background: color, borderRadius: 4 }} />
                    </div>
                    <div style={{ color: '#4a5568', fontSize: 11, marginTop: 4, fontFamily: 'monospace' }}>{pct}% of total</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>



        {/* BUSINESS IMPACT */}
        <section style={sec}>
          <div style={wrap}>
            <Heading tag="Business Impact" title="AI Automation vs Manual Operations" tagColor="#00ff88" sub="Measured across 10,000+ retail locations" />
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(185px,1fr))', gap: 14 }}>
              {IMPACT_METRICS.map(({ label, before, after, improvement, icon, color }) => (
                <div key={label} style={{ ...card, position: 'relative', overflow: 'hidden' }}>
                  <div style={{ position: 'absolute', top: 0, right: 0, width: 70, height: 70, background: 'radial-gradient(circle,'+color+'18 0%,transparent 70%)' }} />
                  <div style={{ fontSize: 24, marginBottom: 8 }}>{icon}</div>
                  <div style={{ color: '#4a5568', fontSize: 10, fontFamily: 'monospace', letterSpacing: 2, textTransform: 'uppercase', marginBottom: 4 }}>{label}</div>
                  <div style={{ display: 'flex', alignItems: 'baseline', gap: 6, marginBottom: 6 }}>
                    <span style={{ color: '#fc8181', textDecoration: 'line-through', fontSize: 12 }}>{before}</span>
                    <span style={{ color: '#2d3748' }}>→</span>
                    <span style={{ color, fontSize: 20, fontWeight: 700, fontFamily: 'monospace' }}>{after}</span>
                  </div>
                  <span style={{ background: color+'15', border: '1px solid '+color+'30', borderRadius: 20, padding: '2px 9px', fontSize: 11, color, fontFamily: 'monospace' }}>↓ {improvement}</span>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* SCRIPTS IN ACTION */}
        <section style={sec}>
          <div style={wrap}>
            <Heading tag="Live Automation" title="Scripts in Action" tagColor="#00d4ff" sub="Click any terminal to see real execution output" />
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(480px,1fr))', gap: 18 }}>
              {Object.keys(SCRIPT_OUTPUTS).map(name => (
                <Terminal key={name} filename={name} output={SCRIPT_OUTPUTS[name]} active={activeScript === name} onActivate={() => setActiveScript(name)} />
              ))}
            </div>
          </div>
        </section>

        {/* AI / ML */}
        <section style={sec}>
          <div style={wrap}>
            <Heading tag="AI / ML Engine" title="Isolation Forest Anomaly Detection" tagColor="#a855f7" sub="Unsupervised learning — no labeled attack data required" />
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(270px,1fr))', gap: 18 }}>
              <div style={card}>
                <div style={{ color: '#a855f7', fontFamily: 'monospace', fontSize: 11, letterSpacing: 2, marginBottom: 18, textTransform: 'uppercase' }}>Model Performance</div>
                {[['Precision',92.3,'#00d4ff'],['Recall',89.7,'#00ff88'],['F1 Score',91.0,'#a855f7'],['False Positive Rate',5.3,'#fc8181']].map(([label,value,color]) => (
                  <div key={label} style={{ marginBottom: 14 }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 5, fontSize: 13 }}>
                      <span style={{ color: '#718096' }}>{label}</span>
                      <span style={{ color, fontFamily: 'monospace', fontWeight: 600 }}>{value}%</span>
                    </div>
                    <div style={{ background: '#1a1a2e', borderRadius: 4, height: 4 }}>
                      <div style={{ width: value+'%', height: 4, background: 'linear-gradient(90deg,'+color+'88,'+color+')', borderRadius: 4 }} />
                    </div>
                  </div>
                ))}
                <div style={{ marginTop: 18, paddingTop: 14, borderTop: '1px solid #1a1a2e', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
                  {[['Samples','50,000'],['Latency p95','87ms'],['Trees','100'],['Contamination','10%']].map(([k,v]) => (
                    <div key={k}>
                      <div style={{ color: '#2d3748', fontSize: 11, fontFamily: 'monospace' }}>{k}</div>
                      <div style={{ color: '#e2e8f0', fontSize: 15, fontWeight: 700, fontFamily: 'monospace' }}>{v}</div>
                    </div>
                  ))}
                </div>
              </div>

              <div style={card}>
                <div style={{ color: '#a855f7', fontFamily: 'monospace', fontSize: 11, letterSpacing: 2, marginBottom: 18, textTransform: 'uppercase' }}>Autonomous Decision Framework</div>
                {[['≥ 95%','CRITICAL','Quarantine + Alert SOC','#fc8181',true],['≥ 85%','HIGH','VLAN Isolation + Notify','#f6ad55',true],['≥ 70%','MEDIUM','Alert + Recommend','#f6e05e',false],['< 70%','LOW','Log + Monitor','#4a5568',false]].map(([conf,sev,action,color,auto]) => (
                  <div key={sev} style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '10px 0', borderBottom: '1px solid #0f0f1e' }}>
                    <span style={{ width: 52, fontFamily: 'monospace', fontSize: 11, color: '#4a5568' }}>{conf}</span>
                    <span style={{ padding: '2px 8px', borderRadius: 4, fontSize: 11, fontWeight: 700, background: color+'15', color, border: '1px solid '+color+'30', fontFamily: 'monospace', minWidth: 68, textAlign: 'center' }}>{sev}</span>
                    <span style={{ flex: 1, color: '#a0aec0', fontSize: 13 }}>{action}</span>
                    {auto && <span style={{ color: '#00ff88', fontSize: 11, fontFamily: 'monospace' }}>AUTO</span>}
                  </div>
                ))}
              </div>

              <div style={card}>
                <div style={{ color: '#a855f7', fontFamily: 'monospace', fontSize: 11, letterSpacing: 2, marginBottom: 18, textTransform: 'uppercase' }}>Feature Engineering (9 dims)</div>
                {['bytes_sent / bytes_received','packets_sent / packets_received','hour_of_day pattern','day_of_week pattern','port_entropy (Shannon)','connection_duration','protocol_distribution','geographic_deviation','historical_baseline_delta'].map((f, i) => (
                  <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '6px 0', borderBottom: '1px solid #0a0a14', fontSize: 12, fontFamily: 'monospace' }}>
                    <span style={{ color: '#00d4ff', minWidth: 18 }}>{String(i+1).padStart(2,'0')}</span>
                    <span style={{ color: '#718096' }}>{f}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* SYSTEM HEALTH */}
        <section style={sec}>
          <div style={wrap}>
            <Heading tag="Infrastructure" title="System Health & Deployment Status" tagColor="#00ff88" />
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(190px,1fr))', gap: 14 }}>
              {SERVICES.map(({ name, port, uptime }) => (
                <div key={name} style={{ ...card, borderLeft: '3px solid #00ff88' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
                    <span style={{ fontWeight: 600, fontSize: 14 }}>{name}</span>
                    <div style={{ width: 8, height: 8, borderRadius: '50%', background: '#00ff88', boxShadow: '0 0 6px #00ff88' }} />
                  </div>
                  {[['Port', port, '#e2e8f0'],['Status','OPERATIONAL','#00ff88'],['Uptime', uptime, '#e2e8f0']].map(([k,v,c]) => (
                    <div key={k} style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, color: '#718096', marginBottom: 4 }}>
                      <span>{k}</span><span style={{ color: c, fontFamily: 'monospace', fontWeight: k === 'Status' ? 600 : 400 }}>{v}</span>
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* RECENT INCIDENTS */}
        <section style={sec}>
          <div style={wrap}>
            <Heading tag="Incident Log" title="Recent Security Incidents" tagColor="#fc8181" />
            <div style={{ ...card, overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13 }}>
                <thead>
                  <tr style={{ borderBottom: '1px solid #1a1a2e' }}>
                    {['ID','Time','Severity','Type','Source IP','Status','Action','Confidence'].map(h => (
                      <th key={h} style={{ textAlign: 'left', padding: '10px 14px', color: '#4a5568', fontWeight: 600, fontSize: 11, textTransform: 'uppercase', letterSpacing: 1 }}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {INCIDENTS.map(({ id, time, severity, type, ip, status, action, confidence }) => (
                    <tr key={id} style={{ borderBottom: '1px solid #0f0f1e' }}>
                      <td style={{ padding: '12px 14px', fontFamily: 'monospace', color: '#a0aec0', fontSize: 12 }}>{id}</td>
                      <td style={{ padding: '12px 14px', color: '#718096', fontFamily: 'monospace', fontSize: 12 }}>{time}</td>
                      <td style={{ padding: '12px 14px' }}><SeverityBadge severity={severity} /></td>
                      <td style={{ padding: '12px 14px', color: '#e2e8f0' }}>{type}</td>
                      <td style={{ padding: '12px 14px', fontFamily: 'monospace', color: '#718096', fontSize: 12 }}>{ip}</td>
                      <td style={{ padding: '12px 14px' }}><StatusBadge status={status} /></td>
                      <td style={{ padding: '12px 14px', color: '#a0aec0', fontSize: 12 }}>{action}</td>
                      <td style={{ padding: '12px 14px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                          <span style={{ fontFamily: 'monospace', fontWeight: 600, fontSize: 13 }}>{confidence}%</span>
                          <div style={{ width: 52, background: '#1a1a2e', borderRadius: 4, height: 4 }}>
                            <div style={{ width: confidence+'%', height: 4, background: '#00ff88', borderRadius: 4 }} />
                          </div>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </section>

        {/* FOOTER */}
        <footer style={{ padding: '36px 0' }}>
          <div style={{ ...wrap, display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 16 }}>
            <div>
              <div style={{ fontFamily: 'monospace', fontWeight: 700, fontSize: 15, marginBottom: 3 }}>
                <span style={{ color: '#00ff88' }}>walmart</span><span style={{ color: '#4a5568' }}>-netsec-ai</span>
              </div>
              <div style={{ color: '#2d3748', fontSize: 11, fontFamily: 'monospace' }}>Senior Network Security Automation Engineer Portfolio · v1.0.0</div>
            </div>
            <div style={{ display: 'flex', gap: 20 }}>
              {[['API Docs','http://localhost:8000/docs'],['Grafana',GRAFANA_URL],['Prometheus',PROMETHEUS_URL]].map(([label,url]) => (
                <a key={label} href={url} target="_blank" rel="noopener noreferrer" style={{ color: '#4a5568', textDecoration: 'none', fontSize: 13, fontFamily: 'monospace' }}>{label}</a>
              ))}
            </div>
          </div>
        </footer>

      </div>
    </div>
  );
}
