import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { useNavigate } from 'react-router-dom';
import {
    Play,
    Mail,
    Lock,
    User,
    ArrowRight,
    Sparkles,
    Github
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import toast from 'react-hot-toast';

const AuthPage = () => {
    const navigate = useNavigate();
    const { login } = useAuth();
    const [isLogin, setIsLogin] = useState(true);

    useEffect(() => { document.title = isLogin ? 'Login — VBOX Episense' : 'Sign Up — VBOX Episense'; }, [isLogin]);
    const [isShaking, setIsShaking] = useState(false);
    const [isSuccess, setIsSuccess] = useState(false);
    const [authError, setAuthError] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    // Form State
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [name, setName] = useState('');

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setAuthError(null);

        // Validation check (triggers shake if empty)
        if (!email || !password || (!isLogin && !name)) {
            setIsShaking(true);
            setTimeout(() => setIsShaking(false), 500);
            return;
        }

        setIsLoading(true);

        try {
            if (isLogin) {
                const res = await api.post('/auth/login', { email, password });
                login(res.data.access_token, res.data.name);
            } else {
                const res = await api.post('/auth/signup', { email, password, name });
                login(res.data.access_token, res.data.name);
            }

            // Trigger Success State & Confetti
            setIsSuccess(true);
            toast.success(isLogin ? "Welcome back!" : "Studio configured!", {
                icon: '🎬',
                duration: 3000,
                style: {
                    border: '4px solid #0A192F',
                    padding: '16px',
                    color: '#0A192F',
                    background: '#D4FF33',
                    fontWeight: 900,
                    textTransform: 'uppercase',
                    borderRadius: '999px',
                    boxShadow: '4px 4px 0px #0A192F'
                }
            });
            setTimeout(() => navigate('/dashboard'), 2000);
        } catch (err: any) {
            console.error('Auth error:', err);
            const msg = err.response?.data?.detail || 'Authentication failed. Please try again.';
            setAuthError(msg);
            toast.error(msg, {
                position: 'bottom-center',
                style: {
                    border: '4px solid #0A192F',
                    padding: '16px',
                    color: '#0A192F',
                    background: '#FF9E9E',
                    fontWeight: 900,
                    borderRadius: '999px',
                    boxShadow: '4px 4px 0px #0A192F'
                },
                iconTheme: {
                    primary: '#0A192F',
                    secondary: '#FF9E9E',
                },
            });
            setIsShaking(true);
            setTimeout(() => setIsShaking(false), 500);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-[#FDFBF7] text-[#0A192F] font-sans flex items-center justify-center p-4 relative overflow-hidden selection:bg-[#D4FF33] selection:text-[#0A192F]">

            {/* Background Floating Elements (Neo-Pop Theme) */}
            <div className="absolute top-16 left-8 md:left-24 w-20 h-20 bg-[#C7B9FF] border-2 border-[#0A192F] rounded-full opacity-60 animate-float shadow-[4px_4px_0px_#0A192F]"></div>
            <div className="absolute bottom-16 right-8 md:right-24 w-28 h-28 bg-[#D4FF33] border-2 border-[#0A192F] rounded-[2rem] rotate-12 opacity-60 animate-float" style={{ animationDelay: '1s' }}></div>
            <div className="absolute top-1/4 right-[15%] bg-[#33A1FF] border-2 border-[#0A192F] text-white rounded-full px-4 py-2 font-bold text-sm shadow-[4px_4px_0px_#0A192F] -rotate-12 animate-float" style={{ animationDelay: '2s' }}>
                🎬 Let's write!
            </div>

            {/* Success Confetti overlay */}
            {isSuccess && <Confetti />}

            {/* Main Auth Card Container */}
            <div className={`w-full max-w-[420px] relative z-10 transition-all duration-700 ease-in-out ${isSuccess ? 'opacity-0 scale-90 pointer-events-none' : 'opacity-100 scale-100'}`}>

                {/* The Bento Box Card */}
                <div className={`bg-white border-4 border-[#0A192F] rounded-[2.5rem] p-8 shadow-[8px_8px_0px_#0A192F] animate-modal-in ${isShaking ? 'animate-shake' : ''}`}>

                    {/* Header & Logo */}
                    <div className="flex flex-col items-center mb-8">
                        <div className="w-14 h-14 bg-[#FF9E9E] rounded-full border-2 border-[#0A192F] flex items-center justify-center mb-5 shadow-[4px_4px_0px_#0A192F]">
                            <Play className="w-6 h-6 text-[#0A192F] fill-current ml-1" />
                        </div>
                        <h2 className="text-3xl font-black tracking-tight text-center leading-[1.1]">
                            Join the Story <br /> Revolution.
                        </h2>
                    </div>

                    {/* Toggle Tabs (Sliding Pill Design) */}
                    <div className="bg-[#FDFBF7] border-2 border-[#0A192F] rounded-full p-1.5 mb-8 relative flex items-center shadow-inner">
                        {/* Sliding Background Indicator */}
                        <div
                            className="absolute top-1.5 bottom-1.5 w-[calc(50%-6px)] bg-[#D4FF33] border-2 border-[#0A192F] rounded-full shadow-[2px_2px_0px_#0A192F] transition-transform duration-300 cubic-bezier(0.34, 1.56, 0.64, 1)"
                            style={{ transform: isLogin ? 'translateX(0)' : 'translateX(100%)' }}
                        ></div>

                        <button
                            type="button"
                            onClick={() => { setIsLogin(true); setEmail(''); setPassword(''); setName(''); }}
                            className={`flex-1 py-2 text-sm font-bold z-10 transition-colors ${isLogin ? 'text-[#0A192F]' : 'text-[#0A192F]/40 hover:text-[#0A192F]'}`}
                        >
                            Login
                        </button>
                        <button
                            type="button"
                            onClick={() => { setIsLogin(false); setEmail(''); setPassword(''); setName(''); }}
                            className={`flex-1 py-2 text-sm font-bold z-10 transition-colors ${!isLogin ? 'text-[#0A192F]' : 'text-[#0A192F]/40 hover:text-[#0A192F]'}`}
                        >
                            Sign Up
                        </button>
                    </div>

                    {/* Auth Form */}
                    <form onSubmit={handleSubmit} className="space-y-4">

                        {/* Name Field (Smooth expand/collapse for Signup mode) */}
                        <div className={`overflow-hidden transition-all duration-300 ease-in-out ${isLogin ? 'h-0 opacity-0 mb-0' : 'h-[60px] opacity-100 mb-4'}`}>
                            <div className="relative h-full">
                                <User className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-[#0A192F]/40" />
                                <input
                                    type="text"
                                    placeholder="Creator Name"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                    className="w-full h-full bg-[#FDFBF7] border-2 border-[#0A192F] rounded-2xl pl-12 pr-4 font-bold text-[#0A192F] placeholder-[#0A192F]/40 focus:outline-none focus:bg-white focus:ring-4 focus:ring-[#33A1FF]/30 transition-all"
                                />
                            </div>
                        </div>

                        {/* Email Field */}
                        <div className="relative h-[60px]">
                            <Mail className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-[#0A192F]/40" />
                            <input
                                type="email"
                                placeholder="Email Address"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="w-full h-full bg-[#FDFBF7] border-2 border-[#0A192F] rounded-2xl pl-12 pr-4 font-bold text-[#0A192F] placeholder-[#0A192F]/40 focus:outline-none focus:bg-white focus:ring-4 focus:ring-[#33A1FF]/30 transition-all"
                            />
                        </div>

                        {/* Password Field */}
                        <div className="relative h-[60px]">
                            <Lock className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-[#0A192F]/40" />
                            <input
                                type="password"
                                placeholder="Password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full h-full bg-[#FDFBF7] border-2 border-[#0A192F] rounded-2xl pl-12 pr-4 font-bold text-[#0A192F] placeholder-[#0A192F]/40 focus:outline-none focus:bg-white focus:ring-4 focus:ring-[#33A1FF]/30 transition-all"
                            />
                        </div>

                        {/* Forgot Password Link */}
                        {isLogin && (
                            <div className="text-right mt-2">
                                <a href="#" className="text-xs font-bold text-[#33A1FF] hover:text-[#0A192F] hover:underline transition-colors">Forgot password?</a>
                            </div>
                        )}

                        {/* Error Message */}
                        {authError && (
                            <div className="text-center text-[#FF4D4D] text-sm font-bold bg-[#FF4D4D]/10 py-2 rounded-xl border border-[#FF4D4D]/30">
                                {authError}
                            </div>
                        )}

                        {/* Neo-Pop Submit Button */}
                        <button
                            type="submit"
                            disabled={isLoading}
                            className="w-full bg-[#0A192F] text-white font-black text-lg py-4 rounded-2xl mt-6 flex items-center justify-center gap-2 hover:-translate-y-1 transition-transform shadow-[4px_4px_0px_#33A1FF] hover:shadow-[6px_6px_0px_#33A1FF] active:translate-x-[4px] active:translate-y-[4px] active:shadow-none group disabled:opacity-70 disabled:cursor-not-allowed"
                        >
                            {isLoading ? (
                                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                            ) : (
                                <>
                                    {isLogin ? 'Enter Studio' : 'Create Account'}
                                    <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                                </>
                            )}
                        </button>
                    </form>

                    {/* Separator */}
                    <div className="flex items-center gap-4 my-8">
                        <div className="flex-1 h-0.5 bg-[#0A192F]/10"></div>
                        <span className="text-xs font-black text-[#0A192F]/40 uppercase tracking-widest">Or continue with</span>
                        <div className="flex-1 h-0.5 bg-[#0A192F]/10"></div>
                    </div>

                    {/* Social Auth Buttons */}
                    <div className="grid grid-cols-2 gap-4">
                        <button className="flex items-center justify-center gap-2 bg-white border-2 border-[#0A192F] rounded-2xl py-3.5 font-bold hover:bg-[#FDFBF7] hover:-translate-y-0.5 transition-all shadow-[2px_2px_0px_#0A192F] active:translate-x-[2px] active:translate-y-[2px] active:shadow-none">
                            <svg className="w-5 h-5" viewBox="0 0 24 24"><path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" /><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" /><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" /><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" /></svg>
                            Google
                        </button>
                        <button className="flex items-center justify-center gap-2 bg-white border-2 border-[#0A192F] rounded-2xl py-3.5 font-bold hover:bg-[#FDFBF7] hover:-translate-y-0.5 transition-all shadow-[2px_2px_0px_#0A192F] active:translate-x-[2px] active:translate-y-[2px] active:shadow-none">
                            <Github className="w-5 h-5" />
                            GitHub
                        </button>
                    </div>

                </div>
            </div>

            {/* Post-Login Mock Dashboard Redirect State */}
            {isSuccess && (
                <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-full text-center z-20 animate-modal-in" style={{ animationDelay: '0.4s' }}>
                    <div className="inline-flex items-center justify-center gap-3 bg-white border-4 border-[#0A192F] rounded-full px-8 py-4 shadow-[6px_6px_0px_#0A192F] font-black text-xl text-[#0A192F]">
                        <Sparkles className="w-6 h-6 text-[#33A1FF] animate-pulse" />
                        Loading Studio...
                    </div>
                </div>
            )}

            {/* Embedded CSS for confetti pop animation (unique to this page) */}
            <style dangerouslySetInnerHTML={{
                __html: `
        @keyframes pop {
          0% { transform: translate(0, 0) scale(0) rotate(0deg); opacity: 1; }
          70% { opacity: 1; }
          100% { transform: translate(var(--tx), var(--ty)) scale(1.5) rotate(var(--rot)); opacity: 0; }
        }
      `}} />
        </div>
    );
};

// Custom Confetti Particle System Component
const Confetti = () => {
    // Neo-Pop palette
    const colors = ['#D4FF33', '#33A1FF', '#FF9E9E', '#C7B9FF', '#0A192F'];

    // Generate 60 random particles
    const particles = Array.from({ length: 60 }).map((_, i) => {
        const isCircle = Math.random() > 0.5;
        const color = colors[Math.floor(Math.random() * colors.length)];
        return {
            id: i,
            color: color,
            size: Math.random() * 12 + 6, // 6px to 18px
            tx: (Math.random() - 0.5) * 800 + 'px', // Wide X spread
            ty: (Math.random() - 0.5) * 800 - 300 + 'px', // Wide Y spread, favoring top
            rot: Math.random() * 720 + 'deg',
            delay: Math.random() * 0.15 + 's', // Staggered explosion
            shape: isCircle ? '50%' : '4px' // Circle or rounded square
        };
    });

    return (
        <div className="absolute inset-0 z-0 pointer-events-none flex items-center justify-center overflow-hidden">
            {particles.map((p) => (
                <div
                    key={p.id}
                    className="absolute shadow-[2px_2px_0px_rgba(10,25,47,0.2)]"
                    style={{
                        backgroundColor: p.color,
                        width: p.size + 'px',
                        height: p.size + 'px',
                        borderRadius: p.shape,
                        border: p.color !== '#0A192F' ? '2px solid #0A192F' : 'none', // Outline colored confetti
                        '--tx': p.tx,
                        '--ty': p.ty,
                        '--rot': p.rot,
                        animation: `pop 1.5s cubic-bezier(0.25, 1, 0.5, 1) ${p.delay} forwards`
                    } as React.CSSProperties & Record<string, string>}
                />
            ))}
        </div>
    );
};

export default AuthPage;