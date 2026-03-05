import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Wand2,
    ArrowLeft,
    Minus,
    Plus,
    Play,
    PenTool,
    BrainCircuit,
    Timer
} from 'lucide-react';

const EpisenseInputCanvas = () => {
    const navigate = useNavigate();
    const [concept, setConcept] = useState('');
    const [episodes, setEpisodes] = useState(5);
    const [selectedGenres, setSelectedGenres] = useState(['Thriller']);
    const [isProcessing, setIsProcessing] = useState(false);
    const [processStep, setProcessStep] = useState(0);

    const availableGenres = ['Thriller', 'Sci-Fi', 'Rom-Com', 'Horror', 'Drama', 'Lore/Myth'];

    // Magic Auto-fill for demo purposes
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

    const toggleGenre = (genre: string) => {
        setSelectedGenres(prev =>
            prev.includes(genre)
                ? prev.filter(g => g !== genre)
                : [...prev, genre]
        );
    };

    const handleArchitect = () => {
        if (!concept.trim()) return;
        setIsProcessing(true);

        // Simulate engine processing steps
        setTimeout(() => setProcessStep(1), 800);  // Tokenizing
        setTimeout(() => setProcessStep(2), 1600); // Emotional Arc
        setTimeout(() => setProcessStep(3), 2500); // Slicing Episodes

        // Reset/Redirect mock
        setTimeout(() => {
            setIsProcessing(false);
            setProcessStep(0);
            setConcept('');
            navigate('/breakdown');
        }, 3500);
    };

    return (
        <div className="min-h-screen bg-[#FDFBF7] text-[#0A192F] font-sans relative overflow-x-hidden selection:bg-[#33A1FF] selection:text-white pb-20">

            {/* Neo-Pop Dotted Background */}
            <div className="fixed inset-0 z-0 pointer-events-none opacity-[0.15]"
                style={{ backgroundImage: 'radial-gradient(#0A192F 2px, transparent 2px)', backgroundSize: '24px 24px' }}>
            </div>

            <div className="max-w-7xl mx-auto px-6 pt-8 relative z-10">

                {/* Studio Navigation */}
                <nav className="flex justify-between items-center mb-12">
                    <button
                        onClick={() => navigate('/')}
                        className="flex items-center gap-3 font-black uppercase text-sm hover:-translate-x-2 transition-transform">
                        <div className="w-10 h-10 bg-[#FF9E9E] border-2 border-[#0A192F] rounded-full flex items-center justify-center shadow-[2px_2px_0px_#0A192F]">
                            <ArrowLeft className="w-5 h-5 text-[#0A192F]" />
                        </div>
                        Back to Hub
                    </button>

                    <div className="bg-white border-2 border-[#0A192F] rounded-full px-4 py-2 shadow-[2px_2px_0px_#0A192F] flex items-center gap-3">
                        <div className="w-2 h-2 rounded-full bg-[#D4FF33] animate-pulse"></div>
                        <span className="font-mono text-xs font-bold uppercase tracking-widest">VBOX Engine Ready</span>
                    </div>
                </nav>

                {/* Page Header */}
                <div className="mb-10">
                    <h1 className="text-5xl md:text-6xl font-black tracking-tight mb-4">
                        The Canvas.
                    </h1>
                    <p className="text-xl font-medium text-[#0A192F]/60 max-w-2xl">
                        Drop your raw narrative. We'll enforce the 90-second constraint and algorithmically structure the perfect multi-part hook.
                    </p>
                </div>

                {/* The Bento Layout */}
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8">

                    {/* Main Input Area (Spans 8 cols) */}
                    <div className="lg:col-span-8 bg-white border-4 border-[#0A192F] rounded-[2.5rem] p-6 md:p-8 shadow-[8px_8px_0px_#0A192F] relative flex flex-col group">

                        <div className="flex justify-between items-start mb-6">
                            <div className="flex items-center gap-3">
                                <div className="bg-[#C7B9FF] border-2 border-[#0A192F] p-2 rounded-xl shadow-[2px_2px_0px_#0A192F]">
                                    <PenTool className="w-5 h-5" />
                                </div>
                                <h2 className="text-2xl font-black uppercase tracking-tight">Core Concept</h2>
                            </div>

                            {/* Magic Button */}
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

                        {/* Live Character/Token Count */}
                        <div className="flex justify-between items-center pt-4 border-t-2 border-dashed border-[#0A192F]/20 mt-4">
                            <span className="font-mono text-xs font-bold text-[#0A192F]/50 uppercase">
                                {concept.length === 0 ? 'Awaiting Input...' : 'Extracting Entities...'}
                            </span>
                            <span className={`font-mono text-sm font-black ${concept.length > 500 ? 'text-[#33A1FF]' : 'text-[#0A192F]'}`}>
                                {concept.length} chars
                            </span>
                        </div>
                    </div>

                    {/* Constraints & Parameters (Spans 4 cols) */}
                    <div className="lg:col-span-4 flex flex-col gap-6">

                        {/* Episode Constraint Block */}
                        <div className="bg-[#D4FF33] border-4 border-[#0A192F] rounded-[2rem] p-6 shadow-[6px_6px_0px_#0A192F] flex flex-col justify-between relative overflow-hidden">
                            {/* Graphic element */}
                            <div className="absolute -right-4 -top-4 w-24 h-24 border-4 border-[#0A192F]/10 rounded-full"></div>

                            <div className="relative z-10 mb-6">
                                <div className="flex items-center gap-2 mb-1">
                                    <Timer className="w-5 h-5" />
                                    <h3 className="font-black text-xl uppercase tracking-tight">Timeline</h3>
                                </div>
                                <p className="font-medium text-sm text-[#0A192F]/70">VBOX 90-second constraint enforced.</p>
                            </div>

                            {/* Tactile Stepper UI */}
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

                        {/* Vibe/Genre Sticker Block */}
                        <div className="bg-white border-4 border-[#0A192F] rounded-[2rem] p-6 shadow-[6px_6px_0px_#0A192F] flex-1">
                            <h3 className="font-black text-xl uppercase tracking-tight mb-4">The Vibe</h3>
                            <div className="flex flex-wrap gap-2">
                                {availableGenres.map(genre => {
                                    const isSelected = selectedGenres.includes(genre);
                                    return (
                                        <button
                                            key={genre}
                                            onClick={() => toggleGenre(genre)}
                                            className={`px-4 py-2 border-2 border-[#0A192F] rounded-full font-bold text-sm transition-all shadow-[2px_2px_0px_#0A192F] active:translate-y-[2px] active:translate-x-[2px] active:shadow-none
                        ${isSelected ? 'bg-[#C7B9FF] text-[#0A192F]' : 'bg-[#FDFBF7] hover:bg-[#EAEAEA]'}`}
                                        >
                                            {isSelected && <span className="mr-1">★</span>}
                                            {genre}
                                        </button>
                                    );
                                })}
                            </div>
                        </div>

                    </div>
                </div>

                {/* Giant Action Footer */}
                <div className="mt-8">
                    <button
                        onClick={handleArchitect}
                        disabled={!concept.trim()}
                        className="w-full bg-[#0A192F] text-white border-4 border-[#0A192F] rounded-[2.5rem] p-6 md:p-8 flex items-center justify-between group disabled:opacity-50 disabled:cursor-not-allowed shadow-[8px_8px_0px_#33A1FF] hover:shadow-[10px_10px_0px_#33A1FF] hover:-translate-y-1 active:translate-y-[4px] active:translate-x-[4px] active:shadow-none transition-all overflow-hidden relative"
                    >
                        {/* Hover shine effect */}
                        <div className="absolute top-0 -left-[100%] w-1/2 h-full bg-gradient-to-r from-transparent via-white/20 to-transparent skew-x-[-20deg] group-hover:animate-shine"></div>

                        <div className="flex items-center gap-6 relative z-10">
                            <div className="w-16 h-16 bg-[#33A1FF] border-2 border-[#0A192F] rounded-full flex items-center justify-center shadow-[4px_4px_0px_#0A192F] group-hover:scale-110 transition-transform">
                                <BrainCircuit className="w-8 h-8 text-[#0A192F]" />
                            </div>
                            <div className="text-left">
                                <h2 className="text-3xl md:text-4xl font-black uppercase tracking-tight">Architect the Series</h2>
                                <span className="font-mono text-sm text-[#33A1FF] font-bold">Inject into NLP Pipeline &rarr;</span>
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

            {/* Engine Processing Overlay (Replaces standard spinner with a cool narrative breakdown visual)
      */}
            <div className={`fixed inset-0 z-50 bg-[#FDFBF7]/90 backdrop-blur-xl flex flex-col items-center justify-center transition-all duration-500 ${isProcessing ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'}`}>

                <div className="max-w-xl w-full px-6">
                    <div className="flex items-center gap-4 mb-8">
                        <div className="w-12 h-12 bg-[#D4FF33] border-4 border-[#0A192F] rounded-full animate-spin flex items-center justify-center shadow-[4px_4px_0px_#0A192F]">
                            <div className="w-4 h-4 bg-[#0A192F] rounded-full"></div>
                        </div>
                        <h2 className="text-4xl font-black uppercase tracking-tight">VBOX Engine<br />Active.</h2>
                    </div>

                    <div className="bg-white border-4 border-[#0A192F] rounded-3xl p-6 shadow-[8px_8px_0px_#0A192F]">

                        <div className="space-y-4">
                            {/* Step 1 */}
                            <div className={`flex items-center gap-4 p-3 rounded-xl border-2 transition-all ${processStep >= 1 ? 'border-[#0A192F] bg-[#33A1FF]/10' : 'border-transparent opacity-30'}`}>
                                <div className={`w-6 h-6 rounded-full border-2 border-[#0A192F] flex items-center justify-center ${processStep >= 1 ? 'bg-[#33A1FF]' : 'bg-transparent'}`}>
                                    {processStep >= 1 && <div className="w-2 h-2 bg-[#0A192F] rounded-full"></div>}
                                </div>
                                <span className="font-bold text-lg">Decomposing entities & timeline...</span>
                            </div>

                            {/* Step 2 */}
                            <div className={`flex items-center gap-4 p-3 rounded-xl border-2 transition-all ${processStep >= 2 ? 'border-[#0A192F] bg-[#FF9E9E]/10' : 'border-transparent opacity-30'}`}>
                                <div className={`w-6 h-6 rounded-full border-2 border-[#0A192F] flex items-center justify-center ${processStep >= 2 ? 'bg-[#FF9E9E]' : 'bg-transparent'}`}>
                                    {processStep >= 2 && <div className="w-2 h-2 bg-[#0A192F] rounded-full"></div>}
                                </div>
                                <span className="font-bold text-lg">Mapping emotional trajectory...</span>
                            </div>

                            {/* Step 3 (Visualizing the 5-8 blocks) */}
                            <div className={`flex items-center gap-4 p-3 rounded-xl border-2 transition-all ${processStep >= 3 ? 'border-[#0A192F] bg-[#D4FF33]/10' : 'border-transparent opacity-30'}`}>
                                <div className={`w-6 h-6 rounded-full border-2 border-[#0A192F] flex items-center justify-center ${processStep >= 3 ? 'bg-[#D4FF33]' : 'bg-transparent'}`}>
                                    {processStep >= 3 && <div className="w-2 h-2 bg-[#0A192F] rounded-full"></div>}
                                </div>
                                <div className="flex-1">
                                    <span className="font-bold text-lg block mb-2">Slicing into {episodes} vertical arcs...</span>
                                    <div className="flex gap-2">
                                        {[...Array(episodes)].map((_, i) => (
                                            <div
                                                key={i}
                                                className="h-8 flex-1 bg-[#0A192F] border-2 border-[#0A192F] rounded-md animate-pop-in"
                                                style={{ animationDelay: `${(i * 0.1) + 2.5}s`, opacity: processStep >= 3 ? 1 : 0 }}
                                            ></div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
            </div>

            {/* Embedded Styles for custom brutalist/pop animations */}
            <style dangerouslySetInnerHTML={{
                __html: `
        @keyframes shine {
          100% { left: 200%; }
        }
        @keyframes popIn {
          0% { transform: scale(0); opacity: 0; }
          70% { transform: scale(1.1); opacity: 1; }
          100% { transform: scale(1); opacity: 1; }
        }
        .animate-shine {
          animation: shine 1.5s ease-in-out infinite;
        }
        .animate-pop-in {
          animation: popIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        }
      `}} />
        </div>
    );
};

export default EpisenseInputCanvas;