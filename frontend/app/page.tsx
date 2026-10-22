'use client';

import { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { Terminal, Shield, ScanSearch, CheckCircle2, Play } from 'lucide-react';

export default function Home() {
  const [url, setUrl] = useState('');
  const [logs, setLogs] = useState<any[]>([]);
  const [isScanning, setIsScanning] = useState(false);
  const [reportUrl, setReportUrl] = useState(''); // New state for download link
  const ws = useRef<WebSocket | null>(null);

  const [agents, setAgents] = useState({
    System: 'idle',
    Crawler: 'idle',
    Security: 'idle',
    Vision: 'idle',
    Critic: 'idle',
    Reporter: 'idle'
  });

  useEffect(() => {
    ws.current = new WebSocket('ws://localhost:8000/ws/audit-logs');
    
    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setLogs((prev) => [...prev, data]);
      
      if (data.agent) {
        setAgents((prev) => ({ ...prev, [data.agent]: data.status }));
      }
      
      // Update when scan finishes
      if (data.status === 'completed') {
        setIsScanning(false);
        if (data.report_id) {
          setReportUrl(`http://localhost:8000/download-report/${data.report_id}`);
        }
      }
    };

    return () => {
      if (ws.current) ws.current.close();
    };
  }, []);

  const startAudit = () => {
    if (!url) return;
    setIsScanning(true);
    setLogs([]);
    setReportUrl(''); // Reset report link on new scan
    setAgents({ System: 'idle', Crawler: 'idle', Security: 'idle', Vision: 'idle', Critic: 'idle', Reporter: 'idle' });
    
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify({ action: "START_SCAN", url: url }));
    }
  };

  const getGlowStyle = (status: string) => {
    switch (status) {
      case 'active': return { boxShadow: '0 0 20px 5px rgba(59, 130, 246, 0.5)', borderColor: '#3b82f6' };
      case 'success': return { boxShadow: '0 0 20px 5px rgba(34, 197, 94, 0.5)', borderColor: '#22c55e' };
      case 'warning': return { boxShadow: '0 0 20px 5px rgba(234, 179, 8, 0.5)', borderColor: '#eab308' };
      case 'error': return { boxShadow: '0 0 20px 5px rgba(239, 68, 68, 0.5)', borderColor: '#ef4444' };
      default: return { borderColor: '#3f3f46' };
    }
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-white font-sans selection:bg-blue-500/30 p-8">
      
      <header className="max-w-6xl mx-auto mb-10 flex flex-col md:flex-row gap-6 items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-cyan-300 bg-clip-text text-transparent flex items-center gap-3">
            <Shield className="text-blue-500" /> AutoAudit AI Pro
          </h1>
          <p className="text-zinc-400 text-sm mt-1">Autonomous Multi-Agent Vulnerability & UI Scanner</p>
        </div>

        <div className="flex w-full md:w-auto gap-3">
          <input 
            type="url" 
            placeholder="https://example.com" 
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="w-full md:w-80 bg-zinc-900 border border-zinc-700 rounded-lg px-4 py-2 text-zinc-100 focus:outline-none focus:border-blue-500"
          />
          <button 
            onClick={startAudit}
            disabled={isScanning}
            className={`flex items-center gap-2 px-6 py-2 rounded-lg font-medium transition-all ${isScanning ? 'bg-zinc-800 text-zinc-500 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-500 text-white shadow-[0_0_15px_rgba(37,99,235,0.5)] hover:shadow-[0_0_25px_rgba(37,99,235,0.7)]'}`}
          >
            {isScanning ? <span className="animate-pulse">Scanning...</span> : <><Play size={18} /> Start Audit</>}
          </button>
        </div>
      </header>

      {/* New Download Button Appears Here When Done */}
      {reportUrl && (
        <div className="max-w-6xl mx-auto mb-6 text-center animate-fade-in">
          <a 
            href={reportUrl} 
            download 
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-8 py-3 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-400 hover:to-emerald-500 text-white font-bold rounded-lg shadow-[0_0_20px_rgba(16,185,129,0.4)] transition-all"
          >
            <CheckCircle2 size={20} />
            Download Final Audit Report (Markdown)
          </a>
        </div>
      )}

      <main className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6 relative overflow-hidden">
          <h2 className="text-lg font-semibold text-zinc-300 mb-8 flex items-center gap-2">
            <ScanSearch size={20} /> Multi-Agent Execution Graph
          </h2>
          
          <div className="flex flex-col items-center gap-10">
            <motion.div animate={getGlowStyle(agents.Crawler)} className="w-48 bg-zinc-950 border-2 rounded-lg p-4 text-center transition-all duration-300 z-10">
              <h3 className="font-bold text-zinc-100">Crawler Agent</h3>
              <p className="text-xs text-zinc-500">Maps Attack Surface</p>
            </motion.div>

            <div className="flex w-full justify-around relative px-10">
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-[2px] bg-zinc-800 -z-0"></div>
              
              <motion.div animate={getGlowStyle(agents.Security)} className="w-40 bg-zinc-950 border-2 rounded-lg p-4 text-center transition-all duration-300 z-10">
                <h3 className="font-bold text-zinc-100">Security Agent</h3>
                <p className="text-xs text-zinc-500">Finds Vulnerabilities</p>
              </motion.div>

              <motion.div animate={getGlowStyle(agents.Vision)} className="w-40 bg-zinc-950 border-2 rounded-lg p-4 text-center transition-all duration-300 z-10">
                <h3 className="font-bold text-zinc-100">Vision Agent</h3>
                <p className="text-xs text-zinc-500">Audits UI/UX via LLM</p>
              </motion.div>
            </div>

            <motion.div animate={getGlowStyle(agents.Reporter)} className="w-48 bg-zinc-950 border-2 rounded-lg p-4 text-center transition-all duration-300 z-10">
              <h3 className="font-bold text-zinc-100">Reporter Agent</h3>
              <p className="text-xs text-zinc-500">Synthesizes Final Report</p>
            </motion.div>
          </div>
        </div>

        <div className="bg-black border border-zinc-800 rounded-xl p-0 flex flex-col h-[500px] overflow-hidden shadow-2xl">
          <div className="bg-zinc-900 px-4 py-3 border-b border-zinc-800 flex items-center gap-2">
            <Terminal size={18} className="text-zinc-400" />
            <span className="text-sm font-mono text-zinc-400">live-agent-logs.sh</span>
          </div>
          
          <div className="p-4 overflow-y-auto flex-1 font-mono text-sm space-y-2 flex flex-col-reverse">
            <div className="space-y-2">
              {logs.length === 0 && <span className="text-zinc-600">Awaiting target URL...</span>}
              {logs.map((log, index) => (
                <div key={index} className="flex gap-3">
                  <span className="text-zinc-500 min-w-[70px]">{log.timestamp}</span>
                  <span className="text-blue-400 font-bold min-w-[90px]">[{log.agent}]</span>
                  <span className={`${
                    log.status === 'error' ? 'text-red-400' : 
                    log.status === 'warning' ? 'text-yellow-400' : 
                    log.status === 'success' ? 'text-green-400' : 
                    'text-zinc-300'
                  }`}>
                    {log.message}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

      </main>
    </div>
  );
}