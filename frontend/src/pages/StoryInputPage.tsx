import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Wand2,
    ArrowLeft,
    Minus,
    Plus,
    Play,
    PenTool,
    BrainCircuit,
    Timer,
    Users,
    ArrowRight,
    CheckCircle2,
    X,
    Compass,
    Zap,
    Eye,
    Layers
} from 'lucide-react';
import { generateSeries, analyzeSeries, getDirections } from '../services/api';

// ─── Types ───────────────────────────────────────────────────────────────────

type AudienceOption = {
    id: string;
    label: string;
    emoji: string;
    desc: string;
    color: string;
};

type Direction = {
    id: string;
    title: string;
    tagline: string;
    reason: string;
    color: string;
    icon: React.ReactNode;
};

// ─── Constants ────────────────────────────────────────────────────────────────

const AUDIENCE_OPTIONS: AudienceOption[] = [
    { id: 'myself', label: 'Just Me', emoji: '✍️', desc: 'Personal journal / passion project', color: '#C7B9FF' },
    { id: 'genz', label: 'Gen Z', emoji: '⚡', desc: '18–25 · Fast, punchy, raw energy', color: '#D4FF33' },
    { id: 'millennials', label: 'Millennials', emoji: '🎯', desc: '25–40 · Relatable, nostalgic, layered', color: '#33A1FF' },
    { id: 'adults', label: 'Adults 40+', emoji: '🧭', desc: '40+ · Deep narrative, rich context', color: '#FF9E9E' },
    { id: 'families', label: 'Families', emoji: '🏠', desc: 'All ages · Warm, inclusive, safe', color: '#FFD700' },
    { id: 'corporate', label: 'Professionals', emoji: '💼', desc: 'B2B · Insight-driven, data-backed', color: '#0A192F' },
];

const FALLBACK_DIRECTIONS: Direction[] = [
    {
        id: 'slow-burn',
        title: 'The Slow Burn',
        tagline: 'Build tension, then ignite.',
        reason: 'Opens with an ordinary world that feels slightly wrong. Each episode peels back one layer, keeping viewers hooked through creeping dread and earned payoffs.',
        color: '#FF9E9E',
        icon: <Layers className="w-6 h-6" />,
    },
    {
        id: 'in-medias-res',
        title: 'In Medias Res',
        tagline: 'Drop into the chaos. Explain later.',
        reason: 'Episode 1 starts at the most intense moment of the story. Viewers are disoriented in the best way — they must watch the next part.',
        color: '#33A1FF',
        icon: <Zap className="w-6 h-6" />,
    },
    {
        id: 'revelation-arc',
        title: 'The Revelation Arc',
        tagline: 'One secret. Revealed in pieces.',
        reason: 'A central mystery is seeded in episode 1 and a new clue drops every episode. The audience becomes detectives.',
        color: '#D4FF33',
        icon: <Eye className="w-6 h-6" />,
    },
];

const PROCESS_STEPS = [
    { label: 'Decomposing entities & timeline...', color: '#33A1FF' },
    { label: 'Mapping emotional trajectory...', color: '#FF9E9E' },
    { label: 'Applying narrative direction...', color: '#C7B9FF' },
    { label: 'Slicing into vertical arcs...', color: '#D4FF33' },
];

// ─── Component ────────────────────────────────────────────────────────────────

const DIRECTION_ICONS = [<Layers className="w-6 h-6" />, <Zap className="w-6 h-6" />, <Eye className="w-6 h-6" />];
const DIRECTION_COLORS = ['#FF9E9E', '#33A1FF', '#D4FF33'];

const StoryInputPage = () => {
    const navigate = useNavigate();

    // Core inputs
    const [concept, setConcept] = useState('');
    const [episodes, setEpisodes] = useState(5);
    const [selectedAudience, setSelectedAudience] = useState<string | null>(null);

    // Directions popup
    const [showDirections, setShowDirections] = useState(false);
    const [selectedDirection, setSelectedDirection] = useState<string | null>(null);
    const [directions, setDirections] = useState<Direction[]>(FALLBACK_DIRECTIONS);
    const [loadingDirections, setLoadingDirections] = useState(false);

    // Processing overlay
    const [isProcessing, setIsProcessing] = useState(false);
    const [processStep, setProcessStep] = useState(0);
    const [progressPct, setProgressPct] = useState(0);

    // Error toast
    const [errorMsg, setErrorMsg] = useState<string | null>(null);

    // Page title
    useEffect(() => { document.title = 'Story Input — VBOX Episense'; }, []);

    // ── Handlers ──────────────────────────────────────────────────────────────

    const handleMagicFill = () => {
        const idea = "A deep-sea welder discovers a completely dry, oxygen-rich room inside a sunken 1800s galleon. On a wooden desk sits a modern smartphone, plugged into a wall outlet that shouldn't exist. Suddenly, the phone starts ringing. The caller ID says it's his daughter, who is supposed to be asleep on the surface.";
        let i = 0;
        setConcept('');
        const typing = setInterval(() => {
            if (i < idea.length) {
                setConcept(prev => prev + idea.charAt(i));
                i++;
            } else {
                clearInterval(typing);
            }
        }, 15);
    };

    // Step 1: user clicks "Architect" → fetch directions from API, then show popup
    const handleArchitect = async () => {
        if (!concept.trim() || !selectedAudience) return;
        setSelectedDirection(null);
        setLoadingDirections(true);
        setShowDirections(true);

        try {
            const res = await getDirections(concept);
            const mapped: Direction[] = res.suggested_directions.map((d, i) => ({
                id: `dir-${i}`,
                title: d.direction_name,
                tagline: d.category,
                reason: d.why_it_fits,
                color: DIRECTION_COLORS[i % DIRECTION_COLORS.length],
                icon: DIRECTION_ICONS[i % DIRECTION_ICONS.length],
            }));
            setDirections(mapped);
        } catch {
            setDirections(FALLBACK_DIRECTIONS);
        } finally {
            setLoadingDirections(false);
        }
    };

    // Step 2: user picks a direction → start processing + API calls
    const handleGenerate = async () => {
        if (!selectedDirection) return;
        setShowDirections(false);
        setIsProcessing(true);
        setProcessStep(0);
        setProgressPct(0);

        // Smooth progress bar
        let pct = 0;
        const ticker = setInterval(() => {
            pct += 1;
            setProgressPct(Math.min(pct, 95)); // Cap at 95% until API returns
            if (pct >= 95) clearInterval(ticker);
        }, 35);

        // Step reveals
        setTimeout(() => setProcessStep(1), 700);
        setTimeout(() => setProcessStep(2), 1500);
        setTimeout(() => setProcessStep(3), 2400);

        try {
            // Call backend: generate episodes
            const directionName = selectedDirectionObj?.title || selectedDirection;
            const audienceName = selectedAudienceObj?.label || 'Gen Z';
            const series = await generateSeries(concept, episodes, [], audienceName, directionName);

            setTimeout(() => setProcessStep(4), 100);

            // Call backend: analyze the generated episodes
            const analysis = await analyzeSeries(series.episodes, series.category);

            // Complete progress
            clearInterval(ticker);
            setProgressPct(100);

            // Brief delay to show 100%, then navigate with data
            setTimeout(() => {
                setIsProcessing(false);
                setProcessStep(0);
                setProgressPct(0);
                navigate('/breakdown', {
                    state: { series, analysis, concept, audience: audienceName },
                });
            }, 400);
        } catch (err) {
            console.error('Engine error:', err);
            clearInterval(ticker);
            setProgressPct(100);
            setTimeout(() => setProcessStep(4), 100);

            // Show error toast
            setErrorMsg('Generation failed — showing demo data instead.');
            setTimeout(() => setErrorMsg(null), 4000);

            // Fallback: navigate without data so app doesn't break
            setTimeout(() => {
                setIsProcessing(false);
                setProcessStep(0);
                setProgressPct(0);
                navigate('/breakdown');
            }, 800);
        }
    };

    const canArchitect = concept.trim().length > 0 && selectedAudience !== null;
    const selectedAudienceObj = AUDIENCE_OPTIONS.find(a => a.id === selectedAudience);
    const selectedDirectionObj = directions.find(d => d.id === selectedDirection);

    return (
        <div className="min-h-screen bg-[#FDFBF7] text-[#0A192F] font-sans relative overflow-x-hidden selection:bg-[#33A1FF] selection:text-white pb-20">

            {/* Neo-Pop Dotted Background */}
            <div className="fixed inset-0 z-0 pointer-events-none opacity-[0.15]"
                style={{ backgroundImage: 'radial-gradient(#0A192F 2px, transparent 2px)', backgroundSize: '24px 24px' }} />

            <div className="max-w-7xl mx-auto px-6 pt-8 relative z-10">

                {/* ── Nav ── */}
                <nav className="flex justify-between items-center mb-12">
                    <button
                        onClick={() => navigate('/dashboard')}
                        className="flex items-center gap-3 font-black uppercase text-sm hover:-translate-x-2 transition-transform">
                        <div className="w-10 h-10 bg-[#FF9E9E] border-2 border-[#0A192F] rounded-full flex items-center justify-center shadow-[2px_2px_0px_#0A192F]">
                            <ArrowLeft className="w-5 h-5 text-[#0A192F]" />
                        </div>
                        Back to Hub
                    </button>

                    <div className="bg-white border-2 border-[#0A192F] rounded-full px-4 py-2 shadow-[2px_2px_0px_#0A192F] flex items-center gap-3">
                        <div className="w-2 h-2 rounded-full bg-[#D4FF33] animate-pulse" />
                        <span className="font-mono text-xs font-bold uppercase tracking-widest">VBOX Engine Ready</span>
                    </div>
                </nav>

                {/* ── Header ── */}
                <div className="mb-10">
                    <h1 className="text-5xl md:text-6xl font-black tracking-tight mb-4">The Canvas.</h1>
                    <p className="text-xl font-medium text-[#0A192F]/60 max-w-2xl">
                        Drop your raw narrative, pick your audience, and we'll structure the perfect multi-part hook.
                    </p>
                </div>

                {/* ── Bento Layout ── */}
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8">

                    {/* Main Input — 8 cols */}
                    <div className="lg:col-span-8 bg-white border-4 border-[#0A192F] rounded-[2.5rem] p-6 md:p-8 shadow-[8px_8px_0px_#0A192F] relative flex flex-col group">
                        <div className="flex justify-between items-start mb-6">
                            <div className="flex items-center gap-3">
                                <div className="bg-[#C7B9FF] border-2 border-[#0A192F] p-2 rounded-xl shadow-[2px_2px_0px_#0A192F]">
                                    <PenTool className="w-5 h-5" />
                                </div>
                                <h2 className="text-2xl font-black uppercase tracking-tight">Core Concept</h2>
                            </div>

                            <button
                                onClick={handleMagicFill}
                                className="flex items-center gap-2 bg-[#FDFBF7] border-2 border-[#0A192F] px-4 py-2 rounded-full text-sm font-bold shadow-[2px_2px_0px_#0A192F] hover:bg-[#D4FF33] active:translate-y-[2px] active:translate-x-[2px] active:shadow-none transition-all"
                            >
                                <Wand2 className="w-4 h-4 text-[#33A1FF]" />
                                Auto-Fill Idea
                            </button>
                        </div>

                        <textarea
                            value={concept}
                            onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setConcept(e.target.value)}
                            placeholder="What happens in your story? Who is the protagonist? What is the core conflict? Just brain-dump it here..."
                            className="flex-1 w-full min-h-[300px] bg-transparent text-2xl font-bold leading-relaxed text-[#0A192F] placeholder-[#0A192F]/20 resize-none focus:outline-none"
                        />

                        <div className="flex justify-between items-center pt-4 border-t-2 border-dashed border-[#0A192F]/20 mt-4">
                            <span className="font-mono text-xs font-bold text-[#0A192F]/50 uppercase">
                                {concept.length === 0 ? 'Awaiting Input...' : 'Extracting Entities...'}
                            </span>
                            <span className={`font-mono text-sm font-black ${concept.length > 500 ? 'text-[#33A1FF]' : 'text-[#0A192F]'}`}>
                                {concept.length} chars
                            </span>
                        </div>
                    </div>

                    {/* Right Column — 4 cols */}
                    <div className="lg:col-span-4 flex flex-col gap-6">

                        {/* ── Episode Stepper ── */}
                        <div className="bg-[#D4FF33] border-4 border-[#0A192F] rounded-[2rem] p-6 shadow-[6px_6px_0px_#0A192F] flex flex-col justify-between relative overflow-hidden">
                            <div className="absolute -right-4 -top-4 w-24 h-24 border-4 border-[#0A192F]/10 rounded-full" />
                            <div className="relative z-10 mb-6">
                                <div className="flex items-center gap-2 mb-1">
                                    <Timer className="w-5 h-5" />
                                    <h3 className="font-black text-xl uppercase tracking-tight">Timeline</h3>
                                </div>
                                <p className="font-medium text-sm text-[#0A192F]/70">VBOX 90-second constraint enforced.</p>
                            </div>
                            <div className="bg-white border-2 border-[#0A192F] rounded-2xl p-2 flex items-center justify-between shadow-inner relative z-10">
                                <button
                                    onClick={() => setEpisodes(Math.max(5, episodes - 1))}
                                    disabled={episodes <= 5}
                                    className="w-12 h-12 bg-[#FDFBF7] border-2 border-[#0A192F] rounded-xl flex items-center justify-center hover:bg-[#FF9E9E] disabled:opacity-50 disabled:hover:bg-[#FDFBF7] transition-colors shadow-[2px_2px_0px_#0A192F] active:shadow-none active:translate-y-[2px]"
                                >
                                    <Minus className="w-6 h-6" />
                                </button>
                                <div className="flex flex-col items-center">
                                    <span className="text-4xl font-black leading-none">{episodes}</span>
                                    <span className="font-mono text-[10px] font-bold uppercase tracking-widest text-[#0A192F]/50">Episodes</span>
                                </div>
                                <button
                                    onClick={() => setEpisodes(Math.min(8, episodes + 1))}
                                    disabled={episodes >= 8}
                                    className="w-12 h-12 bg-[#FDFBF7] border-2 border-[#0A192F] rounded-xl flex items-center justify-center hover:bg-[#33A1FF] disabled:opacity-50 disabled:hover:bg-[#FDFBF7] transition-colors shadow-[2px_2px_0px_#0A192F] active:shadow-none active:translate-y-[2px]"
                                >
                                    <Plus className="w-6 h-6" />
                                </button>
                            </div>
                        </div>

                        {/* ── Target Audience ── */}
                        <div className="bg-white border-4 border-[#0A192F] rounded-[2rem] p-6 shadow-[6px_6px_0px_#0A192F] flex-1">
                            <div className="flex items-center gap-2 mb-4">
                                <div className="bg-[#FF9E9E] border-2 border-[#0A192F] p-2 rounded-xl shadow-[2px_2px_0px_#0A192F]">
                                    <Users className="w-4 h-4" />
                                </div>
                                <h3 className="font-black text-xl uppercase tracking-tight">Target Audience</h3>
                            </div>

                            <div className="grid grid-cols-2 gap-2">
                                {AUDIENCE_OPTIONS.map(opt => {
                                    const isSelected = selectedAudience === opt.id;
                                    const isPersonal = opt.id === 'myself';
                                    return (
                                        <button
                                            key={opt.id}
                                            onClick={() => setSelectedAudience(isSelected ? null : opt.id)}
                                            className={`
                                                relative p-3 border-2 border-[#0A192F] rounded-2xl text-left transition-all
                                                shadow-[2px_2px_0px_#0A192F] active:translate-y-[2px] active:translate-x-[2px] active:shadow-none
                                                ${isPersonal ? 'col-span-2' : ''}
                                                ${isSelected
                                                    ? 'text-[#0A192F] scale-[1.02]'
                                                    : 'bg-[#FDFBF7] hover:bg-[#F0EEE9]'}
                                            `}
                                            style={isSelected ? { backgroundColor: opt.color } : {}}
                                        >
                                            {isSelected && (
                                                <div className="absolute top-2 right-2 w-4 h-4 bg-[#0A192F] rounded-full flex items-center justify-center">
                                                    <div className="w-1.5 h-1.5 bg-white rounded-full" />
                                                </div>
                                            )}
                                            <div className="text-xl mb-1">{opt.emoji}</div>
                                            <div className="font-black text-sm leading-tight">{opt.label}</div>
                                            <div className="font-medium text-[10px] text-[#0A192F]/60 mt-0.5 leading-tight">{opt.desc}</div>
                                        </button>
                                    );
                                })}
                            </div>
                        </div>

                    </div>
                </div>

                {/* ── Action Footer ── */}
                <div className="mt-8">
                    <button
                        onClick={handleArchitect}
                        disabled={!canArchitect}
                        className="w-full bg-[#0A192F] text-white border-4 border-[#0A192F] rounded-[2.5rem] p-6 md:p-8 flex items-center justify-between group disabled:opacity-40 disabled:cursor-not-allowed shadow-[8px_8px_0px_#33A1FF] hover:shadow-[10px_10px_0px_#33A1FF] hover:-translate-y-1 active:translate-y-[4px] active:translate-x-[4px] active:shadow-none transition-all overflow-hidden relative"
                    >
                        <div className="absolute top-0 -left-[100%] w-1/2 h-full bg-gradient-to-r from-transparent via-white/20 to-transparent skew-x-[-20deg] group-hover:animate-shine" />

                        <div className="flex items-center gap-6 relative z-10">
                            <div className="w-16 h-16 bg-[#33A1FF] border-2 border-[#0A192F] rounded-full flex items-center justify-center shadow-[4px_4px_0px_#0A192F] group-hover:scale-110 transition-transform">
                                <BrainCircuit className="w-8 h-8 text-[#0A192F]" />
                            </div>
                            <div className="text-left">
                                <h2 className="text-3xl md:text-4xl font-black uppercase tracking-tight">Architect the Series</h2>
                                <span className="font-mono text-sm text-[#33A1FF] font-bold">
                                    {!concept.trim()
                                        ? 'Enter your concept first'
                                        : !selectedAudience
                                            ? 'Select a target audience'
                                            : `For ${selectedAudienceObj?.label} · ${episodes} Episodes → Pick a Direction`}
                                </span>
                            </div>
                        </div>

                        <div className="hidden md:flex bg-white/10 p-4 rounded-2xl border-2 border-white/20 items-center gap-4 backdrop-blur-sm relative z-10">
                            <div className="text-right">
                                <div className="font-black text-xl">{episodes} Parts</div>
                                <div className="font-mono text-xs opacity-70">Target Output</div>
                            </div>
                            <Play className="w-8 h-8 fill-current text-[#D4FF33]" />
                        </div>
                    </button>
                </div>
            </div>

            {/* ════════════════════════════════════════════════
                  DIRECTIONS POPUP
              ════════════════════════════════════════════════ */}
            {showDirections && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[#0A192F]/60 backdrop-blur-sm animate-fade-in">
                    <div className="w-full max-w-2xl bg-[#FDFBF7] border-4 border-[#0A192F] rounded-[2.5rem] p-6 md:p-8 shadow-[12px_12px_0px_#0A192F] animate-modal-in">

                        {/* Header */}
                        <div className="flex items-start justify-between mb-6">
                            <div>
                                <div className="flex items-center gap-2 mb-2">
                                    <div className="bg-[#C7B9FF] border-2 border-[#0A192F] p-2 rounded-xl shadow-[2px_2px_0px_#0A192F]">
                                        <Compass className="w-4 h-4" />
                                    </div>
                                    <span className="font-mono text-xs font-black uppercase tracking-widest text-[#0A192F]/50">Step 2 of 2</span>
                                </div>
                                <h2 className="text-3xl font-black tracking-tight leading-tight">Choose your<br />Narrative Direction.</h2>
                                <p className="text-sm font-medium text-[#0A192F]/50 mt-1">
                                    Audience: <span className="font-black text-[#0A192F]">{selectedAudienceObj?.emoji} {selectedAudienceObj?.label}</span>
                                    {' · '}{episodes} episodes
                                </p>
                            </div>
                            <button
                                onClick={() => setShowDirections(false)}
                                className="w-10 h-10 bg-white border-2 border-[#0A192F] rounded-full flex items-center justify-center shadow-[2px_2px_0px_#0A192F] hover:bg-[#FF9E9E] transition-colors active:shadow-none active:translate-y-[2px]"
                            >
                                <X className="w-4 h-4" />
                            </button>
                        </div>

                        {/* Direction Cards */}
                        <div className="space-y-3 mb-6">
                            {loadingDirections ? (
                                <div className="flex flex-col items-center justify-center py-12">
                                    <div className="w-10 h-10 border-4 border-[#0A192F] border-t-[#D4FF33] rounded-full animate-spin mb-4"></div>
                                    <p className="font-black text-sm uppercase tracking-widest text-[#0A192F]/50">Analyzing story directions...</p>
                                </div>
                            ) : directions.map((dir: Direction, idx: number) => {
                                const isSelected = selectedDirection === dir.id;
                                return (
                                    <button
                                        key={dir.id}
                                        onClick={() => setSelectedDirection(isSelected ? null : dir.id)}
                                        className={`
                                            w-full text-left p-5 border-3 border-[#0A192F] rounded-2xl transition-all
                                            shadow-[3px_3px_0px_#0A192F] active:shadow-none active:translate-y-[3px] active:translate-x-[3px]
                                            ${isSelected ? 'border-[#0A192F] scale-[1.01]' : 'bg-white hover:scale-[1.005]'}
                                        `}
                                        style={isSelected ? { backgroundColor: dir.color, borderWidth: '3px' } : { borderWidth: '3px' }}
                                    >
                                        <div className="flex items-start gap-4">
                                            <div className={`w-10 h-10 rounded-xl border-2 border-[#0A192F] flex items-center justify-center shrink-0 mt-0.5 shadow-[2px_2px_0px_#0A192F] transition-colors ${isSelected ? 'bg-[#0A192F] text-white' : 'bg-[#FDFBF7]'}`}>
                                                {dir.icon}
                                            </div>
                                            <div className="flex-1">
                                                <div className="flex items-center gap-2 mb-1">
                                                    <span className="font-black text-lg leading-tight">{dir.title}</span>
                                                    <span className="font-mono text-xs bg-[#0A192F]/10 px-2 py-0.5 rounded-full font-bold">
                                                        #{idx + 1}
                                                    </span>
                                                    {isSelected && <CheckCircle2 className="w-4 h-4 text-[#0A192F] ml-auto" />}
                                                </div>
                                                <p className="font-bold text-sm text-[#0A192F]/70 mb-2 italic">"{dir.tagline}"</p>
                                                <p className="font-medium text-xs text-[#0A192F]/60 leading-relaxed">{dir.reason}</p>
                                            </div>
                                        </div>
                                    </button>
                                );
                            })}
                        </div>

                        {/* Generate CTA */}
                        {!loadingDirections && (
                            <button
                                onClick={handleGenerate}
                                disabled={!selectedDirection}
                                className="w-full bg-[#0A192F] text-white font-black text-lg py-5 rounded-2xl flex items-center justify-center gap-3 disabled:opacity-40 disabled:cursor-not-allowed shadow-[4px_4px_0px_#33A1FF] hover:shadow-[6px_6px_0px_#33A1FF] hover:-translate-y-0.5 active:translate-y-[4px] active:translate-x-[4px] active:shadow-none transition-all group"
                            >
                                <BrainCircuit className="w-5 h-5" />
                                {selectedDirection
                                    ? `Generate with "${selectedDirectionObj?.title}"`
                                    : 'Select a Direction Above'}
                                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                            </button>
                        )}
                    </div>
                </div>
            )}

            {/* Error Toast */}
            {errorMsg && (
                <div className="fixed bottom-8 left-1/2 -translate-x-1/2 z-60 bg-[#FF4D4D] text-white border-4 border-[#0A192F] rounded-full px-6 py-3 font-black text-sm uppercase shadow-[4px_4px_0px_#0A192F] animate-fade-in">
                    {errorMsg}
                </div>
            )}

            {/* ════════════════════════════════════════════════
                  PROCESSING OVERLAY
              ════════════════════════════════════════════════ */}
            <div className={`fixed inset-0 z-50 bg-[#FDFBF7]/95 backdrop-blur-xl flex flex-col items-center justify-center transition-all duration-500 ${isProcessing ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'}`}>
                <div className="max-w-xl w-full px-6">

                    {/* Engine Header */}
                    <div className="flex items-center gap-4 mb-8">
                        <div className="w-14 h-14 bg-[#D4FF33] border-4 border-[#0A192F] rounded-full flex items-center justify-center shadow-[4px_4px_0px_#0A192F] relative">
                            <div className="absolute inset-0 rounded-full border-4 border-t-[#33A1FF] border-r-transparent border-b-transparent border-l-transparent animate-spin" />
                            <div className="w-4 h-4 bg-[#0A192F] rounded-full" />
                        </div>
                        <div>
                            <h2 className="text-4xl font-black uppercase tracking-tight leading-none">VBOX Engine</h2>
                            <span className="font-mono text-sm font-bold text-[#33A1FF] uppercase tracking-widest">Active · Processing</span>
                        </div>
                    </div>

                    {/* Progress Bar */}
                    <div className="mb-6">
                        <div className="flex justify-between items-center mb-2">
                            <span className="font-mono text-xs font-black uppercase tracking-widest text-[#0A192F]/50">Pipeline Progress</span>
                            <span className="font-mono text-sm font-black text-[#0A192F]">{progressPct}%</span>
                        </div>
                        <div className="h-3 bg-[#EAEAEA] border-2 border-[#0A192F] rounded-full overflow-hidden shadow-inner">
                            <div
                                className="h-full bg-[#0A192F] rounded-full transition-all duration-100 ease-linear relative overflow-hidden"
                                style={{ width: `${progressPct}%` }}
                            >
                                {/* Shimmer on the bar */}
                                <div className="absolute inset-0 bg-linear-to-r from-transparent via-white/30 to-transparent animate-shimmer" />
                            </div>
                        </div>
                    </div>

                    {/* Steps */}
                    <div className="bg-white border-4 border-[#0A192F] rounded-3xl p-6 shadow-[8px_8px_0px_#0A192F]">
                        <div className="space-y-3">
                            {PROCESS_STEPS.map((step, idx) => {
                                const active = processStep > idx;
                                const current = processStep === idx;
                                return (
                                    <div
                                        key={idx}
                                        className={`flex items-center gap-4 p-3 rounded-xl border-2 transition-all duration-500 ${active
                                            ? 'border-[#0A192F]'
                                            : current
                                                ? 'border-[#0A192F]/30 animate-pulse'
                                                : 'border-transparent opacity-25'
                                            }`}
                                        style={active ? { backgroundColor: step.color + '25' } : {}}
                                    >
                                        {/* Step indicator */}
                                        <div
                                            className={`w-7 h-7 rounded-full border-2 border-[#0A192F] flex items-center justify-center shrink-0 transition-all duration-500 ${active ? 'scale-110' : ''}`}
                                            style={active ? { backgroundColor: step.color } : { backgroundColor: 'transparent' }}
                                        >
                                            {active
                                                ? <div className="w-2 h-2 bg-[#0A192F] rounded-full" />
                                                : <span className="font-black text-xs text-[#0A192F]/40">{idx + 1}</span>
                                            }
                                        </div>
                                        <span className={`font-bold text-base transition-all duration-300 ${active ? 'text-[#0A192F]' : 'text-[#0A192F]/40'}`}>
                                            {step.label}
                                        </span>
                                        {active && (
                                            <CheckCircle2 className="w-4 h-4 ml-auto shrink-0 text-[#0A192F]" />
                                        )}
                                    </div>
                                );
                            })}

                            {/* Episode Visualizer — appears on last step */}
                            <div className={`transition-all duration-700 overflow-hidden ${processStep >= 4 ? 'max-h-24 opacity-100' : 'max-h-0 opacity-0'}`}>
                                <div className="pt-2 px-3">
                                    <div className="flex gap-2">
                                        {[...Array(episodes)].map((_, i) => (
                                            <div
                                                key={i}
                                                className="h-10 flex-1 bg-[#0A192F] border-2 border-[#0A192F] rounded-md animate-pop-in"
                                                style={{ animationDelay: `${i * 0.08}s` }}
                                            />
                                        ))}
                                    </div>
                                    <p className="font-mono text-xs font-bold text-[#0A192F]/50 uppercase tracking-widest mt-2 text-center">
                                        {episodes} arcs locked in
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Direction tag */}
                    {selectedDirectionObj && (
                        <div className="mt-4 flex items-center justify-center gap-2">
                            <div className="inline-flex items-center gap-2 bg-white border-2 border-[#0A192F] rounded-full px-4 py-2 shadow-[2px_2px_0px_#0A192F]">
                                <span className="font-mono text-xs font-black uppercase tracking-widest text-[#0A192F]/50">Direction:</span>
                                <span className="font-black text-sm text-[#0A192F]">{selectedDirectionObj.title}</span>
                                <div className="w-3 h-3 rounded-full border border-[#0A192F]" style={{ backgroundColor: selectedDirectionObj.color }} />
                            </div>
                        </div>
                    )}
                </div>
            </div>

            {/* ── Styles (page-specific only) ── */}
            <style dangerouslySetInnerHTML={{
                __html: `
          @keyframes shine {
            100% { left: 200%; }
          }
          @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(400%); }
          }
          .animate-shine { animation: shine 1.5s ease-in-out infinite; }
          .animate-shimmer { animation: shimmer 1.4s ease-in-out infinite; }
          .border-3 { border-width: 3px; }
        `}} />
        </div>
    );
};

export default StoryInputPage;