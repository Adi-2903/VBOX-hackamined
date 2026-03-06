import { useState, useMemo, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
    ArrowLeft,
    Activity,
    Flame,
    AlertTriangle,
    CheckCircle2,
    Wand2,
    PlaySquare,
    Zap
} from 'lucide-react';
import type { GeneratedSeries, SeriesAnalysis } from '../services/api';

// Fallback mock data when no API data is available
const fallbackEpisodeData = [
    {
        id: 1, title: "The Dry Room", duration: "90s", health: "optimal",
        summary: "Diver descends into the Mariana Trench. Communications fail. Suddenly, sonar detects a geometric cube.",
        cliffhanger: { score: 94, text: "The unplugged smartphone begins to ring." },
        retentionTimeline: [80, 85, 90, 88, 85, 82, 90, 95, 100],
        riskZone: null, suggestion: null,
    },
    {
        id: 2, title: "The Caller ID", duration: "85s", health: "risk",
        summary: "The diver hesitates, staring at the ringing phone. He picks it up and looks at the caller ID.",
        cliffhanger: { score: 72, text: "It's his daughter, supposed to be asleep on the surface." },
        retentionTimeline: [90, 85, 70, 60, 55, 65, 70, 80, 85],
        riskZone: { start: "0:30", end: "0:50", reason: "Pacing stalls." },
        suggestion: "Accelerate the walk to the desk by 15 seconds.",
    },
];

const EpisodeBreakdownPage = () => {
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => { document.title = 'Episode Breakdown — VBOX Episense'; }, []);

    // Read data from Router state (passed from StoryInputPage)
    const routerState = location.state as {
        series?: GeneratedSeries;
        analysis?: SeriesAnalysis;
    } | null;

    // Map API data to component's episode format
    const episodeData = useMemo(() => {
        if (!routerState?.series || !routerState?.analysis) return fallbackEpisodeData;

        return routerState.series.episodes.map((ep, idx) => {
            const meta = routerState.analysis!.episodes[idx];
            const a = meta?.analysis;
            const highRiskSeg = a?.features?.dropoff_prediction?.segments?.find(s => s.dropoff_risk > 0.4);
            return {
                id: ep.episode_number,
                title: ep.title,
                duration: "90s",
                health: a?.retention?.risk_level === "HIGH" ? "risk" : "optimal",
                summary: ep.story.slice(0, 250) + (ep.story.length > 250 ? "..." : ""),
                cliffhanger: {
                    score: a ? Math.round(a.cliffhanger.cliffhanger_score * 10) : 80,
                    text: ep.cliffhanger,
                },
                retentionTimeline: a?.features?.dropoff_prediction?.segments
                    ? a.features.dropoff_prediction.segments.map(s => Math.round(s.engagement_score * 100))
                    : [80, 85, 90, 88, 85, 82, 90, 95, 100],
                riskZone: highRiskSeg
                    ? { start: highRiskSeg.label.split("(")[1]?.split("-")[0] || "0:00", end: highRiskSeg.label.split("-")[1]?.replace(")", "") || "0:90", reason: `Drop-off risk ${Math.round(highRiskSeg.dropoff_risk * 100)}% in ${highRiskSeg.label} segment.` }
                    : null,
                suggestion: a?.retention?.recommendations?.[0]?.suggestion || null,
            };
        });
    }, [routerState]);

    const [activeEp, setActiveEp] = useState(episodeData[0]);
    const [fixedEpisodes, setFixedEpisodes] = useState(new Set());

    const isFixed = fixedEpisodes.has(activeEp.id);
    const currentRisk = isFixed ? null : activeEp.riskZone;
    const handleApplyFix = () => {
        setFixedEpisodes(new Set(fixedEpisodes).add(activeEp.id));
    };

    const currentHookScore = isFixed ? Math.min(100, activeEp.cliffhanger.score + 25) : activeEp.cliffhanger.score;

    return (
        <div className="min-h-screen bg-[#FDFBF7] text-[#0A192F] font-sans relative overflow-x-hidden selection:bg-[#33A1FF] selection:text-[#0A192F] pb-20">

            {/* Neo-Pop Grid Background */}
            <div className="fixed inset-0 z-0 pointer-events-none opacity-[0.1]"
                style={{ backgroundImage: 'linear-gradient(#0A192F 2px, transparent 2px), linear-gradient(90deg, #0A192F 2px, transparent 2px)', backgroundSize: '40px 40px' }}>
            </div>

            <div className="max-w-7xl mx-auto px-4 md:px-6 pt-6 relative z-10 flex flex-col h-full">

                {/* Top Navbar */}
                <header className="flex flex-col md:flex-row items-start md:items-center justify-between mb-8 gap-4">
                    <div className="flex items-center gap-4">
                        <button
                            onClick={() => navigate('/input')}
                            className="w-12 h-12 bg-white border-4 border-[#0A192F] rounded-full flex items-center justify-center hover:bg-[#D4FF33] active:translate-y-[2px] transition-all shadow-[4px_4px_0px_#0A192F] flex-shrink-0">
                            <ArrowLeft className="w-6 h-6" />
                        </button>
                        <div>
                            <div className="flex items-center gap-2 mb-1">
                                <span className="bg-[#0A192F] text-[#D4FF33] px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-widest">{routerState?.series ? `Project: ${routerState.series.direction}` : 'Episode Breakdown'}</span>
                            </div>
                            <h1 className="text-3xl font-black tracking-tight leading-none">Intelligence Dashboard</h1>
                        </div>
                    </div>

                    <button
                        onClick={() => navigate('/analytics', { state: { analysis: routerState?.analysis, series: routerState?.series } })}
                        className="w-full md:w-auto bg-[#33A1FF] border-4 border-[#0A192F] text-[#0A192F] px-6 py-3 rounded-full font-black text-sm uppercase tracking-wide shadow-[4px_4px_0px_#0A192F] hover:shadow-[6px_6px_0px_#0A192F] hover:-translate-y-1 active:translate-y-[2px] active:shadow-none transition-all flex items-center justify-center gap-2"
                    >
                        <Activity className="w-5 h-5" /> Analyze Series
                    </button>
                </header>

                {/* The Minimap (Horizontal Episode Strip) */}
                <div className="flex gap-4 overflow-x-auto pb-6 hide-scrollbar snap-x">
                    {episodeData.map((ep) => {
                        const isActive = activeEp.id === ep.id;
                        const hasRisk = ep.health === 'risk' && !fixedEpisodes.has(ep.id);

                        return (
                            <button
                                key={ep.id}
                                onClick={() => setActiveEp(ep)}
                                className={`snap-start flex-shrink-0 w-48 text-left transition-all duration-300 rounded-3xl border-4 shadow-[4px_4px_0px_#0A192F] p-4 relative overflow-hidden group
                  ${isActive ? 'bg-[#D4FF33] border-[#0A192F] scale-100' : 'bg-white border-[#0A192F] hover:bg-[#FDFBF7] scale-95 hover:scale-100'}`}
                            >
                                {/* Risk Indicator Pip */}
                                {hasRisk && (
                                    <div className="absolute top-3 right-3 w-3 h-3 bg-[#FF9E9E] border-2 border-[#0A192F] rounded-full animate-pulse"></div>
                                )}

                                <div className="font-mono text-xs font-black uppercase mb-2 opacity-60">Part {ep.id}</div>
                                <h3 className="font-black text-xl leading-none tracking-tight mb-4 truncate">{ep.title}</h3>

                                <div className="flex justify-between items-end">
                                    <div className="font-mono text-[10px] font-bold uppercase bg-white border-2 border-[#0A192F] px-2 py-1 rounded shadow-[2px_2px_0px_#0A192F]">
                                        {ep.duration}
                                    </div>
                                    {hasRisk ? (
                                        <AlertTriangle className="w-5 h-5 text-[#FF4D4D]" />
                                    ) : (
                                        <CheckCircle2 className="w-5 h-5 text-[#0A192F]" />
                                    )}
                                </div>
                            </button>
                        );
                    })}
                </div>

                {/* Active Episode Detail View (Bento Grid) */}
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 animate-fade-in key-ep">

                    {/* Left Column: Script & Summary (7 cols) */}
                    <div className="lg:col-span-7 flex flex-col gap-6">

                        <div className="bg-white border-4 border-[#0A192F] rounded-[2.5rem] p-6 shadow-[8px_8px_0px_#0A192F] flex-1 flex flex-col">
                            <div className="flex items-center gap-3 mb-6">
                                <div className="w-10 h-10 bg-[#C7B9FF] border-2 border-[#0A192F] rounded-full flex items-center justify-center shadow-[2px_2px_0px_#0A192F]">
                                    <PlaySquare className="w-5 h-5 text-[#0A192F]" />
                                </div>
                                <h2 className="text-2xl font-black uppercase tracking-tight">Narrative Block</h2>
                            </div>

                            <div className="flex-1 bg-[#FDFBF7] border-4 border-[#0A192F] rounded-3xl p-6 relative group">
                                {/* Simulated editable script area */}
                                <textarea
                                    value={activeEp.summary}
                                    readOnly
                                    className="w-full h-full min-h-[150px] bg-transparent resize-none focus:outline-none text-xl md:text-2xl font-bold leading-relaxed text-[#0A192F] selection:bg-[#FF9E9E]"
                                />
                                <button className="absolute top-4 right-4 bg-white border-2 border-[#0A192F] rounded-full px-4 py-2 text-xs font-black uppercase shadow-[2px_2px_0px_#0A192F] hover:bg-[#D4FF33] transition-colors opacity-0 group-hover:opacity-100">
                                    Edit Script
                                </button>
                            </div>
                        </div>

                        {/* Cliffhanger Scoring Box */}
                        <div className="bg-[#FF9E9E] border-4 border-[#0A192F] rounded-[2rem] p-6 shadow-[8px_8px_0px_#0A192F] flex flex-col md:flex-row gap-6 items-center">
                            <div className="flex-1">
                                <div className="flex items-center gap-2 mb-2 text-[#0A192F]">
                                    <Flame className="w-5 h-5 fill-current" />
                                    <span className="font-black uppercase tracking-tight">Hook Score</span>
                                </div>
                                <div className="bg-white border-4 border-[#0A192F] rounded-2xl p-4 shadow-inner text-lg font-bold">
                                    "{activeEp.cliffhanger.text}"
                                </div>
                            </div>

                            <div className="w-32 h-32 bg-white border-4 border-[#0A192F] rounded-full flex flex-col items-center justify-center shadow-[4px_4px_0px_#0A192F] flex-shrink-0 relative overflow-hidden">
                                {/* Visual indicator of score */}
                                <div
                                    className="absolute bottom-0 w-full bg-[#0A192F] transition-all duration-1000 ease-out"
                                    style={{ height: `${currentHookScore}%`, opacity: 0.1 }}
                                ></div>
                                <span className="font-black text-5xl tracking-tighter relative z-10">{currentHookScore}</span>
                                <span className="font-mono text-[10px] font-bold uppercase relative z-10">/ 100</span>
                            </div>
                        </div>

                    </div>

                    {/* Right Column: Intelligence & Analytics (5 cols) */}
                    <div className="lg:col-span-5 flex flex-col gap-6">

                        {/* The 90s Radar (Timeline Visualization) */}
                        <div className="bg-[#0A192F] text-white border-4 border-[#0A192F] rounded-[2.5rem] p-6 shadow-[8px_8px_0px_#33A1FF]">
                            <div className="flex justify-between items-center mb-6">
                                <h3 className="text-xl font-black uppercase tracking-tight flex items-center gap-2">
                                    <Activity className="w-5 h-5 text-[#33A1FF]" />
                                    90s Radar
                                </h3>
                                <span className="bg-[#33A1FF]/20 text-[#33A1FF] border border-[#33A1FF]/50 px-2 py-1 rounded text-[10px] font-mono font-bold uppercase">
                                    ML Retention Model
                                </span>
                            </div>

                            {/* CapCut style timeline graphic */}
                            <div className="relative h-32 bg-[#1a2b4a] border-2 border-white/10 rounded-2xl p-2 flex items-end gap-1 mb-4 overflow-hidden">
                                {/* Background Grid */}
                                <div className="absolute inset-0 grid grid-cols-3 opacity-20 pointer-events-none">
                                    <div className="border-r border-white border-dashed"></div>
                                    <div className="border-r border-white border-dashed"></div>
                                </div>

                                {/* Risk Overlay */}
                                {currentRisk && (
                                    <div className="absolute top-0 bottom-0 bg-[#FF4D4D]/20 border-x-2 border-[#FF4D4D] z-10 animate-pulse"
                                        style={{ left: '30%', right: '10%' }}>
                                    </div>
                                )}

                                {/* Audio/Pacing Bars */}
                                {activeEp.retentionTimeline.map((val, i) => {
                                    const isRiskArea = currentRisk && i >= 3 && i <= 7;
                                    return (
                                        <div
                                            key={i}
                                            className={`flex-1 rounded-sm transition-all duration-500 relative z-20 ${isRiskArea ? 'bg-[#FF9E9E]' : 'bg-[#33A1FF]'}`}
                                            style={{ height: `${val}%` }}
                                        ></div>
                                    );
                                })}
                            </div>

                            <div className="flex justify-between font-mono text-[10px] text-white/50 font-bold">
                                <span>0:00</span>
                                <span>0:45</span>
                                <span>1:30</span>
                            </div>
                        </div>

                        {/* Optimisation Engine Box */}
                        <div className={`flex-1 border-4 border-[#0A192F] rounded-[2.5rem] p-6 shadow-[8px_8px_0px_#0A192F] transition-colors duration-500
              ${currentRisk ? 'bg-white' : 'bg-[#D4FF33]'}`}>

                            <div className="flex items-center gap-3 mb-6">
                                <div className="w-10 h-10 bg-[#0A192F] rounded-full flex items-center justify-center shadow-[2px_2px_0px_#0A192F]">
                                    <Zap className={`w-5 h-5 ${currentRisk ? 'text-[#FF9E9E]' : 'text-[#D4FF33]'}`} />
                                </div>
                                <h3 className="text-xl font-black uppercase tracking-tight">Suggestion Engine</h3>
                            </div>

                            {currentRisk ? (
                                <div className="animate-fade-in">
                                    <div className="inline-flex items-center gap-2 bg-[#FF9E9E] border-2 border-[#0A192F] px-3 py-1 rounded-full text-[10px] font-black uppercase mb-4 shadow-[2px_2px_0px_#0A192F]">
                                        <span className="w-2 h-2 rounded-full bg-[#0A192F] animate-pulse"></span>
                                        Drop-off Risk ({currentRisk.start} - {currentRisk.end})
                                    </div>

                                    <p className="font-bold text-[#0A192F] leading-snug mb-6 bg-[#FDFBF7] p-4 border-2 border-[#0A192F] rounded-2xl">
                                        "{activeEp.suggestion}"
                                    </p>

                                    <button
                                        onClick={() => {
                                            handleApplyFix();
                                            navigate('/suggestions', { state: { analysis: routerState?.analysis, series: routerState?.series } });
                                        }}
                                        className="w-full bg-[#D4FF33] border-4 border-[#0A192F] text-[#0A192F] px-4 py-4 rounded-2xl font-black uppercase tracking-wide shadow-[4px_4px_0px_#0A192F] hover:-translate-y-1 active:translate-y-[2px] active:shadow-none transition-all flex items-center justify-center gap-2"
                                    >
                                        <Wand2 className="w-5 h-5" /> Open Suggestion Engine
                                    </button>
                                </div>
                            ) : (
                                <div className="h-full flex flex-col items-center justify-center text-center animate-fade-in p-4">
                                    <CheckCircle2 className="w-16 h-16 text-[#0A192F] mb-4" />
                                    <h4 className="text-2xl font-black uppercase tracking-tight mb-2">Arc Optimized</h4>
                                    <p className="font-medium text-[#0A192F]/70 text-sm">Pacing and retention models indicate maximum viewer completion rate.</p>
                                </div>
                            )}
                        </div>

                    </div>
                </div>
            </div>

        </div>
    );
};

export default EpisodeBreakdownPage;