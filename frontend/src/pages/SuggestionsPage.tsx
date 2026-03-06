import React, { useState, useEffect, useMemo } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
    ArrowLeft,
    RefreshCw,
    TrendingUp,
    CheckCircle2,
    AlertTriangle,
    Flame,
    Clock,
    SplitSquareHorizontal,
    Wand2
} from 'lucide-react';
import type { SeriesAnalysis, GeneratedSeries } from '../services/api';
import { createProject } from '../services/api';
import toast from 'react-hot-toast';

interface Suggestion {
    id: number;
    type: string;
    icon: React.ElementType;
    title: string;
    problem: string;
    fix: string;
    impact: string;
    color: string;
    diff: {
        before: string;
        after: string;
    } | null;
    applied: boolean;
}

const fallbackSuggestions: Suggestion[] = [
    {
        id: 1, type: "Retention Risk", icon: AlertTriangle,
        title: "Pacing Stall @ 0:50 - 0:75",
        problem: "ML predicts a massive 35% audience drop-off. The action stalls as the diver searches the desk.",
        fix: "Cut 15 seconds of internal monologue. Introduce the secondary threat immediately.",
        impact: "+35% Retention", color: "bg-[#FF9E9E]",
        diff: { before: "The diver stares at the crack. He walks over to the desk, opening drawers one by one.", after: "The crack splinters. Suddenly, the desk lamp violently explodes. Plunged into darkness." },
        applied: false,
    },
    {
        id: 2, type: "Weak Cliffhanger", icon: Flame,
        title: "Insufficient Psychological Friction",
        problem: "Hook score is only 72/100. Ending doesn't create a strong enough curiosity gap.",
        fix: "End abruptly on the visual reveal of the Caller ID. Cut dialogue.",
        impact: "+22 Hook Score", color: "bg-[#D4FF33]",
        diff: { before: "He picks up the phone. 'Hello? Who is this?'", after: "The screen illuminates the room: CALLER ID - SARAH (DAUGHTER). Cut to black." },
        applied: false,
    },
    {
        id: 3, type: "Flat Zone", icon: Clock,
        title: "Emotional Plateau @ 0:15 - 0:27",
        problem: "Sentiment analysis detects 12 seconds of emotional flatness during the initial sequence.",
        fix: "Overlay a high-tension sound design spike at 0:18.",
        impact: "+15% Engagement", color: "bg-[#33A1FF]",
        diff: null,
        applied: false,
    },
];

const ICON_MAP: Record<string, React.ElementType> = {
    "Retention Risk": AlertTriangle,
    "Weak Cliffhanger": Flame,
    "Flat Zone": Clock,
    "Pacing": SplitSquareHorizontal,
};
const COLOR_MAP = ["bg-[#FF9E9E]", "bg-[#D4FF33]", "bg-[#33A1FF]", "bg-[#C7B9FF]"];

const SuggestionsPage = () => {
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => { document.title = 'Suggestions — VBOX Episense'; }, []);

    const routerState = location.state as { analysis?: SeriesAnalysis; series?: GeneratedSeries } | null;
    const routerAnalysis = routerState?.analysis;

    // Build suggestions from API analysis data
    const derivedSuggestions = useMemo<Suggestion[]>(() => {
        if (!routerAnalysis) return fallbackSuggestions;

        const suggestions: Suggestion[] = [];
        let id = 1;
        for (const meta of routerAnalysis.episodes) {
            const a = meta.analysis;
            if (!a?.retention?.recommendations) continue;
            for (const rec of a.retention.recommendations) {
                const type = rec.area.toLowerCase().includes("hook") ? "Weak Cliffhanger"
                    : rec.area.toLowerCase().includes("drop") || rec.area.toLowerCase().includes("retention") ? "Retention Risk"
                        : rec.area.toLowerCase().includes("pacing") || rec.area.toLowerCase().includes("flat") ? "Flat Zone"
                            : "Pacing";
                suggestions.push({
                    id: id++,
                    type,
                    icon: ICON_MAP[type] || AlertTriangle,
                    title: `Ep ${meta.episode_number}: ${meta.title}`,
                    problem: a.retention.reason || "Analysis flagged this episode.",
                    fix: rec.suggestion,
                    impact: `${rec.priority} — Risk: ${a.retention.risk_level}`,
                    color: COLOR_MAP[(id - 1) % COLOR_MAP.length],
                    diff: null,
                    applied: false,
                });
            }
        }
        return suggestions.length > 0 ? suggestions : fallbackSuggestions;
    }, [routerAnalysis]);

    const [suggestions, setSuggestions] = useState<Suggestion[]>(derivedSuggestions);
    const [isLoaded, setIsLoaded] = useState(false);
    const [processingId, setProcessingId] = useState<number | null>(null);
    const [expandedDiffId, setExpandedDiffId] = useState<number | null>(null);

    useEffect(() => {
        setIsLoaded(true);
    }, []);

    const handleApply = (id: number) => {
        setProcessingId(id);

        // Simulate the wave fill and network request delay
        setTimeout(() => {
            setSuggestions(prev =>
                prev.map(s => s.id === id ? { ...s, applied: true } : s)
            );
            setProcessingId(null);
            // Auto-collapse diff if open
            if (expandedDiffId === id) setExpandedDiffId(null);
        }, 1000); // 1s interaction delay
    };

    const toggleDiff = (id: number) => {
        setExpandedDiffId(prev => prev === id ? null : id);
    };

    const handleRegenerate = () => {
        setIsLoaded(false);
        setTimeout(() => {
            setSuggestions(derivedSuggestions); // Reset state
            setIsLoaded(true);
        }, 500);
    };

    return (
        <div className="min-h-screen bg-[#FDFBF7] text-[#0A192F] font-sans relative overflow-x-hidden selection:bg-[#33A1FF] selection:text-white pb-24">

            {/* Neo-Pop Grid Background */}
            <div className="fixed inset-0 z-0 pointer-events-none opacity-[0.1]"
                style={{ backgroundImage: 'radial-gradient(#0A192F 2px, transparent 2px)', backgroundSize: '32px 32px' }}>
            </div>

            <div className="max-w-4xl mx-auto px-4 md:px-6 pt-8 relative z-10">

                {/* Header */}
                <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-12 gap-6">
                    <div className="flex items-center gap-4">
                        <button
                            onClick={() => navigate('/analytics', { state: { analysis: routerAnalysis, series: routerState?.series } })}
                            className="w-12 h-12 bg-white border-4 border-[#0A192F] rounded-full flex items-center justify-center hover:bg-[#D4FF33] transition-all shadow-[4px_4px_0px_#0A192F] active:translate-y-[2px] active:shadow-none flex-shrink-0 group">
                            <ArrowLeft className="w-6 h-6 group-hover:-translate-x-1 transition-transform" />
                        </button>
                        <div>
                            <div className="text-[10px] font-black uppercase tracking-widest text-[#33A1FF] mb-1">{routerState?.series?.direction || 'Series Refinement'}</div>
                            <h1 className="text-3xl md:text-5xl font-black tracking-tight leading-none">Refine Series.</h1>
                        </div>
                    </div>

                    <button
                        onClick={handleRegenerate}
                        className="bg-white text-[#0A192F] border-4 border-[#0A192F] rounded-full px-6 py-3 font-black text-sm uppercase tracking-wide shadow-[4px_4px_0px_#0A192F] hover:bg-[#FDFBF7] hover:shadow-[6px_6px_0px_#0A192F] hover:-translate-y-1 active:translate-y-[2px] active:shadow-none transition-all flex items-center gap-2 group"
                    >
                        <RefreshCw className="w-4 h-4 group-hover:rotate-180 transition-transform duration-500" /> Regenerate Analysis
                    </button>
                </header>

                {/* Suggestions List */}
                <div className="flex flex-col gap-8">
                    {suggestions.map((suggestion, index) => {
                        const isProcessing = processingId === suggestion.id;
                        const isApplied = suggestion.applied;
                        const isDiffExpanded = expandedDiffId === suggestion.id;
                        const Icon = suggestion.icon;

                        return (
                            <div
                                key={suggestion.id}
                                className={`bg-white border-4 border-[#0A192F] rounded-[2.5rem] p-6 md:p-8 transition-all duration-500 relative
                  ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-12'}
                  ${isApplied ? 'shadow-[4px_4px_0px_#0A192F] bg-[#FDFBF7]' : 'shadow-[8px_8px_0px_#0A192F] hover:-translate-y-1 hover:shadow-[12px_12px_0px_#0A192F]'}`}
                                style={{ transitionDelay: isLoaded ? `${index * 150}ms` : '0ms' }}
                            >

                                {/* Main Card Content */}
                                <div className="flex flex-col md:flex-row gap-6 items-start relative z-10">

                                    {/* Left Column: Icon & Meta */}
                                    <div className="flex-shrink-0 flex items-center gap-4 md:w-48">
                                        <div className={`w-12 h-12 rounded-full border-4 border-[#0A192F] flex items-center justify-center shadow-[2px_2px_0px_#0A192F] relative transition-colors duration-300
                      ${isApplied ? 'bg-[#D4FF33]' : suggestion.color}`}>

                                            {/* Checkmark Fly-in Animation */}
                                            <CheckCircle2 className={`w-6 h-6 text-[#0A192F] absolute transition-all duration-500 cubic-bezier(0.34, 1.56, 0.64, 1)
                        ${isApplied ? 'scale-100 opacity-100' : 'scale-0 opacity-0'}`} />

                                            {/* Original Icon Fade-out */}
                                            <Icon className={`w-6 h-6 text-[#0A192F] absolute transition-all duration-300
                        ${isApplied ? 'scale-0 opacity-0' : 'scale-100 opacity-100'}`} />
                                        </div>

                                        <div>
                                            <div className="text-[10px] font-black uppercase text-[#0A192F]/50 tracking-widest">{suggestion.type}</div>
                                            <div className={`inline-flex items-center gap-1 px-2 py-0.5 mt-1 rounded text-[10px] font-black uppercase border-2 border-[#0A192F] bg-white shadow-[2px_2px_0px_#0A192F]
                        ${isApplied ? 'text-[#0A192F]/50' : 'text-[#33A1FF]'}`}>
                                                <TrendingUp className="w-3 h-3" /> {suggestion.impact}
                                            </div>
                                        </div>
                                    </div>

                                    {/* Middle Column: Text */}
                                    <div className="flex-1">
                                        <h3 className={`text-xl font-black tracking-tight mb-2 transition-colors ${isApplied ? 'text-[#0A192F]/40 line-through' : 'text-[#0A192F]'}`}>
                                            {suggestion.title}
                                        </h3>

                                        <div className="space-y-4">
                                            <div>
                                                <div className="text-[10px] font-black uppercase text-[#FF4D4D] mb-1 flex items-center gap-1">
                                                    <AlertTriangle className="w-3 h-3" /> Issue
                                                </div>
                                                <p className={`font-bold text-sm leading-snug transition-opacity ${isApplied ? 'opacity-40' : 'opacity-100'}`}>
                                                    {suggestion.problem}
                                                </p>
                                            </div>

                                            <div className={`p-4 rounded-2xl border-2 transition-colors duration-300
                        ${isApplied ? 'bg-white border-[#0A192F]/10' : 'bg-[#D4FF33]/20 border-[#0A192F]'}`}>
                                                <div className="text-[10px] font-black uppercase text-[#0A192F] mb-1 flex items-center gap-1">
                                                    <Wand2 className="w-3 h-3" /> Engine Fix
                                                </div>
                                                <p className={`font-bold text-sm leading-snug ${isApplied ? 'text-[#0A192F]/60' : 'text-[#0A192F]'}`}>
                                                    {suggestion.fix}
                                                </p>
                                            </div>
                                        </div>
                                    </div>

                                    {/* Right Column: Actions */}
                                    <div className="flex flex-col gap-3 w-full md:w-auto flex-shrink-0">
                                        {isApplied ? (
                                            <div className="bg-[#D4FF33] border-4 border-[#0A192F] px-6 py-3 rounded-full font-black text-sm uppercase text-center shadow-[4px_4px_0px_#0A192F] flex items-center justify-center gap-2 cursor-default animate-pop-in">
                                                <CheckCircle2 className="w-4 h-4" /> Optimized
                                            </div>
                                        ) : (
                                            <button
                                                onClick={() => handleApply(suggestion.id)}
                                                disabled={isProcessing}
                                                className={`relative overflow-hidden border-4 border-[#0A192F] px-8 py-3 rounded-full font-black text-sm uppercase text-center shadow-[4px_4px_0px_#0A192F] hover:shadow-[6px_6px_0px_#0A192F] hover:-translate-y-1 active:translate-y-[2px] active:shadow-none transition-all flex items-center justify-center gap-2 group disabled:pointer-events-none
                          ${isProcessing ? 'bg-white text-[#0A192F]' : 'bg-[#0A192F] text-[#D4FF33]'}`}
                                            >
                                                {/* Wave Fill Animation Layer */}
                                                {isProcessing && (
                                                    <div className="absolute inset-0 bg-[#D4FF33] animate-fill-wave z-0 origin-left"></div>
                                                )}

                                                <span className="relative z-10 flex items-center gap-2">
                                                    {isProcessing ? 'Applying...' : 'Apply Fix'}
                                                </span>
                                            </button>
                                        )}

                                        {suggestion.diff && !isApplied && (
                                            <button
                                                onClick={() => toggleDiff(suggestion.id)}
                                                className="bg-white border-2 border-[#0A192F] px-6 py-2 rounded-full font-black text-[10px] uppercase text-center shadow-[2px_2px_0px_#0A192F] hover:bg-[#FDFBF7] active:translate-y-[1px] active:shadow-none transition-all flex items-center justify-center gap-2"
                                            >
                                                <SplitSquareHorizontal className="w-3 h-3" /> {isDiffExpanded ? 'Hide Diff' : 'View Diff'}
                                            </button>
                                        )}
                                    </div>
                                </div>

                                {/* Diff Split-Screen (Slide down transition via CSS Grid) */}
                                <div className={`grid transition-[grid-template-rows] duration-500 ease-[cubic-bezier(0.34,1.56,0.64,1)] ${isDiffExpanded ? 'grid-rows-[1fr]' : 'grid-rows-[0fr]'}`}>
                                    <div className="overflow-hidden">
                                        <div className="pt-6 mt-6 border-t-4 border-dashed border-[#0A192F]/20">
                                            <div className="flex flex-col md:flex-row gap-4">

                                                {/* Before */}
                                                <div className="flex-1 bg-[#FF9E9E]/10 border-2 border-[#FF4D4D] rounded-2xl p-4 relative">
                                                    <div className="absolute -top-3 left-4 bg-[#FF4D4D] text-white px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-widest border-2 border-[#0A192F]">Before</div>
                                                    <p className="font-medium text-sm text-[#0A192F]/70 line-through decoration-[#FF4D4D]/50 mt-2">
                                                        {suggestion.diff?.before}
                                                    </p>
                                                </div>

                                                {/* After */}
                                                <div className="flex-1 bg-[#D4FF33]/20 border-2 border-[#00A36C] rounded-2xl p-4 relative">
                                                    <div className="absolute -top-3 left-4 bg-[#D4FF33] text-[#0A192F] px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-widest border-2 border-[#0A192F]">After</div>
                                                    <p className="font-bold text-sm text-[#0A192F] mt-2">
                                                        {suggestion.diff?.after}
                                                    </p>
                                                </div>

                                            </div>
                                        </div>
                                    </div>
                                </div>

                            </div>
                        );
                    })}
                </div>

                {/* Finalize CTA */}
                <div className="mt-12 flex justify-center">
                    <button
                        onClick={async () => {
                            console.log("[SAVE] Button clicked");

                            if (!routerState) {
                                console.error("[SAVE] No routerState at all");
                                toast.error("No state available");
                                return;
                            }

                            if (!routerState.series) {
                                console.error("[SAVE] series is missing from routerState", routerState);
                                toast.error("No series data to save");
                                return;
                            }

                            const saveData = {
                                title: routerState.series.direction || 'Untitled Series',
                                concept: (routerState as any).concept || routerState.series.hook || 'No concept provided',
                                genres: [],
                                generated_series: routerState.series,
                                analysis: routerAnalysis || null,
                            };

                            console.log("[SAVE] Preparing to call createProject with:", saveData);

                            try {
                                console.log("[SAVE] Calling createProject...");
                                const result = await createProject(saveData);
                                console.log("[SAVE] Success:", result);
                                toast.success("Saved to Dashboard");
                                navigate('/dashboard');
                            } catch (err: any) {
                                console.error("[SAVE] Failed:", {
                                    message: err.message,
                                    response: err.response?.data,
                                    status: err.response?.status,
                                    config: {
                                        url: err.config?.url,
                                        method: err.config?.method,
                                        headers: err.config?.headers,
                                    }
                                });
                                toast.error(err.message || "Save failed — check console");
                            }
                        }}
                        className="bg-[#0A192F] text-[#D4FF33] border-4 border-[#0A192F] rounded-full px-10 py-4 font-black text-lg uppercase tracking-wide shadow-[6px_6px_0px_#D4FF33] hover:shadow-[8px_8px_0px_#D4FF33] hover:-translate-y-1 active:translate-y-[2px] active:shadow-none transition-all flex items-center gap-3"
                    >
                        <CheckCircle2 className="w-6 h-6" /> Finalize & Save to Dashboard
                    </button>
                </div>
            </div>

        </div>
    );
};

export default SuggestionsPage;