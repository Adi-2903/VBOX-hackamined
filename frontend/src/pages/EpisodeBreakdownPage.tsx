import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    ArrowLeft,
    Activity,
    Flame,
    AlertTriangle,
    CheckCircle2,
    Wand2,
    Download,
    PlaySquare,
    Zap
} from 'lucide-react';

// Narrative Arc Data (Continuing the Deep Sea Prompt)
const episodeData = [
    {
        id: 1,
        title: "The Dry Room",
        duration: "90s",
        health: "optimal",
        summary: "Diver descends into the Mariana Trench. Communications fail. Suddenly, sonar detects a geometric cube. He breaches it to find a completely dry, oxygen-rich 1800s study. In the center sits a modern smartphone.",
        cliffhanger: { score: 94, text: "The unplugged smartphone begins to ring." },
        retentionTimeline: [80, 85, 90, 88, 85, 82, 90, 95, 100], // 10-sec blocks
        riskZone: null,
        suggestion: null
    },
    {
        id: 2,
        title: "The Caller ID",
        duration: "85s",
        health: "risk",
        summary: "The diver hesitates, staring at the ringing phone. He checks his own depth gauge—it makes no sense. He walks slowly toward the desk. He picks up the phone and looks at the caller ID.",
        cliffhanger: { score: 72, text: "It's his daughter, supposed to be asleep on the surface." },
        retentionTimeline: [90, 85, 70, 60, 55, 65, 70, 80, 85],
        riskZone: { start: "0:30", end: "0:50", reason: "Excessive hesitation/internal monologue. Pacing stalls." },
        suggestion: "Cut the depth-gauge check. Accelerate the walk to the desk by 15 seconds to bridge the curiosity gap faster."
    },
    {
        id: 3,
        title: "The Voice",
        duration: "90s",
        health: "optimal",
        summary: "He answers. It's his daughter, but she sounds older. She frantically warns him not to turn around. He asks what she means. She says 'The crack is already behind you.'",
        cliffhanger: { score: 98, text: "The sound of glass splintering directly behind his helmet." },
        retentionTimeline: [85, 88, 92, 95, 94, 96, 98, 99, 100],
        riskZone: null,
        suggestion: null
    },
    {
        id: 4,
        title: "The Breach",
        duration: "88s",
        health: "risk",
        summary: "He turns. A hairline fracture in the seemingly impenetrable glass wall is leaking water. He tries to find a way to plug it, searching the 1800s desk for tools, panicking.",
        cliffhanger: { score: 65, text: "The water reaches his ankles." },
        retentionTimeline: [100, 95, 90, 80, 75, 75, 70, 68, 65],
        riskZone: { start: "0:50", end: "0:90", reason: "Action feels repetitive. The stakes plateau instead of escalating." },
        suggestion: "Heuristics flag weak hook. Introduce a secondary threat—the lights shorting out as the water rises. Change cliffhanger to pitch blackness."
    },
    {
        id: 5,
        title: "The Loop",
        duration: "90s",
        health: "optimal",
        summary: "Pitch black. Water at his chest. He realizes the phone is still connected. He speaks to his daughter one last time, realizing she wasn't warning him—she was giving him the exact time of his death.",
        cliffhanger: { score: 95, text: "Final dial tone as the room implodes. Series End." },
        retentionTimeline: [70, 75, 85, 90, 95, 98, 99, 100, 100],
        riskZone: null,
        suggestion: null
    }
];

const EpisenseDashboard = () => {
    const navigate = useNavigate();
    const [activeEp, setActiveEp] = useState(episodeData[0]);
    const [fixedEpisodes, setFixedEpisodes] = useState(new Set()); // Track applied suggestions
    const [isExporting, setIsExporting] = useState(false);

    const isFixed = fixedEpisodes.has(activeEp.id);
    const currentRisk = isFixed ? null : activeEp.riskZone;
    const handleApplyFix = () => {
        setFixedEpisodes(new Set(fixedEpisodes).add(activeEp.id));
    };

    const currentHookScore = isFixed ? Math.min(100, activeEp.cliffhanger.score + 25) : activeEp.cliffhanger.score;

    const handleExport = () => {
        setIsExporting(true);
        setTimeout(() => setIsExporting(false), 2000);
    };

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
                            onClick={() => navigate('/')}
                            className="w-12 h-12 bg-white border-4 border-[#0A192F] rounded-full flex items-center justify-center hover:bg-[#D4FF33] active:translate-y-[2px] transition-all shadow-[4px_4px_0px_#0A192F] flex-shrink-0">
                            <ArrowLeft className="w-6 h-6" />
                        </button>
                        <div>
                            <div className="flex items-center gap-2 mb-1">
                                <span className="bg-[#0A192F] text-[#D4FF33] px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-widest">Project: VBOX_DeepSea</span>
                            </div>
                            <h1 className="text-3xl font-black tracking-tight leading-none">Intelligence Dashboard</h1>
                        </div>
                    </div>

                    <button
                        onClick={handleExport}
                        disabled={isExporting}
                        className="w-full md:w-auto bg-[#33A1FF] border-4 border-[#0A192F] text-[#0A192F] px-6 py-3 rounded-full font-black text-sm uppercase tracking-wide shadow-[4px_4px_0px_#0A192F] hover:shadow-[6px_6px_0px_#0A192F] hover:-translate-y-1 active:translate-y-[2px] active:shadow-none transition-all flex items-center justify-center gap-2"
                    >
                        {isExporting ? <span className="animate-pulse">Rendering Arc...</span> : <><Download className="w-5 h-5" /> Export to VBOX</>}
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
                                            navigate('/suggestions');
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

            {/* Embedded Styles */}
            <style dangerouslySetInnerHTML={{
                __html: `
        /* Hide scrollbar for the minimap */
        .hide-scrollbar::-webkit-scrollbar {
          display: none;
        }
        .hide-scrollbar {
          -ms-overflow-style: none;
          scrollbar-width: none;
        }
        
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        
        .animate-fade-in {
          animation: fadeIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
        }
      `}} />
        </div>
    );
};

export default EpisenseDashboard;