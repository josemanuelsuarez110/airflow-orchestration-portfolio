"use client";

import React, { useState, useEffect } from 'react';
import { Network, ServerCog, Activity, Clock, CheckCircle2, Play, AlertCircle, RefreshCw } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';

const mockExecutionData = [
  { time: '02:00', load: 85, duration: 4.2 },
  { time: '03:00', load: 120, duration: 5.1 },
  { time: '04:00', load: 105, duration: 4.8 },
  { time: '05:00', load: 156, duration: 6.2 },
  { time: '06:00', load: 190, duration: 7.5 },
  { time: '07:00', load: 140, duration: 5.5 },
  { time: '08:00', load: 95, duration: 4.5 },
];

export default function OrchestraDashboard() {
  const [activeDag, setActiveDag] = useState(2);
  const [isSimulating, setIsSimulating] = useState(true);

  return (
    <div className="min-h-screen bg-[#02000f] text-gray-200 p-8 font-sans">
      
      {/* HEADER SECTION */}
      <header className="flex justify-between items-center mb-8 border-b border-cyan-500/30 pb-4">
        <div className="flex items-center gap-4">
          <div className="p-3 glass-panel rounded-full glow-box-cyan">
            <Network className="w-8 h-8 text-[#00f0ff]" />
          </div>
          <div>
            <h1 className="text-3xl font-bold glow-text-cyan tracking-wider">ORCHESTRA FLOW</h1>
            <p className="text-cyan-400/70 text-sm tracking-widest mt-1">APACHE AIRFLOW CONTROL CENTER</p>
          </div>
        </div>
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${isSimulating ? 'bg-[#39ff14] glow-text-green animate-pulse' : 'bg-red-500'}`} />
            <span className="text-sm text-gray-400 font-mono">SCHEDULER STATUS</span>
          </div>
          <button 
            onClick={() => setIsSimulating(!isSimulating)}
            className="flex items-center gap-2 px-4 py-2 bg-cyan-900/40 border border-[#00f0ff] rounded-lg text-[#00f0ff] hover:bg-[#00f0ff]/20 transition-all glow-box-cyan"
          >
            {isSimulating ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
            {isSimulating ? 'RUNNING' : 'TRIGGER DAG'}
          </button>
        </div>
      </header>

      {/* METRICS ROW */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        {[
          { icon: Activity, label: "SUCCESS RATE", value: "99.8%", color: "text-[#39ff14]", border: "border-[#39ff14]/30", glow: "glow-text-green" },
          { icon: CheckCircle2, label: "TOTAL EXECUTIONS", value: "12,456", color: "text-[#00f0ff]", border: "border-[#00f0ff]/30", glow: "glow-text-cyan" },
          { icon: AlertCircle, label: "RETRIES (24H)", value: "14", color: "text-[#ff00ff]", border: "border-[#ff00ff]/30", glow: "glow-text-magenta" },
          { icon: Clock, label: "AVG PIPELINE TIME", value: "14.2m", color: "text-[#00f0ff]", border: "border-[#00f0ff]/30", glow: "" }
        ].map((metric, idx) => (
          <div key={idx} className={`glass-panel p-6 border ${metric.border} flex items-center justify-between`}>
            <div>
              <p className="text-xs text-gray-400 mb-1 tracking-wider">{metric.label}</p>
              <h3 className={`text-2xl font-bold ${metric.color} ${metric.glow}`}>{metric.value}</h3>
            </div>
            <metric.icon className={`w-8 h-8 ${metric.color} opacity-80`} />
          </div>
        ))}
      </div>

      {/* MAIN CONTENT SPLIT */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* LEFT COLUMN: DAG VISUALIZATION */}
        <div className="lg:col-span-2 space-y-6">
          <div className="glass-panel p-6 h-full border-cyan-500/30 relative overflow-hidden">
            <h2 className="text-xl font-semibold mb-6 text-[#00f0ff] flex items-center gap-2">
              <ServerCog className="w-5 h-5" /> RECENT PIPELINE: Transformation_DAG
            </h2>
            
            {/* Airflow Visual Representation */}
            <div className="relative mt-12 mb-8 flex flex-col items-center">
              
              {/* DAG Nodes */}
              <div className="flex justify-center w-full relative z-10">
                <div className="px-6 py-3 bg-[#00f0ff]/10 border border-[#00f0ff] rounded-md text-[#00f0ff] glow-box-cyan text-sm">
                  start_transform
                </div>
              </div>
              
              <div className="w-px h-8 bg-cyan-500/50"></div>
              
              <div className="px-6 py-2 bg-purple-900/30 border border-[#9d00ff] rounded-md text-[#9d00ff] text-sm font-mono border-dashed">
                TaskGroup: wait_for_data
              </div>
              
              <div className="w-full flex justify-center gap-32">
                <div className="w-px h-8 bg-cyan-500/50 border-l border-cyan-500/50 transform -rotate-45 translate-y-4 translate-x-12"></div>
                <div className="w-px h-8 bg-cyan-500/50 border-l border-cyan-500/50 transform rotate-45 translate-y-4 -translate-x-12"></div>
              </div>

              <div className="flex justify-center gap-16 mt-8 w-full z-10">
                <div className="px-4 py-3 bg-[#39ff14]/10 border border-[#39ff14] rounded-md text-[#39ff14] text-xs">
                  [Sensor_Sales]
                </div>
                <div className="px-4 py-3 bg-[#39ff14]/10 border border-[#39ff14] rounded-md text-[#39ff14] text-xs">
                  [Sensor_Inventory]
                </div>
              </div>

              {/* Middle Section omitted for brevity, adding ending node directly for visual representation */}
              
              <div className="w-full flex justify-center gap-32 mt-8">
                <div className="w-px h-12 bg-cyan-500/50 border-l border-cyan-500/50 transform rotate-45 translate-y-2 translate-x-12"></div>
                <div className="w-px h-12 bg-cyan-500/50 border-l border-cyan-500/50 transform -rotate-45 translate-y-2 -translate-x-12"></div>
              </div>

              <div className="px-6 py-3 mt-10 bg-[#00f0ff]/10 border border-[#00f0ff] rounded-md text-[#00f0ff] glow-box-cyan text-sm z-10">
                end_transform
              </div>
            </div>
            
            {/* Overlay Grid effect */}
            <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-5 pointer-events-none"></div>
          </div>
        </div>

        {/* RIGHT COLUMN: GRAPHS & LOGS */}
        <div className="space-y-6 flex flex-col">
          
          <div className="glass-panel p-6 border-cyan-500/30 flex-1">
            <h2 className="text-lg font-semibold mb-4 text-[#ff00ff] glow-text-magenta">DATA THROUGHPUT (GB/h)</h2>
            <div className="h-48">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={mockExecutionData}>
                  <defs>
                    <linearGradient id="colorLoad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#ff00ff" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#ff00ff" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="time" stroke="#00f0ff" fontSize={12} tickLine={false} axisLine={false} />
                  <Tooltip contentStyle={{ backgroundColor: '#02000f', borderColor: '#ff00ff', color: '#fff' }} />
                  <Area type="monotone" dataKey="load" stroke="#ff00ff" fillOpacity={1} fill="url(#colorLoad)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="glass-panel p-6 border-green-500/30 flex-1">
            <h2 className="text-lg font-semibold mb-4 text-[#39ff14] glow-text-green">EXECUTION TIME (mins)</h2>
            <div className="h-48">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={mockExecutionData}>
                  <XAxis dataKey="time" stroke="#39ff14" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis stroke="#39ff14" fontSize={12} tickLine={false} axisLine={false} />
                  <Tooltip contentStyle={{ backgroundColor: '#02000f', borderColor: '#39ff14', color: '#fff' }} />
                  <Line type="stepAfter" dataKey="duration" stroke="#39ff14" strokeWidth={3} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
