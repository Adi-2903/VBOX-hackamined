import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Play,
    Scissors,
    Flame,
    TrendingDown,
    HeartPulse,
    Smartphone,
    CheckCircle2
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const LandingPage = () => {
    const navigate = useNavigate();
    const { isAuthenticated } = useAuth();
    const [activeTab, setActiveTab] = useState(0);

    useEffect(() => { document.title = 'VBOX Episense — AI Story Intelligence'; }, []);

    // Auto-switch tabs in the demo section
    useEffect(() => {
        const timer = setInterval(() => {
            setActiveTab((prev) => (prev + 1) % 3);
        }, 3000);
        return () => clearInterval(timer);
    }, []);

    return (
        <div className="min-h-screen bg-[#FDFBF7] text-[#0A192F] font-sans selection:bg-[#D4FF33] selection:text-[#0A192F] overflow-x-hidden">

            {/* Playful Floating Navigation */}
            <nav className="fixed top-6 left-1/2 transform -translate-x-1/2 z-50 w-[90%] max-w-4xl bg-white/80 backdrop-blur-xl border-2 border-[#0A192F] rounded-full px-4 py-3 flex justify-between items-center shadow-[4px_4px_0px_#0A192F] transition-all hover:shadow-[6px_6px_0px_#0A192F] hover:-translate-y-0.5">
                <div className="flex items-center gap-2 pl-2">
                    <div className="w-8 h-8 bg-[#FF9E9E] rounded-full border-2 border-[#0A192F] flex items-center justify-center">
                        <Play className="w-4 h-4 text-[#0A192F] fill-current ml-0.5" />
                    </div>
                    <span className="font-bold text-xl tracking-tight">Episense</span>
                </div>
                <div className="hidden md:flex items-center gap-6 font-semibold text-sm">
                    <a href="#features" className="hover:text-[#FF4D4D] transition-colors">The Toolkit</a>
                    <a href="#demo" className="hover:text-[#33A1FF] transition-colors">How it Works</a>
                </div>
                <button
                    onClick={() => navigate(isAuthenticated ? '/dashboard' : '/auth')}
                    className="bg-[#D4FF33] border-2 border-[#0A192F] text-[#0A192F] px-6 py-2 rounded-full font-bold text-sm hover:bg-[#C2FA00] transition-colors shadow-[2px_2px_0px_#0A192F] active:translate-x-[2px] active:translate-y-[2px] active:shadow-none">
                    {isAuthenticated ? 'Open Studio' : 'Try the Beta'}
                </button>
            </nav>

            {/* Casual, High-Impact Hero */}
            <section className="pt-40 pb-20 px-6 max-w-7xl mx-auto relative">
                {/* Background "Sticker" Elements */}
                <div className="absolute top-20 right-10 md:right-32 bg-[#C7B9FF] border-2 border-[#0A192F] rounded-full px-4 py-2 font-bold text-sm shadow-[4px_4px_0px_#0A192F] rotate-12 animate-float">
                    ✨ 90s Constraint
                </div>
                <div className="absolute bottom-20 left-10 md:left-20 bg-[#33A1FF] border-2 border-[#0A192F] text-white rounded-full px-4 py-2 font-bold text-sm shadow-[4px_4px_0px_#0A192F] -rotate-6 animate-float" style={{ animationDelay: '1s' }}>
                    📈 Stop the scroll
                </div>

                <div className="flex flex-col items-center text-center max-w-4xl mx-auto z-10 relative">
                    <div className="inline-flex items-center gap-2 bg-white border-2 border-[#0A192F] rounded-full px-4 py-1.5 text-xs font-bold uppercase tracking-wider mb-8 shadow-[2px_2px_0px_#0A192F]">
                        <span className="w-2 h-2 rounded-full bg-[#FF4D4D] animate-pulse"></span>
                        Quantloop VBOX Hackathon
                    </div>

                    <h1 className="text-5xl md:text-7xl lg:text-[5.5rem] font-black tracking-tight leading-[0.95] mb-8">
                        Write vertical series that <br className="hidden md:block" />
                        <span className="relative inline-block mt-2">
                            <span className="relative z-10">refuse to be swiped.</span>
                            <span className="absolute bottom-1 md:bottom-3 left-0 w-full h-4 md:h-6 bg-[#D4FF33] -z-10 -rotate-1 rounded-sm"></span>
                        </span>
                    </h1>

                    <p className="text-lg md:text-xl text-[#0A192F]/70 font-medium max-w-2xl mb-10 leading-relaxed">
                        Drop your raw story idea. Our intelligence engine slices it into a perfect 5-to-8 episode arc, scores your cliffhangers, and flags exactly where viewers will get bored.
                    </p>

                    <div className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
                        <button
                            onClick={() => navigate(isAuthenticated ? '/dashboard' : '/auth')}
                            className="bg-[#0A192F] text-white text-lg font-bold px-8 py-4 rounded-full flex items-center justify-center gap-3 hover:-translate-y-1 transition-transform shadow-[4px_4px_0px_#FF9E9E]">
                            <Smartphone className="w-5 h-5" /> Start Analyzing
                        </button>
                        <button className="bg-white border-2 border-[#0A192F] text-[#0A192F] text-lg font-bold px-8 py-4 rounded-full flex items-center justify-center gap-3 hover:bg-[#FDFBF7] transition-colors shadow-[4px_4px_0px_#0A192F]">
                            View Engine Architecture
                        </button>
                    </div>
                </div>
            </section>

            {/* Media Creator "Bento Box" Features */}
            <section id="features" className="py-20 px-6 max-w-7xl mx-auto">
                <div className="mb-12">
                    <h2 className="text-4xl font-black mb-4">The Creator Toolkit</h2>
                    <p className="text-[#0A192F]/60 font-medium text-lg">Five intelligence modules built for the vertical format.</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 auto-rows-[280px]">

                    {/* Module 1: Decomposer (Spans 2 cols) */}
                    <div className="md:col-span-2 bg-[#C7B9FF] rounded-[2.5rem] border-2 border-[#0A192F] p-8 shadow-[6px_6px_0px_#0A192F] relative overflow-hidden group">
                        <div className="relative z-10 w-full md:w-2/3">
                            <div className="w-12 h-12 bg-white rounded-full border-2 border-[#0A192F] flex items-center justify-center mb-4 shadow-[2px_2px_0px_#0A192F]">
                                <Scissors className="w-6 h-6 text-[#0A192F]" />
                            </div>
                            <h3 className="text-2xl font-black mb-2">Story Decomposer</h3>
                            <p className="font-medium text-[#0A192F]/80">
                                LLMs and NLP pipelines ingest your single idea and auto-slice it into 5-8 structured, 90-second episodes. Timeline and character continuity are locked in automatically.
                            </p>
                        </div>
                        {/* Playful UI Mock element */}
                        <div className="absolute right-0 bottom-0 w-64 translate-x-12 translate-y-12 md:translate-x-4 md:translate-y-4 bg-white border-2 border-[#0A192F] rounded-2xl p-4 shadow-lg rotate-[-5deg] group-hover:rotate-0 transition-transform duration-300">
                            <div className="flex gap-2 mb-2">
                                <div className="w-12 h-16 bg-[#FF9E9E] rounded-lg border-2 border-[#0A192F]"></div>
                                <div className="w-12 h-16 bg-[#33A1FF] rounded-lg border-2 border-[#0A192F]"></div>
                                <div className="w-12 h-16 bg-[#D4FF33] rounded-lg border-2 border-[#0A192F]"></div>
                            </div>
                            <div className="text-xs font-bold uppercase text-center mt-2">Arc Generated</div>
                        </div>
                    </div>

                    {/* Module 2: Cliffhanger */}
                    <div className="bg-[#FF9E9E] rounded-[2.5rem] border-2 border-[#0A192F] p-8 shadow-[6px_6px_0px_#0A192F] flex flex-col justify-between hover:-translate-y-1 transition-transform">
                        <div>
                            <div className="w-12 h-12 bg-white rounded-full border-2 border-[#0A192F] flex items-center justify-center mb-4 shadow-[2px_2px_0px_#0A192F]">
                                <Flame className="w-6 h-6 text-[#FF4D4D] fill-current" />
                            </div>
                            <h3 className="text-2xl font-black mb-2">The Hook Score</h3>
                            <p className="font-medium text-[#0A192F]/80 text-sm">
                                Heuristic scoring analyzes the final 5 seconds of an episode. If your cliffhanger is weak, we'll tell you to cut it.
                            </p>
                        </div>
                        <div className="bg-white border-2 border-[#0A192F] rounded-full px-4 py-2 font-black text-xl flex justify-between items-center mt-4">
                            <span>Score:</span>
                            <span className="text-[#FF4D4D]">94/100</span>
                        </div>
                    </div>

                    {/* Module 3: Retention */}
                    <div className="bg-[#D4FF33] rounded-[2.5rem] border-2 border-[#0A192F] p-8 shadow-[6px_6px_0px_#0A192F] flex flex-col justify-between hover:-translate-y-1 transition-transform">
                        <div>
                            <div className="w-12 h-12 bg-white rounded-full border-2 border-[#0A192F] flex items-center justify-center mb-4 shadow-[2px_2px_0px_#0A192F]">
                                <TrendingDown className="w-6 h-6 text-[#0A192F]" />
                            </div>
                            <h3 className="text-2xl font-black mb-2">Drop-off Radar</h3>
                            <p className="font-medium text-[#0A192F]/80 text-sm">
                                ML models predict exactly when viewers will swipe away within your 90-second timeline.
                            </p>
                        </div>
                        {/* Simple timeline visual */}
                        <div className="h-4 w-full bg-white rounded-full border-2 border-[#0A192F] relative mt-4 overflow-hidden">
                            <div className="absolute top-0 left-0 h-full w-[45%] bg-[#0A192F]"></div>
                            <div className="absolute top-[-4px] left-[45%] w-1.5 h-6 bg-[#FF4D4D] rotate-12"></div>
                        </div>
                    </div>

                    {/* Module 4: Emotional & Optimization (Spans 2 cols) */}
                    <div className="md:col-span-2 bg-[#33A1FF] rounded-[2.5rem] border-2 border-[#0A192F] p-8 shadow-[6px_6px_0px_#0A192F] relative overflow-hidden group text-white">
                        <div className="relative z-10 w-full md:w-2/3">
                            <div className="w-12 h-12 bg-white rounded-full border-2 border-[#0A192F] flex items-center justify-center mb-4 shadow-[2px_2px_0px_#0A192F]">
                                <HeartPulse className="w-6 h-6 text-[#33A1FF]" />
                            </div>
                            <h3 className="text-2xl font-black mb-2 text-white">Vibe Check & Optimization</h3>
                            <p className="font-medium text-white/90">
                                Sentiment analysis maps the emotional arc to find "flat zones." Our Suggestion Engine then provides structured fixes (like moving a plot twist earlier) to rescue engagement.
                            </p>
                        </div>
                        <div className="absolute right-8 bottom-8 hidden md:flex flex-col gap-2">
                            <div className="bg-white text-[#0A192F] font-bold text-xs px-3 py-1.5 rounded-full border-2 border-[#0A192F] shadow-[2px_2px_0px_#0A192F] animate-bounce">
                                Fix pacing @ 0:42 🔧
                            </div>
                            <div className="bg-[#D4FF33] text-[#0A192F] font-bold text-xs px-3 py-1.5 rounded-full border-2 border-[#0A192F] shadow-[2px_2px_0px_#0A192F] translate-x-4">
                                Add B-roll here 🎥
                            </div>
                        </div>
                    </div>

                </div>
            </section>

            {/* Interactive "Vertical Player" Demo Section */}
            <section id="demo" className="py-20 bg-[#0A192F] text-white border-y-2 border-[#0A192F] relative">
                {/* Subtle grid in dark mode */}
                <div className="absolute inset-0 opacity-10" style={{ backgroundImage: 'radial-gradient(#ffffff 1px, transparent 1px)', backgroundSize: '24px 24px' }}></div>

                <div className="max-w-7xl mx-auto px-6 relative z-10 flex flex-col lg:flex-row items-center gap-16">

                    <div className="flex-1">
                        <div className="inline-block bg-[#FF9E9E] text-[#0A192F] px-3 py-1 rounded-full font-bold text-xs uppercase mb-6 border-2 border-[#0A192F] shadow-[2px_2px_0px_#FF4D4D]">Live Engine Output</div>
                        <h2 className="text-4xl md:text-5xl font-black mb-6">Optimizing for the scroll.</h2>
                        <p className="text-white/70 font-medium text-lg mb-8 max-w-lg">
                            See how the Episense engine analyzes a 90-second vertical episode in real-time, mapping emotion and predicting retention.
                        </p>

                        {/* Custom Tab UI */}
                        <div className="flex flex-col gap-3">
                            {[
                                { title: "Sentiment Analysis", desc: "Detecting flat zones in dialogue.", color: "bg-[#33A1FF]" },
                                { title: "Retention Prediction", desc: "ML flags drop-off risk at 0:45.", color: "bg-[#FF9E9E]" },
                                { title: "Cliffhanger Score", desc: "Evaluating final 5s curiosity gap.", color: "bg-[#D4FF33]" }
                            ].map((tab, idx) => (
                                <div
                                    key={idx}
                                    className={`p-4 rounded-2xl border-2 transition-all cursor-pointer ${activeTab === idx ? 'bg-white text-[#0A192F] border-white' : 'bg-[#0A192F] border-[#ffffff30] hover:border-white text-white'}`}
                                    onClick={() => setActiveTab(idx)}
                                >
                                    <div className="flex items-center gap-3">
                                        <div className={`w-3 h-3 rounded-full border-2 border-[#0A192F] ${tab.color}`}></div>
                                        <h4 className="font-bold">{tab.title}</h4>
                                    </div>
                                    {activeTab === idx && <p className="text-sm mt-2 opacity-80 font-medium ml-6">{tab.desc}</p>}
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Vertical Video Phone Mockup */}
                    <div className="w-[300px] h-[600px] bg-white rounded-[3rem] border-8 border-[#1a2b4a] shadow-[12px_12px_0px_rgba(0,0,0,0.5)] relative overflow-hidden flex-shrink-0">
                        {/* Phone Notch */}
                        <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-1/3 h-6 bg-[#1a2b4a] rounded-b-xl z-20"></div>

                        {/* Fake Video Content Area */}
                        <div className="absolute inset-0 bg-[#E5E5EA] flex items-center justify-center">
                            <div className="text-[#0A192F]/20 font-black text-4xl text-center leading-none">VBOX<br />VIDEO<br />FEED</div>
                        </div>

                        {/* Dynamic UI Overlay based on active tab */}
                        <div className="absolute inset-0 z-10 p-4 flex flex-col justify-end">
                            {/* Visualizer Area */}
                            <div className="bg-white/90 backdrop-blur-sm border-2 border-[#0A192F] rounded-2xl p-4 shadow-[4px_4px_0px_#0A192F] mb-4 transition-all duration-300">

                                {activeTab === 0 && (
                                    <div className="animate-fade-in">
                                        <div className="text-xs font-bold text-[#0A192F] mb-2">EMOTIONAL ARC</div>
                                        <div className="flex items-end h-12 gap-1">
                                            {[4, 6, 5, 8, 4, 4, 4, 4, 7, 9, 10].map((h, i) => (
                                                <div key={i} className={`flex-1 rounded-t-sm ${i >= 4 && i <= 7 ? 'bg-[#FF4D4D]' : 'bg-[#33A1FF]'}`} style={{ height: `${h * 10}%` }}></div>
                                            ))}
                                        </div>
                                        <div className="text-[10px] font-bold text-[#FF4D4D] mt-2">! Flat zone detected</div>
                                    </div>
                                )}

                                {activeTab === 1 && (
                                    <div className="animate-fade-in">
                                        <div className="text-xs font-bold text-[#0A192F] mb-2">RETENTION RISK</div>
                                        <div className="w-full h-8 bg-gray-200 rounded-full overflow-hidden relative border-2 border-[#0A192F]">
                                            <div className="absolute top-0 left-0 h-full w-[60%] bg-[#D4FF33]"></div>
                                            <div className="absolute top-0 left-[60%] h-full w-[15%] bg-[#FF4D4D]"></div>
                                            <div className="absolute top-0 left-[75%] h-full w-[25%] bg-gray-300"></div>
                                        </div>
                                        <div className="text-[10px] font-bold text-[#0A192F] mt-2">High drop-off @ 0:45</div>
                                    </div>
                                )}

                                {activeTab === 2 && (
                                    <div className="animate-fade-in">
                                        <div className="text-xs font-bold text-[#0A192F] mb-2">CLIFFHANGER SCORE</div>
                                        <div className="flex items-baseline gap-1">
                                            <span className="text-3xl font-black text-[#0A192F]">92</span>
                                            <span className="text-sm font-bold text-gray-500">/100</span>
                                        </div>
                                        <div className="w-full h-2 bg-[#D4FF33] mt-2 rounded-full border border-[#0A192F]"></div>
                                        <div className="text-[10px] font-bold text-[#33A1FF] mt-2 flex items-center gap-1"><CheckCircle2 className="w-3 h-3" /> Swipe guaranteed</div>
                                    </div>
                                )}

                            </div>

                            {/* Bottom Video Controls Mock */}
                            <div className="flex items-center gap-2">
                                <div className="w-8 h-8 rounded-full bg-white border-2 border-[#0A192F] flex flex-shrink-0"></div>
                                <div className="h-8 bg-white border-2 border-[#0A192F] rounded-full flex-1 flex items-center px-3">
                                    <div className="w-2/3 h-2 bg-gray-200 rounded-full overflow-hidden">
                                        <div className="w-1/2 h-full bg-[#0A192F]"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Casual Marquee Footer Separator */}
            <div className="bg-[#D4FF33] py-3 border-b-2 border-[#0A192F] overflow-hidden flex whitespace-nowrap">
                <div className="animate-marquee inline-block font-black uppercase text-[#0A192F] tracking-wide">
                    {[...Array(6)].map((_, j) => (
                        <span key={j} className="inline-flex items-center gap-6 mx-4">
                            <span>NLP Pipelines</span> <span>❋</span>
                            <span>Sentiment Analysis</span> <span>❋</span>
                            <span>ML Prediction</span> <span>❋</span>
                            <span>Heuristic Scoring</span> <span>❋</span>
                        </span>
                    ))}
                </div>
            </div>

            {/* Playful Footer */}
            <footer className="bg-white py-12 px-6">
                <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
                    <div className="flex items-center gap-2">
                        <div className="w-8 h-8 bg-[#33A1FF] rounded-full border-2 border-[#0A192F] flex items-center justify-center">
                            <Play className="w-4 h-4 text-white fill-current ml-0.5" />
                        </div>
                        <span className="font-black text-2xl tracking-tight">Episense</span>
                    </div>

                    <div className="flex gap-6 font-bold text-sm text-[#0A192F]/70">
                        <a href="#" className="hover:text-[#FF4D4D] transition-colors">Docs</a>
                        <a href="https://thevbox.in/" className="hover:text-[#33A1FF] transition-colors">VBOX Project</a>
                        <a href="#" className="hover:text-[#D4FF33] transition-colors">Hackathon</a>
                    </div>

                    <div className="text-xs font-bold text-[#0A192F]/50 uppercase bg-[#FDFBF7] px-4 py-2 rounded-full border-2 border-[#0A192F]/10">
                        Built for Quantloop Tech 2026
                    </div>
                </div>
            </footer>

            {/* Embedded Styles for custom brutalist/pop animations */}
            <style dangerouslySetInnerHTML={{
                __html: `
        @keyframes float {
          0%, 100% { transform: translateY(0) rotate(var(--tw-rotate, 0deg)); }
          50% { transform: translateY(-10px) rotate(var(--tw-rotate, 0deg)); }
        }
        @keyframes marquee {
          0% { transform: translateX(0%); }
          100% { transform: translateX(-50%); }
        }
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(5px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-float {
          animation: float 4s ease-in-out infinite;
        }
        .animate-marquee {
          animation: marquee 15s linear infinite;
        }
        .animate-fade-in {
          animation: fadeIn 0.3s ease-out forwards;
        }
      `}} />
        </div>
    );
};

export default LandingPage;