import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Activity,
    Flame,
    ArrowLeft,
    Download,
    AlertTriangle,
    Eye,
    Wand2
} from 'lucide-react';

const EpisenseAnalytics = () => {
    const navigate = useNavigate();
    const [isLoaded, setIsLoaded] = useState(false);
    const [activeEpisodeHover, setActiveEpisodeHover] = useState<number | null>(null);

    useEffect(() => {
        // Trigger entry animations
        setIsLoaded(true);
    }, []);

    // Mock Data for the 5-Episode Arc
    const seriesData = {
        globalScore: 88,
        projectedCompletion: "74%",
        flatZones: 2,
        episodes: [
            { id: 1, title: "The Descent", sentiment: 80, hook: 94, riskLevel: "Low", dropTime: null },
            { id: 2, title: "The Dry Room", sentiment: 30, hook: 72, riskLevel: "High", dropTime: "0:42" },
            { id: 3, title: "The Ringing", sentiment: 90, hook: 98, riskLevel: "Low", dropTime: null },
            { id: 4, title: "The Paradox", sentiment: 20, hook: 65, riskLevel: "Critical", dropTime: "0:60" },
            { id: 5, title: "The Loop", sentiment: 100, hook: 95, riskLevel: "Low", dropTime: null }
        ]
    };

    // Calculate SVG Path for Emotional Arc (Rollercoaster effect)
    const generatePath = () => {
        // Smooth bezier curve approximation
        return `M 0,${100 - seriesData.episodes[0].sentiment} 
            C 20,${100 - seriesData.episodes[0].sentiment} 
              15,${100 - seriesData.episodes[1].sentiment} 
              25,${100 - seriesData.episodes[1].sentiment}
            S 40,${100 - seriesData.episodes[2].sentiment} 
              50,${100 - seriesData.episodes[2].sentiment}
            S 65,${100 - seriesData.episodes[3].sentiment} 
              75,${100 - seriesData.episodes[3].sentiment}
            S 90,${100 - seriesData.episodes[4].sentiment} 
              100,${100 - seriesData.episodes[4].sentiment}`;
    };

    return (
        <div className="min-h-screen bg-[#FDFBF7] text-[#0A192F] font-sans relative overflow-x-hidden selection:bg-[#D4FF33] selection:text-[#0A192F] pb-24">

            {/* Neo-Pop Grid Background */}
            <div className="fixed inset-0 z-0 pointer-events-none opacity-[0.15]"
                style={{ backgroundImage: 'radial-gradient(#0A192F 2px, transparent 2px)', backgroundSize: '32px 32px' }}>
            </div>

            <div className="max-w-7xl mx-auto px-4 md:px-6 pt-8 relative z-10">

                {/* Navigation & Header */}
                <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-10 gap-6">
                    <div className="flex items-center gap-4">
                        <button
                            onClick={() => navigate(-1)}
                            className="w-12 h-12 bg-white border-4 border-[#0A192F] rounded-full flex items-center justify-center hover:bg-[#FF9E9E] hover:-translate-y-1 transition-all shadow-[4px_4px_0px_#0A192F] active:translate-y-[2px] active:shadow-none flex-shrink-0 group">
                            <ArrowLeft className="w-6 h-6 group-hover:-translate-x-1 transition-transform" />
                        </button>
                        <div>
                            <div className="flex items-center gap-3 mb-1">
                                <span className="bg-[#D4FF33] border-2 border-[#0A192F] rounded-full px-3 py-0.5 text-[10px] font-black uppercase tracking-widest shadow-[2px_2px_0px_#0A192F]">Intelligence Report</span>
                                <span className="text-[#0A192F]/50 font-bold text-sm uppercase">VBOX_DeepSea</span>
                            </div>
                            <h1 className="text-4xl md:text-5xl font-black tracking-tight leading-none">Series Analytics.</h1>
                        </div>
                    </div>

                    <button className="bg-[#0A192F] text-white border-4 border-[#0A192F] rounded-full px-6 py-3 font-black text-sm uppercase tracking-wide shadow-[4px_4px_0px_#33A1FF] hover:shadow-[6px_6px_0px_#33A1FF] hover:-translate-y-1 active:translate-y-[2px] active:shadow-none transition-all flex items-center gap-2">
                        <Download className="w-5 h-5" /> Export PDF Report
                    </button>
                </header>

                {/* Top KPI Bento Boxes */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">

                    {/* Completion Rate KPI */}
                    <div className={`bg-[#33A1FF] text-white border-4 border-[#0A192F] rounded-[2rem] p-6 shadow-[6px_6px_0px_#0A192F] flex flex-col justify-between transition-all duration-700 ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
                        <div className="flex justify-between items-start mb-4">
                            <div className="w-12 h-12 bg-white border-4 border-[#0A192F] rounded-full flex items-center justify-center shadow-[2px_2px_0px_#0A192F]">
                                <Eye className="w-6 h-6 text-[#33A1FF]" />
                            </div>
                            <span className="bg-white/20 border-2 border-white/40 px-3 py-1 rounded-full text-xs font-black uppercase tracking-wider backdrop-blur-sm">Avg. Retention</span>
                        </div>
                        <div>
                            <div className="text-5xl font-black tracking-tighter mb-1">{seriesData.projectedCompletion}</div>
                            <p className="font-bold text-white/80 text-sm">Predicted viewer completion rate across 5 episodes.</p>
                        </div>
                    </div>

                    {/* Hook Score KPI */}
                    <div className={`bg-[#FF9E9E] border-4 border-[#0A192F] rounded-[2rem] p-6 shadow-[6px_6px_0px_#0A192F] flex flex-col justify-between transition-all duration-700 delay-100 ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
                        <div className="flex justify-between items-start mb-4">
                            <div className="w-12 h-12 bg-white border-4 border-[#0A192F] rounded-full flex items-center justify-center shadow-[2px_2px_0px_#0A192F]">
                                <Flame className="w-6 h-6 text-[#FF4D4D] fill-current" />
                            </div>
                            <span className="bg-white/40 border-2 border-[#0A192F] px-3 py-1 rounded-full text-xs font-black uppercase tracking-wider">Global Hook</span>
                        </div>
                        <div>
                            <div className="flex items-baseline gap-1 mb-1">
                                <span className="text-5xl font-black tracking-tighter">{seriesData.globalScore}</span>
                                <span className="text-xl font-bold opacity-60">/100</span>
                            </div>
                            <p className="font-bold text-[#0A192F]/70 text-sm">Average cliffhanger heuristic score.</p>
                        </div>
                    </div>

                    {/* Risk KPI */}
                    <div className={`bg-[#D4FF33] border-4 border-[#0A192F] rounded-[2rem] p-6 shadow-[6px_6px_0px_#0A192F] flex flex-col justify-between transition-all duration-700 delay-200 ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
                        <div className="flex justify-between items-start mb-4">
                            <div className="w-12 h-12 bg-white border-4 border-[#0A192F] rounded-full flex items-center justify-center shadow-[2px_2px_0px_#0A192F]">
                                <AlertTriangle className="w-6 h-6 text-[#0A192F]" />
                            </div>
                            <span className="bg-white/40 border-2 border-[#0A192F] px-3 py-1 rounded-full text-xs font-black uppercase tracking-wider">Flat Zones</span>
                        </div>
                        <div>
                            <div className="text-5xl font-black tracking-tighter mb-1 text-[#FF4D4D]">{seriesData.flatZones}</div>
                            <p className="font-bold text-[#0A192F]/70 text-sm">Critical engagement drops requiring script edits.</p>
                        </div>
                    </div>

                </div>

                {/* Main Analytics Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">

                    {/* Emotional Arc Visualizer (Spans 8 Cols) */}
                    <div className={`lg:col-span-8 bg-white border-4 border-[#0A192F] rounded-[2.5rem] p-6 md:p-8 shadow-[8px_8px_0px_#0A192F] flex flex-col transition-all duration-1000 delay-300 ${isLoaded ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-10'}`}>

                        <div className="flex justify-between items-start mb-8">
                            <div>
                                <h2 className="text-3xl font-black uppercase tracking-tight flex items-center gap-3 mb-2">
                                    <Activity className="w-8 h-8 text-[#C7B9FF]" />
                                    Emotional Arc
                                </h2>
                                <p className="font-bold text-[#0A192F]/60 text-sm">Sentiment analysis trajectory across the 5-part series.</p>
                            </div>
                            <div className="hidden sm:flex gap-2">
                                <span className="flex items-center gap-2 text-[10px] font-black uppercase bg-[#FDFBF7] border-2 border-[#0A192F] px-2 py-1 rounded-lg"><div className="w-2 h-2 bg-[#D4FF33] rounded-full"></div> Peak</span>
                                <span className="flex items-center gap-2 text-[10px] font-black uppercase bg-[#FDFBF7] border-2 border-[#0A192F] px-2 py-1 rounded-lg"><div className="w-2 h-2 bg-[#FF9E9E] rounded-full"></div> Valley</span>
                            </div>
                        </div>

                        {/* Custom SVG Chart Area */}
                        <div className="flex-1 relative min-h-[250px] w-full mt-4 bg-[#FDFBF7] border-4 border-[#0A192F] rounded-3xl p-4 overflow-hidden group">

                            {/* Grid Lines */}
                            <div className="absolute inset-0 flex flex-col justify-between p-4 opacity-10 pointer-events-none">
                                <div className="border-t-2 border-[#0A192F] w-full"></div>
                                <div className="border-t-2 border-[#0A192F] w-full"></div>
                                <div className="border-t-2 border-[#0A192F] w-full"></div>
                                <div className="border-t-2 border-[#0A192F] w-full"></div>
                            </div>

                            {/* The SVG Line */}
                            <svg className="absolute inset-0 w-full h-full px-8 py-8 overflow-visible" preserveAspectRatio="none">
                                <path
                                    d={generatePath()}
                                    fill="none"
                                    stroke="#0A192F"
                                    strokeWidth="6"
                                    vectorEffect="non-scaling-stroke"
                                    className="animate-draw drop-shadow-[4px_4px_0px_#C7B9FF]"
                                />
                            </svg>

                            {/* Interactive Data Points */}
                            <div className="absolute inset-0 px-8 py-8 flex justify-between">
                                {seriesData.episodes.map((ep) => (
                                    <div
                                        key={ep.id}
                                        className="relative h-full flex flex-col"
                                        onMouseEnter={() => setActiveEpisodeHover(ep.id)}
                                        onMouseLeave={() => setActiveEpisodeHover(null)}
                                    >
                                        {/* The physical dot */}
                                        <div
                                            className={`absolute w-6 h-6 border-4 border-[#0A192F] rounded-full transform -translate-x-1/2 -translate-y-1/2 cursor-pointer transition-all duration-300 z-10
                        ${ep.sentiment > 50 ? 'bg-[#D4FF33]' : 'bg-[#FF9E9E]'}
                        ${activeEpisodeHover === ep.id ? 'scale-150 shadow-[4px_4px_0px_#0A192F]' : 'shadow-[2px_2px_0px_#0A192F]'}
                      `}
                                            style={{ top: `${100 - ep.sentiment}%`, left: '0' }}
                                        ></div>

                                        {/* Tooltip */}
                                        <div className={`absolute bottom-full left-1/2 transform -translate-x-1/2 mb-4 w-48 bg-white border-4 border-[#0A192F] rounded-2xl p-3 shadow-[6px_6px_0px_#0A192F] transition-all duration-200 z-20 pointer-events-none
                      ${activeEpisodeHover === ep.id ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}
                                        >
                                            <div className="text-[10px] font-black uppercase text-[#0A192F]/50 mb-1">Episode {ep.id}</div>
                                            <div className="font-bold text-sm leading-tight mb-2">{ep.title}</div>
                                            <div className="flex justify-between items-center text-xs">
                                                <span className="font-black text-[#C7B9FF]">Vibe:</span>
                                                <span className="font-mono font-bold">{ep.sentiment}%</span>
                                            </div>
                                        </div>

                                        {/* X-Axis Label */}
                                        <div className="absolute bottom-[-30px] left-1/2 transform -translate-x-1/2 text-xs font-black uppercase tracking-wider">
                                            Ep {ep.id}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                    </div>

                    {/* Retention Risk & Cliffhanger Stack (Spans 4 Cols) */}
                    <div className="lg:col-span-4 flex flex-col gap-6">

                        {/* Cliffhanger Leaderboard */}
                        <div className={`bg-white border-4 border-[#0A192F] rounded-[2.5rem] p-6 shadow-[8px_8px_0px_#0A192F] flex-1 transition-all duration-1000 delay-400 ${isLoaded ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-10'}`}>
                            <h2 className="text-2xl font-black uppercase tracking-tight flex items-center gap-3 mb-6">
                                <Flame className="w-6 h-6 text-[#FF4D4D] fill-current" />
                                Hook Ranking
                            </h2>

                            <div className="space-y-4">
                                {/* Sort episodes by hook score to create leaderboard */}
                                {[...seriesData.episodes].sort((a, b) => b.hook - a.hook).map((ep, idx) => (
                                    <div key={ep.id} className="flex items-center gap-4 group">
                                        <div className={`w-8 h-8 rounded-full border-2 border-[#0A192F] flex items-center justify-center font-black text-sm shadow-[2px_2px_0px_#0A192F] flex-shrink-0
                      ${idx === 0 ? 'bg-[#D4FF33]' : idx === 4 ? 'bg-[#FF9E9E]' : 'bg-[#FDFBF7]'}`}>
                                            {idx + 1}
                                        </div>

                                        <div className="flex-1">
                                            <div className="flex justify-between items-center mb-1">
                                                <span className="font-bold text-sm truncate pr-2">Ep {ep.id}: {ep.title}</span>
                                                <span className="font-mono font-black text-sm">{ep.hook}</span>
                                            </div>
                                            <div className="h-2 w-full bg-[#FDFBF7] border border-[#0A192F] rounded-full overflow-hidden">
                                                <div
                                                    className={`h-full border-r border-[#0A192F] transition-all duration-1000 delay-[1000ms] ${idx === 4 ? 'bg-[#FF4D4D]' : 'bg-[#0A192F]'}`}
                                                    style={{ width: isLoaded ? `${ep.hook}%` : '0%' }}
                                                ></div>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Critical Risk Alert Box */}
                        <div className={`bg-[#0A192F] text-white border-4 border-[#0A192F] rounded-[2.5rem] p-6 shadow-[8px_8px_0px_#FF4D4D] transition-all duration-1000 delay-500 relative overflow-hidden ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
                            {/* Warning stripes background */}
                            <div className="absolute inset-0 opacity-10 pointer-events-none" style={{ backgroundImage: 'repeating-linear-gradient(45deg, transparent, transparent 10px, #FF4D4D 10px, #FF4D4D 20px)' }}></div>

                            <div className="relative z-10">
                                <div className="inline-flex items-center gap-2 bg-[#FF4D4D] text-white border-2 border-white px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest mb-4 shadow-[2px_2px_0px_#fff]">
                                    <span className="w-2 h-2 rounded-full bg-white animate-pulse"></span>
                                    Action Required
                                </div>

                                <h3 className="text-2xl font-black mb-2">High Retention Risk</h3>
                                <p className="font-medium text-white/70 text-sm mb-6">
                                    ML Prediction flags a massive viewer drop-off in <strong className="text-[#FF9E9E]">Episode 4 @ 0:60</strong> due to pacing stall.
                                </p>

                                <button
                                    onClick={() => navigate('/suggestions')}
                                    className="w-full bg-[#D4FF33] border-2 border-white text-[#0A192F] font-black uppercase text-sm py-3 rounded-xl flex items-center justify-center gap-2 hover:bg-white transition-colors">
                                    <Wand2 className="w-4 h-4" /> Open Suggestion Engine
                                </button>
                            </div>
                        </div>

                    </div>
                </div>

            </div>

            {/* Embedded CSS for custom neo-pop animations */}
            <style dangerouslySetInnerHTML={{
                __html: `
        @keyframes draw {
          from { stroke-dashoffset: 1000; }
          to { stroke-dashoffset: 0; }
        }
        
        .animate-draw {
          stroke-dasharray: 1000;
          stroke-dashoffset: 1000;
          animation: draw 2s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
          animation-delay: 0.8s;
        }
      `}} />
        </div>
    );
};

export default EpisenseAnalytics;