import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Plus,
    Clock,
    Flame,
    Activity,
    X,
    FileJson,
    User,
    LogOut,
    Sparkles,
    FileText,
    Loader2
} from 'lucide-react';
import { listProjects, type ProjectResponse, type GeneratedSeries, type SeriesAnalysis } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import toast from 'react-hot-toast';

// Mock Data with varying content to demonstrate Masonry layout
interface Project {
    id: number | string;
    title: string;
    excerpt: string;
    episodes: number;
    hookScore: number;
    lastEdited: string;
    thumbnailColor: string;
    pattern: string;
    generated_series?: GeneratedSeries;
    analysis?: SeriesAnalysis;
}

const COLORS = ["bg-[#33A1FF]", "bg-[#FF9E9E]", "bg-[#D4FF33]", "bg-[#C7B9FF]", "bg-[#FFB033]"];
const PATTERNS = ["circle", "stripes", "dots", "grid"];

const fallbackProjects: Project[] = [
    { id: 1, title: "The Deep Sea Paradox", excerpt: "A diver finds an oxygen-rich 1800s study at the bottom of the Mariana Trench.", episodes: 5, hookScore: 94, lastEdited: "2 hours ago", thumbnailColor: "bg-[#33A1FF]", pattern: "circle" },
    { id: 2, title: "Neon Shadows: Tokyo", excerpt: "Cyberpunk detective thriller involving memory-altering neon signs.", episodes: 8, hookScore: 88, lastEdited: "Yesterday", thumbnailColor: "bg-[#FF9E9E]", pattern: "stripes" },
    { id: 3, title: "The Silent Orbit", excerpt: "Astronaut wakes up alone, but the ship's AI insists there is a full crew on board.", episodes: 6, hookScore: 72, lastEdited: "3 days ago", thumbnailColor: "bg-[#D4FF33]", pattern: "dots" },
];

function mapApiToProject(p: ProjectResponse, idx: number): Project {
    return {
        id: p.id,
        title: p.title,
        excerpt: p.concept.slice(0, 120) + (p.concept.length > 120 ? "..." : ""),
        episodes: p.episode_count || 0,
        hookScore: p.overall_score || 0,
        lastEdited: p.created_at ? new Date(p.created_at).toLocaleDateString() : "Unknown",
        thumbnailColor: COLORS[idx % COLORS.length],
        pattern: PATTERNS[idx % PATTERNS.length],
        generated_series: p.generated_series as any,
        analysis: p.analysis as any,
    };
}

const DashboardPage = () => {
    const navigate = useNavigate();
    const { user, logout } = useAuth();
    const [isLoaded, setIsLoaded] = useState(false);

    useEffect(() => { document.title = 'Creator Studio — VBOX Episense'; }, []);
    const [selectedProject, setSelectedProject] = useState<Project | null>(null);
    const [exportFormat, setExportFormat] = useState('json');
    const [isExporting, setIsExporting] = useState(false);
    const [projects, setProjects] = useState<Project[]>(fallbackProjects);

    useEffect(() => {
        // Fetch projects from backend, fallback to mock data
        listProjects()
            .then(apiProjects => {
                if (apiProjects.length > 0) {
                    setProjects(apiProjects.map(mapApiToProject));
                }
            })
            .catch((err: any) => {
                const status = err?.response?.status;
                if (status === 401) {
                    toast.error("Session expired — please login again.");
                    logout();
                    return;
                }
                toast.error("Could not load projects. Showing demo projects instead.");
                // Backend unavailable — keep fallback data
            })
            .finally(() => setIsLoaded(true));
    }, []);

    const openModal = (project: Project) => {
        setSelectedProject(project);
        setExportFormat('json');
    };

    const closeModal = () => {
        setSelectedProject(null);
        setIsExporting(false);
    };

    // Helper to render abstract thumbnails
    const renderThumbnail = (color: string, pattern: string) => {
        return (
            <div className={`w-full h-32 rounded-2xl border-4 border-[#0A192F] mb-4 relative overflow-hidden ${color}`}>
                {pattern === 'circle' && <div className="absolute -bottom-10 -right-10 w-24 h-24 bg-[#0A192F]/10 rounded-full"></div>}
                {pattern === 'stripes' && <div className="absolute inset-0 opacity-10" style={{ backgroundImage: 'repeating-linear-gradient(45deg, transparent, transparent 10px, #0A192F 10px, #0A192F 20px)' }}></div>}
                {pattern === 'dots' && <div className="absolute inset-0 opacity-20" style={{ backgroundImage: 'radial-gradient(#0A192F 2px, transparent 2px)', backgroundSize: '12px 12px' }}></div>}
                {pattern === 'grid' && <div className="absolute inset-0 opacity-10" style={{ backgroundImage: 'linear-gradient(#0A192F 2px, transparent 2px), linear-gradient(90deg, #0A192F 2px, transparent 2px)', backgroundSize: '20px 20px' }}></div>}

                {/* Play icon overlay */}
                <div className="absolute inset-0 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity bg-white/20 backdrop-blur-sm cursor-pointer">
                    <div className="w-10 h-10 bg-white border-2 border-[#0A192F] rounded-full flex items-center justify-center shadow-[2px_2px_0px_#0A192F]">
                        <Sparkles className="w-5 h-5 text-[#0A192F]" />
                    </div>
                </div>
            </div>
        );
    };

    return (
        <div className="min-h-screen bg-[#FDFBF7] text-[#0A192F] font-sans relative overflow-x-hidden selection:bg-[#33A1FF] selection:text-white pb-24">

            {/* Neo-Pop Dot Background */}
            <div className="fixed inset-0 z-0 pointer-events-none opacity-[0.15]"
                style={{ backgroundImage: 'radial-gradient(#0A192F 2px, transparent 2px)', backgroundSize: '24px 24px' }}>
            </div>

            <div className="max-w-7xl mx-auto px-4 md:px-6 pt-8 relative z-10">

                {/* Header: Avatar + New Story */}
                <header className="flex flex-col sm:flex-row justify-between items-center mb-12 gap-6 bg-white border-4 border-[#0A192F] rounded-full p-4 shadow-[8px_8px_0px_#0A192F]">

                    {/* Avatar Profile */}
                    <div className="flex items-center gap-4">
                        <div className="w-14 h-14 bg-[#FF9E9E] border-4 border-[#0A192F] rounded-full flex items-center justify-center shadow-[2px_2px_0px_#0A192F] overflow-hidden">
                            <User className="w-6 h-6 text-[#0A192F]" strokeWidth={3} />
                        </div>
                        <div>
                            <h2 className="text-xl font-black tracking-tight leading-none mb-1">{user ? user : 'Creator Studio'}</h2>
                            <p className="font-bold text-xs text-[#0A192F]/50 uppercase tracking-widest">Your Workspace</p>
                        </div>
                        <button
                            onClick={logout}
                            className="bg-[#FDFBF7] border-2 border-[#0A192F] rounded-full p-2 hover:bg-[#FF9E9E] transition-colors shadow-[2px_2px_0px_#0A192F] active:shadow-none active:translate-y-[2px] ml-4"
                            title="Logout"
                        >
                            <LogOut className="w-4 h-4 text-[#0A192F]" />
                        </button>
                    </div>

                    <button
                        onClick={() => navigate('/input')}
                        className="w-full sm:w-auto bg-[#D4FF33] text-[#0A192F] border-4 border-[#0A192F] rounded-full px-8 py-3 font-black text-sm uppercase tracking-wide shadow-[4px_4px_0px_#0A192F] hover:shadow-[6px_6px_0px_#0A192F] hover:-translate-y-1 active:translate-y-[2px] active:shadow-none transition-all flex items-center justify-center gap-2 group">
                        <Plus className="w-5 h-5 group-hover:rotate-90 transition-transform" strokeWidth={3} /> New Story Arc
                    </button>
                </header>

                {/* Section Title */}
                <div className="mb-8 flex items-center gap-3">
                    <div className="w-4 h-4 bg-[#33A1FF] border-2 border-[#0A192F] rounded-sm"></div>
                    <h3 className="text-2xl font-black uppercase tracking-tight">Your Series</h3>
                </div>

                {/* Masonry Grid */}
                <div className="columns-1 md:columns-2 lg:columns-3 gap-6 space-y-6">
                    {projects.map((project, index) => (
                        <div
                            key={project.id}
                            onClick={() => openModal(project)}
                            className={`break-inside-avoid inline-block w-full bg-white border-4 border-[#0A192F] rounded-[2rem] p-5 cursor-pointer transition-all duration-500 group
                ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-12'}
                shadow-[6px_6px_0px_#0A192F] hover:-translate-y-2 hover:shadow-[12px_12px_0px_#0A192F]`}
                            style={{ transitionDelay: isLoaded ? `${index * 100}ms` : '0ms' }}
                        >

                            {/* Abstract Thumbnail */}
                            {renderThumbnail(project.thumbnailColor, project.pattern)}

                            {/* Title & Excerpt */}
                            <h4 className="text-xl font-black leading-tight mb-2 group-hover:text-[#33A1FF] transition-colors">{project.title}</h4>
                            <p className="font-bold text-sm text-[#0A192F]/60 mb-6 leading-snug">
                                {project.excerpt}
                            </p>

                            {/* Stats Footer */}
                            <div className="flex items-center justify-between pt-4 border-t-4 border-dashed border-[#0A192F]/10">
                                <div className="flex flex-col gap-1">
                                    <div className="flex items-center gap-1.5 text-[10px] font-black uppercase tracking-widest text-[#0A192F]/50">
                                        <Clock className="w-3 h-3" /> {project.lastEdited}
                                    </div>
                                    <div className="flex items-center gap-1.5 text-[10px] font-black uppercase tracking-widest text-[#0A192F]">
                                        <Activity className="w-3 h-3 text-[#33A1FF]" /> {project.episodes} Episodes
                                    </div>
                                </div>

                                <div className="flex flex-col items-end">
                                    <span className="text-[10px] font-black uppercase tracking-widest text-[#0A192F]/50 mb-1">Hook Score</span>
                                    <div className="bg-[#FDFBF7] border-2 border-[#0A192F] px-2 py-1 rounded-lg text-sm font-black flex items-center gap-1 shadow-[2px_2px_0px_#0A192F]">
                                        {project.hookScore} <Flame className="w-3 h-3 text-[#FF4D4D] fill-current" />
                                    </div>
                                </div>
                            </div>

                        </div>
                    ))}
                </div>
            </div>

            {/* Export Modal Overlay */}
            <div className={`fixed inset-0 z-50 flex items-center justify-center transition-all duration-300 ${selectedProject ? 'opacity-100 pointer-events-auto bg-[#0A192F]/80 backdrop-blur-md' : 'opacity-0 pointer-events-none'}`}>

                {selectedProject && (
                    <div className="bg-white border-4 border-[#0A192F] rounded-[2.5rem] w-[90%] max-w-lg shadow-[16px_16px_0px_#D4FF33] animate-modal-in flex flex-col overflow-hidden relative">

                        {/* Modal Header */}
                        <div className="bg-[#FDFBF7] border-b-4 border-[#0A192F] p-6 flex justify-between items-center relative">
                            <div>
                                <span className="bg-[#D4FF33] border-2 border-[#0A192F] px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-widest mb-2 inline-block">Export & Share</span>
                                <h2 className="text-2xl font-black tracking-tight">{selectedProject.title}</h2>
                            </div>
                            <button
                                onClick={closeModal}
                                className="w-10 h-10 bg-white border-2 border-[#0A192F] rounded-full flex items-center justify-center shadow-[2px_2px_0px_#0A192F] hover:bg-[#FF9E9E] hover:scale-105 active:scale-95 transition-all"
                            >
                                <X className="w-5 h-5" />
                            </button>
                        </div>

                        {/* Modal Body */}
                        <div className="p-6 md:p-8">

                            <h4 className="text-xs font-black uppercase tracking-widest text-[#0A192F]/50 mb-4">Select Format</h4>

                            {/* Format Options Grid */}
                            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">

                                <button
                                    onClick={() => !isExporting && setExportFormat('json')}
                                    className={`flex flex-col items-center gap-3 p-4 rounded-2xl border-4 transition-all
                    ${exportFormat === 'json' ? 'bg-[#33A1FF]/10 border-[#33A1FF] shadow-[4px_4px_0px_#33A1FF]' : 'bg-[#FDFBF7] border-[#0A192F] hover:shadow-[4px_4px_0px_#0A192F]'}`}
                                >
                                    <FileJson className={`w-8 h-8 ${exportFormat === 'json' ? 'text-[#33A1FF]' : 'text-[#0A192F]'}`} />
                                    <span className="font-black text-sm uppercase">JSON</span>
                                </button>

                                <button
                                    onClick={() => !isExporting && setExportFormat('pdf')}
                                    className={`flex flex-col items-center gap-3 p-4 rounded-2xl border-4 transition-all
                    ${exportFormat === 'pdf' ? 'bg-[#FF9E9E]/10 border-[#FF4D4D] shadow-[4px_4px_0px_#FF4D4D]' : 'bg-[#FDFBF7] border-[#0A192F] hover:shadow-[4px_4px_0px_#0A192F]'}`}
                                >
                                    <FileText className={`w-8 h-8 ${exportFormat === 'pdf' ? 'text-[#FF4D4D]' : 'text-[#0A192F]'}`} />
                                    <span className="font-black text-sm uppercase">PDF</span>
                                </button>

                                <button
                                    onClick={() => !isExporting && navigate('/analytics')}
                                    className={`flex flex-col items-center gap-3 p-4 rounded-2xl border-4 transition-all
                    ${exportFormat === 'link' ? 'bg-[#D4FF33]/20 border-[#0A192F] shadow-[4px_4px_0px_#0A192F]' : 'bg-[#FDFBF7] border-[#0A192F] hover:shadow-[4px_4px_0px_#0A192F]'}`}
                                >
                                    <Activity className={`w-8 h-8 text-[#0A192F]`} />
                                    <span className="font-black text-sm uppercase">Analytics</span>
                                </button>

                            </div>

                            {/* Dynamic Detail Text */}
                            <div className="bg-[#0A192F] text-white p-4 rounded-xl mb-8 flex gap-4 items-start">
                                <div className="mt-1">
                                    {exportFormat === 'json' && <FileJson className="w-5 h-5 text-[#33A1FF]" />}
                                    {exportFormat === 'pdf' && <FileText className="w-5 h-5 text-[#FF9E9E]" />}
                                    {exportFormat === 'link' && <Activity className="w-5 h-5 text-[#D4FF33]" />}
                                </div>
                                <div>
                                    <h5 className="font-black text-sm mb-1 uppercase tracking-wide">
                                        {exportFormat === 'json' ? 'API Payload Ready' : exportFormat === 'pdf' ? 'Script Document' : 'Series Analytics'}
                                    </h5>
                                    <p className="text-xs font-medium text-white/70">
                                        {exportFormat === 'json' ? 'Exports raw narrative blocks, sentiment scores, and continuity maps required by the VBOX rendering engine.' :
                                            exportFormat === 'pdf' ? 'Generates a clean, readable script format perfect for sharing with voice actors or producers.' :
                                                'Generates a secure, read-only URL to share the Episode Breakdown and Analytics dashboard with your team.'}
                                    </p>
                                </div>
                            </div>

                            {/* Action Area */}
                            <button
                                onClick={() => {
                                    if (selectedProject) {
                                        toast.success("Opening workspace...", {
                                            icon: '🚀',
                                            duration: 2000,
                                            style: {
                                                border: '4px solid #0A192F',
                                                padding: '16px',
                                                color: '#0A192F',
                                                background: '#33A1FF',
                                                fontWeight: 900,
                                                textTransform: 'uppercase',
                                                borderRadius: '999px',
                                                boxShadow: '4px 4px 0px #0A192F'
                                            }
                                        });
                                        navigate('/breakdown', {
                                            state: {
                                                series: selectedProject.generated_series,
                                                analysis: selectedProject.analysis
                                            }
                                        });
                                    } else {
                                        navigate('/breakdown');
                                    }
                                }}
                                disabled={isExporting}
                                className="w-full bg-[#0A192F] text-white border-4 border-[#0A192F] px-6 py-4 rounded-full font-black text-lg uppercase tracking-wide shadow-[4px_4px_0px_#33A1FF] hover:shadow-[6px_6px_0px_#33A1FF] hover:-translate-y-1 active:translate-y-[2px] active:shadow-none transition-all flex items-center justify-center gap-3 disabled:pointer-events-none disabled:opacity-90"
                            >
                                {isExporting ? (
                                    <><Loader2 className="w-6 h-6 animate-spin text-[#D4FF33]" /> Processing...</>
                                ) : (
                                    <>Open Workspace</>
                                )}
                            </button>

                        </div>
                    </div>
                )}
            </div>

        </div>
    );
};

export default DashboardPage;